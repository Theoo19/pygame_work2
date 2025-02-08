from .constants import Default as _Default
from .loaders import FunctionLoader as _FunctionLoader
from copy import deepcopy as _deepcopy
from math import inf as _inf
from collections.abc import Sequence as _Sequence


class Time:
    """A class to represent a timestamp with seconds, minutes and hours."""

    def __init__(self, counter=0, factor=1):
        """Initiate Time object.

        :param counter: the amount of time
        :type counter: int
        :param factor: conversion rate between counter and seconds
        :type factor: int
        """
        self._counter = counter
        self._factor = factor

    def set_counter(self, counter):
        """set counter to a given value.

        :param counter: the amount of time
        :type counter: int
        """
        self._counter = counter

    def set_factor(self, factor):
        """Set factor to a given value.

        :param factor: conversion rate between counter and seconds
        :type factor: int
        """
        self._factor = factor

    def get_counter(self):
        """Get counter.

        :return: the amount of time, unconverted
        :rtype: int
        """
        return self._counter

    def get_factor(self):
        """Get factor.

        :return: conversion rate between counter and seconds
        :rtype: int
        """
        return self._factor

    def milliseconds(self):
        """Get the amount of milliseconds.

        :return: milliseconds
        :rtype: float
        """
        return self._counter / self._factor * 1000

    def seconds(self):
        """Get the amount of seconds.

        :return: seconds
        :rtype: int
        """
        return self._counter // self._factor

    def minutes(self):
        """Get the amount of minutes.

        :return: minutes
        :rtype: int
        """
        return self.seconds() // 60

    def hours(self):
        """Get the amount of hours.

        :return: hours
        :rtype: int
        """
        return self.minutes() // 60

    def time(self):
        """Get tuple containing timestamp

        :return: hour, minutes, seconds
        :rtype: (int, int, int)
        """
        return self.hours(), self.minutes() % 60, self.seconds() % 60

    def time_string(self):
        """Get string containing timestamp: "hh:mm:ss" or "mm:ss"

        :return: hours, minutes, seconds
        :rtype: str
        """
        hours, minutes, seconds = self.time()
        if seconds < 10:
            seconds = "0{}".format(seconds)
        if minutes < 10:
            minutes = "0{}".format(minutes)
        if hours == 0:
            return "{}:{}".format(minutes, seconds)
        elif hours < 10:
            hours = "0{}".format(hours)
        return "{}:{}:{}".format(hours, minutes, seconds)

    def __add__(self, other):
        """Return self + other"""
        timer = _deepcopy(self)
        timer._counter += other.get_counter() * timer._factor
        return timer

    def __sub__(self, other):
        """Return self - other."""
        timer = _deepcopy(self)
        timer._counter -= other.get_counter() * timer._factor
        return timer

    def __mul__(self, other):
        """Return self * other."""
        timer = _deepcopy(self)
        timer._counter *= other
        return timer

    def __truediv__(self, other):
        """Return self / other."""
        timer = _deepcopy(self)
        timer._counter /= other
        return timer

    def __floordiv__(self, other):
        """Return self // other."""
        timer = _deepcopy(self)
        timer._counter //= other
        return timer

    def __mod__(self, other):
        """Return self % other."""
        timer = _deepcopy(self)
        timer._counter %= other
        return timer

    def __and__(self, other):
        """Return self & other."""
        timer = _deepcopy(self)
        timer._counter &= other
        return timer

    def __xor__(self, other):
        """Return self ^ other."""
        timer = _deepcopy(self)
        timer._counter ^= other
        return timer

    def __invert__(self):
        """Return ~self."""
        timer = _deepcopy(self)
        timer._counter = ~self._counter
        return timer

    def __or__(self, other):
        """Return self | other."""
        timer = _deepcopy(self)
        timer._counter |= other
        return timer

    def __pow__(self, power):
        """Return self**power."""
        timer = _deepcopy(self)
        timer._counter = pow(timer._counter, power)
        return timer

    def __radd__(self, other):
        """Return self += other."""
        self._counter = other.get_counter() * self._factor + self._counter
        return self

    def __rsub__(self, other):
        """Return self -= other."""
        self._counter = other.get_counter() * self._factor - self._counter
        return self

    def __rmul__(self, other):
        """Return self *= other."""
        self._counter = other * self._counter
        return self

    def __rtruediv__(self, other):
        """Return self /= other."""
        self._counter = other / self._counter
        return self

    def __rfloordiv__(self, other):
        """Return self //= other."""
        self._counter = other // self._counter
        return self

    def __rmod__(self, other):
        """Return self %= other."""
        self._counter = other % self._counter
        return self

    def __rand__(self, other):
        """Return self &= other."""
        self._counter = other & self._counter
        return self

    def __rxor__(self, other):
        """Return self ^= other."""
        self._counter = other ^ self._counter
        return self

    def __ror__(self, other):
        """Return self |= other."""
        self._counter = other | self._counter
        return self

    def __rpow__(self, other):
        """Return self **= other."""
        self._counter = pow(other, self._counter)
        return self

    def __iadd__(self, other):
        """Return self += other."""
        self._counter += other.get_counter() * self._factor
        return self

    def __isub__(self, other):
        """Return self -= other."""
        self._counter -= other.get_counter() * self._factor
        return self

    def __imul__(self, other):
        """Return self *= other."""
        self._counter *= other
        return self

    def __itruediv__(self, other):
        """Return self /= other."""
        self._counter /= other
        return self

    def __ifloordiv__(self, other):
        """Return self //= other."""
        self._counter //= other
        return self

    def __imod__(self, other):
        """Return self %= other."""
        self._counter %= other
        return self

    def __ipow__(self, other):
        """Return self **= other."""
        self._counter **= other
        return self

    def __lt__(self, other):
        """Return self < other."""
        return self.milliseconds() < other

    def __le__(self, other):
        """Return self <= other."""
        return self.milliseconds() <= other

    def __eq__(self, other):
        """Return self == other."""
        return self.milliseconds() == other

    def __ne__(self, other):
        """Return self != other."""
        return self.milliseconds() != other

    def __gt__(self, other):
        """Return self > other."""
        return self.milliseconds() > other

    def __ge__(self, other):
        """Return self >= other."""
        return self.milliseconds() >= other

    def __neg__(self):
        """Return -self."""
        self._counter = -self._counter
        return self

    def __pos__(self):
        """Return +self."""
        self._counter = +self._counter
        return self

    def __abs__(self):
        """Return abs(self)."""
        self._counter = abs(self._counter)
        return self

    def __round__(self, n=None):
        """Return round(self, n)."""
        self._counter = round(self._counter, n)
        return self

    def __str__(self):
        """Return str(self)."""
        return self.time_string()

    def __repr__(self):
        """Return repr(self)."""
        return self.time_string()

    def __int__(self):
        """Return int(self)."""
        return self.seconds()

    def __float__(self):
        """Return float(self)."""
        return self._counter / self._factor

    def __bool__(self):
        """Return self != 0."""
        return self._counter != 0

    @staticmethod
    def in_seconds(seconds, factor):
        """Create Time object from seconds instead of counter.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :return:
        :rtype: Time
        """
        return Time(int(seconds * factor), factor)

    @staticmethod
    def in_app_seconds(seconds):
        """Create Time object from seconds instead of counter, with factor from Default.ticks.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :return:
        :rtype: Time
        """
        factor = _Default.ticks
        return Time.in_seconds(seconds, factor)


