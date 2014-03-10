# -*- coding: utf-8 -*-
import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)
#brick = ev3.find_brick_by_name('ev3', by_ip=False)

color = ev3.HiTechnicColorSensor(brick, 1)

color_id = color.get_color_id_mode()
print color_id.fetch_sample()


rgb_mode = color.get_rgb_mode()
print rgb_mode.fetch_sample()
print rgb_mode.get_color()

time.sleep(5)
print "Good Night"