from copy import deepcopy as _deepcopy
from math import sqrt as _sqrt, atan2 as _atan2, cos as _cos, sin as _sin, pi as _pi
from fractions import Fraction
from pygame import draw as _draw, Color as _Color

from ..logic.layout import LayoutDefault as _LayoutDefault
from ..logic.common import represent


class Point:
    """A class to represent a point with no visual representation in two-dimensional space."""

    def __init__(self, x, y):
        """Initiate Point object.

        :type x: float
        :type y: float
        """
        self.x = x
        self.y = y

    def move_x(self, dx):
        """Move x-coordinate a given dx amount.

        :type dx: float
        """
        self.set_x(self.x + dx)

    def move_y(self, dy):
        """Move y-coordinate a given dy amount.

        :type dy: float
        """
        self.set_y(self.y + dy)

    def move(self, dx, dy):
        """Move x- and y-coordinate given dx and dy amounts.

        :type dx: float
        :type dy: float
        """
        self.set_pos(self.x + dx, self.y + dy)

    def set_x(self, x):
        """Set x-coordinate to a given value.

        :type x: float
        """
        self.x = x

    def set_y(self, y):
        """Set y-coordinate to a given value.

        :type y: float
        """
        self.y = y

    def set_pos(self, x, y):
        """Set x- and y-coordinate to given values.

        :type x: float
        :type y: float
        """
        self.set_x(x)
        self.set_y(y)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black ring as representation on a surface.

        :type surface: _Surface
        """
        _draw.circle(surface, _Color(0, 0, 0), (self.x, self.y), 5, 1)

    def loop_behavior(self):
        """Code behavior of the shapes during the loop of the application.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This function
        will be called once per application tick and will alter the behavior of a shapes during its presence in the
        application. This class should have no extra behavior during the application loop.
        """
        pass

    def distance_to(self, point):
        """Calculate distance between self and given point.

        :type point: Point
        :return: distance between self and given point
        :rtype: float
        """
        return Geometry.distance(self, point)

    def angle_to(self, point):
        """Calculate angle between self and given point.

        :type point: Point
        :return: angle in radians between self and given point
        :rtype: float
        """
        return Geometry.angle(self, point)

    def gradient(self, point):
        """Calculate gradient between self and given point.

        :type point: Point
        :return: gradient between self and given point
        :rtype: float
        """
        return Geometry.gradient(self, point)

    def rotate_along_origin(self, angle):
        """Rotate point relative to origin (0, 0) given an angle.

        :param angle: angle in radians to rotate point with
        :type angle: float
        """
        x2, y2 = Geometry.rotate_along_origin(self, angle)
        self.set_pos(x2, y2)

    # TODO: what are these methods?
    def add(self, p2):
        """Add x- and y-coordinate values of given point to x- and y-coordinate values of self.

        :type p2: Point
        """
        self.set_pos(self.x + p2.x, self.y + p2.y)

    def sub(self, p2):
        """Subtract x- and y-coordinate values of given point from x- and y-coordinate values of self.

        :type p2: Point
        """
        self.set_pos(self.x - p2.x, self.y - p2.y)

    def mul(self, n):
        """Multiply x- and y-coordinate values with a constant.

        :type n: float
        """
        self.set_pos(self.x * n, self.y * n)

    def truediv(self, n):
        """True divide x- and y-coordinate values with a constant.

        :type n: float
        """
        self.set_pos(self.x / n, self.y / n)

    def floordiv(self, n):
        """Floor divide x- and y-coordinate values with a constant.

        :type n: float
        """
        self.set_pos(self.x // n, self.y // n)

    def mod(self, n):
        """Modulo x- and y-coordinate values with a constant

        :type n: float
        """
        self.set_pos(self.x % n, self.y % n)

    def __add__(self, p2):
        """Return self + p2."""
        p1 = _deepcopy(self)
        p1.add(p2)
        return p1

    def __sub__(self, p2):
        """Return self - p2."""
        p1 = _deepcopy(self)
        p1.sub(p2)
        return p1

    def __mul__(self, n):
        """Return self * n."""
        p1 = _deepcopy(self)
        p1.mul(n)
        return p1

    def __truediv__(self, n):
        """Return self / n."""
        p1 = _deepcopy(self)
        self.truediv(n)
        return p1

    def __floordiv__(self, n):
        """Return self // n."""
        p1 = _deepcopy(self)
        p1.floordiv(n)
        return p1

    def __mod__(self, n):
        """return self % n."""
        p1 = _deepcopy(self)
        p1.mod(n)
        return p1

    def __getitem__(self, item):
        """Get x- or y-coordinate depending on the index.

        :type item: int
        :rtype: float
        """
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        raise IndexError

    def __iter__(self):
        """Initiate iteration sequence.

        :return: self
        :rtype: Point
        """
        self.__index = 0
        return self

    def __len__(self):
        """Return dimension of self. Is always 2 for two-dimensional Point.

        :return: dimension of self
        :rtype: int
        """
        return 2

    def __next__(self):
        """Progress iteration sequence.

        :rtype: float
        """
        if self.__index == 0:
            self.__index += 1
            return self.x
        if self.__index == 1:
            self.__index += 1
            return self.y
        raise StopIteration

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y", self.x, self.y)


