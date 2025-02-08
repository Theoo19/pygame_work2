from .basic import FilledRect as _FilledRect, Text as _Text, LineRect as _LineRect, FilledLine as _FilledLine
from .collection import SurfaceGroup as _Group
from .button import AbstractButton as _AbstractButton, CircleButton as _CircleButton, RectButton as _RectButton
from ..logic.constants import Format as _Format, KeyType as _KeyType, CharacterType as _CharacterType
from ..logic.common import clamp as _clamp
from ..logic.loaders import FunctionLoader as _FunctionLoader
from ..pc_input.mouse import Mouse as _Mouse
from ..pc_input.keyboard import Keyboard as _Keyboard
from ..pc_output.pages import Application as _Application
from pygame import Color as _Color
from math import inf as _inf


class AbstractSlider(_AbstractButton):
    """A class to contain the abstract functionality of a slider without a visual implementation."""

    def __init__(self, val_range, default_value, rounding, value_change_function):
        """Initiate AbstractSlider object, inheriting from AbstractButton class.

        :param val_range: number range between which sliver-value is defined
        :type val_range: (float, float)
        :param default_value: default sliver-value
        :type default_value: float
        :param rounding: to which decimal point the sliver-value is rounded (0 is int)
        :type rounding: int
        :param value_change_function: object to store function and needed parameters, called when value is changed
        :type value_change_function: _FunctionLoader
        """
        _AbstractButton.__init__(self, None, None, None, None)
        self.min_value = val_range[0]
        self.max_value = val_range[1]
        self.default_value = default_value
        self.rounding = rounding
        self.value = default_value
        self.value_change = True
        self.value_change_function = _FunctionLoader.from_variable(value_change_function)

    def set_value(self, value):
        """Set sliver-value to a given value.

        Only update if the value is different from the current value. Clamp value between min- and max value.
        Round value to the correct decimal point, call value_change_function.

        :param value: new value slider-value
        :type value: float
        """
        if value != self.value:
            value = _clamp(value, self.min_value, self.max_value)

            if self.rounding > 0:
                self.value = round(value, self.rounding)
            else:
                self.value = int(value)
            self.value_change = True
            self.value_change_function.execute()

    def reset_value(self):
        """Set sliver-value to default value."""
        self.set_value(self.default_value)


