from .basic import FilledRect as _FilledRect
from ..logic.common import clamp as _clamp

"""
AbstractTimer?
Timer

AbstractProgress
ProgressBar
ProgressPie

AbstractDataTable
DataTable
"""


class ProgressBar(_FilledRect):
    def __init__(self, x, y, width, height, x_mode, y_mode, color, progress=1, horizontal=True):
        self.progress = 0
        self.horizontal = horizontal

        if self.horizontal:
            self.max_length = width
        else:
            self.max_length = height

        _FilledRect.__init__(self, x, y, width, height, x_mode, y_mode, color)
        self.set_progress(progress)

    def set_progress(self, progress):
        self.progress = _clamp(progress, 0, 1)

        if self.horizontal:
            self.set_width(self.max_length * self.progress)
        else:
            self.set_height(self.max_length * self.progress)

    def set_time_progress(self, timer):
        self.set_progress(timer.get_counter() / timer.get_base())

    def draw(self, surface):
        if self.progress > 0:
            _FilledRect.draw(self, surface)


# class ProgressText(_TextDisplay):
#     def __init__(self, base, goal, ticks, x=0, y=0, characters="0123456789", font=None, pt=None, color=None,
#                  x_mode=_Al.df(), y_mode=_Al.df(), x_offset=0, y_offset=0, width=None, height=None):
#         self.base = base
#         self.goal = goal
#         self.ticks = ticks
#         self.progress = base
#         self.progress_per_tick = (self.goal - self.base) / self.ticks
#
#         _TextDisplay.__init__(self, x, y, characters, font, pt, color, x_mode, y_mode, x_offset, y_offset, width,
#                               height, self.progress)
#
#     def update_progress_per_tick(self):
#         self.progress_per_tick = (self.goal - self.base) / self.ticks
#
#     def set_progress(self, progress):
#         if progress < self.base:
#             self.progress = self.base
#         elif progress > self.goal:
#             self.progress = self.goal
#         else:
#             self.progress = progress
#
#     def set_base(self, base):
#         self.base = base
#         self.update_progress_per_tick()
#
#     def set_goal(self, goal):
#         self.goal = goal
#         self.update_progress_per_tick()
#
#     def set_ticks(self, ticks):
#         self.ticks = ticks
#         self.update_progress_per_tick()
#
#     def reset_progress(self):
#         self.progress = self.base
#
#     def reach_goal(self):
#         self.progress = self.goal
#         self.set_text(self.goal)
#
#     def update_text(self):
#         if self.progress < self.goal:
#             if self.progress + self.progress_per_tick <= self.goal:
#                 self.progress += self.progress_per_tick
#             else:
#                 self.progress = self.goal
#             self.set_text(int(self.progress))
#
#     def functions(self):
#         self.update_text()
#         self.display()