class Box(Point):
    """A class to represent a rectangle with no visual representation in two-dimensional space."""

    def __init__(self, x, y, width, height):
        Point.__init__(self, x, y)
        self.width = width
        self.height = height
        self.x2 = self.x + self.width
        self.y2 = self.y + self.height

    def _update_x2(self):
        """Update right x-coordinate x2."""
        self.x2 = self.x + self.width

    def _update_y2(self):
        """Update bottom y-coordinate y2."""
        self.y2 = self.y + self.height

    def set_x(self, x):
        """Set x-coordinate to a given value.

        :type x: float
        """
        Point.set_x(self, x)
        self._update_x2()

    def set_y(self, y):
        """Set y-coordinate to a given value.

        :type y: float
        """
        Point.set_y(self, y)
        self._update_y2()

    def set_pos(self, x, y):
        """Set x- and y-coordinate to given values.

        :type x: float
        :type y: float
        """
        self.set_x(x)
        self.set_y(y)

    def move_width(self, d_width):
        """Move width a given amount d_width.

        :type d_width: float
        """
        self.set_width(self.width + d_width)

    def move_height(self, d_height):
        """Move height a given amount d_height.

        :type d_height: float
        """
        self.set_height(self.height + d_height)

    def move_size(self, d_width, d_height):
        """Move width and height given amounts d_width and d_height.

        :type d_width: float
        :type d_height: float
        """
        self.set_size(self.width + d_width, self.height + d_height)

    def set_width(self, width):
        """Set width to a given value.

        :type width: float
        """
        self.width = width
        self._update_x2()

    def set_height(self, height):
        """Set height to a given value.

        :type height: float
        """
        self.height = height
        self._update_y2()

    def set_size(self, width, height):
        """Set width and height to given values.

        :type width: float
        :type height: float
        """
        self.set_width(width)
        self.set_height(height)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black box as representation on a surface.

        :type surface: _Surface
        """
        _draw.rect(surface, _Color(0, 0, 0), ((self.x, self.y), (self.width, self.height)), 1)

    def collide_point(self, point):
        """Check if point is within the boundaries of the Rect

        :type point: Point
        :rtype: bool
        """
        return Collision.rect_point(self, point)

    def __getitem__(self, item):
        """Get x-, y-coordinate, width or height depending on the index.

        :type item: int
        :rtype: float
        """
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.width
        if item == 3:
            return self.height
        raise IndexError

    def __iter__(self):
        """Initiate iteration sequence.

        :return: self
        :rtype: Rect
        """
        self.__index = 0
        return self

    def __len__(self):
        """Return dimension of self. Is always 4 for two-dimensional Rect.

        :return: dimension of self
        :rtype: int
        """
        return 4

    def __next__(self):
        """Progress iteration sequence.

        :rtype: float
        """
        if self.__index == 0:
            self.__index += 1
            return self.x
        if self.__index == 1:
            self.__index += 1
            return self.y
        if self.__index == 2:
            self.__index += 1
            return self.width
        if self.__index == 3:
            self.__index += 1
            return self.height
        raise StopIteration

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height", self.x, self.y, self.width, self.height)


class Rect(Box):
    """A class to represent a rectangle with no visual representation in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode):
        """Initiate Rect object, inheriting from Point class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        """
        Box.__init__(self, x, y, width, height)
        self.x_mode = _LayoutDefault.from_variable(x_mode)
        self.y_mode = _LayoutDefault.from_variable(y_mode)

    def set_width(self, width):
        """Set width to a given value.

        :type width: float
        """
        dx = width - self.width
        self.width = width
        self.x_mode.update_alignment_x(self, dx)
        self._update_x2()

    def set_height(self, height):
        """Set height to a given value.

        :type height: float
        """
        dy = height - self.height
        self.height = height
        self.y_mode.update_alignment_y(self, dy)
        self._update_y2()

    def set_x_mode(self, x_mode):
        self.x_mode = _LayoutDefault.from_variable(x_mode)

    def set_y_mode(self, y_mode):
        self.y_mode = _LayoutDefault.from_variable(y_mode)

    def update_alignment(self, total_width, total_height, x_start=0, y_start=0):
        """Update the dimensions of the shapes within a given rect using x_mode and y_mode to specify their alignment.

        TODO: update this, it is outdated.

        Depending on the mode for the x- or y-axis, the shapes will be updated differently:
        -Layout.default: shapes will not be updated.
        -Layout.middle: shapes x or y value will be aligned in the middle of given rect and moved using x_ or y_offset.
        -Layout.fill: shapes width or height value will be filled in the given rect and changed using x_ or y_offset.

        -Layout.left: shapes x value will be aligned along the left-side of given rect and moved using x_offset.
        -Layout.right: shapes x value will be aligned along the right-side of given rect and moved using x_offset.

        -Layout.above: shapes y value will be aligned along the top-side of given rect and moved using y_offset.
        -Layout.below: shapes y value will be aligned along the bottom-side of given rect and moved using y_offset.


        :param total_width: width of the square in which this shapes is updated
        :type total_width: float
        :param total_height: height of the square in which this shapes is updated
        :type total_height: float
        :param x_start: starting x-coordinate of the square in which this shapes is updated
        :type x_start: float
        :param y_start: starting y-coordinate of the square in which this shapes is updated
        :type y_start: float
        """
        self.x_mode.align_x(self, total_width, total_height, x_start, y_start)
        self.y_mode.align_y(self, total_width, total_height, x_start, y_start)

    def update_alignment_in_rect(self, rect):
        """Update the dimensions of the shapes within a given rect using x_mode and y_mode to specify their alignment.

        :param rect: rect in which shapes will be updated
        :type rect: Rect
        """
        self.x_mode.align_from_rect_x(self, rect)
        self.y_mode.align_from_rect_y(self, rect)


