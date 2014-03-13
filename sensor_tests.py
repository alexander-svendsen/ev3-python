# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)
#brick = ev3.find_brick_by_name('ev3', by_ip=False)

color_sensor = ev3.EV3ColorSensor(brick, 1)
print "opened color"
time.sleep(10)
# color_sensor.close()
touch_sensor = ev3.EV3TouchSensor(brick, 1)
print "opened touch"

print ev3.SENSOR_PORTS._fields
print ev3.SENSOR_PORTS.index(0)