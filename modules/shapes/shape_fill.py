from pygame import draw as _draw, Color as _Color, Surface as _Surface


def transition(surface, x, y, width, height, color_1, color_2, horizontal=True):
    """Draw color transition from color_1 to color_2 on specific rect on given surface.

    :param surface: surface to get drawn on
    :type surface: _Surface
    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param width: length along x-axis
    :type width: float
    :param height: length along y-axis
    :type height: float
    :param color_1: left- or top RGB color
    :type color_1: _Color
    :param color_2: right- or bottom RGB color
    :type color_2: _Color
    :param horizontal: transition is horizontal if True, else transition is vertical
    :type horizontal: bool
    """
    if horizontal:
        length = int(width)
    else:
        length = int(height)

    r = color_1[0]
    g = color_1[1]
    b = color_1[2]

    dr = (color_2[0] - color_1[0]) / length
    dg = (color_2[1] - color_1[1]) / length
    db = (color_2[2] - color_1[2]) / length

    for i in range(0, length):
        if horizontal:
            _draw.rect(surface, (r, g, b), ((x, y), (1, height)))
            x += 1
        else:
            _draw.rect(surface, (r, g, b), ((x, y), (width, 1)))
            y += 1
        r += dr
        g += dg
        b += db


def multiple_transitions(surface, x, y, width, height, color_list, horizontal=True):
    """Draw color transition from color_list on specific rect on given surface.

    :param surface: surface to get drawn on
    :type surface: _Surface
    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param width: length along x-axis
    :type width: float
    :param height: length along y-axis
    :type height: float
    :param color_list: list of colors to transition to from left to right or top to bottom
    :type color_list: list of _Color
    :param horizontal: transition is horizontal if True, else transition is vertical
    :type horizontal: bool
    """
    if horizontal:
        length = width
    else:
        length = height
    avg_length = int(length / (len(color_list) - 1))
    color_1 = color_list[0]

    for color_2 in color_list[1:]:
        if horizontal:
            transition(surface, x, y, avg_length, height, color_1, color_2, horizontal)
            x += avg_length
        else:
            transition(surface, x, y, width, avg_length, color_1, color_2, horizontal)
            y += avg_length
        color_1 = color_2


def rainbow_transition(surface, x, y, width, height, rgb=255, horizontal=True):
    """Draw color transition from rainbow color_list on specific rect on given surface.

    :param surface: surface to get drawn on
    :type surface: _Surface
    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param width: length along x-axis
    :type width: float
    :param height: length along y-axis
    :type height: float
    :param rgb: brightness of rainbow transition, range = [0, 255]
    :type rgb: int
    :param horizontal: transition is horizontal if True, else transition is vertical
    :type horizontal: bool
    """
    color_list = [_Color(rgb, 0, 0), _Color(rgb, rgb, 0), _Color(0, rgb, 0), _Color(0, rgb, rgb), _Color(0, 0, rgb),
                  _Color(rgb, 0, rgb), _Color(rgb, 0, 0)]
    multiple_transitions(surface, x, y, width, height, color_list, horizontal)
