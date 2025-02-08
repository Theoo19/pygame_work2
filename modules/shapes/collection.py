from pygame import Color as _Color
from .basic import SurfaceRect as _SurfaceRect
from ..math.geometry import Rect as _Rect
from ..logic.constants import Format as _Format
from ..logic.common import represent as _represent
from ..logic.layout import LayoutDefault as _LayoutDefault, LayoutFill as _LayoutFill


class Group:
    def __init__(self, *shapes):
        self.shapes = list(shapes)

    def _update_group_dimensions(self): ...

    def _update_added_shapes(self, *shapes): ...

    def _update_shapes_x(self, dx):
        """Move all x-coordinates of shapes a given amount.

        Function should only be used internally.

        :param dx: change made to the x-coordinates
        :type dx: float
        """
        for shape in self.shapes:
            shape.move_x(dx)

    def _update_shapes_y(self, dy):
        """Move all y-coordinates of shapes a given amount.

        Function should only be used internally.

        :param dy: change made to the y-coordinates
        :type dy: float
        """
        for shape in self.shapes:
            shape.move_y(dy)

    def _update_shapes_pos(self, dx, dy):
        """Move all x- and y-coordinates of shapes given amounts.

        Function should only be used internally.

        :param dx: change made to the x-coordinates
        :type dx: float
        :param dy: change made to the y-coordinates
        :type dy: float
        """
        self._update_shapes_x(dx)
        self._update_shapes_y(dy)

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        for shape in self.shapes:
            shape.update_alignment(total_width, total_height, x_start, y_start)

    def draw(self, surface):
        """Draw shapes of shapes list to a given surface.

        Group will have no explicit visual representation, but if any of it's shapes do, it will get drawn.

        :param surface: surface to get drawn on
        :type surface: _Surface
        """
        for shape in self.shapes:
            shape.draw(surface)

    def loop_behavior(self):
        """Code behavior of the shapes during the loop of the application.

        Group will have no own explicit loop_behavior, but if any of it's shapes do, it will be executed.
        """
        for shape in reversed(self.shapes):
            shape.loop_behavior()

    def set_shapes(self, shapes):
        """Set shape list to a new given shape list.

        :param shapes: new shape list
        :type shapes: list of _Rect
        """
        self.shapes = shapes
        self._update_added_shapes(*shapes)
        self._update_group_dimensions()

    def append(self, shape):
        """Add shapes to end of shapes list.

        :param shape: shapes inheriting from Rect class
        :type shape: _Rect
        """
        self.shapes.append(shape)
        self._update_added_shapes(shape)
        self._update_group_dimensions()

    def clear(self):
        """Clear shapes list."""
        self.shapes.clear()
        self._update_group_dimensions()

    def count(self, shape):
        """Count amount of occurrences of given shapes in shapes list

        :param shape: shapes inheriting from Rect class
        :type shape: _Rect
        :return: amount of occurrences
        :rtype: int
        """
        return self.shapes.count(shape)

    def extend(self, shapes):
        """Extend shapes list with additional shapes list.

        :param shapes: list of shapes inheriting from Rect class
        :type shapes: list of _Rect
        """
        self.shapes.extend(shapes)
        self._update_added_shapes(*shapes)
        self._update_group_dimensions()

    def index(self, shape, start=0, stop=0):
        """Find index of given shapes.

        :param shape: shapes inheriting from Rect class, to be searched in shapes list
        :type shape: _Rect
        :param start: starting point in search
        :type start: int
        :param stop: stopping point in search
        :type stop: int
        :return: index of given shapes in shapes list
        :rtype: int
        """
        return self.shapes.index(shape, start, stop)

    def insert(self, index, shape):
        """Insert shapes at given index in shapes list.

        :param index: index in shapes list
        :type index: int
        :param shape: shapes inheriting from Rect class
        :type shape: _Rect
        """
        self.shapes.insert(index, shape)
        self._update_added_shapes(shape)
        self._update_group_dimensions()

    def pop(self, index):
        """Remove shapes from shapes list by index.

        :param index: index of shapes
        :type index: int
        """
        self.shapes.pop(index)
        self._update_group_dimensions()

    def remove(self, shape):
        """Remove shapes from shapes list by object.

        :param shape: shapes inheriting from Rect class to remove
        :type shape: _Rect
        """
        self.shapes.remove(shape)
        self._update_group_dimensions()

    def reverse(self):
        """Reverse the order of the shapes list."""
        self.shapes.reverse()

    def __setitem__(self, key, value):
        """Set certain shape depending on the key.
        :param key: index for self.shapes
        :type key: int
        :param value: shapes inheriting from Rect class
        :type value: _Rect
        """
        self.shapes[key] = value
        self._update_added_shapes(value)
        self._update_group_dimensions()

    def __getitem__(self, item):
        """Get certain shape depending on the index.

        :param item: index for self.shapes
        :type item: int
        :return: shapes inheriting from Rect class
        :rtype: _Rect
        """
        return self.shapes[item]

    def __iter__(self):
        """Initiate iteration sequence.

        :return: self
        :rtype: DynamicGroup
        """
        self.__index = 0
        return self

    def __len__(self):
        """Return length of shapes list.

        :return: length of shapes list
        :rtype: int
        """
        return len(self.shapes)

    def __next__(self):
        """Progress iteration sequence.

        :return: next shapes inheriting from Rect class of shapes list
        :rtype: _Rect
        """
        if self.__index < len(self.shapes):
            shape = self.shapes[self.__index]
            self.__index += 1
            return shape
        else:
            raise StopIteration

    def __repr__(self):
        """Generate string describing attributes of self.

        :return: description of own attributes
        :rtype: str
        """
        return _represent("shapes_amount", len(self))


