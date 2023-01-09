import math


def radToDegrees(theta):
    return theta * 180/ math.pi


def getForce(force, length, thetaVelocity, theta, massCart, massPole):
    tMass = massCart + massPole
    return (force + massPole * length * thetaVelocity ** 2 * math.sin(theta)) / tMass


def getThetaAccel(theta, forceVar, massPole, length, massCart):
    tMass = massCart + massPole
    return (9.8 * math.sin(theta) - math.cos(theta) * forceVar) / (
            length * (4 / 3 - massPole * math.cos(theta) ** 2 / tMass))


def getXAccel(forceVar, massPole, length, theta, thetaAccelleration, massCart):
    return forceVar - massPole * length * thetaAccelleration * math.cos(theta) / (massCart + massPole)


# thetaAcc = thetaDoubleDot = acceleration
# thetaDot = thetaDot = velocity
# tau = DT = time interval
# x tracks the total distance from the center always as a positive value
massPole = 0.2
massCart = 4.0
length = 1.0
force = 10.0
tau = 0.01
theta = math.pi / 24
thetaVelocity = 0
xVelocity = 0
x = 0
t = 0

# main driver
print("Starting position theta = " + str(theta) + ", " + str(radToDegrees(theta)) + " degrees" + " Pos = " + str(x))

if theta < 0:
    force = -1 * abs(force)

while True:
    forceVar = getForce(force, length, thetaVelocity, theta, massCart, massPole)
    thetaAcceleration = getThetaAccel(theta, forceVar, massPole, length, massCart)
    xAcceleration = getXAccel(forceVar, massPole, length, theta, thetaAcceleration, massCart)

    thetaOld = theta
    theta += thetaVelocity * tau
    thetaVelocity += thetaAcceleration * tau
    x += xVelocity * tau
    xVelocity += xAcceleration * tau
    t += tau

    # determining if pole is to the left (-theta) or right (+theta)
    # pole shifted to the left
    if theta < 0 <= thetaOld:
        force = -1 * abs(force)
        print("Theta: " + str(theta) + ", " + str(radToDegrees(theta)) + "degrees. Cart Acceleration: " + str(
            xVelocity) + " Pos = " + str(x))
    # pole shifted to the right
    if theta > 0 >= thetaOld:
        force = abs(force)
        print("Theta: " + str(theta) + ", " + str(radToDegrees(theta)) + "degrees. Force: " + str(
            xVelocity) + " Pos = " + str(x))
    # Failure to balance if the pole has dropped below horizon (theta > 90 or theta < -90
    if theta < -1.57 or theta > 1.57:
        print("Failure to balance at T = " + str(t))
        print("Theta: " + str(theta) + ", " + str(radToDegrees(theta)) + "degrees. Force: " + str(
            xVelocity) + " Pos = " + str(x))
        break
    print("Theta: " + str(theta) + ", " + str(radToDegrees(theta)) + "degrees. Cart Acceleration: " + str(
        xVelocity) + " Distance = " + str(x))
