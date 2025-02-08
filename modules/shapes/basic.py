from pygame import transform as _transform, Surface as _Surface, Color as _Color, SRCALPHA as _SRCALPHA, \
     draw as _draw, image as _image

from ..logic.constants import Format as _Format, Default as _Default
from ..logic.layout import LayoutDefault as _LayoutDefault
from ..logic.common import represent, load_font
from ..math.geometry import Geometry as _Geometry, Collision as _Collision, Rect as _Rect, Line as _Line,\
     Circle as _Circle, Ellipse as _Ellipse, Polygon as _Polygon


class SurfaceRect(_Surface, _Rect):
    """A class to represent a rectangle with a two-dimensional color-array in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, width, height):
        """Initiate SurfaceRect object, inheriting from Surface and Rect class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        """
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        _Surface.__init__(self, (self.width, self.height), _SRCALPHA)

    def _update_surface_type(self):
        """Re-initiate Surface to update width and height"""
        _Surface.__init__(self, (self.width, self.height), _SRCALPHA)

    def _update_surface(self):
        """Copy self, re-initiate Surface to update width and height, then blit copied self on new self"""
        surface = self.copy()
        self._update_surface_type()
        self.blit(surface, (0, 0))

    def set_surface(self, surface):
        """Set own surface to a given surface object and resize accordingly.

        :param surface: given surface object that gets drawn on self
        :type surface: _Surface
        """
        self.set_size(surface.get_width(), surface.get_height())
        self.fill(_Color(0, 0, 0, 0))
        self.blit(surface, (0, 0))

    def move_width(self, d_width):
        """Move width a given amount d_width.

        :type d_width: float
        """
        _Rect.move_width(self, d_width)
        self._update_surface()

    def move_height(self, d_height):
        """Move height a given amount d_height.

        :type d_height: float
        """
        _Rect.move_height(self, d_height)
        self._update_surface()

    def move_size(self, d_width, d_height):
        """Move width and height given amounts d_width and d_height.

        :type d_width: float
        :type d_height: float
        """
        _Rect.move_size(self, d_width, d_height)
        self._update_surface()

    def set_width(self, width):
        """Set width to a given value.

        :type width: float
        """
        _Rect.set_width(self, width)
        self._update_surface()

    def set_height(self, height):
        """Set height to a given value.

        :type height: float
        """
        _Rect.set_height(self, height)
        self._update_surface()

    def set_size(self, width, height):
        """Set width and height to given values.

        :type width: float
        :type height: float
        """
        _Rect.set_width(self, width)
        _Rect.set_height(self, height)
        self._update_surface()

    def chop(self, x, y, width, height):
        """Reset self to part of its own surface"""
        pass

    def flip(self, x_bool, y_bool):
        """Reset self to flipped version of surface, horizontally and/or vertically.

        :param x_bool: flip horizontal
        :type x_bool: bool
        :param y_bool: flip vertical
        :type y_bool: bool
        """
        self.set_surface(_transform.flip(self, x_bool, y_bool))

    def rotate(self):
        """Reset self to rotation of its own surface."""
        pass

    def rotozoom(self):
        """Reset self to rotation and zoom of its own surface."""
        pass

    def scale(self, width, height):
        """Reset self to a scaled version of its own surface.

        :type width: float
        :type height: float
        """
        self.set_surface(_transform.scale(self, (int(width), int(height))))

    def scale2x(self):
        """Reset self to a scaled version (2x) of its own surface."""
        pass

    def smoothscale(self):
        """Reset self to a smooth scaled version of its own surface."""
        pass

    def save(self, filename):
        """Save own surface to file.

        :type filename: str
        """
        _image.save(self, filename)

    def tostring(self, str_format, flipped=False):
        """Get string version of own surface.

        :param str_format: P, RGB, RGBX, RGBA, ARGB, RGBA_PREMULT, ARGB_PREMULT
        :type str_format: Literal
        :type flipped: bool
        :return: string of surface
        :rtype: bytes
        """
        return _image.tostring(self, str_format, flipped)

    def draw(self, surface):
        """Draw SurfaceRect to a given surface.

        :type surface: _Surface
        """
        surface.blit(self, (self.x, self.y))

    def collide_point(self, point):
        """Check if point is within the boundaries of the Rect.

        :type point: Point
        :rtype: bool
        """
        return _Collision.surface_point(self, point)

    @staticmethod
    def from_surface(x, y, x_mode, y_mode, surface):
        """Create SurfaceRect from existing surface.

        :type x: float
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param surface: existing surface to load from
        :type surface: _Surface
        :rtype: SurfaceRect
        """
        new_surface = SurfaceRect(x, y, x_mode, y_mode, surface.get_width(), surface.get_height())
        new_surface.blit(surface, (0, 0))
        return new_surface

    @staticmethod
    def from_image(x, y, x_mode, y_mode, image_path):
        """Create SurfaceRect from existing image.

        :type x: float
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param image_path: path on OS to image
        :type image_path: str
        :rtype: SurfaceRect
        """
        return SurfaceRect.from_surface(x, y, x_mode, y_mode, _image.load(image_path))


class FilledRect(_Rect):
    """A class to represent a rectangle with color in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode, color):
        """Initiate Rect object, inheriting from Rect class.

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
        """
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        self.color = color

    def draw(self, surface):
        """Draw Rectangle to a given surface

        :type surface: _Surface
        """
        _draw.rect(surface, self.color, ((self.x, self.y), (self.width, self.height)))


