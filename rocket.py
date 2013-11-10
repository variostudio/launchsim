from flyobj import *
import math


class Rocket(FlyObject):
    mass_fuel = 0.0
    head = 0.0
    engine_on = False

    width = 0.0
    height = 0.0

    fuel_eff = 0.0
    fuel_consume = 0.0
    fuel_weight = 0.0

    t = 0
    mode = 0

    #Creates new flying object like planet or star
    def __init__(self, name, mass, x, y, vx, vy, fuel_eff, fuel_consume, fuel_weight):
        super().__init__(name, mass, x, y, vx, vy)

        self.fuel_eff = fuel_eff
        self.fuel_consume = fuel_consume
        self.fuel_weight = fuel_weight

        self.radius = 20

    def initImages(self, engineOffImage, engineOnImage):
        self.image = image.load(engineOffImage)
        self.imageEngine = image.load(engineOnImage)

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def flightProgram(self):
        pass

    def setFuel(self, mass):
        self.mass_fuel = mass
        print("Fuel added:", mass)

    def getMass(self):
        return self.mass + self.mass_fuel * self.fuel_weight

    def fx(self, x):
        a = super().fx(x)

        if self.isEngineOn():
            accel = self.fuel_eff * self.fuel_consume / self.getMass()

            a += math.sin(math.radians(self.head)) * accel

        return a

    def fy(self, y):
        a = super().fy(y)

        if self.engine_on and self.mass_fuel > 0:
            accel = self.fuel_eff * self.fuel_consume / self.getMass()

            a -= math.cos(math.radians(self.head)) * accel

        return a

    def update(self):
        super().update()

        self.t += T
        if self.isEngineOn():
            self.mass_fuel -= T * self.fuel_consume

    def draw(self, screen, zoom, dx, dy):
        if self.isEngineOn():
            img = self.imageEngine
        else:
            img = self.image

        new_x = int((self.x - self.width // 2) * zoom + dx)
        new_y = int((self.y - self.height // 2) * zoom + dy)

        screen.blit(transform.rotozoom(img, (-1) * self.head, zoom), (new_x, new_y))

    def getSize(self):
        return max(self.image.get_width()//2, self.image.get_height()//2)

    def setHead(self, head):
        self.head = head

    def getHead(self):
        return self.head

    def engineOn(self):
        self.engine_on = True
        print("Engine is ON at: {0:6.2f} flight time".format(self.t))

    def engineOff(self):
        self.engine_on = False
        print("Engine is OFF at: {0:6.2f} flight time, fuel left {1:6.2f}".format(self.t, self.mass_fuel))

    def isEngineOn(self):
        return self.engine_on and self.mass_fuel > 0

