from pygame_work2 import *
import pygame
from pygame import Color
from math import pi


@Mouse.key_bind_up(MouseButtonType.left)
def update1():
    main_page = Application.get_page("main")
    star = main_page.shapes[0]
    main_page.timeline.append(Rotate(star, 2*pi, 1 * Application.ticks, ParabolaChange))
    main_page.timeline.append(ColorTransition(star, Color(0, 0, 255), 1 * Application.ticks, ParabolaChange))
    print(star)


@Mouse.key_bind_up(MouseButtonType.right)
def update2():
    main_page = Application.get_page("main")
    star = main_page.shapes[0]
    main_page.timeline.append(Rotate(star, -2*pi, 1 * Application.ticks, ParabolaChange))
    main_page.timeline.append(ColorTransition(star, Color(255, 0, 0), 1 * Application.ticks, ParabolaChange))


def main():
    Application.init("main")
    Display.set_mode(500, 500, resizable=True)
    Display.clear_icon()
    pygame.display.set_caption("Testing ground")

    star = FilledPolygon(0, 0, Points.star(250, 100, 5), Format.middle, Format.middle, Color(255, 0, 0))
    page = Page("main", [star])

    Application.add_page(page)
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