class StaticGroup(Group, _Rect):
    def __init__(self, x, y, x_mode, y_mode, shapes, width, height):
        """Initiate StaticGroup object, inheriting from Group and Rect class.

        The StaticGroup x- and y-coordinate will be defined as the given x- and y-parameters. The x- and y-coordinates
        of the shapes will be treated as an additional change to their final x- and y-coordinates. This means the
        StaticGroup has a fixed position with all shapes having a relative position.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param shapes: list of shapes inheriting from Rect class
        :type shapes: list of _Rect
        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        """
        Group.__init__(self, *shapes)
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        self._update_group_dimensions()

    # TODO: unify this with RowsGroup
    #       Check where this function is used. Then make sure that, when new shapes are added, the function
    #       update_rows_alignment() is called again to update all the rows.
    def _update_added_shapes(self, *shapes):
        for shape in shapes:
            shape.move(self.x, self.y)

    # TODO: possibly update all shapes of self.rows?
    def _update_pos(self):
        """Position of StaticGroup is fixed."""
        pass

    def _update_width(self):
        """Update size of DynamicGroup to accurately reflect the dimensions of shapes in list.

        If there are shapes, then:
            width_max_1 is the largest width of all shapes
            width_max_2 is the largest distance between self.x and shapes.x2 for all shapes with mode "Layout.default"
            (This means self.x, self.y should already be defined when executing this function)
            width_max is the largest out of max_width_1 and max_width_2
        If there are no shapes, then:
            width_max, height_max are 0
        width and height will be set to width_max and height_max if DynamicGroup modes aren't "Layout.fill".
        """
        if len(self.shapes) > 0:
            max_widths_1 = set(shape.width for shape in self.shapes if type(shape.x_mode) is not _LayoutFill)
            max_widths_2 = set(shape.x2 - self.x for shape in self.shapes if type(shape.x_mode) is _LayoutDefault)
            max_widths = max_widths_1 | max_widths_2
            if len(max_widths) > 0:
                width_max = max(max_widths)
            else:
                width_max = 0
        else:
            width_max = 0

        if self.x_mode != _Format.fill:
            _Rect.set_width(self, width_max)

    def _update_height(self):
        """Update size of DynamicGroup to accurately reflect the dimensions of shapes in list.

        If there are shapes, then:
            height_max_1 is the largest height of all shapes
            height_max_2 is the largest distance between self.y and shapes.y2 for all shapes with mode "Layout.default"
            (This means self.x, self.y should already be defined when executing this function)
            height_max is the largest out of max_height_1 and max_height_2
        If there are no shapes, then:
            width_max, height_max are 0
        width and height will be set to width_max and height_max if DynamicGroup modes aren't "Layout.fill".
        """
        if len(self.shapes) > 0:
            max_heights_1 = set(shape.height for shape in self.shapes if type(shape.y_mode) is not _LayoutFill)
            max_heights_2 = set(shape.y2 - self.y for shape in self.shapes if type(shape.y_mode) is _LayoutDefault)
            max_heights = max_heights_1 | max_heights_2
            if len(max_heights) > 0:
                height_max = max(max_heights)
            else:
                height_max = 0
        else:
            height_max = 0

        if self.y_mode != _Format.fill:
            _Rect.set_height(self, height_max)

    def _update_size(self):
        self._update_width()
        self._update_height()

    # TODO: update to work with self.rows instead
    def _update_shape_alignment(self):
        """Update the dimensions of shapes within StaticGroup using x_mode and y_mode to specify their alignment."""
        for shape in self.shapes:
            shape.update_alignment_in_rect(self)

    def _update_group_dimensions(self):
        """Update position of StaticGroup. Update size of StaticGroup. Update dimensions of shapes in StaticGroup."""
        self._update_pos()
        self._update_size()
        self._update_shape_alignment()

    # TODO: change _update_shapes_x to work with self.rows
    def set_x(self, x):
        """Set x-coordinate to a given value and update shapes accordingly.

        :param x: new value x-coordinate
        :type x: float
        """
        self._update_shapes_x(x - self.x)
        _Rect.set_x(self, x)

    # TODO: change _update_shapes_y to work with self.rows
    def set_y(self, y):
        """Set y-coordinate to a given value and update shapes accordingly.

        :param y: new value y-coordinate
        :type y: float
        """
        self._update_shapes_y(y - self.y)
        _Rect.set_y(self, y)

    # TODO: change _update_shapes_pos to work with self.rows
    def set_pos(self, x, y):
        """Set x- and y-coordinate to given values and update shapes accordingly.

        :param x: new value x-coordinate
        :type x: float
        :param y: new value y-coordinate
        :type y: float
        """
        self._update_shapes_pos(x - self.x, y - self.y)
        _Rect.set_x(self, x)
        _Rect.set_y(self, y)

    # TODO: only _update_shape_alignment() should be changed (note already made)
    def set_width(self, width):
        """Set width to a given value and update shapes accordingly.

        :param width: new value width
        :type width: float
        """
        _Rect.set_width(self, width)
        self._update_shape_alignment()

    def set_height(self, height):
        """Set height to a given value and update shapes accordingly.

        :param height: new value height
        :type height: float
        """
        _Rect.set_height(self, height)
        self._update_shape_alignment()

    def set_size(self, width, height):
        """Set width and height to given values and update shapes accordingly.

        :param width: new value width
        :type width: float
        :param height: new value height
        :type height: float
        """
        _Rect.set_size(self, width, height)
        self._update_shape_alignment()

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        """Update the dimensions of the shapes within a given rect using x_mode and y_mode to specify their alignment.

        Update shapes accordingly.

        :param total_width: width of the square in which this shapes is updated
        :type total_width: float
        :param total_height: height of the square in which this shapes is updated
        :type total_height: float
        :param x_start: starting x-coordinate of the square in which this shapes is updated
        :type x_start: float
        :param y_start: starting y-coordinate of the square in which this shapes is updated
        :type y_start: float
        """
        _Rect.update_alignment(self, total_width, total_height, x_start, y_start)
        self._update_shape_alignment()

    def __repr__(self):
        """Generate string describing attributes of self.

        :return: description of own attributes
        :rtype: str
        """
        return _represent("x y width height shapes_amount", self.x, self.y, self.width, self.height, len(self))


