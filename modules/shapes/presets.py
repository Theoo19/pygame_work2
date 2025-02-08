from pygame import Color as _Color
from .basic import Text as _Text
from .collection import SurfaceGroup as _Group
from .interactables import Slider as _Slider, CheckBox as _CheckBox
from .button import RectButton as _RectButton
from ..logic.constants import Default as _Default, Format as _Layout


def default_slider(x, y, x_mode, y_mode, color, font, header_text, val_range, default_value,
                   rounding, value_change_function=None):
    """Create default slider using preset.

    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param x_mode: alignment type along x-axis within given rect
    :type x_mode: int
    :param y_mode: alignment type along y-axis within given rect
    :type y_mode: int
    :param color: base RGB color of all shapes in Slider
    :type color: _Color
    :param font: text font of header and value
    :type font: str
    :param header_text: text list of header-text
    :type header_text: list or set or tuple
    :param val_range: number range between which sliver-value is defined
    :type val_range: (float, float)
    :param default_value: default sliver-value
    :type default_value: float
    :param rounding: to which decimal point the sliver-value is rounded (0 is int)
    :type rounding: int
    :param value_change_function: object to store function and needed parameters, called when value is changed
    :type value_change_function: _FunctionLoader
    :return:
    :rtype: _Slider
    """
    header_color = color - _Color(30, 30, 30, 0)
    slider_color = color + _Color(30, 30, 30, 0)
    value_color = color

    return _Slider(x, y, x_mode, y_mode, 270, 90, 200, 50, header_color, font, 30, header_text, slider_color,
                   _Color(30, 30, 30), _Color(250, 250, 250), value_color, font, 30, ["-"], val_range, default_value,
                   rounding, value_change_function)


def default_check_box(x, y, x_mode, y_mode, color, box_text, value1, value2, value_change_function=None):
    """Create default checkbox using preset.

    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param x_mode: alignment type along x-axis within given rect
    :type x_mode: int
    :param y_mode: alignment type along y-axis within given rect
    :type y_mode: int
    :param color: RGB color of the box
    :type color: _Color
    :param box_text: default text to display
    :type box_text: str
    :param value1: primary and default checkbox-value
    :type value1: object
    :param value2: secondary checkbox-value
    :type value2: object
    :param value_change_function: object to store function and needed parameters, called when value is changed
    :type value_change_function: _FunctionLoader
    :return:
    :rtype: _Checkbox
    """
    box_color = color
    line_color = color - _Color(30, 30, 30, 0)
    value_color = _Default.shape_color1

    return _CheckBox(x, y, x_mode, y_mode, 50, 50, box_color, value_color, line_color, 5, _Default.font, _Default.pt,
                     (box_text,), value1, value2, value_change_function)


def default_button(x, y, x_mode, y_mode, color, box_text, press_up_function, press_down_function=None,
                   pressed_function=None, hover_function=None, width=150, height=50):
    """Create default rectangular button using preset.

    :param x: x-coordinate
    :type x: float
    :param y: y-coordinate
    :type y: float
    :param x_mode: alignment type along x-axis within given rect
    :type x_mode: int
    :param y_mode: alignment type along y-axis within given rect
    :type y_mode: int
    :param color: RGB color
    :type color: _Color or (int, int, int)
    :param box_text: content of centre text of button
    :type box_text: str
    :param press_up_function: object to store function and needed parameters, called when button is pressed up
    :type press_up_function: FunctionLoader or _Sequence or function or None
    :param press_down_function: object to store function and needed parameters, called when button is pressed down
    :type press_down_function: FunctionLoader or _Sequence or function or None
    :param pressed_function: object to store function and needed parameters, called when button is pressed
    :type pressed_function: FunctionLoader or _Sequence or function or None
    :param hover_function: object to store function and needed parameters, called when button is hovered over
    :type hover_function: FunctionLoader or _Sequence or function or None
    :return:
    :rtype: _Group
    """
    button = _RectButton(0, 0, width, height, 0, 0, color, press_up_function, press_down_function, pressed_function,
                         hover_function)
    text = _Text(0, 0, _Layout.middle, _Layout.middle, 35, _Default.font, [[box_text]])

    return _Group(x, y, x_mode, y_mode, [button, text], 200, 100)
