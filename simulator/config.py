import configparser
import argparse
import textwrap
from simulator.rocket import *


class Config:
    width = 0
    height = 0
    starts = 0
    display = (0, 0)
    initial_x = 0
    initial_y = 0
    landing_max_speed = 0.0
    initial_zoom = 1
    star_colors = []

    def __init__(self):
        parser = argparse.ArgumentParser(description='Solar mechanics simulator',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog=textwrap.dedent('''\
                Keys used:
                    q or ESC     = Exit
                    p or SPACE   = Pause
                    f            = Toggle full screen (if supported)
                    z            = Zoom in
                    x            = Zoom out
                    arrow keys   = Screen move
                    s            = Start/Stop saving screens to screens/ directory. If started,
                 screen shot per second will be stored
                    TAB          = Center view to next object
            '''))

        parser.add_argument('-f', '--file',
                            dest='file',
                            default='config/main.ini',
                            help='configuration file')

        args = parser.parse_args()

        self.config = configparser.ConfigParser()
        self.config.read(args.file)

        sys = self.config['System']
        self.width = int(sys.get("WIN_WIDTH", 800))
        self.height = int(sys.get("WIN_HEIGHT", 640))
        self.stars = int(sys.get("STAR_NUM", 10))

        self.initial_x = int(sys.get("X", 0))
        self.initial_y = int(sys.get("Y", 0))

        self.landing_max_speed = float(sys.get("LANDING_MAX_SPEED", 2))
        self.initial_zoom = float(sys.get("ZOOM", 1))

        self.display = (self.width, self.height)

        colors = sys.get("STAR_COLORS")
        self.star_colors = colors.split(',')

        self.space_color = sys.get("SPACE_COLOR")

    def getSystem(self):
        s = []

        for i in self.config.sections():
            if i != "System":
                object_type = self.config[i]["type"]

                if object_type == 'planet':
                    obj = FlyObject(i,
                                    int(self.config[i]["Mass"]),
                                    float(self.config[i]["X"]),
                                    float(self.config[i]["Y"]),
                                    float(self.config[i]["VX"]),
                                    float(self.config[i]["VY"]))

                    obj.initSurface(int(self.config[i]["R"]),
                                    self.config[i]["color"])

                    s.append(obj)

                if object_type == 'rocket':
                    rocket_class = self.getClass(self.config[i]["RocketClass"])

                    obj = rocket_class(i,
                                       int(self.config[i]["Mass"]),
                                       float(self.config[i]["X"]),
                                       float(self.config[i]["Y"]),
                                       float(self.config[i]["VX"]),
                                       float(self.config[i]["VY"]),
                                       float(self.config[i]["FuelEfficient"]),
                                       float(self.config[i]["FuelConsume"]),
                                       float(self.config[i]["FuelWeight"])
                    )

                    obj.setFuel(float(self.config[i]["Fuel"]))

                    obj.initImages(self.config[i]["EngineOffImage"], self.config[i]["EngineOnImage"])

                    s.append(obj)

        return s

    def getDisplay(self):
        return self.display

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getStarNumber(self):
        return self.stars

    def getStarColors(self):
        return self.star_colors

    def getSpaceColor(self):
        return self.space_color

    def getInitialX(self):
        return self.initial_x

    def getInitialY(self):
        return self.initial_y

    def getInitialZoom(self):
        return self.initial_zoom

    def getLandingMaxSpeed(self):
        return self.landing_max_speed

    def getClass(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m