class FilledLine(_Line):
    def __init__(self, x, y, width, height, x_mode, y_mode, thickness, color):
        """Initiate Line  object, inheriting from Rect class.

        :type x: float
        :type y: float
        :type width: float
        :type height: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type thickness: int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        """
        _Line.__init__(self, x, y, width, height, x_mode, y_mode)
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        """Draw Line to a given surface

        :type surface: _Surface
        """
        _draw.line(surface, self.color, (self.x, self.y), (self.x2, self.y2), self.thickness)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y x2 y2 thickness", self.x, self.y, self.x2, self.y2, self.thickness)

    @staticmethod
    def from_angle(x, y, length, angle, x_mode, y_mode, thickness, color):
        """Create Line from given length and angle.

        :type x: float
        :type y: float
        :type length: float
        :type angle: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type thickness: int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :rtype: Line
        """
        width, height = _Geometry.get_dimensions(angle, length)
        return FilledLine(x, y, width, height, x_mode, y_mode, thickness, color)

    @staticmethod
    def from_points(x, y, x2, y2, x_mode, y_mode, thickness, color):
        """Create Line from given secondary point.

        :type x: float
        :type y: float
        :type x2: float
        :type y2: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type thickness: int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :rtype: Line
        """
        return FilledLine(x, y, x2 - x, y2 - y, x_mode, y_mode, thickness, color)


class FilledCircle(_Circle):
    def __init__(self, x, y, radius, x_mode, y_mode, color):
        _Circle.__init__(self, x, y, radius, x_mode, y_mode)
        self.color = color

    def draw(self, surface):
        """Draw Circle to a given surface

        :type surface: _Surface
        """
        _draw.circle(surface, self.color, self.get_middle_pos(), int(self.radius))


class FilledEllipse(_Ellipse):
    def __init__(self, x, y, width, height, x_mode, y_mode, color):
        _Ellipse.__init__(self, x, y, width, height, x_mode, y_mode)
        self.color = color

    def draw(self, surface):
        """Draw Ellipse to a given surface

        :type surface: _Surface
        """
        _draw.ellipse(surface, self.color, ((self.x, self.y), (self.width, self.height)))


class FilledPolygon(_Polygon):
    """A class to represent a polygon with color in two-dimensional space."""

    def __init__(self, x, y, points, x_mode, y_mode, color):
        """Initiate Polygon object, inheriting from PointsRect class.

        :type x: float
        :type y: float
        :type points: list of Point or tuple of Point or list of (float, float) or tuple of (float, float)
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        """
        _Polygon.__init__(self, x, y, 0, 0, x_mode, y_mode, points)
        self.color = color

    def draw(self, surface):
        """Draw Polygon to a given surface.

        :type surface: _Surface
        """
        if len(self.points) > 0:
            _draw.polygon(surface, self.color, self.points)