class Slider(_Group, AbstractSlider):
    """A class to represent a slider with defined visual representation in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, total_width, total_height, slider_width, slider_height,
                 header_color, header_font, header_pt, header_text, slider_color, slider_button_color,
                 slider_line_color, value_color, value_font, value_pt, value_text, val_range, default_value, rounding,
                 value_change_function):
        """Initiate Slider object, inheriting from Group and AbstractSlider class.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: int
        :param total_width: total length along x-axis
        :type total_width: float
        :param total_height: total length along y-axis
        :type total_height: float
        :param slider_width: width of slider-rect
        :type slider_width: float
        :param slider_height: height of slider-rect
        :type slider_height: float
        :param header_color: RGB color of header-rect
        :type header_color: _Color
        :param header_font: font of header-text
        :type header_font: str
        :param header_pt: font size
        :type header_pt: int
        :param header_text: text list of header-text
        :type header_text: list or set or tuple
        :param slider_color: RGB color of slider-rect
        :type slider_color: _Color
        :param slider_button_color: RGB color of slider-button
        :type slider_button_color: _Color
        :param slider_line_color: RGB color of slider-line
        :type slider_line_color: _Color
        :param value_color: RGB color of value-rect
        :type value_color: _Color
        :param value_font: font of value-text
        :type value_font: str
        :param value_pt: font size
        :type value_pt: int
        :param value_text: text list of value-text
        :type value_text: list or set or tuple
        :param val_range: number range between which sliver-value is defined
        :type val_range: (float, float)
        :param default_value: default sliver-value
        :type default_value: float
        :param rounding: to which decimal point the sliver-value is rounded (0 is int)
        :type rounding: int
        :param value_change_function: object to store function and needed parameters, called when value is changed
        :type value_change_function: _FunctionLoader
        """
        h_height = total_height - slider_height
        v_width = total_width - slider_width
        line_y = h_height + slider_height / 2

        self.header = _FilledRect(0, 0, total_width, h_height, 0, 0, header_color)
        self.slider = _FilledRect(0, h_height, slider_width, slider_height, 0, 0, slider_color)
        self.value_rect = _FilledRect(slider_width, h_height, v_width, slider_height, 0, 0, value_color)
        self.header_text = _Text(10, 0, 0, _Format.middle, header_pt, header_font, header_text)
        self.value_text = _Text(0, 0, _Format.middle, _Format.middle, value_pt, value_font, value_text)
        self.line = _FilledLine(0.1 * slider_width, line_y, 0.8 * slider_width, 0, 0, 0, 5, slider_line_color)
        self.circle = _CircleButton(0, line_y - 10, 10, 0, 0, slider_button_color, None, None, None, None)

        AbstractSlider.__init__(self, val_range, default_value, rounding, value_change_function)
        _Group.__init__(self, x, y, x_mode, y_mode, [self.header, self.slider, self.value_rect, self.line, self.circle,
                        self.value_text, self.header_text], 0, 0)

        self.set_value(self.default_value / 1)
        self.update_slider()
        self._update_display_number()
        self.header_text.update_alignment_in_rect(self.header)

    def _update_state(self):
        """Update the visual representation of the button state using the state_change attribute."""
        if self.state_change == 0:
            self.circle.color = self.circle.default_color
        elif self.state_change == 1:
            self.circle.color = self.circle.hover_color
        elif self.state_change == 2:
            self.circle.color = self.circle.click_color

    def _update_shape_alignment(self):
        """Ignore shape alignment because that is already done."""
        pass

    def _update_display_number(self):
        """Update visual representation of slider-value and redraw surface."""
        self.value_text.set_content(str(self.value), 0)
        self.value_text.update_alignment_in_rect(self.value_rect)
        self._update_draw()

    def move_slider(self):
        """Depending on the position of the mouse, set value to min-value, max-value or anywhere in between."""
        if _Mouse.x < self.line.x:
            self.circle.set_x(self.line.x - self.circle.radius)
            self.set_value(self.min_value)
        elif _Mouse.x > self.line.x2:
            self.circle.set_x(self.line.x2 - self.circle.radius)
            self.set_value(self.max_value)
        else:
            self.circle.set_x(_Mouse.x - self.circle.radius)
            self.update_value()

    def set_value(self, value):
        """Set sliver-value to a given value, then update visual representation of slider-value.

        :param value: new value slider-value
        :type value: float
        """
        AbstractSlider.set_value(self, value)
        self.update_slider()

    def update_value(self):
        """Update slider-value based on button position and update visual representation of slider-value."""
        percentage = (self.circle.xm - self.line.x) / self.line.width
        AbstractSlider.set_value(self, self.min_value + percentage * (self.max_value - self.min_value))
        self._update_display_number()

    def update_slider(self):
        """Update button position based on slider-value and update visual representation of button position."""
        percentage = (self.value - self.min_value) / (self.max_value - self.min_value)
        self.circle.set_x(self.line.x + self.line.width * percentage - 10)
        self._update_display_number()

    def loop_behavior(self):
        """Code behavior of the slider during the loop of the application."""
        self.value_change = False
        update = self.mouse_states()
        if self.mouse_hover and self.mouse_click:
            self.move_slider()
            update = True
        if update:
            self._update_draw()
        return update

    @staticmethod
    def preset(x, y, x_mode, y_mode, total_width, total_height, average_color, header_str, pt, font,
               text_color, val_range, default_value, rounding, value_change_function=None):
        """Create Slider object with preset values.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: int
        :param total_width: total length along x-axis
        :type total_width: float
        :param total_height: total length along y-axis
        :type total_height: float
        :param average_color: average RGB color of all shapes in Slider
        :type average_color: _Color
        :param header_str: content of header-text
        :type header_str: str
        :param pt: font size of header and value
        :type pt: int
        :param font: text font of header and value
        :type font: str
        :param text_color: RGB color of header- and value-text
        :type text_color: _Color
        :param val_range: number range between which sliver-value is defined
        :type val_range: (float, float)
        :param default_value: default sliver-value
        :type default_value: float
        :param rounding: to which decimal point the sliver-value is rounded (0 is int)
        :type rounding: int
        :param value_change_function: object to store function and needed parameters, called when value is changed
        :type value_change_function: _FunctionLoader
        :return:
        :rtype: Slider
        """
        slider_width = total_width * 0.8
        slider_height = total_height * 0.5
        header_color = average_color + _Color(20, 20, 20, 0)
        slider_color = average_color - _Color(20, 20, 20, 0)
        value_color = average_color - _Color(50, 50, 50, 0)

        slider_button_color = _Color(150, 150, 150)
        slider_line_color = _Color(10, 10, 10)

        return Slider(x, y, x_mode, y_mode, total_width, total_height, slider_width, slider_height, header_color,
                      font, pt, [(header_str, text_color)], slider_color, slider_button_color, slider_line_color,
                      value_color, font, pt, [("", text_color)], val_range, default_value, rounding,
                      value_change_function)


class AbstractCheckBox:
    """A class to contain the abstract functionality of a checkbox without a visual implementation."""

    def __init__(self, value1, value2, value_change_function):
        """Initiate AbstractCheckbox object.

        :param value1: primary and default checkbox-value
        :type value1: object
        :param value2: secondary checkbox-value
        :type value2: object
        :param value_change_function: object to store function and needed parameters, called when value is changed
        :type value_change_function: _FunctionLoader
        """
        self.value1 = value1
        self.value2 = value2
        self.value = value1
        self.value_change = True
        self.value_change_function = _FunctionLoader.from_variable(value_change_function)

    def toggle_value(self):
        """Toggle value between primary and secondary value."""
        if self.value == self.value1:
            self.value = self.value2
        else:
            self.value = self.value1
        self.value_change = True
        self.value_change_function.execute()


class CheckBox(_Group, AbstractCheckBox):
    """A class to represent a checkbox with defined visual representation in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, width, height, val1_color, val2_color, line_color,
                 line_width, font, pt, box_text, value1, value2, value_change_function):
        """Initiate CheckBox object, inheriting from Group and AbstractCheckBox class.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: int
        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        :param val1_color: RGB color for primary value
        :type val1_color: _Color
        :param val2_color: RGB color for secondary value
        :type val2_color: _Color
        :param line_color: RGB color for checkbox-edge
        :type line_color: _Color
        :param line_width: thickness of checkbox-edge
        :type line_width: int
        :param font: text font
        :type font: str
        :param pt: font size
        :type pt: int
        :param box_text: list of attributes containing content and any properties deviating from default values
        :type box_text: list or set or tuple
        :param value1: primary and default checkbox-value
        :type value1: object
        :param value2: secondary checkbox-value
        :type value2: object
        :param value_change_function: object to store function and needed parameters, called when value is changed
        :type value_change_function: _FunctionLoader
        """
        self.val1_color = val1_color
        self.val2_color = val2_color

        self.check_button = _RectButton(0, 0, width, height, 0, 0, val1_color, self.toggle_value, None, None, None)
        self.line_box = _LineRect(0, 0, width, height, 0, 0, line_color, line_width)
        self.text = _Text(width + 10, 0, 0, _Format.middle, pt, font, [box_text, str(value1)])

        AbstractCheckBox.__init__(self, value1, value2, value_change_function)
        _Group.__init__(self, x, y, x_mode, y_mode, [self.check_button, self.line_box, self.text], 0, 0)
        self._update_text_box()
        self._update_draw()

    def _update_shape_alignment(self):
        """Ignore shape alignment because that is already done."""
        pass

    def _update_text_box(self):
        """Update content text and alignment of text in rect, update size of self."""
        self.text.set_content(str(self.value), 1)
        self.text.update_alignment_in_rect(self)
        self._update_size()

    def toggle_value(self):
        """Toggle value between primary and secondary value."""
        AbstractCheckBox.toggle_value(self)
        if self.check_button.default_color == self.val1_color:
            self.check_button.set_color(self.val2_color)
        else:
            self.check_button.set_color(self.val1_color)
        self._update_text_box()
        self._update_draw()


