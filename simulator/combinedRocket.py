from simulator.rocket import Rocket
from pygame import *


class CombinedRocket(Rocket):
    rockets = []
    config = ''
    dx = 9999
    dy = 9999

    def __init__(self, rockets, cfg):
        self.rockets = rockets
        self.config = cfg
        ix = 0
        iy = 0
        mass = self.getMass()

        for i in self.rockets:
            ix += i.vx * i.getMass()
            iy += i.vy * i.getMass()

        self.combineImage()
        self.initXY()

        self.vx = ix / mass
        self.vy = iy / mass

        print("Docking complete:", self.getName(), self.getMass(), self.vx, self.vy)

    def initXY(self):
        minx = 9999
        miny = 9999

        for i in self.rockets:
            if i.x <= minx:
                minx = i.x

            if i.y <= miny:
                miny = i.y

        self.x = minx - self.dx
        self.y = miny - self.dy

        #print("MINx: ", minx, "DX: ", self.dx, "X: ", self.x)
        #print("MINy: ", miny, "DY: ", self.dy, "Y: ", self.y)

    def combineImage(self):
        minx = 9999
        miny = 9999
        w = 0
        h = 0

        for i in self.rockets:
            w += i.image.get_width()
            h += i.image.get_height()

            if i.x <= minx:
                minx = i.x
                self.dy = i.y

            if i.y <= miny:
                miny = i.y
                self.dx = i.x

        self.image = Surface((w, h))
        self.image.fill(Color(self.config.getSpaceColor()))

        for i in self.rockets:
            self.image.blit(transform.rotate(i.image, (-1)*i.getHead()), (i.x - minx, i.y - miny))

        self.dx -= minx
        self.dy -= miny

    def getName(self):
        name = ''
        is_first = True
        for i in self.rockets:
            if is_first:
                is_first = False
            else:
                name += ' + '
            name += i.getName()
        return name

    def getMass(self):
        mass = 0
        for i in self.rockets:
            mass += i.getMass()
        return mass

    def getSize(self):
        size = 0
        for i in self.rockets:
            size += i.getSize()
        return size

    def flightProgram(self):
        for i in self.rockets:
            i.flightProgram()


