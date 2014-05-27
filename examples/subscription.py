# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')
color_sensor = ev3.EV3ColorSensor(brick, 1)


def print_samples(samples):
    print samples

sub = ev3.Subscription(subscribe_on_sensor_changes=False, subscribe_on_sample_data=True)
sub.subscribe_on_samples(print_samples)

brick.set_subscription(sub)
time.sleep(4) # let it run some
