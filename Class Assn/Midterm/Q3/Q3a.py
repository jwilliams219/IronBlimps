from math import cos, sin, radians, degrees, sqrt
import random

def dist(x1, x2, y1, y2, z1, z2):
    return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

d1 = 0          #can be set to anything, just affects z
d2 = 0.5
d3 = 1.0
d6 = 0.2        #constant

x_goal = 1.2
y_goal = 0.8
z_goal = 0.5

n = 1000000

t1 = radians(-90)
t4 = radians(-90)
t5 = radians(90)
t6 = radians(40)       #does not affect solution
threshold = 0.006

x = (cos(t1) * cos(t4) * sin(t5) * d6) - (sin(t1) * cos(t5) * d6) - (sin(t1) * d3)
y = (sin(t1) * cos(t4) * sin(t5) * d6) + (cos(t1) * cos(t5) * d6) + (cos(t1) * d3)
z = 0 - (sin(t4) * sin(t5) * d6) + d1 + d2

print("Start x, y, z: {:.2f}, {:.2f}, {:.2f}".format(x,y,z))

for i in range(n):
    t1_diff = (random.random() - 0.5) * .3
    t4_diff = (random.random() - 0.5) * .3
    t5_diff = (random.random() - 0.5) * .3
    t1_tmp = t1 + t1_diff
    t4_tmp = t4 + t4_diff
    t5_tmp = t5 + t5_diff
    
    d2_tmp = random.random() * 0.6
    d3_tmp = random.random() * 2.0
    
    x_tmp = (cos(t1_tmp) * cos(t4_tmp) * sin(t5_tmp) * d6) - (sin(t1_tmp) * cos(t5_tmp) * d6) - (sin(t1_tmp) * d3_tmp)
    y_tmp = (sin(t1_tmp) * cos(t4_tmp) * sin(t5_tmp) * d6) + (cos(t1_tmp) * cos(t5_tmp) * d6) + (cos(t1_tmp) * d3_tmp)
    z_tmp = 0 - (sin(t4_tmp) * sin(t5_tmp) * d6) + d1 + d2_tmp
    
    if abs(x - x_goal) < threshold and abs(y - y_goal) < threshold and abs(z - z_goal) < threshold:
        print("Success")
        break
        
    curDist = dist(x_goal, x, y_goal, y, z_goal, z)
    tempDist = dist(x_goal, x_tmp, y_goal, y_tmp, z_goal, z_tmp)
    
    if curDist < tempDist:
        pass
    else:
        t1 = t1_tmp
        t4 = t4_tmp
        t5 = t5_tmp
        d2 = d2_tmp
        d3 = d3_tmp
        x = x_tmp
        y = y_tmp
        z = z_tmp

print("X = {:.5f}\nY = {:.5f}\nZ = {:.5f}".format(x,y,z))
print("theta 1 = {:.5f}\ntheta 4 = {:.5f}\ntheta 5 = {:.5f}".format(degrees(t1_tmp), degrees(t4_tmp), degrees(t5_tmp)))
print("d2 = {:.5f}\nd3 = {:.5f}".format(d2_tmp, d3_tmp))
