from .loaders import Fonts as _Fonts
from pygame import font as _font, error as _error, Surface as _Surface, SRCALPHA as _SRCALPHA
from pygame.image import load as _load


def clamp(value, min_value, max_value):
    """Clamp value between min_value and max_value"""
    return min(max_value, max(min_value, value))


def represent(value_string, *values):
    """Universal formatting method of __repr__

    :param value_string: value names separated by spaces
    :type value_string: str
    :param values: values to represent
    :return: formatted string for __repr__
    :rtype: str
    """
    strings = value_string.split()
    return "<{}>".format(", ".join("{}: {}".format(strings[i], values[i]) for i in range(0, len(values))))


def load_font(name, pt, bold=False, italic=False, underline=False):
    """Load font from name and pt into Fonts object. If not available, load default font.

    :param name: name of the font
    :type name: str
    :param pt: font size
    :type pt: int
    :param bold: bold font
    :type bold: bool
    :param italic: italic font
    :type italic: bool
    :param underline: underlined font
    :type underline: bool
    :return: pygame font object
    :rtype: _font.Font
    """
    if not _font.get_init():
        _font.init()

    if name.lower() in _font.get_fonts():
        try:
            font = _font.SysFont(name, pt)
        except _error:
            font = _font.SysFont(name, pt)
    else:
        try:
            font = _font.Font(_Fonts[name], pt)
        except KeyError:
            print("Error: font: {} couldn't be loaded".format(name))
            font = _font.SysFont("", pt)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    return font


def frames_from_image(filename, width, height, frame_count):
    """Load multiple surfaces from one image.

    :param filename: path to image
    :type filename: str
    :param width: width of one surface
    :type width: int
    :param height: height of one surface
    :type height: int
    :param frame_count: amount of surfaces to load from image
    :type frame_count: int
    :return: frame list
    :rtype: list of _Surface
    """
    image = _load(filename).convert_alpha()
    frames = list()
    img_width = image.get_width()
    img_height = image.get_height()

    if img_width == width:
        frame_count = min(frame_count, int(img_height / height))
        for y in range(frame_count):
            frame = _Surface((width, height), _SRCALPHA)
            frame.blit(image, (0, -y * height))
            frames.append(frame)
    elif img_height == height:
        frame_count = min(frame_count, int(img_width / width))
        for x in range(frame_count):
            frame = _Surface((width, height), _SRCALPHA)
            frame.blit(image, (-x * width, 0))
            frames.append(frame)
    else:
        for y in range(0, img_height, height):
            for x in range(0, img_width, width):
                frame = _Surface((width, height), _SRCALPHA)
                frame.blit(image, (-x, -y))
                frames.append(frame)
                if len(frames) == frame_count:
                    break
            if len(frames) == frame_count:
                break
    return frames
