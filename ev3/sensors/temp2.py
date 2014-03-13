# -*- coding: utf-8 -*-
import temp1
import common
from common import Sensor, Mode


class EV3GyroSensor(Sensor):
    """
    Class for the Lego EV3 Gyro sensor.
    When the sensor changes between the modes it resets, therefor it should be motionless during this operation
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, RateMode and AngleMode
        """
        super(EV3GyroSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.RateMode(self), self.AngleMode(self)]

    def get_rate_mode(self):
        """
        @rtype: RateMode
        """
        return self.get_mode("Rate")

    def get_angle_mode(self):
        """
        @rtype: AngleMode
        """
        return self.get_mode("Angle")

    def reset(self):
        """
        Resets the sensor. In other words the initial position is set to the current position when this method gets
        called
        """
        self._call_sensor_control_method("reset")

    class AngleMode(Mode):
        """
        Mode for measuring the current angle from the starting position. A positive value indicates a orientation to
        the left and vice versa.
        """
        pass

    class RateMode(Mode):
        """
        Mode for measuring the speed of rotation expressed in degrees/second. A positive value indicates a
        counterclockwise rotation and vice versa
        """
        pass


class EV3ColorSensor(Sensor):
    """
    Class for the Lego EV3 Color sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has four modes, ColorID, Red, RGB and Ambient mode.
        """
        super(EV3ColorSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ColorIDMode(self), self.RedMode(self), self.RGBMode(self), self.AmbientMode(self)]

    def get_color_id_mode(self):
        """
        @rtype: ColorIDMode
        """
        return self.get_mode("ColorID")

    def get_red_mode(self):
        """
        @rtype: ColorIDMode
        """
        return self.get_mode("Red")

    def get_rgb_mode(self):
        """
        @rtype: RGBMode
        """
        return self.get_mode("RGB")

    def get_ambient_mode(self):
        """
        @rtype: AmbientMode
        """
        return self.get_mode("Ambient")

    class ColorIDMode(Mode):
        """
        Mode that measure the color on the source and categorize the result
        """
        colorDict = common.COLOR_DICT

        def get_color_id(self):
            """
            Takes the raw data sample and returns the categorized color value, ie red/blue/etc
            @return: Returns the measured color value
            @rtype: str
            """
            return self.colorDict.get(self.fetch_sample()[0], 'none')

    class RedMode(Mode):
        """
        Mode that measured the light value of the source when illuminated with a red light
        """
        pass

    class RGBMode(Mode):
        """
        Mode that measures the color RGB of the source when illuminated with white light
        """
        def get_color_tuple(self):
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
    """
    Class for the Lego EV3 Ultrasonic sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, Distance and Listen mode.
        """
        super(EV3UltrasonicSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.DistanceMode(self), self.ListenMode(self)]

    def enable(self):
        """
        Enables the sensor, turn on the sensor lights.
        It gets enabled by it self when measuring data, so there is no point to use this method for the functionality,
        but you can use it to be able to blink the sensor lights.
        """
        self._call_sensor_control_method("enable")

    def disable(self):
        """
        Disables the sensor, turn of the sensor lights.
        No point to use it, since the sensor enables itself each time it measures, but you can use this functionality
        to make the sensor blink it lights.
        """
        self._call_sensor_control_method("disable")

    def get_distance_mode(self):
        """
        @rtype: DistanceMode
        """
        return self.get_mode("Distance")

    def get_listen_mode(self):
        """
        @rtype: ListenMode
        """
        return self.get_mode("Listen")

    class DistanceMode(Mode):
        """
        Mode that measures the distance to the closest object in centimeters.
        Accuracy +/- 1 centimeter.
        Max distance is 250 centimeter
        A distance of a negative value means it didn't find any obsticales in fron of it.
        """
        pass

    class ListenMode(Mode):
        """
        Mode that listens for other ultrasonic waves nearby.
        Lack of documentation leads me to believe this mode is not complete yet, but i think it measures distance to the
        other ultrasonic source.
        """
        pass


class EV3TouchSensor(temp1.NXTTouchSensor):
    """
    Class for the Lego EV3 Touch sensor.
    """
    pass