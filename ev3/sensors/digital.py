# -*- coding: utf-8 -*-
from common import Sensor, MODE_TUPLE


class EV3ColorSensor(Sensor):
    pass


class HiTechnicColorSensor(Sensor):  # two modes, maybe must have inner classes to handle the different modes

    class Mother(object):
        pass

    def __init__(self, brick, sensor_port):
        super(HiTechnicColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [MODE_TUPLE("ColorID", 1), MODE_TUPLE("RGB", 3)]


