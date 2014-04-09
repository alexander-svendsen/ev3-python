# -*- coding: utf-8 -*-

# import manager
import ev3
import time

#When a bricks has been connected, the server should be active
ev3.connect_to_brick('10.0.1.1')

print "The End"
time.sleep(10)  # server should be up until this is complete
