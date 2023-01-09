import matplotlib.pyplot as plt
import numpy as np
import math
import time as timer


plt.style.use('_mpl-gallery')


# Creates the list of commands for the bot to follow every tick
def generateCommands(interval, turn):
    commandList = []

    for x in range(int(10 / interval)):
        commandList.append((interval, turn))

    return commandList


# Runs the list of commands to move the bot
def runCommands(kList):
    startTime = timer.time()
    VELOCITY = 8
    RADIUS = 2.5

    time = 0
    xNot = -2.5
    yNot = 0
    theta = 0
    xCoord = [xNot]
    yCoord = [yNot]
    xPoint = [xNot]
    yPoint = [yNot]
    xVels = []
    yVels = []
    # angVels = []
    times = []
    errors = []
    compTimer = []

    for x in range(0, len(kList)):
        xNot, yNot, theta, angVel, xV, yV = kinematics(xNot, yNot, theta, kList[x][1], kList[0][0], VELOCITY)
        xCoord.append(xNot)
        yCoord.append(yNot)
        xVels.append(xV)
        yVels.append(yV)
        # angVels.append(angVel)
        time += kList[0][0]
        times.append(time)
        actualRadians = (VELOCITY * time) / RADIUS
        actualX = RADIUS * -np.cos(actualRadians)
        actualY = RADIUS * np.sin(actualRadians)
        error = np.sqrt(math.pow(xNot - actualX, 2) + math.pow(yNot - actualY, 2))
        errors.append(error)
        # print("Position: (" + str(xNot) + ", " + str(yNot) + ") theta = " + str(theta))
        # print("Trajectory: (" + str(xV) + ", " + str(yV) + ") Angular Velocity = " + str(angVel))
        # print("At T = " + str(time))
        xPoint.append(xNot)
        yPoint.append(yNot)
        endTime = timer.time()
        compTimer.append(endTime - startTime)

    
        

    plotCharts(compTimer, xCoord, yCoord, xPoint, yPoint, xVels, yVels, errors, times, kList[0][0])


# calculates position and velocities
def kinematics(x, y, theta, alpha, tInterval, velocity):
    LENGTH = .75

    xNew = x - velocity * np.sin(theta) * tInterval
    yNew = y + velocity * np.cos(theta) * tInterval
    thetaNew = theta + (velocity / LENGTH) * np.tan(alpha) * tInterval
    aVel = (velocity / LENGTH) * np.tan(alpha)
    xVel = -1 * velocity * np.sin(theta)
    yVel = velocity * np.cos(theta)
    return xNew, yNew, thetaNew, aVel, xVel, yVel


# draws the figures
def plotCharts(compTimer, xCoordinate, yCoordinate, xPos, yPos, xVelocity, yVelocity, errors, tList, deltaT):
    figure, ax = plt.subplots(2, 2, tight_layout=True, figsize=(6, 6))
    Drawing_uncolored_circle = plt.Circle((0, 0),
                                          2.5,
                                          fill=False)
    ax[0, 0].add_artist(Drawing_uncolored_circle)
    ax[0, 0].set_aspect(1)
    if (deltaT > .1):
        ax[0, 0].set(xlim=(-10, 10), ylim=(-10, 10))
    else:
        ax[0, 0].set(xlim=(-3, 3), ylim=(-3, 3))

    ax[0, 0].plot(xPos, yPos, linewidth=2, marker='.')
    ax[0, 0].set_title("Question 1c: " + 'Position \u0394' + "t= " + str(deltaT))

    ax[0, 1].set_xlabel('Simulation Time (s)')
    ax[0, 1].set_ylabel('Total Computational Time (s)')
    ax[0, 1].plot(tList, compTimer)
    ax[0, 1].set_title("Computational Time")

    #ax[1, 0].set_xlabel('t (seconds)')
    #ax[1, 0].set_ylabel('y velocity (m/s)')
    #ax[1, 0].plot(tList, yVelocity)
    #ax[1, 0].set_title("Y Velocity over time")

    ax[1, 1].set_xlabel('t (seconds)')
    ax[1, 1].set_ylabel('position error (m)')
    ax[1, 1].plot(tList, errors)
    ax[1, 1].set_title("Error over Time")

    plt.show(block=False)


# runs the program using different delta-Ts
dt = [.1, .01, 1]

# main driver
for x in range(len(dt)):
    commandListing = generateCommands(dt[x], -.291457)
    runCommands(commandListing)
plt.show()