class Line(Rect):
    """A class to represent a line with color and thickness in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode):
        """Initiate Line  object, inheriting from Rect class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        """
        Rect.__init__(self, x, y, width, height, x_mode, y_mode)

    def get_length(self):
        """Get length of the line.

        :rtype: float
        """
        return Geometry.distance(self, (self.x2, self.y2))

    def get_angle(self):
        """Get angle of the line in radians.

        :rtype: float
        """
        return Geometry.angle(self, (self.x2, self.y2))

    def set_angle(self, angle):
        """Update width and height using angle argument in radians.

        :type angle: float
        """
        width, height = Geometry.get_dimensions(angle, self.get_length())
        self.set_size(width, height)

    def set_length(self, length):
        """Update width and height using length argument.

        :type length: float
        """
        width, height = Geometry.get_dimensions2((self.x, self.y), (self.x2, self.y2), length)
        self.set_size(width, height)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black line as representation on a surface.

        :type surface: _Surface
        """
        _draw.line(surface, _Color(0, 0, 0), (self.x, self.y), (self.x2, self.y2), 1)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y x2 y2", self.x, self.y, self.x2, self.y2)

    @staticmethod
    def from_angle(x, y, length, angle, x_mode, y_mode):
        """Create Line from given length and angle.

        :type x: float
        :type y: float
        :type length: float
        :type angle: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :rtype: Line
        """
        width, height = Geometry.get_dimensions(angle, length)
        return Line(x, y, width, height, x_mode, y_mode)

    @staticmethod
    def from_points(x, y, x2, y2, x_mode, y_mode):
        """Create Line from given secondary point.

        :type x: float
        :type y: float
        :type x2: float
        :type y2: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :rtype: Line
        """
        return Line(x, y, x2 - x, y2 - y, x_mode, y_mode)


