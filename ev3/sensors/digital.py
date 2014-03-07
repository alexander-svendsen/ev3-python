# -*- coding: utf-8 -*-
from common import Sensor, Mode


class EV3ColorSensor(Sensor):
    pass

# Review: How to do change mode?, set it in the command when fetch is called, or simply do a change mode command when
# changing


class HiTechnicColorSensor(Sensor):  # two modes, maybe must have inner classes to handle the different modes
    def __init__(self, brick, sensor_port):
        super(HiTechnicColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ColorIdMode(), self.RGBMode()]

    def get_color_id_mode(self):
        return self._available_modes[0]

    def get_rgb_mode(self):
        return self._available_modes[1]

    class ColorIdMode(Mode):
        def get_color_id(self):
            """
            Returns the color index detected by the sensor.
            @return:
            """
             # * <li> 0 = red
             # * <li> 1 = green
             # * <li> 2 = blue
             # * <li> 3 = yellow
             # * <li> 4 = magenta
             # * <li> 5 = orange
             # * <li> 6 = white
             # * <li> 7 = black
             # * <li> 8 = pink
             # * <li> 9 = gray
             # * <li> 10 = light gray
             # * <li> 11 = dark gray
             # * <li> 12 = cyan
            return self.fetch_sample() # TODO, use it correctly

        @staticmethod
        def get_name():
            return "ColorID"

        @staticmethod
        def get_sample_size():
            return 1

    class RGBMode(Mode):
        @staticmethod
        def get_name():
            return "RGB"

        @staticmethod
        def get_sample_size():
            return 3

        def get_color(self):
            pass