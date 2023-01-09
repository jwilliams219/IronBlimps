import math

t1 = math.radians(30)
t2 = math.radians(45)
t3 = math.radians(90)

d3 = 0
d4 = .14

a1 = .6
a2 = .4

x = (a1 * math.cos(t1)) + (a2 * math.cos(t1 + t2))

y = (a1 * math.sin(t1)) + (a2 * math.sin(t1 + t2))

z = -d3 - d4

print("x: {:.5f}\n".format(x))
print("y: {:.5f}\n".format(y))
print("z: {:.2f}\n".format(z))
