# -*- coding: utf-8 -*-
from collections import namedtuple


class InvalidMotorPortException(Exception):
    pass


motor_ports_named_tuple = namedtuple('MotorPorts', "A B C D")
MOTOR_PORTS = motor_ports_named_tuple("A", "B", "C", "D")  # The only valid motor ports


class Motor():
    def __init__(self, brick, motor_port):
        if motor_port not in MOTOR_PORTS:
            raise InvalidMotorPortException("Must be a valid motor port")