class Circle(Rect):
    """A class to represent a line with color in two-dimensional space."""

    def __init__(self, x, y, radius, x_mode, y_mode):
        """Initiate Circle object, inheriting from Rect class.

        :type x: float
        :type y: float
        :type radius: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode:i int
        """
        Rect.__init__(self, x, y, radius * 2, radius * 2, x_mode, y_mode)
        self.radius = radius
        self.xm = int(self.x + self.radius)
        self.ym = int(self.y + self.radius)

    def _update_xm(self):
        """Update middle x-coordinate."""
        self.xm = int(self.x + self.radius)

    def _update_ym(self):
        """Update middle y-coordinate."""
        self.ym = int(self.y + self.radius)

    def move_x(self, dx):
        """Move x-coordinate a given amount dx.

        :type dx: float
        """
        Rect.move_x(self, dx)
        self._update_xm()

    def move_y(self, dy):
        """Move y-coordinate a given amount dy.

        :type dy: float
        """
        Rect.move_y(self, dy)
        self._update_ym()

    def move(self, dx, dy):
        """Move x- and y-coordinate given amounts dx and dy.

        :type dx: float
        :type dy: float
        """
        self.move_x(dx)
        self.move_y(dy)

    def set_x(self, x):
        """Set x-coordinate to a given value.

        :type x: float
        """
        Rect.set_x(self, x)
        self._update_xm()

    def set_y(self, y):
        """Set y-coordinate to a given value.

        :type y: float
        """
        Rect.set_y(self, y)
        self._update_ym()

    def set_pos(self, x, y):
        """Set x- and y-coordinate to given values.

        :type x: float
        :type y: float
        """
        self.set_x(x)
        self.set_y(y)

    def set_middle_pos(self, x, y):
        """Set middle x- and y-coordinate to given values.

        :type x: float
        :type y: float
        """
        self.set_x(x - self.radius)
        self.set_y(y - self.radius)

    def move_width(self, d_width):
        """Move radius a given amount d_width.

        :type d_width: float
        """
        self.move_radius(d_width / 2)

    def move_height(self, d_height):
        """Move radius a given amount d_height.

        :type d_height: float
        """
        self.move_radius(d_height / 2)

    def move_size(self, d_width, d_height):
        """Move radius with smallest argument.

        :type d_width: float
        :type d_height: float
        """
        self.move_radius(min(d_width, d_height) / 2)

    def set_width(self, width):
        """Set radius to a given value.

        :type width: float
        """
        self.set_radius(width / 2)

    def set_height(self, height):
        """Set radius to a given value.

        :type height: float
        """
        self.set_radius(height / 2)

    def set_size(self, width, height):
        """Set radius to smallest argument.

        :type width: float
        :type height: float
        """
        self.set_radius(min(width, height) / 2)

    def move_radius(self, d_radius):
        """Move radius a given amount.

        :type d_radius: float
        """
        self.radius += d_radius
        Rect.move_width(self, d_radius * 2)
        Rect.move_height(self, d_radius * 2)

    def set_radius(self, radius):
        """Set radius to a given value.

        :type radius: float
        """
        self.radius = radius
        Rect.set_width(self, self.radius * 2)
        Rect.set_height(self, self.radius * 2)

    def get_middle_pos(self):
        """Get middle x- and y-coordinate.

        :rtype: Point
        """
        return Point(self.xm, self.ym)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black circle as representation on a surface.

        :type surface: _Surface
        """
        _draw.circle(surface, _Color(0, 0, 0), (self.xm, self.ym), int(self.radius), 1)

    def collide_point(self, point):
        """Check if point is within the boundaries of the Circle

        :type point: Point
        :rtype: bool
        """
        return Collision.circle_point(self, point)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y radius", self.x, self.y, self.radius)


class Ellipse(Rect):
    """A class to represent an ellipse with color in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode):
        """Initiate Ellipse object, inheriting from Rect class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        """
        Rect.__init__(self, x, y, width, height, x_mode, y_mode)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black ellipse as representation on a surface.

        :type surface: _Surface
        """
        _draw.ellipse(surface, _Color(0, 0, 0), ((self.x, self.y), (self.width, self.height)), 1)


class Polygon(Rect):
    """A class to represent a collection of points with no visual representation in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode, points):
        """Initiate Polygon object, inheriting from Rect class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type points: Polygon or list of Point or tuple of Point or list of (float, float) or tuple of (float, float)
        """
        Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        self.points = tuple(Point(p[0], p[1]) for p in points)
        self._update_pos()
        self._update_size()
        self.ratios = tuple((point.x / self.width, point.y / self.height) for point in self.points)

    def _update_size(self):
        """Find largest width- and height-difference between two points and set values as width and height."""
        for p1 in self.points:
            for p2 in self.points:
                if p1 != p2:
                    width = abs(p1.x - p2.x)
                    height = abs(p1.y - p2.y)
                    if width > self.width:
                        Rect.set_width(self, width)
                    if height > self.height:
                        Rect.set_height(self, height)

    def _update_pos(self):
        """Update points tuple to be compatible with x- and y-coordinate

        Calculate smallest distances dx and dy between x- and y-coordinates of self and of points from self.points.
        When smallest dx and dy are found, the positions of the points in self.points are updated accordingly.
        """

        dx = self.points[0].x - self.x
        dy = self.points[0].y - self.y
        for point in self.points[1:]:
            x_difference = point.x - self.x
            y_difference = point.y - self.y
            if x_difference < dx:
                dx = x_difference
            if y_difference < dy:
                dy = y_difference
        self._update_points_pos(-dx, -dy)

    def _update_points_width(self, new_width):
        """Set width to a given value and update the points to scale accordingly.

        :type new_width: float
        """
        for i in range(0, len(self.points)):
            ratio_width = self.ratios[i][0]
            self.points[i].set_x(self.x + ratio_width * new_width)

    def _update_points_height(self, new_height):
        """Set height to a given value and update the points to scale accordingly.

        :type new_height: float
        """
        for i in range(0, len(self.points)):
            ratio_height = self.ratios[i][1]
            self.points[i].set_y(self.y + ratio_height * new_height)

    def _update_points_x(self, dx):
        """Move all points a certain amount dx along the x-axis.

        :type dx: float
        """
        for point in self.points:
            point.move_x(dx)

    def _update_points_y(self, dy):
        """Move all points a certain amount dy along the y-axis.

        :type dy: float
        """
        for point in self.points:
            point.move_y(dy)

    def _update_points_pos(self, dx, dy):
        """Move all points certain amounts dx and dy.

        :type dx: float
        :type dy: float
        """
        for point in self.points:
            point.move(dx, dy)

    def set_x(self, x):
        """Set x-coordinate to a given value.

        :type x: float
        """
        self._update_points_x(x - self.x)
        Rect.set_x(self, x)

    def set_y(self, y):
        """Set y-coordinate to a given value.

        :type y: float
        """
        self._update_points_y(y - self.y)
        Rect.set_y(self, y)

    def set_width(self, width):
        """Set width to a given value.

        :type width: float
        """
        self._update_points_width(width)
        Rect.set_width(self, width)

    def set_height(self, height):
        """Set height to a given value.

        :type height: float
        """
        self._update_points_height(height)
        Rect.set_height(self, height)

    def set_points(self, points):
        """Set new points and update points tuple to be compatible with x- and y-coordinate.

        :type points: Polygon or list of Point or tuple of Point or list of (float, float) or tuple of (float, float)
        """
        self.points = tuple(Point(p[0], p[1]) for p in points)
        self._update_pos()
        self._update_size()
        self.ratios = tuple((point.x / self.width, point.y / self.height) for point in self.points)

    def draw(self, surface):
        """Draw shapes to a given surface.

        This function is meant as a template for all subclasses to inherit and fill in when necessary. This class will
        have a basic black polygon as representation on a surface.

        :type surface: _Surface
        """
        _draw.polygon(surface, _Color(0, 0, 0), self.points, 1)

    def get_points_avg(self):
        return Geometry.get_points_avg(self)

    def rotate(self, angle):
        """Rotate all points around centre point a given amount of radians

        :type angle: float
        """
        xm, ym = self.get_points_avg()

        for point in self.points:
            angle_2 = Geometry.angle((xm, ym), point) + angle
            length = Geometry.distance((xm, ym), point)
            width, height = Geometry.get_dimensions(angle_2, length)
            point.set_pos(xm + width, ym + height)
        self._update_size()

    def collide_point(self, point):
        """Check if point is within the boundaries of the Polygon

        :type point: Point
        :rtype: bool
        """
        return Collision.polygon_point(self, point)

    def __getitem__(self, item):
        """Get certain point depending on the index.

        :type item: int
        :rtype: Point
        """
        return self.points[item]

    def __iter__(self):
        """Initiate iteration sequence.

        :return: self
        :rtype: Polygon
        """
        self.__index = 0
        return self

    def __len__(self):
        """Return length of points tuple.

        :rtype: int
        """
        return len(self.points)

    def __next__(self):
        """Progress iteration sequence.

        :rtype: Point
        """
        if self.__index < len(self.points):
            point = self.points[self.__index]
            self.__index += 1
            return point
        self._update_pos()
        self._update_size()
        self.ratios = tuple((point.x / self.width, point.y / self.height) for point in self.points)
        raise StopIteration

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height points_amount", self.x, self.y, self.width, self.height, len(self))


