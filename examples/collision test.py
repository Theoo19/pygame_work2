from pygame_work2 import *
import pygame
from pygame import Color
from random import randint

from pygame_work2 import Circle


def resolve_collision(c1, c2):
    distance = Geometry.distance((c1.xm, c1.ym), (c2.xm, c2.ym))
    displacement = (distance - c1.radius - c2.radius) / 2

    c1.move_x(-displacement * (c1.xm - c2.xm) / distance)
    c1.move_y(-displacement * (c1.ym - c2.ym) / distance)

    c2.move_x(displacement * (c1.xm - c2.xm) / distance)
    c2.move_y(displacement * (c1.ym - c2.ym) / distance)


class Particle(FilledCircle):
    def __init__(self, x, y, radius, color):
        FilledCircle.__init__(self, x, y, radius, 0, 0, color)
        self.dx = 0
        self.dy = 0
        self.ax = 0
        self.ay = 0


class MainPage(Page):
    def __init__(self):
        self.circles = list(Particle(randint(0, Display.width), randint(0, Display.height), randint(10, 50),
                                     Color(0, 0, 100)) for i in range(30))
        self.selected = None

        Page.__init__(self, "main", self.circles)

    def loop_function(self):
        for c1 in self.circles:
            for c2 in self.circles:
                if c1 != c2:
                    if Collision.circle_circle(c1, c2):
                        resolve_collision(c1, c2)

        if Mouse.left.get_press_down():
            for c1 in self.shapes:
                if c1.collide_point(Mouse):
                    self.selected = c1
                    break
        elif Mouse.left.get_pressed() and self.selected is not None:
            self.selected.move(Mouse.dx, Mouse.dy)
        elif Mouse.left.get_press_up():
            self.selected = None


def main():
    Application.init("main")
    Display.set_mode(500, 500, resizable=True)
    Display.clear_icon()
    pygame.display.set_caption("Collision test")

    Application.add_page(MainPage())
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
