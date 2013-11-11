from simulator.rocket import Rocket


class EarthLander(Rocket):
    def flightProgram(self):
        #Take off and turn 90" right
        if self.mode == 0:
            self.engineOn()
            self.mode = 1

        if self.t > 12.0 and self.mode == 1:
            self.engineOff()
            self.mode = 2

        if self.t > 46.2 and self.mode == 2:
            self.engineOn()
            self.mode = 3

        if self.t > 55.8 and self.mode == 3:
            self.engineOff()
            self.mode = 4

        if self.t > 100 and self.mode == 4:
            self.engineOn()
            self.mode = 5

        if self.t > 110 and self.mode == 5:
            self.engineOff()
            self.mode = 6

        if self.t > 152.25 and self.mode == 6:
            self.engineOn()
            self.mode = 7

        if self.t > 160.5 and self.mode == 7:
            self.engineOff()
            self.mode = 8

