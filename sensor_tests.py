# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)
#brick = ev3.find_brick_by_name('ev3', by_ip=False)

# start = time.time()
# ev3ColorSensor = ev3.EV3ColorSensor(brick, 1)
# end = time.time()
# print "Opening a sensor took:", end - start
#
#
# color_id = ev3ColorSensor.get_selected_mode()
#
# start = time.time()
# print color_id.get_color_id()
# end = time.time()
# print "Measurement took1:", end - start
#
#
# start = time.time()
# print color_id.get_color_id()
# end = time.time()
# print "Measurement took2:", end - start
#
#
#
# start = time.time()
# print color_id.get_color_id()
# end = time.time()
# print "Measurement took2:", end - start
#
# time.sleep(5)
# print "Good Night"



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