class Geometry:
    """A class to contain static methods regarding vector calculations."""

    @staticmethod
    def get_point(point):
        """Extract point from Point object or iterable.

        :type point: Point or (float, float)
        :return: x, y
        :rtype: (float, float)
        """
        if hasattr(point, "x") and hasattr(point, "y"):
            return point.x, point.y
        return point[0], point[1]

    @staticmethod
    def get_rect(rect):
        """Extract rect from Rect object or iterable.

        :type rect: Rect or tuple of (float, float, float, float) or list of (float, float, float, float)
        :return: x, y, x2, y2
        :rtype: (float, float, float, float)
        """
        if hasattr(rect, "x") and hasattr(rect, "y") and hasattr(rect, "x2") and hasattr(rect, "y2"):
            return rect.x, rect.y, rect.x2, rect.y2
        return rect[0], rect[1], rect[2], rect[3]

    @staticmethod
    def get_points_avg(points):
        """Calculate average x- and y-coordinate based on point list.

        :type points: Polygon or list of Point or tuple of Point or list of (float, float) or tuple of (float, float)
        :rtype: Point
        """
        xm = sum(p[0] for p in points) / len(points)
        ym = sum(p[1] for p in points) / len(points)
        return Point(xm, ym)

    @staticmethod
    def distance(point_1, point_2):
        """Calculate distance between two points.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: float
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        return _sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def distance_squared(point_1, point_2):
        """Calculate squared distance between two points.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: float
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    @staticmethod
    def angle(point_1, point_2):
        """Calculate angle in radians between two points.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: float
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        return _atan2(-(y2 - y1), (x2 - x1))

    @staticmethod
    def rotate_along_origin(point, angle):
        """Calculate rotation of point around (0, 0) using angle in radians.

        :type point: Point or (float, float)
        :type angle: float
        :rtype: Point
        """
        x1, y1 = Geometry.get_point(point)
        x2 = x1 * _cos(angle) - y1 * _sin(angle)
        y2 = y1 * _cos(angle) + x1 * _sin(angle)
        return Point(x2, y2)

    @staticmethod
    def get_dimensions(angle, length):
        """Calculate width, height of line with angle in radians and length.

        :type angle: float
        :type length: float
        :return: width and height of line
        :rtype: (float, float)
        """
        if angle > 2 * _pi:
            angle = angle - 2 * _pi
        angle = -angle
        width = _cos(angle) * length
        height = _sin(angle) * length
        return width, height

    @staticmethod
    def get_dimensions2(point_1, point_2, length=1, dist=None):
        """Calculate width, height of line between two points with length multiplier.
        TODO: what is length?
        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :param length: length multiplier for new width, height
        :type length: float
        :param dist: distance between point_1 and point_2
        :type dist: float or None
        :return: width and height
        :rtype: (float, float)
        """
        if dist is None:
            dist = Geometry.distance(point_1, point_2)
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        width = length * (x2 - x1) / dist
        height = length * (y2 - y1) / dist
        return width, height

    @staticmethod
    def gradient(point_1, point_2):
        """Calculate gradient coefficient between two points.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: float
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        return (y2 - y1) / (x2 - x1)

    @staticmethod
    def rect_points(point_1, point_2):
        """Calculate all the points within a given rectangle.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :return: points of a given rectangle.
        :rtype: list of (float, float)
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)

        point_list = list()
        width = int(abs(x2 - x1))
        height = int(abs(y2 - y1))
        for x in range(width):
            for y in range(height):
                point_list.append((x + x1, y + y1))
        return point_list

    @staticmethod
    def line_points(point_1, point_2):
        """Calculate all the points of a given line.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: list of (float, float)
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)

        point_list = list()
        width = x2 - x1
        height = y2 - y1
        length = _sqrt(width ** 2 + height ** 2)
        dx = width / length
        dy = height / length

        x = x1
        y = y1

        for i in range(int(length)):
            point_list.append((int(x), int(y)))
            x += dx
            y += dy
        return point_list

    @staticmethod
    def dot_product(vector_1, vector_2):
        """Calculate dot product of two vectors.

        :type vector_1: Point or (float, float)
        :type vector_2: Point or (float, float)
        :rtype: float
        """
        x1, y1 = Geometry.get_point(vector_1)
        x2, y2 = Geometry.get_point(vector_2)
        return x1 * x2 + y1 * y2

    @staticmethod
    def ellipse_eccentricity(ellipse):
        """Calculate eccentricity of an ellipse.

        :type ellipse: Ellipse
        :rtype: float
        """
        a = ellipse.width / 2
        b = ellipse.height / 2
        return _sqrt(1 - min(a, b)**2 / max(a, b)**2)


