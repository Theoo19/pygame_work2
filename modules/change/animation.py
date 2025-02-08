from ..math.geometry import Rect as _Rect
from ..logic.time import ResetTimer as _ResetTimer
from pygame.image import load as _load
from math import inf as _inf
from ..logic.common import frames_from_image as _frames_from_image


class LoopRect(_Rect, _ResetTimer):
    def __init__(self, x, y, width, height, x_mode, y_mode, frames, factor=1, max_iter=_inf):
        self._frames = frames
        _Rect.__init__(self, x, y, width, height, x_mode, y_mode)
        _ResetTimer.__init__(self, 1, factor, max_iter=_inf)
        self._update_frames()

    def _update_frames(self):
        self.set_base(len(self._frames) * self._factor)
        self.set_width(max(image.get_width() for image in self._frames))
        self.set_height(max(image.get_height() for image in self._frames))

    def set_frames(self, frames):
        self._frames = frames
        self._update_frames()

    def loop_behavior(self):
        self.tick()

    def draw(self, surface):
        if self._active:
            surface.blit(self._frames[self.seconds()], (self.x, self.y))

    @staticmethod
    def from_image(x, y, width, height, x_mode, y_mode, x_offset, y_offset, filename, max_images, factor=1,
                   max_iter=_inf):
        frames = _frames_from_image(filename, width, height, max_images)
        return LoopRect(x, y, width, height, x_mode, y_mode, x_offset, y_offset, frames, factor, max_iter)

    @staticmethod
    def from_image_set(x, y, width, height, x_mode, y_mode, x_offset, y_offset, filename, max_images, factor=1,
                       max_iter=_inf):
        # Filename should be of a format such as "name_{}.png"
        # Filename numbers should start at 0.
        frames = list()
        for i in range(max_images):
            frame = _load(filename.format(i)).convert_alpha()
            frames.append(frame)
        return LoopRect(x, y, width, height, x_mode, y_mode, x_offset, y_offset, frames, factor, max_iter)
