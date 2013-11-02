from rocket import Rocket


class EarthOrbiter(Rocket):
    def flightProgram(self):
        #Take off and tern 90" right
        if self.mode == 0:
            self.engineOn()
            self.mode = 1

        if self.t > 12.0 and self.mode == 1:
            self.engineOff()
            self.head = 90
            self.mode = 2

        #Go to round orbit
        if self.t > 20 and self.mode == 2:
            self.engineOn()
            self.mode = 3

        if self.t >= 27 and self.mode == 3:
            self.engineOff()
            self.mode = 4

        '''
        #Nose up
        if self.t >= 90 and self.mode == 4:
            self.head = 0
            self.mode = 5

        #GO!

        if self.t >= 190 and self.mode == 4:
            self.engineOn()
            self.mode = 5

        if self.t >= 193 and self.mode == 5:
            self.engineOff()
            self.mode = 6'''
