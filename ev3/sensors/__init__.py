# -*- coding: utf-8 -*-

from .common import *
from .analog import *
from .digital import *


def get_sensor_type_at(brick, sensor_port):
    if sensor_port in brick.get_opened_ports:
        return brick.get_opened_ports[sensor_port].get_name()
    cmd = {"cla": "sensor", "cmd": "get_sensor_type", "sensor_port": sensor_port - 1}
    data = brick.send_command(cmd)
    return data["sample_string"]