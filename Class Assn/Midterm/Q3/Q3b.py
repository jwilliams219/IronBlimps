from math import cos, sin, radians, degrees, sqrt
import random

def dist(x1, x2, y1, y2, z1, z2):
    return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

def minScore(theta1, theta4, theta5, dist2, dist3, curMinScore):
    t1_start = 0
    t4_start = -90
    t5_start = 90
    d2_start = 0.2
    d3_start = 0.3
    
    t1_dist = abs(t1_start - theta1)
    t4_dist = abs(t4_start - theta4)
    t5_dist = abs(t5_start - theta5)
    d2_dist = abs(d2_start - dist2)
    d3_dist = abs(d3_start - dist3)
    
    total_dist = t1_dist + t4_dist + t5_dist + d2_dist + d3_dist
    
    if total_dist < curMinScore[0]:
        curMinScore[0] = total_dist
        curMinScore[1] = theta1
        curMinScore[2] = theta4
        curMinScore[3] = theta5
        curMinScore[4] = dist2
        curMinScore[5] = dist3

    return curMinScore
    
def solveGoal(curMinScore):
    d1 = 0          # can be set to anything, just affects z
    d2 = 0.2
    d3 = 0.3
    d6 = 0.2        #constant

    x_goal = 1.2
    y_goal = 0.8
    z_goal = 0.5

    n = 1000000

    t1 = radians(0)
    t4 = radians(-90)
    t5 = radians(90)
    t6 = radians(40)       #does not affect solution
    threshold = 0.006

    x = (cos(t1) * cos(t4) * sin(t5) * d6) - (sin(t1) * cos(t5) * d6) - (sin(t1) * d3)
    y = (sin(t1) * cos(t4) * sin(t5) * d6) + (cos(t1) * cos(t5) * d6) + (cos(t1) * d3)
    z = 0 - (sin(t4) * sin(t5) * d6) + d1 + d2

    #print("Start x, y, z: {:.2f}, {:.2f}, {:.2f}".format(x,y,z))

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
            minScore(t1, t4, t5, d2, d3, curMinScore)
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
    
# finding the minimum distance
m = 10         # using 100 data points

for j in range(m):
    curMinScore = [1000.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    solveGoal(curMinScore)

# fixed vars
d1 = 0
d6 = 0.2
# changed vars
t1_min = curMinScore[1]
t4_min = curMinScore[2]
t5_min = curMinScore[3]
d2_min = curMinScore[4]
d3_min = curMinScore[5]

x = (cos(t1_min) * cos(t4_min) * sin(t5_min) * d6) - (sin(t1_min) * cos(t5_min) * d6) - (sin(t1_min) * d3_min)
y = (sin(t1_min) * cos(t4_min) * sin(t5_min) * d6) + (cos(t1_min) * cos(t5_min) * d6) + (cos(t1_min) * d3_min)
z = 0 - (sin(t4_min) * sin(t5_min) * d6) + d1 + d2_min


print("Minimized thetas from {} data points".format(m))
print("X = {:.5f}\nY = {:.5f}\nZ = {:.5f}".format(x,y,z))
print("theta 1 = {:.5f}\ntheta 4 = {:.5f}\ntheta 5 = {:.5f}".format(degrees(t1_min), degrees(t4_min), degrees(t5_min)))
print("d2 = {:.5f}\nd3 = {:.5f}".format(d2_min, d3_min))
print("total distances traveled {:.5f}".format(curMinScore[0]))
