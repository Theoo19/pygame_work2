from .constants import Format as _Format


class LayoutDefault:
    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        """Align the x-coordinate of the shape within a given rect.

        :param shape:
        :type shape:
        :param total_width:
        :type total_width:
        :param total_height:
        :type total_height:
        :param x_start:
        :type x_start:
        :param y_start:
        :type y_start:
        """
        ...

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        """Align the y-coordinate of the shape within a given rect.

        :param shape:
        :type shape:
        :param total_width:
        :type total_width:
        :param total_height:
        :type total_height:
        :param x_start:
        :type x_start:
        :param y_start:
        :type y_start:
        """
        ...

    def align_from_rect_x(self, shape, rect):
        self.align_x(shape, rect.width, rect.height, rect.x, rect.y)

    def align_from_rect_y(self, shape, rect):
        self.align_y(shape, rect.width, rect.height, rect.x, rect.y)

    def update_alignment_x(self, shape, dx): ...

    def update_alignment_y(self, shape, dy): ...

    @staticmethod
    def from_variable(obj):
        if isinstance(obj, LayoutDefault):
            return obj
        if obj == _Format.left or obj == _Format.above:
            return LayoutLeftAbove(0)
        if obj == _Format.right or obj == _Format.below:
            return LayoutRightBelow(0)
        if obj == _Format.middle:
            return LayoutMiddle(0)
        if obj == _Format.fill:
            return LayoutFill(0, 0)
        if obj == _Format.default:
            return LayoutDefault()
        print("Warning: type: {} is not valid. Loading default Layout.".format(type(obj)))
        return LayoutDefault()


class LayoutLeftAbove(LayoutDefault):
    def __init__(self, offset):
        self.offset = offset

    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_x(self.offset + x_start)

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_y(self.offset + y_start)

    def set_offset_x(self, shape, offset):
        dx = offset - self.offset
        self.offset = offset
        shape.move_x(dx)

    def set_offset_y(self, shape, offset):
        dy = offset - self.offset
        self.offset = offset
        shape.move_y(dy)


class LayoutRightBelow(LayoutDefault):
    def __init__(self, offset):
        self.offset = offset

    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_x(total_width - shape.width + self.offset + x_start)

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_y(total_height - shape.height + self.offset + y_start)

    def update_alignment_x(self, shape, dx):
        shape.move_x(-dx)

    def update_alignment_y(self, shape, dy):
        shape.move_y(-dy)

    def set_offset_x(self, shape, offset):
        dx = offset - self.offset
        self.offset = offset
        shape.move_x(dx)

    def set_offset_y(self, shape, offset):
        dy = offset - self.offset
        self.offset = offset
        shape.move_y(dy)


class LayoutMiddle(LayoutDefault):
    def __init__(self, offset):
        self.offset = offset

    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_x((total_width - shape.width) / 2 + self.offset + x_start)

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_y((total_height - shape.height) / 2 + self.offset + y_start)

    def update_alignment_x(self, shape, dx):
        shape.move_x(-dx / 2)

    def update_alignment_y(self, shape, dy):
        shape.move_y(-dy / 2)

    def set_offset_x(self, shape, offset):
        dx = offset - self.offset
        self.offset = offset
        shape.move_x(dx)

    def set_offset_y(self, shape, offset):
        dy = offset - self.offset
        self.offset = offset
        shape.move_y(dy)


class LayoutFill(LayoutDefault):
    def __init__(self, offset_1, offset_2):
        self.offset_1 = offset_1
        self.offset_2 = offset_2

    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_x(self.offset_1 + x_start)
        shape.set_width(total_width - shape.x + self.offset_2 + x_start)

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_y(self.offset_1 + y_start)
        shape.set_height(total_height - shape.y + self.offset_2 + y_start)

    def set_offset_1_x(self, shape, offset):
        dx = offset - self.offset_1
        self.offset_1 = offset
        shape.move_x(dx)

    def set_offset_1_y(self, shape, offset):
        dy = offset - self.offset_1
        self.offset_1 = offset
        shape.move_y(dy)

    def set_offset_2_x(self, shape, offset):
        dx = offset - self.offset_2
        self.offset_2 = offset
        shape.move_x(dx)

    def set_offset_2_y(self, shape, offset):
        dy = offset - self.offset_2
        self.offset_2 = offset
        shape.move_y(dy)


class LayoutFraction(LayoutDefault):
    def __init__(self, offset, fraction):
        self.offset = offset
        self.numerator, self.denominator = fraction

    def align_x(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_x(self.numerator / self.denominator * total_width - shape.width / 2 + self.offset + x_start)

    def align_y(self, shape, total_width, total_height, x_start=0, y_start=0):
        shape.set_y(self.numerator / self.denominator * total_height - shape.height / 2 + self.offset + y_start)

    def update_alignment_x(self, shape, dx):
        shape.move_x(self.numerator * -dx / self.denominator)

    def update_alignment_y(self, shape, dy):
        shape.move_y(self.numerator * -dy / self.denominator)

    def set_offset_x(self, shape, offset):
        dx = offset - self.offset
        self.offset = offset
        shape.move_x(dx)

    def set_offset_y(self, shape, offset):
        dy = offset - self.offset
        self.offset = offset
        shape.move_y(dy)
