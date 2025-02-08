from .basic import SurfaceRect as _SurfaceRect, FilledRect as _FilledRect, FilledCircle as _FilledCircle, \
     FilledPolygon as _FilledPolygon
from ..math.geometry import Rect as _Rect
from .collection import SurfaceGroup as _Group
from ..pc_input.mouse import Mouse as _Mouse, MouseObject as _MouseObject
from ..logic.constants import ButtonState as _ButtonState, MouseButtonType as _MouseButtonType
from ..logic.loaders import FunctionLoader as _FunctionLoader
from ..logic.layout import LayoutDefault as _LayoutDefault
from pygame import Color as _Color, Surface as _Surface
from collections.abc import Sequence as _Sequence


class AbstractButton:
    """A class to contain the abstract functionality of a button without a visual implementation."""

    def __init__(self, press_up_function, press_down_function, pressed_function, hover_function):
        """Initiate AbstractButton object.

        :param press_up_function: object to store function and needed parameters, called when button is pressed up
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :param press_down_function: object to store function and needed parameters, called when button is pressed down
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :param pressed_function: object to store function and needed parameters, called when button is pressed
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :param hover_function: object to store function and needed parameters, called when button is hovered over
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """
        self.press_up_function = _FunctionLoader.from_variable(press_up_function)
        self.press_down_function = _FunctionLoader.from_variable(press_down_function)
        self.pressed_function = _FunctionLoader.from_variable(pressed_function)
        self.hover_function = _FunctionLoader.from_variable(hover_function)
        self.mouse_hover = False
        self.mouse_click = False
        self.state_change = _ButtonState.default

    def _update_state(self):
        """Update the visual representation of the button state using the state_change attribute.

        Template to be inherited and modified for visual button classes. If there is a state_change, it should have
        some visual representation.
        """
        pass

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.

        Template to be inherited and modified for visual button classes. If there is a collision, it should return True.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        return False

    def mouse_states(self, mouse_object=_Mouse, mouse_button_type=_MouseButtonType.left):
        """Update the state_change attribute according to the point position and the mouse button states.

        Detect any changes in the state of the button. There is a state change if:
        -The point went from outside the defined area into the defined area of the button (hover)
        -The point went from inside the defined area outside the defined area of the button (default)
        -The left mouse button clicked down while inside the defined area of the button (click)
        -The left mouse button clicked up while inside the defined area of the button (hover)

        Attribute "state_change" will be updated following the state change (default / hover / click), with no state
        change it will be reset (none). Two bool values keep track of the relation between the button and the mouse:
        mouse_hover and mouse_click.

        When state change "hover -> click" occurs, press_down_function is executed.
        When state change "click -> hover" occurs, press_up_function is executed.
        When the point is inside the defined area of the button, pressed_function is executed.


        :param mouse_object: point used for the collision function
        :type mouse_object: _MouseObject
        :param mouse_button_type: specifies mouse button used: left (1), middle (2), right (3)
        :type mouse_button_type: int
        :return: if there is a state change
        :rtype: bool
        """

        mouse_button = mouse_object.get_button(mouse_button_type)
        self.state_change = _ButtonState.none
        if self.collide_point(mouse_object):
            self.hover_function.execute()
            if not self.mouse_hover:
                self.mouse_hover = True
                self.state_change = _ButtonState.hover
            if mouse_button.get_press_down():
                self.mouse_click = True
                self.state_change = _ButtonState.click
                self.press_down_function.execute()
            elif self.mouse_click:
                if mouse_button .get_press_up():
                    self.mouse_click = False
                    self.state_change = _ButtonState.hover
                    self.press_up_function.execute()
                else:
                    self.pressed_function.execute()
        elif self.mouse_hover:
            self.mouse_hover = False
            self.mouse_click = False
            self.state_change = _ButtonState.default
        self._update_state()
        return self.state_change != _ButtonState.none

    def loop_behavior(self):
        """Code behavior of the shapes during the loop of the application."""
        return self.mouse_states()


