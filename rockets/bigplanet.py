from simulator.rocket import Rocket


class BigEarthOrbiter(Rocket):
    def flightProgram(self):
        #Take off and turn 90" right
        if self.mode == 0:
            self.engineOn()
            self.mode = 1

        if self.t > 20.0 and self.mode == 1:
            self.engineOff()
            self.setHead(90)
            self.mode = 2

        #Go to round orbit
        if self.t > 25 and self.mode == 2:
            self.engineOn()
            self.mode = 3

        if self.t >= 37 and self.mode == 3:
            self.engineOff()
            self.mode = 4


class SmoothhOrbiter(Rocket):
    def flightProgram(self):
        #Go to round orbit by smooth head increase
        if self.mode == 0:
            self.engineOn()
            self.mode = 1

        if 11.0 <= self.t <= 28 and self.mode == 1:
            self.setHead(self.getHead() + .4)

        if self.t > 29 and self.mode == 1:
            self.engineOff()
            #self.setHead(90)
            self.mode = 2

