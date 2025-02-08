from pygame_work2 import *
import pygame
from pygame import Color


def main():
    Application.init("main")
    Display.set_mode(560, 500, resizable=True)
    Display.set_min_size(560, 120)
    Display.clear_icon()
    pygame.display.set_caption("")

    Images["state_1"] = "images/state_1.png"
    Images["state_2"] = "images/state_2.png"
    Images["state_3"] = "images/state_3.png"
    rect = FilledRect(0, 0, 100, 50, 0, 0, Color(150, 0, 200))
    text = SurfaceRect.from_image(0, 50, 0, 0, "images/text.png")
    image_list = [Images["state_1"], Images["state_2"], Images["state_3"]]
    point_list = [(0, 100), (100, 100), (50, 0)]

    f1 = FunctionLoader(print, "You just pressed up while hovering over this button.")
    f2 = FunctionLoader(print, "You just pressed down while hovering over this button.")
    f3 = FunctionLoader(print, "You are pressing while hovering over this button.")
    f4 = FunctionLoader(print, "You are hovering over this button.")

    rect_button = RectButton(10, 10, 100, 100, 0, 0, Default.shape_color1, f1, None, None, None)
    circle_button = CircleButton(120, 10, 50, 0, 0, Default.shape_color2, None, f2, None, None)
    surf_button = SurfaceButton(230, 10, 0, 0, 100, 100, image_list, None, None, f3, None)
    pol_button = PolygonButton(340, 10, point_list, 0, 0, Color(0, 200, 50), None, None, None, f4)

    group_button = GroupButton(450, 10, 0, 0, [rect, text], 100, 100, None, None, f3, f4)

    main_page = Page("main", [rect_button, circle_button, surf_button, pol_button, group_button])

    Application.add_page(main_page)
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
