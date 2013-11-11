import random

import pygame

from simulator.rocket import *
from simulator.config import *
from simulator.spacecalc import *


CRASH_DIST = 5
OUT_DIST = 10000


def main():
    cfg = Config()

    offset_x = cfg.getInitialX()
    offset_y = cfg.getInitialY()
    zoom = cfg.getInitialZoom()
    landing_speed = cfg.getLandingMaxSpeed()

    #PyGame init
    pygame.init()
    screen = pygame.display.set_mode(cfg.getDisplay())
    pygame.display.set_caption("RedTroll space program")

    #Space init
    bg = Surface(cfg.getDisplay())
    bg.fill(Color(cfg.getSpaceColor()))
    #Draw fixed stars   
    for i in range(cfg.getStarNumber()):
        draw.circle(bg, Color(random.sample(cfg.getStarColors(), 1)[0]),
                    (random.randrange(cfg.getWidth()),
                     random.randrange(cfg.getHeight())),
                    0)

    #Timer init                     
    timer = pygame.time.Clock()

    #Solar system init
    system = cfg.getSystem()

    #Focus screen on
    focused = -1

    calc = SpaceCalculator(CRASH_DIST, OUT_DIST, landing_speed)

    done = False
    paused = False
    save_screen = False

    frame_no = 0
    frame_saved = 0

    while not done:
        timer.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
                break
            if e.type == KEYDOWN:
                if e.key == K_q or e.key == K_ESCAPE:
                    done = True
                    break
                if e.key == K_p or e.key == K_SPACE:
                    paused = not paused
                if e.key == K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == K_LEFT:
                    offset_x += 10
                if e.key == K_RIGHT:
                    offset_x -= 10
                if e.key == K_UP:
                    offset_y += 10
                if e.key == K_DOWN:
                    offset_y -= 10
                if e.key == K_z:
                    zoom *= 2
                if e.key == K_x:
                    zoom /= 2
                if e.key == K_s:
                    save_screen = not save_screen
                if e.key == K_TAB:
                    focused += 1
                    if focused >= len(system):
                        focused = 0
                    print('View focused on: ' + system[focused].name)

        if not paused:
            calc.newPosition(system)

            #Put space to screen
            screen.blit(bg, (0, 0))

            calc.drawSystem(system, screen, zoom, offset_x, offset_y, focused)

            #update screen
            pygame.display.update()

            frame_no += 1

            if save_screen and (frame_no - frame_saved > 1):
                file_to_save = 'screens/screen%05d.tga' % (frame_saved, )
                image.save(screen, file_to_save)
                frame_saved = frame_no

            if calc.collisionDetected():
                print("Collision detected! Exiting... ")
                break
            if calc.outOfSystemDetected():
                print("Out of system! Exiting...")
                break

    print(":-)")


if __name__ == "__main__":
    main()