class Timer(Time):
    """A class to represent a timestamp that can be activated to increase its value."""

    def __init__(self, counter=0, factor=1):
        """Initiate Timer object, inheriting from Time class.

        :param counter: the amount of time
        :type counter: int
        :param factor: conversion rate between counter and seconds
        :type factor: int
        """
        Time.__init__(self, counter, factor)
        self._active = False

    def set_active(self, active):
        """Set active to a certain value.

        :param active: increase counter or not
        :type active: bool
        """
        self._active = active

    def get_active(self):
        """Get active.

        :return: increase counter or not
        :rtype: bool
        """
        return self._active

    def tick(self):
        """Increase counter if active."""
        if self._active:
            self._counter += 1

    def start(self):
        """Set active to True."""
        self._active = True

    def stop(self):
        """Set active to False."""
        self._active = False

    def toggle_active(self):
        """Toggle active value."""
        self._active = not self._active

    def reset(self, active=False):
        """Reset counter and active value.

        :param active: increase counter or not
        :type active: bool
        """
        self._counter = 0
        self._active = active

    @staticmethod
    def in_seconds(seconds, factor):
        """Create Timer object from seconds instead of counter.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :return:
        :rtype: Timer
        """
        return Timer(int(seconds * factor), factor)

    @staticmethod
    def in_app_seconds(seconds):
        """Create Timer object from seconds instead of counter, with factor from Default.ticks.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :return:
        :rtype: Timer
        """
        factor = _Default.ticks
        return Timer.in_seconds(seconds, factor)