class AbstractWritingBox:
    """A class to contain the abstract functionality of a writing box without a visual implementation."""

    def __init__(self, content, min_length, max_length, allowed_chars):
        """Initiate AbstractWritingBox class.

        :param content: content to be written
        :type content: str
        :param min_length: min length of content
        :type min_length: int
        :param max_length: max length of content
        :type max_length: int
        :param allowed_chars: characters allowed in content (letters / numbers), default should be "CharacterType.all"
        :type allowed_chars: int
        """
        self.content = content
        self.min_length = min_length
        self.max_length = max_length
        self.allowed_chars = allowed_chars
        self.enabled = True

    def get_content(self):
        """Get content of writing-box.

        :return: content of writing-box
        :rtype: str
        """
        return self.content

    def set_content(self, content):
        """Set content of writing-box to a certain value.

        :param content: new content of writing-box
        :type content: str
        """
        self.content = content

    def enable(self):
        """Enable user to edit content of writing-box."""
        self.enabled = True

    def disable(self):
        """Disable user to edit content of writing-box."""
        self.enabled = False

    def toggle_enabled(self):
        """Toggle ability of user to edit content of writing-box."""
        self.enabled = not self.enabled

    def update_content(self):
        """Update content of writing-box if a key is pressed and key-type and min- and max-length allow it."""
        key = _Keyboard.last_key
        if key.get_press_down() or key.get_timed_pressed_interval(_Application.ticks):
            key = _Keyboard.last_key
            if key.check_character_type_validity(self.allowed_chars) and len(self.content) < self.max_length:
                self.content += key.get_char()
            elif key.get_type() == _KeyType.backspace and len(self.content) > self.min_length:
                self.content = self.content[:-1]
        self.set_content(self.content)

    def loop_behavior(self):
        """Code behavior of the writing-box during the loop of the application."""
        if _Keyboard.last_key is not None and self.enabled:
            self.update_content()
            return True


