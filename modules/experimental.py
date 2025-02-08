from .math.geometry  import Rect as _Rect
from pygame import Surface as _Surface, SRCALPHA as _SRCALPHA
from pygame.transform import smoothscale as _smoothscale


class Image(_Rect, _Surface):
    def __init__(self, x, y, width, height, x_mode, y_mode, original_surface):
        self.original_surface = original_surface
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        _Surface.__init__(self, (self.width, self.height), _SRCALPHA)
        self._update_surface()

    def _update_surface_type(self):
        _Surface.__init__(self, (self.width, self.height), _SRCALPHA)

    def _update_surface(self):
        surface = _smoothscale(self.original_surface, (int(self.width), int(self.height)))
        self._update_surface_type()
        self.blit(surface, (0, 0))

    def set_width(self, width):
        _Rect.set_width(self, width)
        self._update_surface()

    def set_height(self, height):
        _Rect.set_height(self, height)
        self._update_surface()

    def draw(self, surface):
        surface.blit(self, (self.x, self.y))
