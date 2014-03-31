# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

touch_sensor = ev3.EV3TouchSensor(brick, 1)
touch = touch_sensor.get_mode(0)

print touch.fetch_sample()