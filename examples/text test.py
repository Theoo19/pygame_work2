from pygame_work2 import *
from random import randint


def main():
    Application.init("main")
    Display.set_mode(600, 600, resizable=True)
    Display.clear_icon()
    Display.set_caption("Testing")

    Default.pt = 60

    text = "Pegasus & Joris en de Draak - De Magische Klok - Efteling".split()
    r1 = list(Text(0, 0, 0, 0, Default.pt, Default.font, [[content]]) for content in text)
    width = r1[0].font.render(" ", True, (0, 0, 0)).get_width()

    g1 = RowsGroup(0, 0, LayoutFill(20, -20), 0, r1, 0, Format.middle, Format.below, True, width)

    page = Page("main", [g1])

    Application.add_page(page)
    Application.loop()
    Application.quit()


if __name__ == '__main__':
    main()
