# -*- coding: utf-8 -*-
from common import Sensor, Mode


class EV3ColorSensor(Sensor):
    pass

# Review: How to do change mode?, set it in the command when fetch is called, or simply do a change mode command when
# changing


class HiTechnicColorSensor(Sensor):  # two modes, maybe must have inner classes to handle the different modes
    def __init__(self, brick, sensor_port):
        super(HiTechnicColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ColorIdMode(self), self.RGBMode(self)]

    def get_color_id_mode(self):
        """
        Return the color id mode. A mode where colors are categorized for you.
        @return: color id mode
        @rtype: ColorIdMode
        """
        return self.get_mode(0)

    def get_rgb_mode(self):
        """
        Return the rgb mode. Where data is returned as a rgb value
        @return: rgb mode
        @rtype: RGBMode
        """
        return self.get_mode(1)

    class ColorIdMode(Mode):
        colorDict = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow', 4: 'magenta', 5: 'orange', 6: 'white', 7: 'black',
                     8: 'pink', 9: 'gray', 10: 'light gray', 11: 'dark gray', 12: 'cyan'}

        def get_color_specter(self):
            return self.colorDict.values()

        def get_color_id(self):
            return self.colorDict[self.fetch_sample()[0]]

        @staticmethod
        def get_name():
            return "ColorID"

        @staticmethod
        def get_sample_size():
            return 1

    class RGBMode(Mode):

        def get_color(self):
            return tuple(int(i) for i in self.fetch_sample())

        @staticmethod
        def get_name():
            return "RGB"

        @staticmethod
        def get_sample_size():
            return 3
