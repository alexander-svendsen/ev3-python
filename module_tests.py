import ev3
from ev3 import Motor, MOTOR_PORTS

import time
import sys

#TODO do something smart with the port
brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)
#brick = ev3.find_brick_by_name('ev3', by_ip=False)

a = Motor(brick, 'A')
b = Motor(brick, 'B')

time.sleep(4)
sys.exit(1)
# print "testing forward a"
# a.forward()
#
# print "testing forward b"
# b.forward()
#
#
# print "Moving?", a.is_moving(), b.is_moving()
#
# time.sleep(5)
# print "stopping both"
# b.stop()
# a.stop()

print "Moving?", a.is_moving(), b.is_moving()
print a.get_position(), b.get_position()

#)
# max = a.get_max_speed()
# print "Max", a.get_max_speed(), b.get_max_speed()
# print "Pos", a.get_position(), b.get_position()
# print "Tacho", a.get_tacho_count(), b.get_tacho_count()


# print "Stalled?", a.is_stalled(), b.is_stalled()
# a.set_speed(800)
# b.set_speed(800)


print "testing forward a"
a.forward()

print "testing forward b"
b.forward()

time.sleep(5)
print "stopping both"
b.stop()
a.stop()
time.sleep(5)
print a.get_position(), b.get_position()
# motor.forward()
# motor.rotate(360, True)

# time.sleep(5)
# motor.rotate(360, True)
# time.sleep(5)

