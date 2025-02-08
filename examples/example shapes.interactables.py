from pygame_work2 import *
import pygame
from pygame import Color


def print_value(self):
    print("The new value is {}".format(self.value))
    main_page = Application.get_page("main")
    main_page.background_color = Color(self.value, self.value, self.value)

    slider_2 = main_page.shapes[1]
    slider_2.set_value(self.value)


def toggle_dark_mode(checkbox):
    main_page = Application.get_page("main")
    if checkbox.value:
        main_page.background_color = Color(50, 50, 50)
    else:
        main_page.background_color = Default.background_color


def main():
    Application.init("main")
    Display.set_mode(560, 500, resizable=True)
    Display.set_min_size(560, 120)
    Display.clear_icon()
    pygame.display.set_caption("")

    slider = Slider.preset(0, 0, 0, 0, 270, 80, Default.shape_color2, "Example slider", 30, "Arial",
                           Color(0, 0, 0), (0, 255), 50, 0, print_value)
    slider2 = default_slider(290, 0, 0, 0, Default.shape_color1, "Arial", "Slider preset", (-100, 300), 0, 1)
    checkbox = CheckBox(0, 90, 0, 0, 60, 60, Color(200, 0, 0), Color(0, 200, 0), Color(0, 0, 0), 5, "Arial", 30,
                               ["Dark mode: "], False, True, toggle_dark_mode)
    writing_box = WritingBox(0, 160, 0, 0, [["Write something"]], 30, "Arial", Default.shape_color1, 250, 50,
                             max_length=20)

    slider.value_change_function.set_parameters(slider)
    checkbox.value_change_function.set_parameters(checkbox)

    main_page = Page("main", [slider, slider2, checkbox, writing_box])

    Application.add_page(main_page)
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