class CountDown(Timer):
    """A class to represent a timestamp that can be activated to count down and stops at 0."""

    def __init__(self, counter=0, factor=1, func=None):
        """Initiate CountDown object, inheriting from Timer class.

        :param counter: the amount of time
        :type counter: int
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when countdown is at 0
        :type func: _FunctionLoader or _Sequence or function or None
        """
        Timer.__init__(self, counter, factor)
        self._base = counter
        self._function = _FunctionLoader.from_variable(func)

    def set_function(self, func):
        """Set function to a certain value.

        :param func: function to call when countdown is at 0
        :type func: function or None
        """
        self._function.function = func

    def set_params(self, *params):
        """Set parameters to a certain value.

        :param params: parameters to use in function to call when countdown is at 0
        :type params: _Sequence
        """
        self._function.set_parameters(*params)

    def set_base(self, base):
        """Set base to a certain value.

        :param base: base number to count down to 0 from.
        :type base: int
        """
        self._base = base
        self._counter = self._base

    def get_base(self):
        """Get base.

        :return: base number to count down to 0 from.
        :rtype: int
        """
        return self._base

    def tick(self):
        """Decrease counter if active, reset and execute function when countdown is at 0."""
        if self._active:
            self._counter -= 1
            if self._counter <= 0:
                self._active = False
                self._function.execute()

    def reset(self, active=False):
        """Reset countdown."""
        self._counter = self._base
        self._active = active

    @staticmethod
    def in_seconds(seconds, factor, func=None):
        """Create CountDown object from seconds instead of counter.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when countdown is at 0
        :type func: _FunctionLoader or _Sequence or function or None
        :return:
        :rtype: CountDown
        """
        return CountDown(int(seconds * factor), factor, func)

    @staticmethod
    def in_app_seconds(seconds, func=None):
        """Create CountDown object from seconds instead of counter, with factor from Default.ticks.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param func: object to store function and needed parameters, called when countdown is at 0
        :type func: _FunctionLoader or _Sequence or function or None
        :return:
        :rtype: CountDown
        """
        factor = _Default.ticks
        return CountDown.in_seconds(seconds, factor, func)


class CountUp(CountDown):
    """A class to represent a timestamp that can be activated to count up and stops at maximum."""

    def __init__(self, maximum, factor=1, func=None):
        """Initiate CountUp object, inheriting from CountDown class.

        :param maximum: the amount of time to count up to
        :type maximum: int
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when countup is at maximum
        :type func: _FunctionLoader or _Sequence or function or None
        """
        CountDown.__init__(self, maximum, factor, func)
        self._counter = 0

    def set_base(self, maximum):
        """Set base to a certain value.

        :param maximum: base number to count up to from 0.
        :type maximum: int
        """
        self._base = maximum
        self._counter = 0

    def tick(self):
        """Increase counter if active, reset and execute function when countup is at base."""
        if self._active:
            self._counter += 1
            if self._counter >= self._base:
                self._active = False
                self._function.execute()

    def reset(self, active=False):
        """Reset countup."""
        self._counter = 0
        self._active = active

    @staticmethod
    def in_seconds(seconds, factor, func=None):
        """Create CountUp object from seconds instead of counter.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when countup is at base
        :type func: _FunctionLoader or _Sequence or function or None
        :return:
        :rtype: CountUp
        """
        return CountUp(int(seconds * factor), factor, func)

    @staticmethod
    def in_app_seconds(seconds, func=None):
        """Create CountDown object from seconds instead of counter, with factor from Default.ticks.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param func: object to store function and needed parameters, called when countup is at base
        :type func: _FunctionLoader or _Sequence or function or None
        :return:
        :rtype: CountUp
        """
        factor = _Default.ticks
        return CountUp.in_seconds(seconds, factor, func)


class ResetTimer(CountUp):
    def __init__(self, maximum, factor=1, func=None, max_iter=_inf):
        """Initiate ResetTimer object, inheriting from CountUp class.

        :param maximum: the amount of time to count up to
        :type maximum: int
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when reset-timer is at maximum
        :type func: _FunctionLoader or _Sequence or function or None
        :param max_iter: the amount of times the timer is restarted
        :type max_iter: int
        """
        CountUp.__init__(self, maximum, factor, func)
        self._max_iter_base = max_iter
        self._max_iter = max_iter

    def tick(self):
        """Increase counter if active, restart and execute function when reset-timer is at base."""
        if self._active:
            self._counter += 1
            if self._counter >= self._base:
                self._max_iter -= 1
                self._function.execute()
                if self._max_iter <= 0:
                    self._active = False
                    self._counter = self._base
                else:
                    self._counter = 0

    def reset(self, active=False):
        """Reset reset-timer."""
        self._counter = 0
        self._active = active
        self._max_iter = self._max_iter_base

    @staticmethod
    def in_seconds(seconds, factor, func=None, max_iter=_inf):
        """Create ResetTimer object from seconds instead of counter.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param factor: conversion rate between counter and seconds
        :type factor: int
        :param func: object to store function and needed parameters, called when reset-timer is at base
        :type func: _FunctionLoader or _Sequence or function or None
        :param max_iter: the amount of times the timer is restarted
        :type max_iter: int
        :return:
        :rtype: CountUp
        """
        return ResetTimer(int(seconds * factor), factor, func, max_iter)

    @staticmethod
    def in_app_seconds(seconds, func=None, max_iter=_inf):
        """Create ResetTimer object from seconds instead of counter, with factor from Default.ticks.

        :param seconds: the amount of seconds for the timer
        :type seconds: float
        :param func: object to store function and needed parameters, called when reset-timer is at base
        :type func: _FunctionLoader or _Sequence or function or None
        :param max_iter: the amount of times the timer is restarted
        :type max_iter: int
        :return:
        :rtype: CountUp
        """
        factor = _Default.ticks
        return ResetTimer.in_seconds(seconds, factor, func, max_iter)
