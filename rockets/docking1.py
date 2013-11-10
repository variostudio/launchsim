from rocket import Rocket


class Active(Rocket):
    def flightProgram(self):
        #Take off and turn 90" right
        if self.mode == 0:
            self.engineOn()
            self.mode = 1

        if self.t > 12.0 and self.mode == 1:
            self.engineOff()
            self.setHead(90)
            self.mode = 2

        #Go to round orbit
        if self.t > 20 and self.mode == 2:
            self.engineOn()
            self.mode = 3

        if self.t >= 27.5 and self.mode == 3:
            self.engineOff()
            self.mode = 4

        if self.t >= 30 and self.mode == 4:
            self.setHead(180)
            self.mode = 5

        if self.t >= 41 and self.mode == 5:
            self.engineOn()
            self.mode = 6

        if self.t >= 42.0 and self.mode == 6:
            self.engineOff()
            self.mode = 7

        if self.t >= 50 and self.mode == 7:
            self.setHead(270)
            self.mode = 8

        if self.t >= 75 and self.mode == 8:
            self.engineOn()
            self.mode = 9

        if self.t >= 77.65  and self.mode == 9:
            self.engineOff()
            self.mode = 10

        #print (self.t)


class Passive(Rocket):
    def flightProgram(self):
        if self.t >= 30 and self.mode == 0:
            self.setHead(90)
            self.mode = 1
