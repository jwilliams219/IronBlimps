from djitellopy import Tello
import cv2
import numpy as np
import pygame


def intializeTello():
    # Connect to drone
    myDrone = Tello()
    myDrone.connect()
    # initialize movement to zero
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    return myDrone


def telloGetFrame(myDrone, w, h):
    # Get image from drone and resizes. Handled in main function
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def findFace(img):
    # Loads haar cascade from cv2 to detect objects
    haar = False
    if (haar):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        profileCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

    else:
        faceCascade = cv2.CascadeClassifier('./Resources/lbpcascade_frontalface_improved.xml')
        profileCascade = cv2.CascadeClassifier('./Resources/lbpcascade_profileface.xml')
    bodyCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    profilesLeft = profileCascade.detectMultiScale(cv2.flip(imgGray, 1), 1.2, 8)
    profilesRight = profileCascade.detectMultiScale(imgGray, 1.2, 8)
    bodies = bodyCascade.detectMultiScale(imgGray, 1.1, 3)

    # stores current faces into arrays
    myFaceListCFace, myFaceListAreaFace = generateObjList(faces, img)
    myFaceListCProfileLeft, myFaceListAreaProfileLeft = generateObjList(profilesLeft, img)
    myFaceListCProfileRight, myFaceListAreaProfileRight = generateObjList(profilesRight, img)
    myFaceListCBody, myFaceListAreaBody = generateObjList(bodies, img)

    # generates rectangle and center dot around each detected face
    myFaceListC = myFaceListCFace + myFaceListCProfileLeft + myFaceListCProfileRight + myFaceListCBody
    myFaceListArea = myFaceListAreaFace + myFaceListAreaProfileLeft + myFaceListAreaProfileRight + myFaceListAreaBody
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        index = 0
        distance = None
        j = 0
        # Obtain item closest to center of screen
        for item in myFaceListC:
            x, y = item
            if distance is None:
                distance = x ** 2 + y ** 2
            else:
                if x ** 2 + y ** 2 < distance:
                    index = j
            j += 1

        #print("myFaceListC: " + str(myFaceListC))
        return img, [myFaceListC[index], myFaceListArea[index]]
    else:
        return img, [[0, 0], 0]


# takes the drone connect data, the face info, frame width and height. PID, and error range
def generateObjList(object, img):
    myFaceListC = []
    myFaceListArea = []
    for (x, y, w, h) in object:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        # cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    return myFaceListC, myFaceListArea


def trackFace(myDrone, info, w, h, pid, pError):
    # info contains the coordinates of the centermost face
    # range of distance to control drone moving forward/away from target
    fbRange = [3200, 6800]
    # area of the face square
    area = info[1]
    # x/y pos of the face square
    x, y = info[0]
    # set flag to print out target x/y pos and velocities
    debugOutput = False
    fb = 0
    # offset from the center
    error = x - w // 2
    errorHeight = y - h // 2

    # gets the required rotation speed to keep drone centered on target
    rotationSpeed = pid[0] * error + pid[1] * (error - pError)
    rotationSpeed = int(np.clip(rotationSpeed, -50, 50))
    # gets required vertical speed to keep drone centered on target
    heightSpeed = pid[0] * errorHeight + pid[1] * (errorHeight - pError)
    heightSpeed = -1 * int(np.clip(heightSpeed, -20, 20))

    # determines if target is too far or close to the drone. Moves closer/away if needed.
    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
        fb = int(fb * (area / fbRange[1] - 1))
    elif area < fbRange[0] and area != 0:
        fb = 20
        fb = int(fb * (fbRange[0] / area - 1))
    if x == 0:
        rotationSpeed = 0
        heightSpeed = 0
        error = 0
    # print(speed, fb)
    # myDrone.send_rc_control(0, fb, 0, rotationSpeed)
    if debugOutput:
        print("x: " + str(x))
        print("y: " + str(y))
        print("errorHeight: " + str(errorHeight))
        print("heightSpeed: " + str(heightSpeed))
    # sends movement commands to keep target centered
    myDrone.send_rc_control(0, fb, heightSpeed, rotationSpeed)
    return error


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans


def drawRectangle(img, bbox, color):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + int(bbox[2])), int(bbox[1] + bbox[3]))
    cv2.rectangle(img, p1, p2, color, 2, 1)
    return p1, p2


def coordFromBox(bbox):
    x1, y1 = (int(bbox[0]), int(bbox[1]))
    x2, y2 = (int(bbox[0] + int(bbox[2])), int(bbox[1] + bbox[3]))
    width, height = x2 - x1, y2 - y1
    cx = x1 + width // 2
    cy = y1 + height // 2
    area = width * height
    info = [[cx, cy], area]
    return info
