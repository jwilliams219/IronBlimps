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

WIDTH = .55
LENGTH = .75
VELOCITY = 8
DIAMETER = 5
DT = .1
time = 0
xNot = 0
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

print("Position: (" + str(xNot) + ", " + str(yNot) + ") theta = " + str(theta))
print("Trajectory: (" + str(0) + ", " + str(0) + ") Angular Velocity = " + str(0))
print("At T = " + str(time))


kList = []

#initalize kList orders
for x in range(5):
    kList.append((.1, 9.76, 6.24))
for x in range(20):
    kList.append((.1, 8.88, 7.12))

for x in range(0, len(kList)):
    for y in range(0, int(kList[x][0]*10)):
        xNot, yNot, theta, angVel, xV, yV = kinematics(kList[x][1], kList[x][2], WIDTH, xNot, yNot, theta, DT)
        xCoord.append(xNot)
        yCoord.append(yNot)
        xVels.append(xV)
        yVels.append(yV)
        angVels.append(angVel)
        time += .1
        times.append(time)
        #print("Position: (" + str(xNot) + ", " + str(yNot) + ") theta = " + str(theta))
        #print("Trajectory: (" + str(xV) + ", " + str(yV) + ") Angular Velocity = " + str(angVel))
        #print("At T = " + str(time))
    xPoint.append(xNot)
    yPoint.append(yNot)

figure, ax = plt.subplots(2, 2, tight_layout=True, figsize=(6, 6))
Drawing_uncolored_circle = plt.Circle((0, 0),
                                      2.5,
                                      fill=False)
ax[0, 0].add_artist(Drawing_uncolored_circle)
ax[0, 0].set_aspect(1)
ax[0, 0].set(xlim=(-3, 3), ylim=(-3, 3))
ax[0, 0].plot(xPoint, yPoint, linewidth = 2, marker = '.')
ax[0, 0].set_title("Question 1: Skid Steer On A Circle")

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