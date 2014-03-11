# -*- coding: utf-8 -*-
from common import Sensor, Mode
import NXTSensors


class EV3GyroSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(EV3GyroSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.RateMode(self), self.AngleMode(self)]

    def reset(self):
        self._call_sensor_control_method("reset")

    class AngleMode(Mode):
        pass

    class RateMode(Mode):
        pass


class EV3ColorSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(EV3ColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ColorIDMode(self), self.RedMode(self), self.RGBMode(self), self.AmbientMode(self)]

    class ColorIDMode(Mode):
        """
        Mode that measure the color on the source and categorize the result
        """
        colorDict = {1: 'black', 2: 'blue', 3: 'green', 4: 'yellow', 5: 'red', 6: 'white', 7: 'brown'}

        def get_color_specter(self):
            return self.colorDict.values()

        def get_color_id(self):
            return self.colorDict.get(self.fetch_sample()[0], 'none')

    class RedMode(Mode):
        """
        Mode that measured the light value of the source when illuminated with a red light source
        """
        pass

    class RGBMode(Mode):
        """
        Mode that measures the color RGB of the source when illuminated the RGB light
        """

        def get_color(self):
            return tuple(int(i) for i in self.fetch_sample())

        @staticmethod
        def get_sample_size():
            return 3

    class AmbientMode(Mode):
        """
        Mode that measures the light value of the source without being illuminated
        """
        pass


class EV3UltrasonicSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(EV3UltrasonicSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.DistanceMode(self), self.ListenMode(self)]

    def enable(self):
        self._call_sensor_control_method("enable")

    def disable(self):
        self._call_sensor_control_method("disable")

    class DistanceMode(Mode):  #Review -1 means infinety
        pass

    class ListenMode(Mode):
        pass


class EV3TouchSensor(NXTSensors.NXTTouchSensor):
    pass