class LineRect(FilledRect):
    """A class to represent a lined rectangle with color and thickness in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode, color, thickness):
        """Initiate LineRect object, inheriting from Rectangle class.

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
        :type thickness: int
        """
        FilledRect.__init__(self, x, y, width, height, x_mode, y_mode, color)
        self.thickness = thickness

    def draw(self, surface):
        """Draw LineRect to a given surface.

        :type surface: _Surface
        """
        _draw.rect(surface, self.color, ((self.x, self.y), (self.width, self.thickness)))
        _draw.rect(surface, self.color, ((self.x, self.y2 - self.thickness), (self.width, self.thickness)))
        _draw.rect(surface, self.color, ((self.x, self.y), (self.thickness, self.height)))
        _draw.rect(surface, self.color, ((self.x2 - self.thickness, self.y), (self.thickness, self.height)))

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height thickness", self.x, self.y, self.width, self.height, self.thickness)


class LineCircle(FilledCircle):
    """A class to represent a lined circle with color and thickness in two-dimensional space."""

    def __init__(self, x, y, radius, x_mode, y_mode, color, thickness):
        """Initiate LineCircle object, inheriting from Circle class.

        :type x: float
        :type y: float
        :type radius: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode:i int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :type thickness: int
        """
        FilledCircle.__init__(self, x, y, radius, x_mode, y_mode, color)
        self.thickness = thickness

    def draw(self, surface):
        """Draw LineCircle to a given surface.

        :type surface: _Surface
        """
        _draw.circle(surface, self.color, (self.xm, self.ym), self.radius, self.thickness)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y radius thickness", self.x, self.y, self.radius, self.thickness)


class LineEllipse(FilledEllipse):
    """A class to represent a lined ellipse with color and thickness in two-dimensional space."""

    def __init__(self, x, y, width, height, x_mode, y_mode, color, thickness):
        """Initiate LineEllipse object, inheriting from Ellipse class.

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
        :type thickness: int
        """
        FilledEllipse.__init__(self, x, y, width, height, x_mode, y_mode, color)
        self.thickness = thickness

    def draw(self, surface):
        """Draw LineEllipse to a given surface.

        :type surface: _Surface
        """
        _draw.ellipse(surface, self.color, ((self.x, self.y), (self.width, self.height)), self.thickness)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height thickness", self.x, self.y, self.width, self.height, self.thickness)


class LinePolygon(FilledPolygon):
    """A class to represent a lined polygon with color and thickness in two-dimensional space."""

    def __init__(self, x, y, points, x_mode, y_mode, color, thickness):
        """Initiate LinePolygon object, inheriting from FilledPolygon class.

        :type x: float
        :type y: float
        :type points: list of Point or tuple of Point or list of (float, float) or tuple of (float, float)
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :param color: RGB color
        :type color: _Color or (int, int, int)
        :type thickness: int
        """
        FilledPolygon.__init__(self, x, y, points, x_mode, y_mode, color)
        self.thickness = thickness

    def draw(self, surface):
        """Draw LinePolygon to a given surface.

        :type surface: _Surface
        """
        _draw.polygon(surface, self.color, self.points, self.thickness)

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height thickness points_amount", self.x, self.y, self.width, self.height,
                         self.thickness, len(self))


class _TextObject(_Surface):
    """A class to represent a text displaying surface with no coordinates."""

    def __init__(self, content, color, font_name, pt, bold=False, italic=False, underline=False):
        """Initiate TextObject object, inheriting from Surface class.

        :param content: text to display
        :type content: str
        :param color: RGB text color
        :type color: _Color or (int, int, int)
        :type font_name: str
        :type pt: int
        :type bold: bool
        :type italic: bool
        :type underline: bool
        """
        self.content = content
        self.color = color
        self.pt = pt
        self.font_name = font_name
        self.font = load_font(self.font_name, self.pt, bold, italic, underline)

        surface = self.font.render(self.content, True, self.color)
        _Surface.__init__(self, (surface.get_width(), surface.get_height()), _SRCALPHA)
        _Surface.blit(self, surface, (0, 0))

    def _update_font(self, bold, italic, underline):
        """Reload font object when any of its properties are changed.

        :type bold: bool
        :type italic: bool
        :type underline: bool
        """
        self.font = load_font(self.font_name, self.pt, bold, italic, underline)

    def _update_content(self):
        """Reload own surface to process any updates in content, color, font or pt."""
        surface = self.font.render(self.content, True, self.color)
        _Surface.__init__(self, (surface.get_width(), surface.get_height()), _SRCALPHA)
        self.blit(surface, (0, 0))

    def set_color(self, color):
        """Set color to a given value.

        :param color: RGB color
        :type color: _Color or (int, int, int)
        """
        self.color = color
        self._update_content()

    def set_content(self, content):
        """Set content to a given value.

        :param content: text to display
        :type content: str
        """
        self.content = content
        self._update_content()

    def set_pt(self, pt):
        """Set font size to a given value.

        :type pt: int
        """
        self.pt = pt
        self._update_font(self.font.get_bold(), self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_font(self, font_name):
        """Set font to a given value.

        :type font_name: str
        """
        self.font_name = font_name
        self._update_font(self.font.get_bold(), self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_bold(self, bold):
        """Set bold True or False.

        :type bold: bool
        """
        self._update_font(bold, self.font.get_italic(), self.font.get_underline())
        self._update_content()

    def set_italic(self, italic):
        """Set italic True or False.

        :type italic: bool
        """
        self._update_font(self.font.get_bold(), italic, self.font.get_underline())
        self._update_content()

    def set_underline(self, underline):
        """Set underline True or False.

        :type underline: bool
        """
        self._update_font(self.font.get_bold(), self.font.get_italic(), underline)
        self._update_content()

    def __repr__(self):
        """Return repr(self)."""
        return represent("content color pt font_name bold italic underline", self.content, self.color, self.pt,
                         self.font_name, self.font.get_bold(), self.font.get_italic(), self.font.get_underline())

    @staticmethod
    def from_tuple(font_name, pt, attributes):
        """Create TextObject object from tuple of attributes or default values.

        Assume certain values as default, then check if attributes contains any values that deviate from this. These
        are content (""), color (Color(0, 0, 0)), bold (False), italic (False), underline (False). If so desired,
        the default values stored in the Default class can be changed beforehand to avoid adding those as attributes.

        :type font_name: str
        :type pt: int
        :param attributes: list of attributes containing values that deviate from default values
        :type attributes: list or set or tuple
        :rtype: _TextObject
        """
        content = ""
        color = _Default.text_color
        bold = _Default.bold
        italic = _Default.italic
        underline = _Default.underline

        for attribute in attributes:
            if type(attribute) is str:
                content = attribute
            elif type(attribute) is _Color:
                color = attribute
            elif attribute == _Format.bold:
                bold = True
            elif attribute == _Format.italic:
                italic = True
            elif attribute == _Format.underline:
                underline = True

        return _TextObject(content, color, font_name, pt, bold, italic, underline)


class Text(SurfaceRect):
    """A class to represent a text object displaying surface in two-dimensional space."""

    def __init__(self, x, y, x_mode, y_mode, pt, font_name, text_list):
        """Initiate Text object, inheriting from SurfaceRect class.

        :type x: float
        :type y: float
        :param x_mode: alignment type along x-axis within given rect
        :type x_mode: _LayoutDefault or int
        :param y_mode: alignment type along y-axis within given rect
        :type y_mode: _LayoutDefault or int
        :type font_name: str
        :type pt: int
        :param text_list: list of lists attributes containing content and any properties deviating from default values
        :type text_list: list or set or tuple
        """
        SurfaceRect.__init__(self, x, y, x_mode, y_mode, 0, 0)
        self.text_objects = list()
        self.pt = pt
        self.font_name = font_name
        self.font = load_font(self.font_name, self.pt)

        for text in text_list:
            self.text_objects.append(_TextObject.from_tuple(self.font_name, self.pt, text))
        self._update_surface()

    def _update_surface(self):
        """Reset the width and the height, clear the surface and redraw all text objects on self."""
        width = sum(text.get_width() for text in self.text_objects)
        height = self.font.get_height()

        if width != self.width or height != self.height:
            _Rect.set_width(self, width)
            _Rect.set_height(self, height)
            self._update_surface_type()

        SurfaceRect.fill(self, _Color(0, 0, 0, 0))
        x = 0
        for text in self.text_objects:
            SurfaceRect.blit(self, text, (x, 0))
            x += text.get_width()

    def _update_font(self):
        """Reload the font and all the text objects."""
        self.font = load_font(self.font_name, self.pt)
        for text in self.text_objects:
            text.set_font(self.font_name)
            text.set_pt(self.pt)

    def set_color(self, color, *index):
        """Set color to various TextObjects according to given indexes.

        If no indexes are given, the first object in the text list will be chosen. Else, the function cycles through
        all indexes, and changes objects from indexes from the text list accordingly.

        :param color: RGB text color
        :type color: _Color
        :param index: index in text list
        :type index: int
        """
        if len(index) == 0:
            for text in self.text_objects:
                text.set_color(color)
        else:
            for i in index:
                self.text_objects[i].set_color(color)
        self._update_surface()

    def set_content(self, content, *index):
        """Set content to various TextObjects according to given indexes.

        If no indexes are given, the first object in the text list will be chosen. Else, the function cycles through
        all indexes, and changes objects from indexes from the text list accordingly.

        :param content: TextObject content
        :type content: str
        :type index: int
        """
        if len(index) == 0:
            for text in self.text_objects:
                text.set_content(content)
        else:
            for i in index:
                self.text_objects[i].set_content(content)
        self._update_surface()

    def set_bold(self, bold, *index):
        """Set bold to various TextObjects according to given indexes.

        If no indexes are given, the first object in the text list will be chosen. Else, the function cycles through
        all indexes, and changes objects from indexes from the text list accordingly.

        :type bold: bool
        :type index: int
        """
        if len(index) == 0:
            for text in self.text_objects:
                text.set_bold(bold)
        else:
            for i in index:
                self.text_objects[i].set_bold(bold)
        self._update_surface()

    def set_italic(self, italic, *index):
        """Set italic to various TextObjects according to given indexes.

        If no indexes are given, the first object in the text list will be chosen. Else, the function cycles through
        all indexes, and changes objects from indexes from the text list accordingly.

        :type italic: bool
        :type index: int
        """
        if len(index) == 0:
            for text in self.text_objects:
                text.set_italic(italic)
        else:
            for i in index:
                self.text_objects[i].set_italic(italic)
        self._update_surface()

    def set_underline(self, underline, *index):
        """Set underline to various TextObjects according to given indexes.

        If no indexes are given, the first object in the text list will be chosen. Else, the function cycles through
        all indexes, and changes objects from indexes from the text list accordingly.

        :type underline: bool
        :type index: int
        """
        if len(index) == 0:
            for text in self.text_objects:
                text.set_underline(underline)
        else:
            for i in index:
                self.text_objects[i].set_underline(underline)
        self._update_surface()

    def set_pt(self, pt):
        """Set font size to a given value.

        :type pt: int
        """
        self.pt = pt
        self._update_font()
        self._update_surface()

    def set_font(self, font_name):
        """Set font to a given value.

        :type font_name: str
        """
        self.font_name = font_name
        self._update_font()
        self._update_surface()

    def __getitem__(self, item):
        """Get certain TextObject depending on the index.

        :type item: int
        :rtype: TextObject
        """
        return self.text_objects[item]

    def __iter__(self):
        """Initiate iteration sequence.

        :rtype: Polygon
        """
        self.__index = 0
        return self

    def __len__(self):
        """Return length of text_objects.

        :rtype: int
        """
        return len(self.text_objects)

    def __next__(self):
        """Progress iteration sequence.

        :rtype: Text
        """
        if self.__index < len(self.text_objects):
            text_object = self.text_objects[self.__index]
            self.__index += 1
            return text_object
        self._update_surface()
        raise StopIteration

    def __repr__(self):
        """Return repr(self)."""
        return represent("x y width height pt font_name", self.x, self.y, self.width, self.height, self.pt,
                         self.font_name)
