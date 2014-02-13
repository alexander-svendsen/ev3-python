# -*- coding: utf-8 -*-
from collections import namedtuple
from brick import Brick
import error
import json


class InvalidMotorPortException(Exception):
    pass


_motor_ports_named_tuple = namedtuple('MotorPorts', "A B C D")
MOTOR_PORTS = _motor_ports_named_tuple("A", "B", "C", "D")  # The only valid motor ports


class Motor():
    def __init__(self, brick, motor_port):
        if motor_port not in MOTOR_PORTS:
            raise InvalidMotorPortException("Must be a valid motor port")

        if not isinstance(brick, Brick):
            raise error.IllegalArgumentError("Invalid brick instance")

        self.motor_port = motor_port
        self.brick = brick

    # REVIEW should i communicate like this?
    def forward(self):
        cmd = {"class": "motor", "cmd": "forward", "port": self.motor_port}
        self.brick.send_command(json.dumps(cmd))

    def backward(self):
        pass

    def stop(self):  # NOTE immediate return or not ?
        cmd = {"class": "motor", "cmd": "stop", "port": self.motor_port}
        self.brick.send_command(json.dumps(cmd))

    def rotate(self, degrees, immediate_return):
        pass

    def rotate_to(self, angle,  immediate_return):
        pass

    def get_tacho_count(self):
        pass

    def get_position(self):
        pass

    def is_moving(self):
        pass

    def is_stalled(self):
        pass

    def set_speed(self, speed):
        pass

    def set_acceleration(self, acceleration):
        pass

    def set_stalled_threshold(self, error, time):
        pass

    def get_max_speed(self):
        pass

    def get_rotation_destination(self):
        pass

    def reset_tacho_count(self):
        pass

    def set_float_mode(self):
        pass