class DynamicGroup(StaticGroup):
    """A class to represent a collection of shapes in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, shapes, width, height):
        """Initiate DynamicGroup object, inheriting from StaticGroup class.

        The DynamicGroup x- and y-coordinate will be defined by the shapes in the shapes list. The given x- and
        y-parameters will be treated as an additional change to the x- and y-coordinate of the DynamicGroup and all its
        shapes. This means the DynamicGroup 'wraps around' the given shapes.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param shapes: list of shapes inheriting from Rect class
        :type shapes: list of _Rect
        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        """
        StaticGroup.__init__(self, 0, 0, x_mode, y_mode, shapes, width, height)
        self.move(x, y)

    def _update_added_shapes(self, *shapes):
        pass

    def _update_pos(self):
        """Update position of DynamicGroup to accurately reflect the dimensions of shapes in list.

        If there are shapes with x_mode "Layout.default", x_min will be the smallest x-coordinate of those shapes.
        If there are shapes with y_mode "Layout.default", y_min will be the smallest y-coordinate of those shapes.

        If there are no shapes with that x_mode, x_min will be self.x.
        If there are no shapes with that y_mode, y_min will be self.y.

        The x- and y-coordinate of the DynamicGroup will then be updated. If it has an x_mode "Layout.middle", it will
        get corrected a dx amount. If it has an y_mode "Layout.middle", it will be corrected a dy amount.
        """
        x_mode_default_x = list(shape.x for shape in self.shapes if type(shape.x_mode) is _LayoutDefault)
        y_mode_default_y = list(shape.y for shape in self.shapes if type(shape.y_mode) is _LayoutDefault)

        if len(x_mode_default_x) > 0:
            x_min = min(x_mode_default_x)
        else:
            x_min = self.x
        if len(y_mode_default_y) > 0:
            y_min = min(y_mode_default_y)
        else:
            y_min = self.y

        dx = self.x - x_min
        dy = self.y - y_min
        _Rect.set_x(self, x_min)
        _Rect.set_y(self, y_min)
        if self.x_mode == _Format.middle:
            self.move_x(dx)
        if self.y_mode == _Format.middle:
            self.move_y(dy)


class SurfaceGroup(_SurfaceRect, DynamicGroup):
    """A class to represent a collection of shapes using a SurfaceRect in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, shapes, width, height):
        """Initiate Group object, inheriting from SurfaceRect and DynamicGroup class.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param shapes: list of shapes inheriting from Rect class
        :type shapes: list of _Rect
        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        """
        _SurfaceRect.__init__(self, x, y, x_mode, y_mode, width, height)
        DynamicGroup.__init__(self, x, y, x_mode, y_mode, shapes, width, height)
        self._update_draw()

    def _update_size(self):
        """Update size of Group to accurately reflect the dimensions of shapes in shapes list.
         
        Update surface accordingly."""
        DynamicGroup._update_size(self)
        self._update_surface()

    def _update_draw(self):
        """Update surface by clearing it and redrawing all the shapes from shapes list."""
        self.fill(_Color(0, 0, 0, 0))
        for shape in self.shapes:
            shape.move(-self.x, -self.y)
            shape.draw(self)
            shape.move(self.x, self.y)

    def _update_group_dimensions(self):
        """Update position, size and dimensions of shapes in Group. Update surface in which shapes are drawn."""
        DynamicGroup._update_group_dimensions(self)
        self._update_draw()

    def set_x(self, x):
        """Set x-coordinate to a given value and update shapes accordingly.

        :param x: new value x-coordinate
        :type x: float
        """
        self._update_shapes_x(x - self.x)
        _SurfaceRect.set_x(self, x)

    def set_y(self, y):
        """Set y-coordinate to a given value and update shapes accordingly.

        :param y: new value y-coordinate
        :type y: float
        """
        self._update_shapes_y(y - self.y)
        _SurfaceRect.set_y(self, y)

    def set_width(self, width):
        """Set width to a given value and update shapes accordingly. Update surface accordingly.

        :param width: new value width
        :type width: float
        """
        _SurfaceRect.set_width(self, width)
        self._update_size()
        self._update_shape_alignment()

    def set_height(self, height):
        """Set height to a given value and update shapes accordingly. Update surface accordingly.

        :param height: new value height
        :type height: float
        """
        _SurfaceRect.set_height(self, height)
        self._update_size()
        self._update_shape_alignment()

    def set_size(self, width, height):
        """Set width and height to given values and update shapes accordingly. Update surface accordingly.

        :param width: new value width
        :type width: float
        :param height: new value height
        :type height: float
        """
        _SurfaceRect.set_size(self, width, height)
        self._update_size()
        self._update_shape_alignment()

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        """Update the dimensions of the shapes within a given rect using x_mode and y_mode to specify their alignment.

        Update shapes accordingly. Update surface accordingly.

        :param total_width: width of the square in which this shapes is updated
        :type total_width: float
        :param total_height: height of the square in which this shapes is updated
        :type total_height: float
        :param x_start: starting x-coordinate of the square in which this shapes is updated
        :type x_start: float
        :param y_start: starting y-coordinate of the square in which this shapes is updated
        :type y_start: float
        """
        _SurfaceRect.update_alignment(self, total_width, total_height, x_start, y_start)
        self._update_shape_alignment()
        self._update_draw()

    def loop_behavior(self):
        """Code behavior of the shapes during the loop of the application.

        Group will have no own explicit loop_behavior, but if any of it's shapes do, it will be executed. If
        loop_behavior() returns True, surface will be updated accordingly.
        """
        # TODO: Does this make sense? This doesn't catch all updates, and shapes e.g. buttons, interactables shouldn't
        #       be in a Group class altogether, they should be in a DynamicGroup.
        update = False
        for shape in self.shapes:
            if shape.loop_behavior() and not update:
                update = True
        if update:
            self._update_draw()
        return update


