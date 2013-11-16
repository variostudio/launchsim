from pygame import *
import math

#Simulation precision. 
#Lower value is better precision but lower simulation speed
T = .05


class FlyObject:
    mass = 0.0
    x, y, vx, vy, ax, ay = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    radius = 0
    surfaceColor = "black"
    others = []
    name = ''
    image = ''

    #Creates new flying object like planet or star
    def __init__(self, name, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.name = name
        self.others = []

        print("{0}, ({1}, {2}) v=({3}, {4}), mass={5}".format(name, x, y, vx, vy, mass))

    def initSurface(self, R, surfaceColor):
        self.radius = R
        self.image = Surface((R * 2, R * 2), SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        draw.circle(self.image, Color(surfaceColor), (R, R), R)

    #Distance to other F.O.
    def dist(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    #Caluculates acceleration to other object
    def calcAccelTo(self, other):
        self.others.append((other.getMass(), other.x, other.y))

    def fx(self, local_x):
        a = 0
        for (mass, x, y) in self.others:
            r = math.hypot(x - local_x, y - self.y)
            a += mass * (x - local_x) / r ** 3

        return a

    def fy(self, local_y):
        a = 0
        for (mass, x, y) in self.others:
            r = math.hypot(x - self.x, y - local_y)
            a += mass * (y - local_y) / r ** 3

        return a

    def calcX(self):
        k1 = T * self.fx(self.x)
        q1 = T * self.vx

        k2 = T * self.fx(self.x + q1 / 2)
        q2 = T * (self.vx + k1 / 2)

        k3 = T * self.fx(self.x + q2 / 2)
        q3 = T * (self.vx + k2 / 2)

        k4 = T * self.fx(self.x + q3)
        q4 = T * (self.vx + k3)

        self.vx += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.x += (q1 + 2 * q2 + 2 * q3 + q4) / 6

    def calcY(self):
        k1 = T * self.fy(self.y)
        q1 = T * self.vy

        k2 = T * self.fy(self.y + q1 / 2)
        q2 = T * (self.vy + k1 / 2)

        k3 = T * self.fy(self.y + q2 / 2)
        q3 = T * (self.vy + k2 / 2)

        k4 = T * self.fy(self.y + q3)
        q4 = T * (self.vy + k3)

        self.vy += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.y += (q1 + 2 * q2 + 2 * q3 + q4) / 6

    def update(self):
        self.calcX()
        self.calcY()
        self.others.clear()

    #Draw to screen
    def draw(self, screen, zoom, dx, dy):
        new_x = int((self.x - self.radius) * zoom + dx)
        new_y = int((self.y - self.radius) * zoom + dy)

        scaled = transform.scale(self.image,
                                 (int(self.image.get_width() * zoom),
                                  int(self.image.get_height() * zoom)))
        screen.blit(scaled, (new_x, new_y))
        del scaled

    def getMass(self):
        return self.mass

    def getSize(self):
        return self.radius

    def getName(self):
        return self.name