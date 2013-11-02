from rocket import Rocket


class EarthOrbiter(Rocket):
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

        if self.t >= 27 and self.mode == 3:
            self.engineOff()
            self.mode = 4
