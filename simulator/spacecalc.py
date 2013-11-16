from simulator.combinedRocket import CombinedRocket
from simulator.rocket import Rocket


class SpaceCalculator:
    N = 10
    circles = 0
    r_min = 9999.0
    r_max = 0.0
    min_dist = 0.0
    land_dist = 0.0
    max_dist = 0.0
    landing_speed = 0.0
    config = ''

    def __init__(self, min_dist, max_dist, landing_speed, cfg):
        self.max_dist = max_dist
        self.min_dist = min_dist
        self.land_dist = 2*min_dist
        self.landing_speed = landing_speed
        self.config = cfg

    def newPosition(self, system):
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

                        if not self.isLanded(i, j, dist):
                            i.calcAccelTo(j)
                            #if isinstance(i, Rocket) and isinstance(j, Rocket):
                                #print(abs(i.vy - j.vy), abs(i.vx - j.vx), i.name, j.name)
                            self.r_min = min(self.r_min, dist)
                        else:
                            #If both of them are rockets, combine them
                            if isinstance(i, Rocket) and isinstance(j, Rocket):
                                self.combineObjects(i, j, system)
                            #If one of them is not a rocket it means landing
                            else:
                                self.landObjects(i, j)

                        #self.r_min = min(self.r_min, dist)
                        self.r_max = max(self.r_max, dist)

            for i in system:
                i.update()

    #Put each object to screen
    def drawSystem(self, system, screen, zoom, offset_x, offset_y, focused_object_id):
        # If view focused on some object - put it to screen
        if focused_object_id >= len(system):
            focused_object_id = len(system)-1
        if focused_object_id > -1:
            dx = screen.get_width() / 2 - system[focused_object_id].x * zoom
            dy = screen.get_height() / 2 - system[focused_object_id].y * zoom
        # Not focused - put view to fixed position
        else:
            dx = (0 + screen.get_width()) * (1-zoom) / 2 + offset_x
            dy = (0 + screen.get_height()) * (1-zoom) / 2 + offset_y

        for i in system:
            i.draw(screen, zoom, dx, dy)

    def isLanded(self, object1, object2, dist):
        res = True

        if isinstance(object1, Rocket) and object1.engine_on:
            res = False

        if isinstance(object2, Rocket) and object2.engine_on:
            res = False

        if dist > self.land_dist:
            res = False

        if abs(object1.vx - object2.vx) > self.landing_speed:
            res = False
            #print("Vx1 - Vx2 is too big", abs(object1.vx - object2.vx))

        if abs(object1.vy - object2.vy) > self.landing_speed:
            res = False
            #print("Vy1 - Vy2 is too big ", abs(object1.vy - object2.vy))

        #if res:
            #print("Landing of ", object1.name, " to ", object2.name, " is DONE!")
        return res

    #TODO: Add decombineObjects functios

    def combineObjects(self, i, j, system):
        if isinstance(i, Rocket) and isinstance(j, Rocket):
            system.remove(i)
            system.remove(j)
            combine = CombinedRocket([i, j], self.config)
            system.append(combine)

    def landObjects(self, i, j):
        vx = (i.vx*i.getMass() + j.vx*j.getMass())/(i.getMass() + j.getMass())
        vy = (i.vy*i.getMass() + j.vy*j.getMass())/(i.getMass() + j.getMass())

        i.vx = vx
        i.vy = vy
        j.vx = vx
        j.vy = vy


    def collisionDetected(self):
        return self.r_min <= self.min_dist

    def outOfSystemDetected(self):
        return self.r_max >= self.max_dist


