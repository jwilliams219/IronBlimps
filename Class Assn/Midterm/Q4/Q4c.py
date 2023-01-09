import math


def getForce(force, length, thetaVelocity, theta, massCart, massPole):
    tMass = massCart + massPole
    return (force + massPole * length * thetaVelocity ** 2 * math.sin(theta)) / tMass


def getThetaAccel(theta, forceVar, massPole, length, massCart):
    tMass = massCart + massPole
    return (9.8 * math.sin(theta) - math.cos(theta) * forceVar) / (
            length * (4 / 3 - massPole * math.cos(theta) ** 2 / tMass))


def getXAccel(forceVar, massPole, length, theta, thetaAccelleration, massCart):
    return forceVar - massPole * length * thetaAccelleration * math.cos(theta) / (massCart + massPole)


massPole = 0.2
massCart = 4.0
length = 1.0
max_force = 6.0
force = 10.0
tau = 0.01
theta = math.pi / 24
thetaVelocity = 0
last_theta = theta
x = 0
xVelocity = 0
t = 5

# thetaAcc = thetaDoubleDot = acceleration
# thetaDot = thetaDot = velocity
# tau = DT = time interval

while True:
    forceVar = getForce(force, length, thetaVelocity, theta, massCart, massPole)
    thetaAcceleration = getThetaAccel(theta, forceVar, massPole, length, massCart)
    xAcceleration = getXAccel(forceVar, massPole, length, theta, thetaAcceleration, massCart)
    if xAcceleration > max_force / (massCart + massPole):
        xAcceleration = max_force / (massCart + massPole)

    thetaOld = theta
    theta += thetaVelocity * tau
    thetaVelocity += thetaAcceleration * tau
    x += xVelocity * tau
    xVelocity += xAcceleration * tau

    # comparing the new angle to the old angle
    if last_theta > theta:
        # the angle decreased, increasing base angle by the amount of change
        print("Pushed Weight to middle from " + str(last_theta) + " to " + str(theta) + "(" + str(
            last_theta - theta) + ")")
        theta = last_theta + (last_theta - theta)
        thetaVelocity = 0
        xVelocity = 0
        x = 0

    if theta > 1.57:
        # the angle decreased, pole still dropping at max force
        print("theta increased by " + str(theta - last_theta) + " test failed. Max recoverable angle is " +
              str(last_theta))
        break
print("Exited while loop")
print("unrecoverable angle = " + str(last_theta))
print("Unrecoverable angle (degrees) = " + str(last_theta * 180 / math.pi))

# while t > 0 and math.pi / 2 > theta > -1 * math.pi / 2:
#     #calculate the accellerations for theta and x
#     curr_theta_acc = theta_acc(length, force, mass_pole, mass_cart, theta, theta_dot)
#     curr_x_acc = x_acc(length, force, mass_pole, mass_cart, theta, theta_dot, curr_theta_acc)
#
#     theta_dot += curr_theta_acc*tau
#     last_theta = theta
#     theta += theta_dot*tau
#     degree = radToDegree(theta)
#     print("theta = " + str(theta))
#     print("degree = " + str(degree))
#     print("force = " + str(force))
#     x_dot += curr_x_acc
#     x += x_dot * tau
#
#     # Basic control
#     if theta < 0 and theta < last_theta:
#         force = -1*max_force
#     elif theta > 0 and theta > last_theta:
#         force = max_force
#     t -= tau
