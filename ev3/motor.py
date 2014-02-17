# -*- coding: utf-8 -*-
from collections import namedtuple
from brick import Brick
import error
import json


class InvalidMotorPortException(Exception):
    pass


class MotorPorts(object):
    """
    Object to keep the valid ports stored
    """
    #future_todo: fix in the future when more ports can be connected
    _valid_values = ["A", "B", "C", "D"]

    def get_valid_ports(self):
        return self._valid_values

    def __contains__(self, item):
        return item in self._valid_values

# REVIEW should i communicate like this?


class Motor():
    """
    Provides the control mechanism for a single motor
    """
    def __init__(self, brick, motor_port):
        """
        @param brick: The brick the motor uses
        @param motor_port: Which motor port to use.
        @see MotorPorts: Contains the valid motor ports to use, default A-D
        @raise error.IllegalArgumentError: If any parameter is wrong this exception is raised

        @type brick: Brick
        @type motor_port: str
        """

        if motor_port not in MotorPorts():
            raise InvalidMotorPortException("Must be a valid motor port")

        if not isinstance(brick, Brick):
            raise error.IllegalArgumentException("Invalid brick instance")

        self._motor_port = motor_port
        self._brick = brick
        self._cmd = {"cla": "motor", "port": self._motor_port}

    def _send_command(self, cmd, immediate_return, **extra_command):
        self._cmd["cmd"] = cmd

        packet = self._cmd.copy()
        packet.update(extra_command)

        if immediate_return:
            self._brick.send_command(json.dumps(packet))
        else:
            packet["immediate"] = immediate_return
            data = self._brick.send_command(json.dumps(packet))
            return json.loads(data)

    def _get_data(self, cmd):
        self._cmd["cmd"] = cmd
        data = self._brick.send_command(json.dumps(self._cmd))
        return json.loads(data)

    def forward(self):
        self._send_command("forward", True)

    def backward(self):
        self._send_command("backward", True)

    def stop(self): #review immidate return?
        self._send_command("stop", True)

    def rotate(self, degrees, immediate_return=True):
        self._send_command("rotate", immediate_return, degrees=str(degrees))

    def rotate_to(self, angle, immediate_return=True):
        self._send_command("rotate_to", immediate_return, degrees=str(angle))

    def set_speed(self, speed):
        self._send_command("set_speed", True, speed=speed)

    def set_acceleration(self, acceleration):
        self._send_command("set_acceleration", True, acceleration=int(acceleration))

    def set_stalled_threshold(self, error, time):
        self._send_command("set_stall_threshold", True, time=time, error=error)

    def reset_tacho_count(self):
        self._send_command("reset_tacho_count", True)

    def set_float_mode(self): #review immidate return?
        self._send_command("set_float_mode", True)

    def get_tacho_count(self):
        data = self._get_data("get_tacho_count")
        return int(data['data'])

    def get_position(self):
        data = self._get_data("get_position")
        return int(data['data'])

    def is_moving(self):
        data = self._get_data("is_moving")
        return bool(data['data'])

    def is_stalled(self):
        data = self._get_data("is_stalled")
        return bool(data['data'])

    def get_max_speed(self):
        data = self._get_data("get_max_speed")
        return float(data['data'])

    def get_rotation_destination(self):
        #Problem dynamicly calulating it as the value is the same between each time
        #starts on 0 when the program is started
        #fixme
        raise NotImplementedError

# TODO : getspeed and get_acc?
