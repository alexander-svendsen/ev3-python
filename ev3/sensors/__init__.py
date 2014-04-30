# -*- coding: utf-8 -*-

from .common import SENSOR_PORTS, Mode, Sensor
from .analog import *
from .digital import *


def get_sensor_type_at(brick, sensor_port):
    """
    Returns the connected sensor name at the specified brick and port. Do note sometimes it's impossible to determine
    and only a more general categorization will be returned. This applies to sensors such as most analog sensors, where
    the name in most cases will be 'AnalogSensor'

    @param brick: The brick where you wish to know what sensor is connected
    @param sensor_port: What sensor port do you want to know what is connected
    @return: name of the connected sensor, if any.
    @rtype: str
    """
    if sensor_port in brick.get_opened_ports:
        return brick.get_opened_ports[sensor_port].get_name()
    cmd = {"cla": "sensor", "cmd": "get_sensor_type", "sensor_port": sensor_port - 1}
    data = brick.send_command(cmd)
    return data["sample_string"]