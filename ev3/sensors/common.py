# -*- coding: utf-8 -*-
import collections
from ev3 import error, Brick


class InvalidSensorPortException(Exception):
    pass


class InvalidModeSelected(Exception):
    pass


#future_todo: fix in the future when more ports can be connected
_sensor_ports_named_tuple = collections.namedtuple('SensorPorts', "PORT_1 PORT_2 PORT_3 PORT_4")
SENSOR_PORTS = _sensor_ports_named_tuple(1, 2, 3, 4)  # The only valid sensor ports

MODE_TUPLE = collections.namedtuple('MODE_TUPLE', "mode_name sample_size")


class Sensor(object):
    def __init__(self, brick, sensor_port):
        if sensor_port not in SENSOR_PORTS:
            raise InvalidSensorPortException("Must be a valid sensor port")

        if not isinstance(brick, Brick):
            raise error.IllegalArgumentException("Invalid brick instance")

        self._sensor_port = sensor_port
        self._brick = brick

        # classes that inherit this variable should override it with the correct mode values
        self._available_modes = [MODE_TUPLE(None, 0)]

        # every sensor starts on mode 0
        self._selected_mode = 0

    def get_available_modes(self):
        return self._available_modes

    def set_mode(self, mode):
        if type(mode) == int:
            if len(self._available_modes) < mode:
                raise InvalidModeSelected("Mode list out of range")
            new_selected_mode = mode
        elif type(mode) == str:
            if mode not in [y[0] for y in self._available_modes]:
                raise InvalidModeSelected("Mode does not exists")
            new_selected_mode = [y[0] for y in self._available_modes].index(mode)

        else:
            raise InvalidModeSelected("Mode must either be int or str")

        if new_selected_mode != self._selected_mode:
            self._selected_mode = new_selected_mode
            #TODO, do something with it

    def get_selected_mode_name(self):
        return self._available_modes[self._selected_mode].mode_name

    def sample_size(self):
        return self._available_modes[self._selected_mode].sample_size

    def fetch_sample(self):
        #TODO: implement it, think it can be implemented here just as well
        pass

    def close(self):
        #TODO, do something with it
        pass

    #incase of garbage collected, close the sensor
    def __del__(self):
        self.close()

    def __str__(self):
        str(self) # FIXME add Name of sensor and mode selected.