import math
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')

def kinematics(l, r, W, x, y, theta, DT):
    xNew = x - .5 * (l + r) * np.sin(theta) * DT
    yNew = y + .5 * (l + r) * np.cos(theta) * DT
    thetaNew = theta + (1 / W) * (r - l) * DT
    aVel = (1 / W) * (r - l)
    xVel = -.5 * (l + r) * np.sin(theta)
    yVel = .5 * (l + r) * np.cos(theta)
    return xNew, yNew, thetaNew, aVel, xVel, yVel

WIDTH = .3
DT = .1
time = 0
xNot = .15
yNot = 0
theta = 0
xCoord = [xNot]
yCoord = [yNot]
xPoint = [xNot]
yPoint = [yNot]
xVels = []
yVels = []
angVels = []
times = []

# (1, .23562, -.23562) = 90 degree clockwise turn
# (1, -.23562, .23562) = 90 degree counterclockwise turn
kList = [(5, 1, 1), #movement sequence
         (1, .23562, -.23562), (1,.3,.3), (1, .23562, -.23562), #turning south sequence
         (5, 1, 1), #movement sequence
         (1, -.23562, .23562), (1, .3, .3), (1, -.23562, .23562)] #turning north sequence



print("(" + str(xNot) + ", " + str(yNot) + ") theta= " + str(theta))
print("At T = " + str(time))
for z in range(0, 9):
    for x in range(0, len(kList)):
        for y in range(0, kList[x][0] * 10):
            xNot, yNot, theta, angVel, xV, yV = kinematics(kList[x][1], kList[x][2], WIDTH, xNot, yNot, theta, DT)
            xCoord.append(xNot)
            yCoord.append(yNot)
            xVels.append(xV)
            yVels.append(yV)
            angVels.append(angVel)
            time += .1
            times.append(time)
            print("Position: (" + str(xNot) + ", " + str(yNot) + ") theta = " + str(theta))
            print("Trajectory: (" + str(xV) + ", " + str(yV) + ") Angular Velocity = " + str(angVel))
            print("At T = " + str(time))
        xPoint.append(xNot)
        yPoint.append(yNot)









fig, ax = plt.subplots(2,2, constrained_layout=True, figsize=(8,8))
ax[0, 0].step(xCoord, yCoord)
ax[0, 0].set_xlabel('x (meters)')
ax[0, 0].set_ylabel('y (meters)')
ax[0, 0].plot(xPoint, yPoint, linewidth = 2, marker = '.')
ax[0, 0].set_title("Skid Steer coverage of 5x5 plot")

ax[0, 1].set_xlabel('t (seconds)')
ax[0, 1].set_ylabel('x velocity (m/s)')
ax[0, 1].plot(times, xVels)
ax[0, 1].set_title("X Velocity over time")

ax[1, 0].set_xlabel('t (seconds)')
ax[1, 0].set_ylabel('y velocity (m/s)')
ax[1, 0].plot(times, yVels)
ax[1, 0].set_title("Y Velocity over time")

ax[1, 1].set_xlabel('t (seconds)')
ax[1, 1].set_ylabel('theta velocity (m/s)')
ax[1, 1].plot(times, angVels)
ax[1, 1].set_title("Angular Velocity over time")

plt.show()
