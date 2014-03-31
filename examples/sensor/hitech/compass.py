# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

compass_sensor = ev3.HiTechnicCompass(brick, 1)

heading = compass_sensor.get_compass_mode()

for _ in range(0, 4):
    time.sleep(2)
    print heading.fetch_sample()