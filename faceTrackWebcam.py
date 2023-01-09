import cv2
import numpy as np
import math


def findFace(img):
    # Loads haar cascade from cv2 to detect objects
    haar = True
    if haar:
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
        #obtain item closest to center of screen
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


def generateObjList(object, img):
    myFaceListC = []
    myFaceListArea = []
    for (x, y, w, h) in object:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    return myFaceListC, myFaceListArea


def trackFace(info, w, h, pid, pError):
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
    rotationSpeed = int(np.clip(rotationSpeed, -100, 100))
    # gets required vertical speed to keep drone centered on target
    heightSpeed = pid[0] * errorHeight + pid[1] * (errorHeight - pError)
    heightSpeed = -1 * int(np.clip(heightSpeed, -20, 20))

    # determines if target is too far or close to the drone. Moves closer/away if needed.
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
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
    #myDrone.send_rc_control(0, fb, heightSpeed, rotationSpeed)
    return error


# define a video capture object
vid = cv2.VideoCapture(0)
w, h = 480, 360
pid = [0.4, 0.4, 0]
pError = 0
#tracker_types = ['MIL', 'KCF', 'CSRT']
tracker_type = "CRST"
tracker = cv2.legacy.TrackerCSRT_create()
makeBox = True
fail_count = 0

while True:

    # Capture the video frame by frame
    ret, frame = vid.read()
    frame = cv2.resize(frame, (w, h))

    if makeBox:
        face_frame, info = findFace(frame)
        # Create bounding box
        side = int(math.sqrt(info[1]))
        x, y = info[0]
        bbox = (int(x-(side/2)), int(y-(side/2)), side, side)
        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)
        makeBox = False
        fail_count = 0

    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    # Draw bounding box
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        # Use drone moving function based on object tracking
        x1, y1 = p1
        x2, y2 = p2
        width, height = x2-x1, y2-y1
        cx = x1 + width // 2
        cy = y1 + height // 2
        area = width * height
        info = [[cx, cy], area]
        print("P Error", trackFace(info, w, h, pid, pError))
    else:
        # Tracking failure
        fail_count += 1
        if fail_count > 60:  # If the tracking failed for long enough, try to reset it.
            makeBox = True
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display tracker type and fps on frame
    cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)


    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
