from ..logic.time import Timer as _Timer
from ..logic.constants import CharacterType as _CharacterType


class Button:
    def __init__(self, index):
        self._type = index
        self._pressed = False
        self._press_down = False
        self._press_up = False
        self._timer = _Timer()
        self._last_pressed_time = 0

    def get_type(self):
        return self._type

    def get_pressed(self):
        return self._pressed

    def get_press_down(self):
        return self._press_down

    def get_press_up(self):
        return self._press_up

    def get_pressed_time(self):
        return self._timer.get_counter()

    def get_timer(self):
        return self._timer

    def get_last_time(self):
        return self._last_pressed_time

    def get_timed_pressed_interval(self, ticks, threshold=1/2, interval=1/15):
        counter = self._timer.get_counter()
        return counter > ticks * threshold and counter % (ticks * interval) == 0

    def set_press_down(self):
        self._press_down = True
        self._pressed = True
        self._timer.start()

    def set_press_up(self):
        self._press_up = True
        self._pressed = False
        self._last_pressed_time = self._timer.get_counter()
        self._timer.reset()

    def reset(self):
        self._press_down = False
        self._press_up = False

    def update(self):
        self.reset()
        self._timer.tick()


class Key(Button):
    def __init__(self, index, mod=0, unicode=""):
        Button.__init__(self, index)
        self._mod = mod
        self._unicode = unicode

    def get_mod(self):
        return self._mod

    def get_unicode(self):
        return self._unicode

    def get_char(self):
        if self._unicode not in ("", "\t", "\r", "\x08", "\x1b"):
            return self._unicode
        return None

    def is_char(self):
        if self._unicode not in ("", "\t", "\r", "\x08", "\x1b"):
            return True
        return False

    def is_char_type(self, char_type):
        if self._unicode in char_type and self._unicode not in ("",):
            return True
        return False

    def is_alpha(self):
        return self.is_char_type("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def is_numeric(self):
        return self.is_char_type("0123456789")

    def is_lower(self):
        return self.is_char_type("abcdefghijklmnopqrstuvwxyz")

    def is_upper(self):
        return self.is_char_type("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def check_character_type_validity(self, char_type):
        if char_type == _CharacterType.all:
            return self.is_char()
        elif char_type == _CharacterType.alpha:
            return self.is_alpha()
        elif char_type == _CharacterType.numeric:
            return self.is_numeric()
        return False
