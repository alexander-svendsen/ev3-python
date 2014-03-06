# -*- coding: utf-8 -*-
from common import Sensor, MODE_TUPLE

#HOW to do modes..... Analog sensors only have a single mode and its already activated.
# The digital on the other hand don't and it can be many, but these must be activated, and stored on the Java side.
    # Just do it on the python side, or already have these things activated on hte


class NXTTouchSensor(Sensor):
    def __init__(self, brick, sensor_port):
        Sensor.__init__(self, brick, sensor_port)
        self._available_modes = [MODE_TUPLE("Touch", 1)]

    def is_pressed(self):
        return bool(int(self.fetch_sample()))


# Exactly the same as NXT, other then EV3 tells who it is
class EV3TouchSensor(NXTTouchSensor):
    def __init__(self, brick, sensor_port):
        NXTTouchSensor.__init__(self, brick, sensor_port)