class Collision:
    """A class to contain static methods regarding collision detections."""

    """Point based collisions"""
    @staticmethod
    def point_point(point_1, point_2):
        """Calculate if two points are the same.

        :type point_1: Point or (float, float)
        :type point_2: Point or (float, float)
        :rtype: bool
        """
        x1, y1 = Geometry.get_point(point_1)
        x2, y2 = Geometry.get_point(point_2)
        return x1 == x2 and y1 == y2

    @staticmethod
    def rect_point(rect, point):
        """Calculate if point is in rect.

        :type rect: Box or tuple of (float, float, float, float) or list of (float, float, float, float)
        :type point: Point or (float, float)
        :rtype: bool
        """
        x, y = Geometry.get_point(point)
        rx, ry, rx2, ry2 = Geometry.get_rect(rect)
        return rx < x < rx2 and ry < y < ry2

    @staticmethod
    def circle_point(circle, point):
        """Calculate if point is in circle.

        :type circle: Circle
        :type point: Point or (float, float)
        :rtype: bool
        """
        if not Collision.rect_point(circle, point):
            return False
        return Geometry.distance_squared(point, (circle.xm, circle.ym)) < circle.radius ** 2

    @staticmethod
    def polygon_point(polygon, point):
        """Calculate if point is in polygon.

        :type polygon: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :type point: Point or (float, float)
        :rtype: bool
        """
        if not Collision.rect_point(polygon, point):
            return False

        point_x, point_y = Geometry.get_point(point)
        x_right = 0
        p1 = polygon[-1]
        for i in range(len(polygon)):
            p2 = polygon[i]

            min_y = min(p1.y, p2.y)
            max_y = max(p1.y, p2.y)

            if min_y <= point_y < max_y:
                if p1.x != p2.x:
                    gradient = Geometry.gradient(p1, p2)
                    x = (point_y - p1.y) / gradient + p1.x
                else:
                    x = p1.x
                if x > point_x:
                    x_right += 1
            p1 = p2

        return x_right % 2 == 1

    @staticmethod
    def surface_point(surface_rect, point):
        """Calculate if point is in surface. This method is pixel perfect.

        :param surface_rect: object inheriting from Rect and Surface class
        :type point: Point or (float, float)
        :rtype: bool
        """
        if not Collision.rect_point(surface_rect, point):
            return False

        x = int(point.x - surface_rect.x)
        y = int(point.y - surface_rect.y)
        color = surface_rect.get_at((x, y))

        return color.a != 0

    """Rect based collisions"""
    @staticmethod
    def rect_rect(rect_1, rect_2):
        """Calculate if rect_1 is in rect_2

        :type rect_1: Rect or tuple of (float, float, float, float) or list of (float, float, float, float)
        :type rect_2: Rect or tuple of (float, float, float, float) or list of (float, float, float, float)
        :rtype: bool
        """
        return rect_1.x < rect_2.x2 and rect_1.x2 > rect_2.x and rect_1.y < rect_2.y2 and rect_1.y2 > rect_2.y

    @staticmethod
    def rect_circle(rect, circle):
        pass

    @staticmethod
    def rect_polygon(rect, polygon):
        pass

    @staticmethod
    def rect_surface(rect, surface):
        pass

    """Circle based collisions"""
    @staticmethod
    def circle_circle(circle_1, circle_2):
        """Calculate if circle_1 in circle_2

        :type circle_1: Circle
        :type circle_2: Circle
        :rtype: bool
        """
        distance_squared = Geometry.distance_squared(circle_1.get_middle_pos(), circle_2.get_middle_pos())
        return distance_squared < (circle_1.radius + circle_2.radius)**2

    @staticmethod
    def circle_polygon(circle, polygon):
        pass

    @staticmethod
    def circle_surface(circle, surface):
        pass

    """Polygon based collisions"""
    @staticmethod
    def polygon_polygon(pol_1, pol_2):
        """Calculate if pol_1 is in pol_2.

        :type pol_1: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :type pol_2: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :rtype: bool
        """
        if not Collision.rect_rect(pol_1, pol_2):
            return False

        if Intersect.polygon_polygon(pol_1, pol_2):
            return True

        for p1 in pol_1:
            if Collision.polygon_point(pol_2, p1):
                return True
        for p2 in pol_2:
            if Collision.polygon_point(pol_1, p2):
                return True

        return False

    @staticmethod
    def polygon_surface(polygon, surface):
        pass

    """Surface based collisions"""
    @staticmethod
    def surface_surface(surface_1, surface_2):
        pass

    @staticmethod
    def between_angles(side_1, side_2, angle):
        """Calculate if angle is between two side angles.

        :param side_1: angle 1 in radians
        :type side_1: float
        :param side_2: angle 2 in radians
        :type side_2: float
        :param angle: angle in radians
        :type angle: float
        :rtype: bool
        """
        angle_a = max(side_1, side_2)
        angle_b = min(side_1, side_2)

        if (side_1 >= 0 and side_2 >= 0) or (side_1 <= 0 and side_2 <= 0) or angle_a - angle_b < _pi:
            return angle_b < angle < angle_a
        return angle_b > angle or angle_a < angle

    @staticmethod
    def between_width(shape, width_1, width_2):
        """Calculate if shape is between widths.

        :type shape: Rect
        :param width_1: left width
        :type width_1: float
        :param width_2: right width
        :type width_2: float
        :rtype: bool
        """
        return width_1 < shape.x < width_2 - shape.width

    @staticmethod
    def between_height(shape, height_1, height_2):
        """Calculate if shape is between heights.

        :type shape: Rect
        :param height_1: top height
        :type height_1: float
        :param height_2: bottom height
        :type height_2: float
        :rtype: bool
        """
        return height_1 < shape.y < height_2 - shape.height


