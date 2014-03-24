# -*- coding: utf-8 -*-
import collections
from ev3.error import *


#future_todo: fix in the future when more ports can be connected
_sensor_ports_named_tuple = collections.namedtuple('SensorPorts', "PORT_1 PORT_2 PORT_3 PORT_4")
SENSOR_PORTS = _sensor_ports_named_tuple(1, 2, 3, 4)  # The only valid sensor ports


def cache(function):
    def new_function(self, *args, **kwargs):
        if self.cache_data:
            return self.cache_data
        return function(self, *args, **kwargs)
    return new_function


class Mode(object):
    def __init__(self, sensor):
        """
        A abstract class meant to be used by inner classes in sensors to have som complete methods common for all modes
        @param sensor: sensor module this mode belongs to
        @type sensor: Sensor
        """
        self._sensor = sensor

    def fetch_sample(self):
        """
        Returns a list with raw data in float for this mode.
        @rtype: list[float]
        """
        return self._sensor.get_raw_data()

    def get_name(self):
        """
        Returns the name of this mode.
        Most cases it's the same as the class name but without the "Mode" part.
        @return: mode name.
        """
        return str(self.__class__.__name__[:-4])

    @staticmethod
    def get_sample_size():
        """
        Returns how big the list of data this mode returns in fetch_sample. Always the same amount.
        @return: sample size.
        """
        return 1

    def __str__(self):
        return self.get_name()


class Sensor(object):
    initialized = False

    def __new__(cls, brick, sensor_port, opened_from_brick=False):  # review: write about this in the report
        if sensor_port in brick.get_opened_ports:
            sensor = brick.get_opened_ports[sensor_port]
            if sensor.__class__ == cls:
                return sensor
        return super(Sensor, cls).__new__(cls, brick, sensor_port, opened_from_brick)

    def __init__(self, brick, sensor_port, opened_from_brick=False):
        """
        Opens the specified sensor at the provided port. Note this class is not meant to be used by itself, but as a
        parent class for other sensors.

        @param brick: Which brick should this sensor be opened on
        @param sensor_port: What sensor port is the sensor on

        @type brick: Brick
        @type sensor_port: int
        """
        if sensor_port not in SENSOR_PORTS:
            raise InvalidSensorPortException("Must be a valid sensor port")

        if self.initialized:  # catches double init
            return

        self._sensor_port = sensor_port
        self._brick = brick
        self._closed = False

        if not self._brick.set_port_to_used(self._sensor_port, self):
            raise InvalidSensorPortException("sensor port already in use by a different sensor")

        self._cmd = {"cla": "sensor",
                     "sensor_port": (self._sensor_port - 1)}

        if not opened_from_brick:  # if not a callback command, we need to open it ourselves
            response = self._send_command("open_sensor", sensor_class_name=self.__class__.__name__)
            if not response["data"]:
                raise InvalidSensorPortException("Can't open sensor")

        # classes that inherit this variable should override it with the correct mode values
        self._available_modes = self._get_modes()

        # every sensor starts on mode 0
        self._selected_mode = 0
        self.initialized = True
        self.cache_data = None

    def _get_modes(self):
        return [Mode(self)]  # Should be overwritten

    def _send_command(self, cmd, **extra_command):
        if self._closed:
            raise SensorNotConnectedException("The sensor was closed, you cannot use this object anymore")

        self._cmd["cmd"] = cmd
        packet = self._cmd.copy()
        packet.update(extra_command)

        data = self._brick.send_command(packet)
        if data in (None, ''):
            raise BrickNotConnectedException("Brick not connected anymore!")
        return data

    def _call_sensor_control_method(self, method_name):
        result = bool(self._send_command("call_method", method=method_name))
        if not result:
            raise InvalidMethodException("Method: {} does not exists", method_name)

    def get_available_modes(self):
        """
        A method for getting the names of the available modes for this sensor
        @return: a list of the modes name in the current sensor
        """
        return [y.get_name() for y in self._available_modes]

    def _set_mode(self, mode):
        if type(mode) == int:
            if len(self._available_modes) < mode:
                raise InvalidModeSelected("Mode list out of range")
            new_selected_mode = mode
        elif type(mode) == str:
            if mode not in [y.get_name() for y in self._available_modes]:
                raise InvalidModeSelected("Mode does not exists")
            new_selected_mode = [y.get_name() for y in self._available_modes].index(mode)
        else:
            raise InvalidModeSelected("Mode must either be int or str")

        if new_selected_mode != self._selected_mode:
            self._selected_mode = new_selected_mode
            self._send_command("set_mode", mode=new_selected_mode)

    def get_mode(self, mode):
        """
        Sets and returns the mode for this sensor
        @param mode: Which mode to get
        @type mode: int|str
        """
        self._set_mode(mode)
        return self.get_selected_mode()

    def get_selected_mode_name(self):
        return self._available_modes[self._selected_mode].get_name()

    def get_selected_mode_sample_size(self):
        return self._available_modes[self._selected_mode].get_sample_size()

    def set_cache_data(self, data):
        self.cache_data = data

    @cache
    def get_raw_data(self):
        return self._send_command("fetch_sample")["sample"]

    def get_selected_mode(self):
        return self._available_modes[self._selected_mode]

    def get_name(self):
        return self.__class__.__name__

    def close(self):
        try:
            self._send_command("close")
        except:
            pass  # at this point we don't care any more because we lost the brick and must restart anyway
        self._brick.set_port_to_unused(self._sensor_port)
        self._closed = True

    #incase of garbage collected, close the sensor
    def __del__(self):
        self.close()

#A dict over what the different values in the colorid modes mean
COLOR_DICT = {
    0: 'red',
    1: 'green',
    2: 'blue',
    3: 'yellow',
    4: 'magenta',
    5: 'orange',
    6: 'white',
    7: 'black',
    8: 'pink',
    9: 'gray',          #unused!
    10: 'light gray',   #unused!
    11: 'dark gray',    #unused!
    12: 'cyan',         #unused!
    13: 'brown'
}