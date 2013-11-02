from rocket import Rocket


class SpaceCalculator:
    N = 10
    circles = 0
    r_min = 9999.0
    r_max = 0.0

    def newPosition(self, system):
        dist = 0

        for cnt in range(self.N):
            for i in system:
                # if object is a Rocket - execute flight program
                if isinstance(i, Rocket):
                    i.flightProgram()

                for j in system:
                    if i != j:
                        dist = i.dist(j)
                        dist -= (i.getSize() + j.getSize())
                        #print("Dist: ", dist)
                        i.calcAccelTo(j)
                        self.r_min = min(self.r_min, dist)
                        self.r_max = max(self.r_max, dist)

            for i in system:
                i.update()

    #Put each object to screen
    def drawSystem(self, system, screen, zoom, offset_x, offset_y, focused_object_id):
        # If view focused on some object - put it to screen
        if focused_object_id > -1:
            dx = screen.get_width() / 2 - system[focused_object_id].x * zoom
            dy = screen.get_height() / 2 - system[focused_object_id].y * zoom
        # Not focused - put view to fixed position
        else:
            dx = (0 + screen.get_width()) * (1-zoom) / 2 + offset_x
            dy = (0 + screen.get_height()) * (1-zoom) / 2 + offset_y


        for i in system:
            i.draw(screen, zoom, dx, dy)

    def getMin(self):
        return self.r_min

    def getMax(self):
        return self.r_max