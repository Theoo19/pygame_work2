from pygame import Color as _Color


class KeyType:
    """A class to store constants about key types."""

    up = 273
    down = 274
    left = 276
    right = 275
    shiftLeft = 304
    shiftRight = 303
    altLeft = 308
    altRight = 307
    ctrlLeft = 306
    ctrlRight = 305
    capsLock = 301
    tab = 9
    backspace = 8
    enter = 13
    windows = 211


class MouseButtonType:
    """A class to store constants about mouse-button types."""

    left = 1
    middle = 2
    right = 3

    scroll_down = 4
    scroll_up = 5


class Format:
    """A class to store constants about layout modes and text modes."""

    default = 0
    left = 1
    right = 2
    middle = 3
    above = 4
    below = 5
    fill = 6

    text_left = 7
    text_right = 8
    text_fill = 9

    bold = 0
    italic = 1
    underline = 2


class Default:
    """A class to store constants about default shape values."""

    pt = 30
    font = "Arial"
    text_color = _Color(0, 0, 0)
    bold = False
    italic = False
    underline = False

    rect_width = 120
    rect_height = 50
    circle_radius = 50

    shape_color1 = _Color(50, 170, 230)
    shape_color2 = _Color(160, 50, 100)
    shape_color3 = _Color(160, 160, 160)

    background_color = _Color(250, 250, 250)

    ticks = 60


class CharacterType:
    """A class to store constants about character types.

    alpha: abcdefghijklmnopqrstuvwxyz
    numeric: 0123456789
    """

    none = -1
    all = 0
    alpha = 1
    numeric = 2


class ButtonState:
    """A class to store constants about button states."""

    none = -1
    default = 0
    hover = 1
    click = 2


Colors = {"red": _Color(255, 0, 0),
          "green": _Color(0, 255, 0),
          "blue": _Color(0, 0, 255),
          "yellow": _Color(255, 255, 0),
          "magenta": _Color(255, 0, 255),
          "cyan": _Color(0, 255, 255),
          "white": _Color(255, 255, 255),
          "black": _Color(0, 0, 0)
          }