class Intersect:
    @staticmethod
    def line_line(line_1, line_2):
        """Calculate if line_1 is intersecting line_2

        :type line_1: Line or Rect
        :type line_2: Line or Rect
        :rtype: bool
        """
        def calc_b(line, r):
            return line.y - r * line.x

        def horizontal(line, x1, dx):
            dy = line.y2 - line.y
            r = dy / dx
            b = calc_b(line, r)
            y = r * x1 + b
            return y_top < y < y_bottom

        dx_1 = line_1.x2 - line_1.x
        dx_2 = line_2.x2 - line_2.x

        if dx_1 == 0 and dx_2 == 0:
            return False

        if dx_1 == 0 or dx_2 == 0:
            y_top = max(min(line_1.y, line_1.y2), min(line_2.y, line_2.y2))
            y_bottom = min(max(line_1.y, line_1.y2), max(line_2.y, line_2.y2))
            if dx_1 == 0:
                return horizontal(line_2, line_1.x, dx_2)
            if dx_2 == 0:
                return horizontal(line_1, line_2.x, dx_1)

        dy_1 = line_1.y2 - line_1.y
        dy_2 = line_2.y2 - line_2.y
        r1 = dy_1 / dx_1
        r2 = dy_2 / dx_2
        dr = r1 - r2

        if dr == 0:
            return False

        b1 = calc_b(line_1, r1)
        b2 = calc_b(line_2, r2)
        x = round((b2 - b1) / dr)
        # y = r1 * x + b1
        x_left = max(min(line_1.x, line_1.x2), min(line_2.x, line_2.x2))
        x_right = min(max(line_1.x, line_1.x2), max(line_2.x, line_2.x2))

        return x_left < x < x_right

    @staticmethod
    def line_line2(line_1, line_2):
        """Calculate if line_1 is intersecting line_2

        :type line_1: (Point, Point) or ((float, float), (float, float)) or [(float, float), (float, float)]
        :type line_2: (Point, Point) or ((float, float), (float, float)) or [(float, float), (float, float)]
        :rtype: bool
        """
        line_1 = Line.from_points(line_1[0][0], line_1[0][1], line_1[1][0], line_1[1][1], 0, 0)
        line_2 = Line.from_points(line_2[0][0], line_2[0][1], line_2[1][0], line_2[1][1], 0, 0)
        return Intersect.line_line(line_1, line_2)

    @staticmethod
    def polygon_polygon(pol_1, pol_2):
        """Calculate if perimeter of pol_1 is intersecting perimeter of pol_2.

        :type pol_1: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :type pol_2: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :rtype: bool
        """
        pol1_p1 = pol_1[-1]
        for pol1_p2 in pol_1:
            pol2_p1 = pol_2[-1]
            for pol2_p2 in pol_2:
                if Intersect.line_line2((pol1_p1, pol1_p2), (pol2_p1, pol2_p2)):
                    return True
                pol2_p1 = pol2_p2
            pol1_p1 = pol1_p2

        return False


class Perimeter:
    """A class to contain static methods regarding perimeter calculations."""

    @staticmethod
    def rect(rect):
        """Calculate perimeter of rect.

        :type rect: Rect
        :rtype: float
        """
        return 2 * rect.width + 2 * rect.height

    @staticmethod
    def circle(circle):
        """Calculate perimeter of circle.

        :type circle: Circle
        :rtype: float
        """
        return circle.radius * 2 * _pi

    @staticmethod
    def ellipse(ellipse):
        pass

    @staticmethod
    def polygon(polygon):
        """Calculate perimeter of polygon.

        :type polygon: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :rtype: float
        """
        length = 0
        p1 = polygon[-1]
        for i in range(len(polygon)):
            p2 = polygon[i]
            length += Geometry.distance(p1, p2)
            p1 = p2
        return length


class Area:
    """A class to contain static methods regarding area calculations."""

    @staticmethod
    def rect(rect):
        """Calculate area of rect.

        :type rect: Rect
        :rtype: float
        """
        return rect.width * rect.height

    @staticmethod
    def circle(circle):
        """Calculate area of circle.

        :type circle: Circle
        :rtype: float
        """
        return circle.radius**2 * _pi

    @staticmethod
    def ellipse(ellipse):
        """Calculate area of ellipse.

        :type ellipse: Ellipse or Rect
        :rtype: float
        """
        return ellipse.width * ellipse.height * _pi

    @staticmethod
    def triangle(polygon):
        """Calculate area of any triangle.

        :param polygon: any object with 3 points
        :type polygon: Polygon or tuple of Point or list of Point or tuple of (float, float) or list of (float, float)
        :rtype: float
        """
        x1, y1 = polygon[0]
        x2, y2 = polygon[1]
        x3, y3 = polygon[2]
        return abs(x1 * (y2 - y3) - x2 * (y1 - y3) + x3 * (y1 - y2)) / 2

    @staticmethod
    def polygon(polygon):
        """Calculate area of any polygon.

        If the polygon self-intersects, an alternative algorithm is used. However this is very slow and should be
        updated soon.

        :type polygon: Polygon
        :rtype: float
        """
        if Intersect.polygon_polygon(polygon, polygon):
            # TODO: this function is slow. Is this fixable?
            print("Warning: current algorithm doesn't work for self-intersecting polygons")
            area = 0
            for x in range(int(polygon.x), int(polygon.x2 + 1)):
                for y in range(int(polygon.y), int(polygon.y2 + 1)):
                    if Collision.polygon_point(polygon, (x, y)):
                        area += 1
            return area

        area = 0
        p1 = polygon[-1]
        for i in range(len(polygon)):
            p2 = polygon[i]
            area += p1.x * p2.y - p1.y * p2.x
            p1 = p2

        return abs(area) / 2


