# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

color_sensor = ev3.EV3ColorSensor(brick, 1)

colorid = color_sensor.get_selected_mode()

for _ in range(0, 4):
    time.sleep(2)
    print colorid.get_color_id()