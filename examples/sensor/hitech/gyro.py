# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)

gyro_sensor = ev3.HiTechnicGyro(brick, 1)

gyro_mode = gyro_sensor.get_gyro_mode()

for _ in range(0, 4):
    time.sleep(2)
    print gyro_mode.fetch_sample()