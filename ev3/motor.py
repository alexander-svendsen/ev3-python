# -*- coding: utf-8 -*-
import collections
import json

import error
from brick import Brick

#future_todo: fix in the future when more ports can be connected
_motor_ports_named_tuple = collections.namedtuple('MotorPorts', "PORT_A PORT_B PORT_C PORT_D")
MOTOR_PORTS = _motor_ports_named_tuple("A", "B", "C", "D")  # The only valid motor ports


class Motor(object):
    """
    Provides the control mechanism for a single motor
    """
    initialized = False

    def __new__(cls, brick, motor_port):
        if motor_port in brick.get_opened_ports:
            motor = brick.get_opened_ports[motor_port]
            if motor.__class__ == cls:
                return motor
        return super(Motor, cls).__new__(cls, brick, motor_port)

    def __init__(self, brick, motor_port):
        """
        @param brick: The brick the motor uses
        @param motor_port: Which motor port to use.
        @see MOTOR_PORTS: Contains the valid motor ports to use, default A-D

        @type brick: Brick
        @type motor_port: str
        """

        if motor_port not in MOTOR_PORTS:
            raise error.InvalidMotorPortException("Must be a valid motor port")

        if not isinstance(brick, Brick):
            raise error.IllegalArgumentException("Invalid brick instance")

        if self.initialized:  # catches double init
            return

        self._motor_port = motor_port
        self._brick = brick

        self._brick.set_port_to_used(self._motor_port, self)
        self._cmd = {"cla": "motor", "motor_port": self._motor_port}
        self._speed = 360
        self._acceleration = 6000

        self._closed = False

    def _send_command(self, cmd, immediate_return, **extra_command):
        if self._closed:
            raise error.MotorNotConnectedException("Motor got closed, you cannot use this object anymore")

        self._cmd["cmd"] = cmd

        packet = self._cmd.copy()
        packet.update(extra_command)

        packet["immediate"] = immediate_return
        data = self._brick.send_command(packet, immediate_return)
        return data

    def _get_data(self, cmd):
        self._cmd["cmd"] = cmd
        data = self._brick.send_command(self._cmd)
        return data

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

    def stop(self, immediate=False):
        """
        Stops the current action of the motor instantaneously. The motor will reset any further motion
        @param immediate:   If true it will not block until the motor has come to a complete stop.
                            Stop can be a quite slow operation if the acceleration is set to a smaller value then
                            initialized.
        @type immediate:    bool
        """
        self._send_command("stop", immediate)

    def rotate(self, degrees, immediate_return=False):
        """
        Rotates the motor by the number of degrees provided
        @param degrees: The number of degrees the motor should rotate
        @param immediate_return: If true the function will not wait until the operation has complete

        @type degrees: int
        @type immediate_return: bool
        """
        self._send_command("rotate", immediate_return, degrees=int(degrees))

    def rotate_to(self, angle, immediate_return=False):
        """
        Rotates the motor to the angle specified
        @param angle: The number of degrees the motor should rotate
        @param immediate_return: If true the function will not wait until the operation has complete

        @type angle: int
        @type immediate_return: bool
        """
        self._send_command("rotate_to", immediate_return, degrees=int(angle))

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
        self._send_command("set_stall_threshold", True, time=int(time), error=int(error))

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

    def close(self):
        """
        Closes the motor port, freeing it for other motor objects
        """
        self._brick.set_port_to_unused(self._motor_port)
        self._closed = True

    def get_name(self):
        return "Motor_" + self._motor_port

    #incase of garbage collected, close the motor port
    def __del__(self):
        self.close()