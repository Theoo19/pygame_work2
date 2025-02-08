from math import pi as _pi, sin as _sin, cos as _cos, log as _log


class AbstractChange:
    """A class to contain the constructors of its functions without any of the definitions."""

    def a(self, t): ...
    def v(self, t): ...
    def s(self, t): ...


class LinearChange(AbstractChange):
    """A class to represent change on a linear path."""

    def __init__(self, difference, ticks):
        """Initiate LinearChange object, inheriting from AbstractChange class.

        :param difference: total difference needed for calculation
        :type difference: float
        :param ticks: time it takes to get the total difference
        :type ticks: int
        """
        self.__a = difference / ticks
        self.__ticks = ticks

    def a(self, t):
        """Get acceleration based on elapsed time.

        Linear change means instant acceleration at the start and instant deceleration at the end to maintain a constant
        speed. In between, speed is not changed, therefore acceleration is 0.

        :param t: elapsed ticks
        :type t: int
        :return: acceleration
        :rtype: float
        """
        if t == 0:
            return self.__a
        elif t == self.__ticks:
            return -self.__a
        return 0

    def v(self, t):
        """Get speed based on elapsed time.

        Derivative from s(t).

        :param t: elapsed ticks
        :type t: int
        :return: speed
        :rtype: float
        """
        return self.__a

    def s(self, t):
        """Get distance based on elapsed time.

        :param t: elapsed ticks
        :type t: int
        :return: distance
        :rtype: float
        """
        return self.__a * t


class ParabolaChange(AbstractChange):
    """A class to represent change on a parabola path."""

    def __init__(self, difference, ticks):
        """Initiate ParabolaChange object, inheriting from AbstractChange class.

        :param difference: total difference needed for calculation
        :type difference: float
        :param ticks: time it takes to get the total difference
        :type ticks: int
        """
        self.__a = -2 * difference / (ticks**3)
        self.__b = 3 * difference / (ticks**2)

    def a(self, t):
        """Get acceleration based on elapsed time.

        Derivative from v(t).

        :param t: elapsed ticks
        :type t: int
        :return: acceleration
        :rtype: float
        """
        return 6 * self.__a * t + 2 * self.__b

    def v(self, t):
        """Get speed based on elapsed time.

        Derivative from s(t).

        :param t: elapsed ticks
        :type t: int
        :return: speed
        :rtype: float
        """
        return 3 * self.__a * t**2 + 2 * self.__b * t

    def s(self, t):
        """Get distance based on elapsed time.

        :param t: elapsed ticks
        :type t: int
        :return: distance
        :rtype: float
        """
        return self.__a * t**3 + self.__b * t**2


class TrigChange(AbstractChange):
    """A class to represent change on a trigonometric, cos-like path."""

    def __init__(self, difference, ticks):
        """Initiate TrigChange object, inheriting from AbstractChange class.

        :param difference: total difference needed for calculation
        :type difference: float
        :param ticks: time it takes to get the total difference
        :type ticks: int
        """
        self.__a = _pi / ticks
        self.__b = difference / 2

    def a(self, t):
        """Get acceleration based on elapsed time.

        Derivative from v(t).

        :param t: elapsed ticks
        :type t: int
        :return: acceleration
        :rtype: float
        """
        return self.__b * self.__a**2 * _cos(self.__a * t)

    def v(self, t):
        """Get speed based on elapsed time.

        Derivative from s(t).

        :param t: elapsed ticks
        :type t: int
        :return: speed
        :rtype: float
        """
        return self.__b * self.__a * _sin(self.__a * t)

    def s(self, t):
        """Get distance based on elapsed time.

        :param t: elapsed ticks
        :type t: int
        :return: distance
        :rtype: float
        """
        return self.__b * (1 - _cos(self.__a * t))


class ExponentialChange(AbstractChange):
    """A class to represent change on an exponential path."""

    def __init__(self, difference, ticks):
        """Initiate ExponentialChange object, inheriting from AbstractChange class.

        :param difference: total difference needed for calculation
        :type difference: float
        :param ticks: time it takes to get the total difference
        :type ticks: int
        """
        self.__a = (abs(difference) + 1)**(1 / ticks)
        if difference >= 0:
            self.__b = 1
        else:
            self.__b = -1

    def a(self, t):
        """Get acceleration based on elapsed time.

        Derivative from v(t).

        :param t: elapsed ticks
        :type t: int
        :return: acceleration
        :rtype: float
        """
        return self.__b * self.__a**t * _log(self.__a)**2

    def v(self, t):
        """Get speed based on elapsed time.

        Derivative from s(t).

        :param t: elapsed ticks
        :type t: int
        :return: speed
        :rtype: float
        """
        return self.__b * self.__a**t * _log(self.__a)

    def s(self, t):
        """Get distance based on elapsed time.

        :param t: elapsed ticks
        :type t: int
        :return: distance
        :rtype: float
        """
        return self.__b * (self.__a**t - 1)
