# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

accel_sensor = ev3.HiTechnicAccelerometer(brick, 1)

accel = accel_sensor.get_acceleration_mode()

for _ in range(0, 4):
    time.sleep(2)
    print accel.fetch_sample()