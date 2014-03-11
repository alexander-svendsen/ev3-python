# -*- coding: utf-8 -*-
from common import Sensor, Mode


class NXTTouchSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(NXTTouchSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.TouchMode(self)]

    class TouchMode(Mode):
        def is_pressed(self):
            return bool(self.fetch_sample()[0])


class NXTUltrasonicSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(NXTUltrasonicSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.ContinuousMode(self), self.PingMode(self)]

    #Real name distance, but since it's not really representative we use its class name
    class ContinuousMode(Mode):
        pass

    #Real name distances, but since it's not really representative we use its class name
    class PingMode(Mode):
        @staticmethod
        def get_sample_size():
            return 8


class NXTLightSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(NXTLightSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.RedMode(self), self.AmbientMode(self)]

    #Strangly enough the real name is set to "None". Since that don't make any sence we use the class name
    class AmbientMode(Mode):
        pass

    class RedMode(Mode):
        pass


class NXTSoundSensor(Sensor):
    def __init__(self, brick, sensor_port):
        super(NXTSoundSensor, self).__init__(brick, sensor_port)
        self._available_modes = [self.DBMode(self), self.DBAMode(self)]

    #Strangly enough the real names is set unlogical. Since that don't make any sence we use the class name
    class DBMode(Mode):
        pass

    class DBAMode(Mode):
        pass


