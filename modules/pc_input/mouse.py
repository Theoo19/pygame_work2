from pygame import mouse as _mouse
from ..math.geometry import Point as _Point, Collision as _Collision
from ..logic.constants import MouseButtonType as _MouseButtonType
from .key import Button as _Button


class MouseObject(_Point):
    def __init__(self, x, y):
        _Point.__init__(self, x, y)
        self.left = _Button(_MouseButtonType.left)
        self.middle = _Button(_MouseButtonType.middle)
        self.right = _Button(_MouseButtonType.right)
        self.moving = True
        self.visible = True
        self.scroll = 0

        self.dx = 0
        self.dy = 0

        self.__key_binds_down = dict()
        self.__key_binds_up = dict()
        self.__key_binds_pressed = dict()

    def get_button(self, index):
        if index == _MouseButtonType.left:
            return self.left
        if index == _MouseButtonType.middle:
            return self.middle
        if index == _MouseButtonType.right:
            return self.middle

    def set_x(self, x):
        _Point.set_x(self, x)
        _mouse.set_pos(self.x, self.y)

    def set_y(self, y):
        _Point.set_y(self, y)
        _mouse.set_pos(self.x, self.y)

    def set_pos(self, x, y):
        _Point.set_pos(self, x, y)
        _mouse.set_pos(self.x, self.y)

    def set_visible(self, visible):
        self.visible = visible
        _mouse.set_visible(visible)

    def update_pos(self):
        mouse_x, mouse_y = _mouse.get_pos()
        if mouse_x != self.x or mouse_y != self.y:
            self.moving = True
            self.dx = mouse_x - self.x
            self.dy = mouse_y - self.y
            self.x = mouse_x
            self.y = mouse_y
        else:
            self.moving = False
            self.dx = 0
            self.dy = 0

    def in_rect(self, rect):
        return _Collision.rect_point(rect, self)

    def in_circle(self, circle):
        return _Collision.circle_point(circle, self)

    def in_polygon(self, polygon):
        return _Collision.polygon_point(polygon, self)

    def update_buttons(self):
        self.left.update()
        self.right.update()
        self.middle.update()
        self.scroll = 0

        if self.left.get_pressed() and self.left.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.left.get_type()]()
        if self.right.get_pressed() and self.right.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.right.get_type()]()
        if self.middle.get_pressed() and self.middle.get_type() in self.__key_binds_pressed:
            self.__key_binds_pressed[self.middle.get_type()]()

    def reset_buttons(self):
        self.left.reset()
        self.right.reset()
        self.middle.reset()

    def update_button_up(self, index=1):
        if index == _MouseButtonType.left:
            self.left.set_press_up()
        elif index == _MouseButtonType.middle:
            self.middle.set_press_up()
        elif index == _MouseButtonType.right:
            self.right.set_press_up()

        if index in self.__key_binds_up:
            self.__key_binds_up[index]()

    def update_button_down(self, index=1):
        if index == _MouseButtonType.left:
            self.left.set_press_down()
        elif index == _MouseButtonType.middle:
            self.middle.set_press_down()
        elif index == _MouseButtonType.right:
            self.right.set_press_down()
        elif index == _MouseButtonType.scroll_down:
            self.scroll = -1
        elif index == _MouseButtonType.scroll_up:
            self.scroll = 1

        if index in self.__key_binds_down:
            self.__key_binds_down[index]()

    def update(self):
        self.update_pos()
        self.update_buttons()

    def get_scroll(self):
        return self.scroll == 1 or self.scroll == -1

    def set_key_bind_down(self, func, index):
        self.__key_binds_down[index] = func

    def set_key_bind_up(self, func, index):
        self.__key_binds_up[index] = func

    def set_key_bind_pressed(self, func, index):
        self.__key_binds_pressed[index] = func

    def set_key_bind_scroll(self, func):
        self.set_key_bind_down(func, _MouseButtonType.scroll_down)
        self.set_key_bind_down(func, _MouseButtonType.scroll_up)

    def key_bind_down(self, index):
        def wrapper(func):
            self.set_key_bind_down(func, index)
            return func
        return wrapper

    def key_bind_up(self, index):
        def wrapper(func):
            self.set_key_bind_up(func, index)
            return func
        return wrapper

    def key_bind_pressed(self, index):
        def wrapper(func):
            self.set_key_bind_pressed(func, index)
            return func
        return wrapper

    def key_bind_scroll(self):
        def wrapper(func):
            self.set_key_bind_scroll(func)
            return func
        return wrapper


Mouse = MouseObject(0, 0)
