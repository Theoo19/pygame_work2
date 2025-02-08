from pygame_work2 import *
import pygame
from pygame import Color
from copy import deepcopy


selected_shape = None


@Mouse.key_bind_down(MouseButtonType.left)
def select():
    main_page = Application.get_page("main")
    for shape in main_page.shapes[1]:
        if shape.collide_point(Mouse):
            global selected_shape
            selected_shape = shape
            break


@Mouse.key_bind_up(MouseButtonType.left)
def deselect():
    global selected_shape
    selected_shape = None


@Keyboard.key_bind_down(pygame.K_SPACE)
def area():
    main_page = Application.get_page("main")
    polygon = main_page.shapes[0]
    print(Area.polygon(polygon))


def set_pos():
    global selected_shape
    main_page = Application.get_page("main")
    polygon = main_page.shapes[0]

    if selected_shape is not None:
        selected_shape.move(Mouse.dx, Mouse.dy)
        buttons = main_page.shapes[1]
        polygon.set_points(list((c.xm, c.ym) for c in buttons))

    if polygon.collide_point(Mouse):
        polygon.color = Color(0, 100, 0)
    else:
        polygon.color = Color(0, 255, 0)
    if Intersect.polygon_polygon(polygon, deepcopy(polygon)):
        polygon.color = Color(255, 0, 0)


def main():
    Application.init("main")
    Display.set_mode(600, 600)
    Display.clear_icon()
    pygame.display.set_caption("Area test")

    buttons = list(CircleButton(pos[0] + 200, pos[1] + 200, 10, 0, 0, Color(255, 0, 0), None, None, None, None) for pos in Points.star(200, 75, 7))
    polygon = FilledPolygon(0, 0, list((c.xm, c.ym) for c in buttons), 0, 0, Color(0, 255, 0))

    page = Page("main", [polygon, DynamicGroup(0, 0, 0, 0, buttons, 0, 0)])
    page.loop_function = set_pos

    Application.add_page(page)
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
