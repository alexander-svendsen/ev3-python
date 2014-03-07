# -*- coding: utf-8 -*-



import ev3,time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)
#brick = ev3.find_brick_by_name('ev3', by_ip=False)

color = ev3.HiTechnicColorSensor(brick, 1)

print color.get_selected_mode_name()

time.sleep(5)
print "Good Night"