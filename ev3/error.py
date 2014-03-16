# -*- coding: utf-8 -*-


class IllegalArgumentException(ValueError):
    pass


class BrickNotFoundException(Exception):
    pass


class BrickNotConnectedException(Exception):
    pass


class SensorNotConnectedException(Exception):
    pass


class InvalidSensorPortException(Exception):
    pass


class InvalidModeSelected(Exception):
    pass


class InvalidMethodException(Exception):
    pass


class MotorNotConnectedException(Exception):
    pass


class InvalidMotorPortException(Exception):
    pass