class WritingBox(_Group, AbstractWritingBox):
    """A class to represent a writing box with defined visual representation in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, text_list, pt, font, color, width, height, content="",
                 min_length=0, max_length=_inf, allowed_chars=_CharacterType.all):
        """Initiate WritingBox object, inheriting from Group and AbstractWritingBox class.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: int
        :param text_list:
        :type text_list:
        :param pt: font size
        :type pt: int
        :param font: text font
        :type font: str
        :param color: RGB color of box
        :type color: _Color
        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        :param content: content to be written
        :type content: str
        :param min_length: min length of content
        :type min_length: int
        :param max_length: max length of content
        :type max_length: int
        :param allowed_chars: characters allowed in content (letters / numbers), default should be "CharacterType.all"
        :type allowed_chars: int
        """
        self.box = _FilledRect(0, 0, width, height, 0, 0, color)
        self.text = _Text(0, 0, _Format.middle, _Format.middle, pt, font, text_list)
        AbstractWritingBox.__init__(self, content, min_length, max_length, allowed_chars)
        _Group.__init__(self, x, y, x_mode, y_mode, [self.box, self.text], width, height)

    def set_content(self, content):
        """Set content of writing-box to a certain value.

        :param content: new content of writing-box
        :type content: str
        """
        self.content = content
        self.text.set_content(content)
        self._update_draw()

    def loop_behavior(self):
        """Code behavior of the writing-box during the loop of the application."""
        return AbstractWritingBox.loop_behavior(self)
