# -*- coding: utf-8 -*-
import common
from common import Sensor, Mode


class HiTechnicColorSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(HiTechnicColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ColorIDMode(self), self.RGBMode(self)]

    def get_color_id_mode(self):
        """
        @rtype: ColorIDMode
        """
        return self.get_mode(0)

    def get_rgb_mode(self):
        """
        @rtype: RGBMode
        """
        return self.get_mode(1)

    class ColorIDMode(Mode):
        colorDict = common.COLOR_DICT

        def get_color_specter(self):
            return self.colorDict.values()

        def get_color_id(self):
            return self.colorDict.get(self.fetch_sample()[0], 'none')

    class RGBMode(Mode):
        def get_color(self):
            return tuple(int(i) for i in self.fetch_sample())

        @staticmethod
        def get_sample_size():
            return 3


class HiTechnicAccelerometer(Sensor):
    def __init__(self, brick, sensor_port):
        super(HiTechnicAccelerometer, self).__init__(brick, sensor_port)
        self._available_modes = [self.AccelerationMode(self)]

    class AccelerationMode(Mode):
        @staticmethod
        def get_sample_size():
            return 3


class HiTechnicGyro(Sensor):
    def __init__(self, brick, sensor_port):
        super(HiTechnicGyro, self).__init__(brick, sensor_port)
        self._available_modes = [self.GyroMode(self)]

    class GyroMode(Mode):
        pass


class HiTechnicCompass(Sensor):
    #TODO: Callibrate ? seems like a pain
    def __init__(self, brick, sensor_port):
        super(HiTechnicCompass, self).__init__(brick, sensor_port)
        self._available_modes = [self.CompassMode(self)]

    class CompassMode(Mode):
        pass


class HiTechnicIRSeeker(Sensor):
    def __init__(self, brick, sensor_port):
        super(HiTechnicIRSeeker, self).__init__(brick, sensor_port)
        self._available_modes = [self.UnmodulatedMode(self)]

    class UnmodulatedMode(Mode):
        pass

