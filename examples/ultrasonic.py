# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)

ultra = ev3.EV3UltrasonicSensor(brick, 1)
distance = ultra.get_mode(0)


print distance.fetch_sample()


listen = ultra.get_mode(1)

print listen.fetch_sample()
print listen.get_name()
print listen.get_sample_size()