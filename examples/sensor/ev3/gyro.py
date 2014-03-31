# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

gyro = ev3.EV3GyroSensor(brick, 1)
angle = gyro.get_mode("Angle")

print "Angle 1:", angle.fetch_sample()
time.sleep(5)

print "Angle 2:", angle.fetch_sample()
time.sleep(5)

print "RESET"
gyro.reset()
time.sleep(5)

print "Angle 1:", angle.fetch_sample()
time.sleep(5)

print "Angle 2:", angle.fetch_sample()


rate = gyro.get_mode("Rate")

print "Rate 1:", rate.fetch_sample()
time.sleep(5)

print "Rate 2:", rate.fetch_sample()
time.sleep(5)

print "RESET"
gyro.reset()
time.sleep(5)

print "Rate 1:", rate.fetch_sample()
time.sleep(5)

print "Rate 2:", rate.fetch_sample()


