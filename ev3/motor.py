# -*- coding: utf-8 -*-
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

    def __str__(self):
        return ','.join(self._valid_values)


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
        self._speed = 360
        self._acceleration = 6000

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
        """
        Rotates the motor forward until told otherwise. Immediate returns
        """
        self._send_command("forward", True)

    def backward(self):
        """
        Rotates the motor backwards until told otherwise. Immediate returns
        """
        self._send_command("backward", True)

    def stop(self, immediate=True):
        """
        Stops the current action of the motor instantaneously. The motor will reset any further motion
        @param immediate:   If true it will not block until the motor has come to a complete stop.
                            Stop can be a quite slow operation if the acceleration is set to a smaller value then
                            initialized.
        @type immediate:    bool
        """
        self._send_command("stop", immediate)

    def rotate(self, degrees, immediate_return=True):
        """
        Rotates the motor by the number of degrees provided
        @param degrees: The number of degrees the motor should rotate
        @param immediate_return: If true the function will not wait until the operation has complete

        @type degrees: int
        @type immediate_return: bool
        """
        self._send_command("rotate", immediate_return, degrees=str(degrees))

    def rotate_to(self, angle, immediate_return=True):
        """
        Rotates the motor to the angle specified
        @param angle: The number of degrees the motor should rotate
        @param immediate_return: If true the function will not wait until the operation has complete

        @type angle: int
        @type immediate_return: bool
        """
        self._send_command("rotate_to", immediate_return, degrees=str(angle))

    def set_speed(self, speed):
        """
        Sets the desired motor speed, in degrees per second. Default value is 360.
        Note you can set it higher then the maximum, but then the motor operations gets a huge
        delay since it tries to catch up the missed motor rotations to have the correct speed.
        @param speed: The desired speed in degrees/second
        @type speed: float
        @see self.get_max_speed(): For more information on the max speed
        """
        self._speed = speed
        self._send_command("set_speed", True, speed=speed)

    def set_acceleration(self, acceleration):
        """
        Sets the desired motor acceleration, in degrees/sec/sec. Default value is 6000, which makes motor operations
        almost instant. Smaller values makes speedup and stop more smooth operations, but take longer.
        @param acceleration:
        @type acceleration: int
        """
        self._acceleration = acceleration
        self._send_command("set_acceleration", True, acceleration=int(acceleration))

    def set_stalled_threshold(self, error, time):
        """
        Set the parameters for a motor to detect if it is stalled. If the offset of the movement is larger then
        error(how much it should have moved vs how much it has moved) for the specified amount of time the motor is
        stalled.
        @param error: How big the movement offset must be in degrees
        @param time: How long the motor must have the given error before it stalled in seconds

        @type error: int
        @type time: int
        """
        self._send_command("set_stall_threshold", True, time=time, error=error)

    def reset_tacho_count(self):
        """
        Reset the tacho count back to zero from the current position. Current movement will be canceled.
        """
        self._send_command("reset_tacho_count", True)

    def set_float_mode(self):
        """
        Set the motors in float mode. Stops the current movement without breaking and position will no longer be
        maintained. Any operation except this one cancels the float mode again.
        """
        self._send_command("set_float_mode", True)

    def get_tacho_count(self):
        """
        Returns the Tacho count
        """
        data = self._get_data("get_tacho_count")
        return int(data['data'])

    def get_position(self):
        """
        Returns the current position the motor is in. Normally the same value as the Tacho count, but in some
        circumstances where the position has been forced to a different place these values may vary.
        @return: degrees
        """
        data = self._get_data("get_position")
        return int(data['data'])

    def is_moving(self):
        """
        Returns if the motor is moving or not.
        """
        data = self._get_data("is_moving")
        return bool(data['data'])

    def is_stalled(self):
        """
        Returns if the motor is stalling
        """
        data = self._get_data("is_stalled")
        return bool(data['data'])

    def get_max_speed(self):
        """
        Returns the motor maximum speed. Its a calculated by :  100 degree/second * Voltage in the brick
        """
        data = self._get_data("get_max_speed")
        return float(data['data'])

    def get_speed(self):
        """
        Returns the current speed of the motor
        """
        return self._speed

    def get_acceleration(self):
        """
        Returns the current acceleration of the motor
        """
        return self._acceleration


