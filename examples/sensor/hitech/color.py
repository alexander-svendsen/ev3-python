# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)

color_sensor = ev3.HiTechnicColorSensor(brick, 1)

colorid = color_sensor.get_color_id_mode()

for _ in range(0, 4):
    time.sleep(2)
    print colorid.get_color_id()