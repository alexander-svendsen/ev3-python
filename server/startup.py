# -*- coding: utf-8 -*-
import ev3
import time

start = 0.0
end = 0.0

def test(samples):
    global end
    global start
    end = time.time()
    print samples
    print "took: ", end - start
    start = time.time()


def main():
    brick = ev3.connect_to_brick('10.0.1.1')
    ultrasonic = ev3.EV3UltrasonicSensor(brick, 1)
    sub = ev3.Subscription(False)
    global start


    sub.subscribe_on_samples(test)
    start = time.time()
    brick.set_subscription(sub)