class Volume:
    """A class to contain static methods regarding volume calculations."""

    @staticmethod
    def cuboid(width, height, length):
        """Calculate volume of cuboid.

        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        :param length: length along z-axis
        :type length: float
        :return: volume
        :rtype: float
        """
        return width * height * length

    @staticmethod
    def pyramid(width, height, length):
        """Calculate volume of cuboid.

        :param width: length along x-axis
        :type width: float
        :param height: length along y-axis
        :type height: float
        :param length: length along z-axis
        :type length: float
        :return: volume
        :rtype: float
        """
        return width * height * length / 3

    @staticmethod
    def sphere(circle):
        """Calculate volume of sphere.

        :param circle: object with "radius" attribute
        :type circle:
        :return: volume
        :rtype: float
        """
        return circle.radius**3 * _pi * 4 / 3

    @staticmethod
    def cylinder(radius, height):
        """Calculate volume of cylinder.

        :param radius: radius of base circle
        :type radius: float
        :param height: height of cylinder
        :type height: float
        :return: volume
        :rtype: float
        """
        return radius**2 * height * _pi

    @staticmethod
    def cone(radius, height):
        """Calculate volume of cone.

        :param radius: radius of base circle
        :type radius: float
        :param height: height of cone
        :type height: float
        :return: volume
        :rtype: float
        """
        return radius**2 * height * _pi / 3


class Points:
    """A class to contain static methods regarding generating point tuples."""

    @staticmethod
    def rhombus(width, height):
        """Create rhombus shaped point tuple.

        :type width: float
        :type height: float
        :rtype: tuple of (float, float)
        """
        return (width / 2, 0), (width, height / 2), (width / 2, height), (0, height / 2)

    @staticmethod
    def plus(width, height, x_thickness, y_thickness):
        """Create plus shaped point tuple.

        :type width: float
        :type height: float
        :type x_thickness: float
        :type y_thickness: float
        :rtype: tuple of (float, float)
        """
        x1 = (width - x_thickness) / 2
        x2 = (width + x_thickness) / 2

        y1 = (height - y_thickness) / 2
        y2 = (height + y_thickness) / 2

        return (x1, 0), (x2, 0), (x2, y1), (width, y1), (width, y2), (x2, y2), (x2, height), (x1, height), (x1, y2),\
               (0, y2), (0, y1), (x1, y1)

    @staticmethod
    def regular_polygon(radius, vertices):
        """Create regular polygon shaped point tuple with same length sides and same angle vertices.

        :param radius: length between centre and vertices
        :type radius: float
        :param vertices: number of vertices of regular polygon, minimal amount of 3
        :type vertices: int
        :rtype: tuple of (float, float)
        """
        d_angle = 2 * _pi / vertices
        return tuple(Geometry.get_dimensions(i * d_angle, radius) for i in range(vertices))

    @staticmethod
    def triangle(width, height, rotation=0):
        """Create isosceles triangle shaped point tuple.

        :type width: float
        :type height: float
        :param rotation: specifies which way the top vertex is oriented
        :type rotation: int
        :rtype: tuple of (float, float)
        """
        if rotation == 0:
            return (width / 2, 0), (width, height), (0, height)
        if rotation == 1:
            return (0, 0), (width, height / 2), (0, height)
        if rotation == 2:
            return (0, 0), (width, 0), (width / 2, height)
        if rotation == 3:
            return (width, 0), (width, height), (0, height / 2)

    @staticmethod
    def rectangle(width, height):
        """Create rectangle shaped point tuple.

        :type width: float
        :type height: float
        :rtype: tuple of (float, float)
        """
        return (0, 0), (width, 0), (width, height), (0, height)

    @staticmethod
    def star(outer_radius, inner_radius, outer_points):
        """Create star shaped point tuple.

        :type outer_radius: float
        :type inner_radius: float
        :param outer_points: number of outside vertices (equal to number of inside vertices), minimal amount of 2
        :type outer_points: int
        :rtype: tuple of (float, float)
        """
        vertices = 2 * outer_points
        d_angle = 2 * _pi / vertices
        points = list()
        for i in range(vertices):
            if i % 2 == 0:
                points.append(Geometry.get_dimensions((i - 0.5) * d_angle, inner_radius))
            else:
                points.append(Geometry.get_dimensions((i - 0.5) * d_angle, outer_radius))
        return tuple(points)


def get_aspect_ratio(width, height):
    """Calculate aspect ratio from width and height.

    :type width: int
    :type height: int
    :rtype: (int, int)
    """
    f = Fraction(width, height)
    return f.numerator, f.denominator
