from ..logic.common import clamp as _clamp
from ..logic.time import CountUp as _CountUp
from ..math.calculus import LinearChange as _LinearChange
from ..math.geometry import Point as _Point
from copy import deepcopy as _deepcopy


class AbstractEffect(_CountUp):
    def __init__(self, shape, original, result, ticks, factor, fixed_end):
        self.shape = shape
        self.original = _deepcopy(original)
        self.result = _deepcopy(result)
        self.fixed_end = fixed_end
        if self.fixed_end:
            func = self.fixed_end_func
        else:
            func = None
        _CountUp.__init__(self, ticks, factor, func)
        self._counter = 1
        self._base += 1

    def shape_update(self):
        pass

    def fixed_end_func(self):
        pass

    def tick(self):
        self.shape_update()
        _CountUp.tick(self)


class Move(AbstractEffect):
    def __init__(self, shape, new_pos, ticks, motion_class=_LinearChange, factor=1, fixed_end=True):
        AbstractEffect.__init__(self, shape, _Point(shape.x, shape.y), new_pos, ticks, factor, fixed_end)
        self.motion_x = motion_class(self.result.x - self.shape.x, ticks)
        self.motion_y = motion_class(self.result.y - self.shape.y, ticks)

    def shape_update(self):
        if self.fixed_end:
            x = self.original.x + self.motion_x.s(self._counter)
            y = self.original.y + self.motion_y.s(self._counter)
            self.shape.set_pos(x, y)
        else:
            dx = self.motion_x.v(self._counter)
            dy = self.motion_y.v(self._counter)
            self.shape.move(dx, dy)

    def fixed_end_func(self):
        self.shape.set_pos(self.result.x, self.result.y)

    @staticmethod
    def linear_from_speed(shape, dx, dy, ticks, factor=1, fixed_end=True):
        x_destination = shape.x + dx * ticks
        y_destination = shape.y + dy * ticks
        return Move(shape, _Point(x_destination, y_destination), ticks, _LinearChange, factor, fixed_end)


class Resize(AbstractEffect):
    def __init__(self, shape, new_size, ticks, motion_class=_LinearChange, factor=1, fixed_end=True):
        AbstractEffect.__init__(self, shape, (shape.width, shape.height), new_size, ticks, factor, fixed_end)
        self.resize_width = motion_class(self.result[0] - self.shape.width, ticks)
        self.resize_height = motion_class(self.result[1] - self.shape.height, ticks)

    def shape_update(self):
        if self.fixed_end:
            width = self.original[0] + self.resize_width.s(self._counter)
            height = self.original[1] + self.resize_height.s(self._counter)
            self.shape.set_size(width, height)
        else:
            d_width = self.resize_width.v(self._counter)
            d_height = self.resize_height.v(self._counter)
            self.shape.move_size(d_width, d_height)

    def fixed_end_func(self):
        self.shape.set_size(self.result[0], self.result[1])

    @staticmethod
    def linear_from_speed(shape, d_width, d_height, ticks, factor=1, fixed_end=True):
        width_result = shape.width + d_width * ticks
        height_result = shape.height + d_height * ticks
        return Resize(shape, (width_result, height_result), ticks, _LinearChange, factor, fixed_end)


class ColorTransition(AbstractEffect):
    def __init__(self, shape, new_color, ticks, motion_class=_LinearChange, factor=1, fixed_end=True):
        AbstractEffect.__init__(self, shape, shape.color, new_color, ticks, factor, fixed_end)
        self.change_r = motion_class(self.result.r - self.shape.color.r, ticks)
        self.change_g = motion_class(self.result.g - self.shape.color.g, ticks)
        self.change_b = motion_class(self.result.b - self.shape.color.b, ticks)

    def shape_update(self):
        if self.fixed_end:
            r = self.original.r + self.change_r.s(self._counter)
            g = self.original.g + self.change_g.s(self._counter)
            b = self.original.b + self.change_b.s(self._counter)
        else:
            r = self.shape.color.r + self.change_r.v(self._counter)
            g = self.shape.color.g + self.change_g.v(self._counter)
            b = self.shape.color.b + self.change_b.v(self._counter)
        self.shape.color.r = int(_clamp(r, 0, 255))
        self.shape.color.g = int(_clamp(g, 0, 255))
        self.shape.color.b = int(_clamp(b, 0, 255))

    def fixed_end_func(self):
        self.shape.color = self.result


class Rotate(AbstractEffect):
    def __init__(self, shape, radians, ticks, motion_class=_LinearChange, factor=1, fixed_end=True):
        """
        Although this effect supports both fixed_end = True and fixed_end = False, it is advised to use fixed_end = True
        here given the complex nature of rotations and how, over time, precision gets lost with these functions.
        """
        AbstractEffect.__init__(self, shape, shape.points, radians, ticks, factor, fixed_end)
        self.radians_motion = motion_class(radians, ticks)

    def shape_update(self):
        if self.fixed_end:
            self.shape.set_points(self.original)
            radians = self.radians_motion.s(self._counter)
        else:
            radians = self.radians_motion.v(self._counter)
        self.shape.rotate(radians)

    def fixed_end_func(self):
        self.shape.set_points(self.original)
        self.shape.rotate(self.result)

    @staticmethod
    def linear_from_speed(shape, rad_speed, ticks, factor=1, fixed_end=True):
        radians = rad_speed * ticks
        return Rotate(shape, radians, ticks, _LinearChange, factor, fixed_end)