class SurfaceButton(AbstractButton, _SurfaceRect):
    """A class to represent a rectangular button with a two-dimensional color-array in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, width, height, state_surfaces, press_up_function, press_down_function,
                 pressed_function, hover_function):
        """Initiate SurfaceButton object, inheriting from AbstractButton and SurfaceRect class.

        :type x: float
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type width: float
        :type height: float
        :param state_surfaces: surface to display depending on the state of the button (default / hover / click)
        :type state_surfaces: [_Surface, _Surface, _Surface]
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """
        _SurfaceRect.__init__(self, x, y, x_mode, y_mode, width, height)
        AbstractButton.__init__(self, press_up_function, press_down_function, pressed_function, hover_function)
        self.state_surfaces = state_surfaces
        self._update_state()

    def _update_state(self):
        """Update the visual representation (surface) of the button state using the state_change attribute."""
        if self.state_change != _ButtonState.none:
            try:
                _SurfaceRect.set_surface(self, self.state_surfaces[self.state_change])
            except IndexError:
                pass

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        return _SurfaceRect.collide_point(self, mouse_object)


class RectButton(AbstractButton, _FilledRect):
    """A class to represent a rectangular button with color in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode, color, press_up_function, press_down_function,
                 pressed_function, hover_function):
        """Initiate RectButton object, inheriting from AbstractButton and Rectangle class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """
        _FilledRect.__init__(self, x, y, width, height, x_mode, y_mode, color)
        AbstractButton.__init__(self, press_up_function, press_down_function, pressed_function, hover_function)
        self.default_color = self.color
        self.hover_color = self.default_color + _Color(40, 40, 40, 0)
        self.click_color = self.default_color - _Color(30, 30, 30, 0)
        self._update_state()

    def _update_state(self):
        """Update the visual representation (color) of the button state using the state_change attribute."""
        if self.state_change == _ButtonState.default:
            self.color = self.default_color
        elif self.state_change == _ButtonState.hover:
            self.color = self.hover_color
        elif self.state_change == _ButtonState.click:
            self.color = self.click_color

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        return _FilledRect.collide_point(self, mouse_object)

    def set_color(self, color, update_hover_click=True):
        """Set color to certain value and update hover- and click-color.

        :param color: RGB color
        :type color: _Color
        :param update_hover_click: determines of hover- and click-color should also be updated
        :type update_hover_click: bool
        """
        self.default_color = color
        if update_hover_click:
            self.hover_color = self.default_color + _Color(40, 40, 40, 0)
            self.click_color = self.default_color - _Color(30, 30, 30, 0)
        if self.mouse_click:
            self.color = self.click_color
        elif self.mouse_hover:
            self.color = self.hover_color
        else:
            self.color = self.default_color


class CircleButton(RectButton, _FilledCircle):
    """A class to represent a circular button with color in two-dimensional space."""

    def __init__(self, x, y, radius, x_mode, y_mode, color, press_up_function, press_down_function, pressed_function,
                 hover_function):
        """Initiate RectButton object, inheriting from AbstractButton and Rectangle class.

        :type x: float
        :type y: float
        :type radius: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """
        _FilledCircle.__init__(self, x, y, radius, x_mode, y_mode, color)
        RectButton.__init__(self, x, y, radius * 2, radius * 2, x_mode, y_mode, color, press_up_function,
                            press_down_function, pressed_function, hover_function)

    def draw(self, surface):
        """Draw Circle to a given surface.

        :type surface: _Surface
        """
        _FilledCircle.draw(self, surface)

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        return _FilledCircle.collide_point(self, mouse_object)


class PolygonButton(_FilledPolygon, RectButton):
    """A class to represent a polygon button with color in two-dimensional space."""

    def __init__(self, x, y, points, x_mode, y_mode, color, press_up_function, press_down_function, pressed_function,
                 hover_function):
        """Initiate PolygonButton object, inheriting from RectButton and Polygon class.

        :type x: float
        :type y: float
        :type points: list of Point or tuple of Point
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """

        RectButton.__init__(self, x, y, 0, 0, x_mode, y_mode, color, press_up_function,
                            press_down_function, pressed_function, hover_function)
        _FilledPolygon.__init__(self, x, y, points, x_mode, y_mode, color)

    def draw(self, surface):
        """Draw Polygon to a given surface.

        :type surface: _Surface
        """
        _FilledPolygon.draw(self, surface)

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        return _FilledPolygon.collide_point(self, mouse_object)


class GroupButton(AbstractButton, _Group):
    """A class to represent a group button with shapes in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, shapes, width, height, press_up_function,
                 press_down_function, pressed_function, hover_function):
        """Initiate GroupButton object, inheriting from AbstractButton and Group class.

        :type x: float
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type shapes: list of _Rect
        :type width: float
        :type height: float
        :type press_up_function: _FunctionLoader or _Sequence or function or None
        :type press_down_function: _FunctionLoader or _Sequence or function or None
        :type pressed_function: _FunctionLoader or _Sequence or function or None
        :type hover_function: _FunctionLoader or _Sequence or function or None
        """
        _Group.__init__(self, x, y, x_mode, y_mode, shapes, width, height)
        AbstractButton.__init__(self, press_up_function, press_down_function, pressed_function, hover_function)

    def collide_point(self, mouse_object=_Mouse):
        """Check if a point is within the defined area of the button.
        
        Here the first shapes in the shapes list is chosen to check the collision against. This is to give the ability
        to add shapes to the group that aren't clickable. If the collision of the base shapes doesn't satisfy, a general
        "Rect" or other shapes with transparent color can be chosen as base_shape to function as collision detection.

        :type mouse_object: _MouseObject
        :rtype: bool
        """
        for shape in self.shapes:
            if shape.collide_point(mouse_object):
                return True
        return False
