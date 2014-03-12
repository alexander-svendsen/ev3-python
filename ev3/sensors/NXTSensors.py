# -*- coding: utf-8 -*-
from common import Sensor, Mode


class NXTTouchSensor(Sensor):
    """
    Class for the Lego NXT Touch Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has one mode, touch mode.
        """
        super(NXTTouchSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.TouchMode(self)]

    def get_touch_mode(self):
        """
        @rtype: TouchMode
        """
        return self.get_mode("Touch")

    class TouchMode(Mode):
        """
        Mode that measures whether the sensor is pressed or not
        """
        def is_pressed(self):
            return bool(self.fetch_sample()[0])


class NXTUltrasonicSensor(Sensor):
    """
    Class for the Lego NXT Ultrasonic Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, Continuous and Ping mode .
        """
        super(NXTUltrasonicSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ContinuousMode(self), self.PingMode(self)]

    def get_continuous_mode(self):
        """
        @rtype: ContinuousMode
        """
        return self.get_mode("Continuous")

    def get_ping_mode(self):
        """
        @rtype: PingMode
        """
        return self.get_mode("Ping")

    #Real name distance, but since it's not really representative we use its class name
    class ContinuousMode(Mode):
        """
        Mode that periodically scans the surrounding and measure the distance to the nearest object. Caches this data
        and returns it when the data get fetched.
        The theoretical range of the sensor is 0,04 to 2.54 meter
        A distance of a negative value means it didn't find any obstacle in front of it.
        """
        pass

    #Real name distances, but since it's not really representative we use its class name
    class PingMode(Mode):
        """
        Mode that scans the surrounding area when fetching data and returns the distance to the eight nearest object.
        The theoretical range of the sensor is 0,04 to 2.54 meter.
        A distance of a negative value means it didn't find any obstacle in front of it.
        This mode takes longer then ContinuousMode (~70ms while ContinuousMode uses ~30ms)
        """
        @staticmethod
        def get_sample_size():
            return 8


class NXTLightSensor(Sensor):
    """
    Class for the Lego Light Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, Red and Ambient mode.
        """
        super(NXTLightSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.RedMode(self), self.AmbientMode(self)]

    def get_red_mode(self):
        """
        @rtype: ColorIDMode
        """
        return self.get_mode("Red")

    def get_ambient_mode(self):
        """
        @rtype: AmbientMode
        """
        return self.get_mode("Ambient")

    #Strangly enough the real name is set to "None". Since that don't make any sence we use the class name
    class AmbientMode(Mode):
        """
        Mode that measures the light value of the source without being illuminated
        """
        pass

    class RedMode(Mode):
        """
        Mode that measures the light value of the source when illuminated with a red light
        """
        pass


class NXTSoundSensor(Sensor):
    """
    Class for the Lego Sound Sensor.
    """
    def __init__(self, brick, sensor_port):
        """
        This sensor has two modes, DB and DBA mode.
        """
        super(NXTSoundSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.DBMode(self), self.DBAMode(self)]

    def get_db_mode(self):
        """
        @rtype: DBMode
        """
        return self.get_mode("DB")

    def get_dba_mode(self):
        """
        @rtype: DBAMode
        """
        return self.get_mode("DBA")

    #Strangly enough the real names is set unlogical. Since that don't make any sence we use the class name
    class DBMode(Mode):
        """
        Mode that measures sound in decibel (DB)
        """
        pass

    class DBAMode(Mode):
        """
        Mode that measures sound pressure level (DBA)
        """
        pass


