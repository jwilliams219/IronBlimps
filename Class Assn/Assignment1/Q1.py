import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import draw

import numpy
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
xNot = 0
yNot = 0
theta = 0
xCoord = [xNot]
yCoord = [yNot]
xPoint = [xNot]
yPoint = [yNot]

kList = [(5, 1, 1.5), (3, -1, -1.5), (8, .8, -2), (10, 2, 2)]
print("Position: (" + str(xNot) + ", " + str(yNot) + ") at T = " + str(time))

for x in range(0, 4):
    for y in range(0, kList[x][0] * 10):
        xNot, yNot, theta, angVel, xV, yV = kinematics(kList[x][1], kList[x][2], WIDTH, xNot, yNot, theta, DT)
        xCoord.append(xNot)
        yCoord.append(yNot)
        time += .1
        print("Position: (" + str(xNot) + ", " + str(yNot) + ") at T = " + str(time))
        # print("Trajectory: (" + str(xV) + ", " + str(yV) + ") Angular Velocity = " + str(angVel))

    xPoint.append(xNot)
    yPoint.append(yNot)

fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 6))
ax.step(xCoord, yCoord)
ax.set_xlabel('x (meters)')
ax.set_ylabel('y (meters)')
plt.title("Question 1: Skid Steer following path")
plt.plot(xPoint, yPoint, linewidth=2, marker='.')
plt.show()
