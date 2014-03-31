# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

ultra = ev3.NXTUltrasonicSensor(brick, 1)

contiounus = ultra.get_continuous_mode()
print contiounus.fetch_sample()

ping = ultra.get_ping_mode()
print ping.fetch_sample()