class RowsGroup(StaticGroup):
    """A class to represent a collection of shapes sorted into rows in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, shapes, max_length, row_mode, shapes_mode, horizontal=True, dist_x=0,
                 dist_y=0):
        """Initiate RowsGroup object, inheriting from StaticGroup class.

        This class works under the following assumptions:
            All objects have an individual width/height smaller than max_length.
            The x- and y-mode are chosen to fit the shape of this class.

        :param x: x-coordinate
        :type x: float
        :param y: y-coordinate
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param shapes: list of shapes inheriting from Rect class
        :type shapes: list of _Rect
        :param max_length: maximum length of the row (maximum width or height depending on horizontal)
        :type max_length: float
        :param row_mode: alignment type along x- or y-axis of the rows within given rect
        :type row_mode: _LayoutDefault or int
        :param shapes_mode: alignment type along x- or y-axis of all the shapes within given row
        :type shapes_mode: _LayoutDefault or int
        :param horizontal: specifies if rows are horizontal or vertical
        :type horizontal: bool
        :param dist_x: horizontal distance between shapes
        :type dist_x: float
        :param dist_y: vertical distance between shapes
        :type dist_y: float
        """
        self.max_length = max_length
        self.row_mode = row_mode
        self.shapes_mode = shapes_mode
        self.horizontal = horizontal
        self.rows = list()

        self.dist_x = dist_x
        self.dist_y = dist_y

        StaticGroup.__init__(self, x, y, x_mode, y_mode, shapes, 0, 0)

    def _update_shapes_x(self, dx):
        """Move all x-coordinates of rows a given amount.

        Function should only be used internally.

        :param dx: change made to the x-coordinates
        :type dx: float
        """
        for row in self.rows:
            row.move_x(dx)

    def _update_shapes_y(self, dy):
        """Move all y-coordinates of rows a given amount.

        Function should only be used internally.

        :param dy: change made to the y-coordinates
        :type dy: float
        """
        for row in self.rows:
            row.move_y(dy)

    def _update_shape_alignment(self):
        """Update the dimensions of rows within RowsGroup using x_mode and y_mode to specify their alignment."""
        for row in self.rows:
            row.update_alignment_in_rect(self)

    def update_rows_alignment(self):
        """Sort all the shapes into rows based on their width or height. Update dimensions of RowsGroup accordingly.

        Algorithm works for both vertical and horizontal sorting."""
        self.rows.clear()
        max_length = max(self.max_length, self.width if self.horizontal else self.height)
        width = 0
        height = 0
        if self.horizontal:
            row = StaticGroup(self.x, self.y, self.row_mode, 0, [], 0, 0)
        else:
            row = StaticGroup(self.x, self.y, 0, self.row_mode, [], 0, 0)

        for shape in self.shapes:
            if self.horizontal:
                shape.set_y_mode(self.shapes_mode)
                if width + shape.width > max_length and len(row) > 0:
                    self.rows.append(row)
                    width = 0
                    height += row.height
                    row = StaticGroup(self.x, self.y + height, self.row_mode, 0, [], 0, 0)
                shape.set_pos(width, 0)
                width += shape.width + self.dist_x
            else:
                shape.set_x_mode(self.shapes_mode)
                if height + shape.height > max_length and len(row) > 0:
                    self.rows.append(row)
                    height = 0
                    width += row.width
                    row = StaticGroup(self.x + width, self.y, 0, self.row_mode, [], 0, 0)
                shape.set_pos(0, height)
                height += shape.height + self.dist_y
            row.append(shape)
        self.rows.append(row)
        if self.horizontal:
            self.set_size(max_length, height + row.height)
        else:
            self.set_size(width + row.width, max_length)

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        """Update the dimensions of the shapes within a given rect using x_mode and y_mode to specify their alignment.

        Update shapes accordingly.

        :param total_width: width of the square in which this shapes is updated
        :type total_width: float
        :param total_height: height of the square in which this shapes is updated
        :type total_height: float
        :param x_start: starting x-coordinate of the square in which this shapes is updated
        :type x_start: float
        :param y_start: starting y-coordinate of the square in which this shapes is updated
        :type y_start: float
        """
        _Rect.update_alignment(self, total_width, total_height, x_start, y_start)
        self.update_rows_alignment()


class StackGroup(StaticGroup):
    # TODO: not done yet, StackGroup.append() and other functions do not yet work
    def __init__(self, x, y, x_mode, y_mode, shapes, horizontal=True, dist=0):
        self.horizontal = horizontal
        self.dist = dist
        StaticGroup.__init__(self, x, y, x_mode, y_mode, shapes, 0, 0)

    # def _update_group_dimensions(self):
    #     pass

    def update_stack_alignment(self):
        if self.horizontal:
            x = self.x
            for shape in self.shapes:
                shape.set_pos(x, self.y)
                x += shape.width + self.dist
        else:
            y = self.y
            for shape in self.shapes:
                shape.set_pos(self.x, y)
                y += shape.height + self.dist
        self._update_pos()
        self._update_size()

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        _Rect.update_alignment(self, total_width, total_height, x_start, y_start)
        self.update_stack_alignment()
        self._update_shape_alignment()
