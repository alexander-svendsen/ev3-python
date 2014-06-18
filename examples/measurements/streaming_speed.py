# -*- coding: utf-8 -*-
import time
import measure
import ev3
import threading

print "setup"
brick = ev3.connect_to_brick(address='10.0.1.1')
ultrasonic_1 = ev3.EV3UltrasonicSensor(brick, 1)
# touch = ev3.EV3TouchSensor(brick, 2)
# gyro = ev3.EV3GyroSensor(brick, 3)
# ultrasonic_2 = ev3.EV3UltrasonicSensor(brick, 4)


class Timer:
    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.prev_time = 0.0
        self.timer = 0
        self.running = True
        self.sub = ev3.Subscription(subscribe_on_sensor_changes=False, subscribe_on_sample_data=True)
        brick.set_subscription(self.sub)

    def new_sample(self, samples):
        self.timer += 1
        if self.timer > 10000:
            self.stop()

    def stop(self):
        self.end = time.time()
        self.running = False

    def run(self):
        print "starting"
        self.start = time.time()
        self.sub.subscribe_on_samples(self.new_sample)
        while self.running:
            time.sleep(1)
        print "end, took", self.end - self.start


print "Starting"
timer = Timer()
m = measure.Measure()
thread =threading.Thread(name="receive_thread", target=m.start_measurement, args=(1,))
thread.daemon = True
thread.start()
timer.run()

print "complete"
