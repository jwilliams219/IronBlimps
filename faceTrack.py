from djitellopy import Tello
import cv2
import faceTrackUtil as ftu
import time
import math

# Makes connection between drone and computer, activates camera, and lifts off
droneFly = True
myDrone = ftu.intializeTello()
print("Battery level: " + str(myDrone.get_battery()))
myDrone.streamon()
if droneFly:
    myDrone.takeoff()
time.sleep(3)
myDrone.send_rc_control(0, 0, 10, 0)
w, h = 480, 360
pid = [0.4, 0.4, 0]
pError = 0
newTracker = True
fail_count = 0
bbox = None
ok = None
result = cv2.VideoWriter('Drone Feed.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (w, h))

tickTime = time.time()
numTicks = 0

outputVideo = None

# Main loop
while True:
    # Receives image from camera feed
    img = myDrone.get_frame_read().frame

    currentTime = time.time()
    if currentTime - tickTime > 10:
        tickTime = currentTime
        numTicks = numTicks + 1
        cv2.imwrite("output" + str(numTicks) + ".png", img)
    # Resizes image to set width/height
    img = cv2.resize(img, (w, h))
    #myDrone.get_battery()

    # Detects face in frame
    img, info = ftu.findFace(img)

    # Create or Reset the Tracker
    if newTracker:
        if info[1] != 0:
            side = int(math.sqrt(info[1]))
            x, y = info[0]
            bbox = (int(x-(side/2)), int(y-(side/2)), side, side)
            # Initialize tracker with first frame and bounding box
            tracker = cv2.legacy.TrackerMOSSE_create()
            ok = tracker.init(img, bbox)
            newTracker = False
            fail_count = 0

    # Update tracker or Reset
    if bbox is not None:
        ok, bbox = tracker.update(img)
        x1, y1, w1, h1 = bbox
        if info[1] != 0:
            faceX, faceY = info[0]
            if x1 < faceX < x1 + w1 and y1 < faceY < y1 + h1:
                tracker = cv2.legacy.TrackerMOSSE_create()
                ok = tracker.init(img, bbox)
        if h1 == 0 or w1/h1 > 1.25 or w1/h1 < 1/1.25:
            ok = False
            newTracker = True

    # Draw face detection on img
    if info[1] != 0:
        x, y = info[0]
        side = int(math.sqrt(info[1]))
        faceBBox = (int(x-(side/2)), int(y-(side/2)), side, side)
        ftu.drawRectangle(img, faceBBox, (0, 255, 0))

    # Use tracking to determine movement for drone
    if ok is not None and ok:
        ftu.drawRectangle(img, bbox, (255, 0, 0))  # Draw object tracking box on img
        info = ftu.coordFromBox(bbox)
        pError = ftu.trackFace(myDrone, info, w, h, pid, pError)

    # Tracking failure
    else:
        fail_count += 1
        if fail_count > 60:  # If the tracking failed for long enough, try to reset it.
            newTracker = True
        # cv2.putText(img, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display image
    result.write(img)
    cv2.imshow("Output", img)

    # press 'q' to land drone and shutdown
    if cv2.waitKey(1) & 0xFF == ord('q'):
        result.release()
        cv2.destroyAllWindows()
        myDrone.streamoff()
        if droneFly:
            myDrone.land()
        break
