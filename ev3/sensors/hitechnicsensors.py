# -*- coding: utf-8 -*-
import common
from common import Sensor, Mode


class HiTechnicColorSensor(Sensor):
    """
    Class for the HiTechnic NXT Color Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, ColorID, and RGB mode.
        """
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

    class RGBMode(Mode):
        """
        Mode that measures the color RGB of the source when illuminated with white light
        """
        def get_color_tuple(self):
            return tuple(int(i) for i in self.fetch_sample())

        @staticmethod
        def get_sample_size():
            return 3


class HiTechnicAccelerometer(Sensor):
    """
    Class for the HiTechnic NXT Accelerometer/Tilt Sensor.
    Measures acceleration in three axes, x, y and z.
    Measures the range -2g to +2g.
    Can be used for tilt measuring since gravity is distributed among the three components.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has one mode, Acceleration mode.
        """
        super(HiTechnicAccelerometer, self).__init__(brick, sensor_port)
        self._available_modes = [self.AccelerationMode(self)]

    def get_acceleration_mode(self):
        """
        @rtype: AccelerationMode
        """
        return self.get_mode("Acceleration")

    class AccelerationMode(Mode):
        """
        Mode for measuring the acceleration
        """
        @staticmethod
        def get_sample_size():
            return 3


class HiTechnicGyro(Sensor):
    """
    Class for the HiTechnic NXT Gyro Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has one mode, Gyro mode
        """
        super(HiTechnicGyro, self).__init__(brick, sensor_port)
        self._available_modes = [self.GyroMode(self)]

    def get_gyro_mode(self):
        """
        @rtype: GyroMode
        """
        return self.get_mode("Gyro")

    class GyroMode(Mode):
        """
        Measures the number of degrees per second of rotation as well as indicating the direction of rotation
        A positive rate indicates a counterclockwise rotation. A negative rate indicates a clockwise rotation.
        """
        pass


class HiTechnicCompass(Sensor):
    """
    Class for the HiTechnic NXT Compass Sensor.
    """
    def __init__(self, brick, sensor_port):
        super(HiTechnicCompass, self).__init__(brick, sensor_port)
        self._available_modes = [self.CompassMode(self)]

    def get_compass_mode(self):
        """
        @rtype: CompassMode
        """
        return self.get_mode("Compass")

    #See in the documentation from the manufacturer that the calibration is actually a separate mode.
    #In theory it should have been implemented as much.
    def start_calibration(self):
        """
        Start calibrating the sensor, to compensate for externally generated magnetic field, ie battery, motors, etc.
        Must rotate the sensor slowly 20 seconds per rotation, taking about 1.5 to 2 full rotations before stopping.
        Must call end_callibration when done
        """
        self._call_sensor_control_method("startCalibration")

    def end_calibration(self):
        """
        Ends the calibration.
        """
        self._call_sensor_control_method("stopCalibration")

    class CompassMode(Mode):
        """
        Measures the earth's magnetic field and outputs a value representing the current heading.
        Calulated in the nearest 1 degrees and returned as a value from 0 to 359.
        """
        pass


class HiTechnicIRSeeker(Sensor):
    """
    Class for the HiTechnic NXT IR Seeker v1.0 Sensor.
    Meant to be used with a Lego power functions IR remote control. Can in theory control the lego program with this
    controller.
    Don't have it, so can't test this
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor only got one mode, Unmodulated mode
        """
        super(HiTechnicIRSeeker, self).__init__(brick, sensor_port)
        self._available_modes = [self.UnmodulatedMode(self)]

    def get_unmodulated_mode(self):
        """
        @rtype: UnmodulatedMode
        """
        return self.get_mode("Unmodulated")

    class UnmodulatedMode(Mode):
        pass

