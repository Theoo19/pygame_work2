from .math.geometry import Point as _Point
from pygame import draw as _draw, Color as _Color


class Particle(_Point):
    def __init__(self, x, y, dx=0, dy=0, ax=0, ay=0, color=_Color(0, 0, 0), size=5):
        _Point.__init__(self, x, y)
        self.dx = dx
        self.dy = dy
        self.ax = ax
        self.ay = ay
        self.color = color
        self.size = size

    def accelerate_x(self, ax):
        self.dx += ax

    def accelerate_y(self, ay):
        self.dy += ay

    def accelerate(self, ax, ay):
        self.accelerate_x(ax)
        self.accelerate_y(ay)

    def update_move(self, drag=1):
        self.accelerate(self.ax, self.ay)
        self.dx *= drag
        self.dy *= drag
        self.move(self.dx, self.dy)

    def update_in_box(self, x1, y1, x2, y2):
        if self.x <= x1:
            self.dx *= -1
            self.x = x1
        elif self.x + self.size >= x2:
            self.dx *= -1
            self.x = x2 - self.size

        if self.y <= y1:
            self.dy *= -1
            self.y = y1
        elif self.y + self.size >= y2:
            self.dy *= -1
            self.y = y2 - self.size

    def update_in_left(self, x):
        if self.x <= x:
            self.dx *= -1
            self.x = x

    def update_in_right(self, x):
        if self.x + self.size >= x:
            self.dx *= -1
            self.x = x - self.size

    def update_in_top(self, y):
        if self.y <= y:
            self.dy *= -1
            self.y = y

    def update_in_bottom(self, y):
        if self.y + self.size >= y:
            self.dy *= -1
            self.y = y - self.size

    def draw(self, surface):
        _draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
