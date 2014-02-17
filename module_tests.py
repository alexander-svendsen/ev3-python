import ev3
from ev3 import Motor, MotorPorts

import time

#TODO do something smart with the port
brick = ev3.connect_to_brick(ip='10.0.1.1', port=9200)
a = Motor(brick, 'A')
b = Motor(brick, 'B')

print "testing forward a"
a.forward()

print "testing forward b"
b.forward()


print "Moving?", a.is_moving(), b.is_moving()

time.sleep(5)
print "stopping both"
b.stop()
a.stop()

print "Moving?", a.is_moving(), b.is_moving()

max = a.get_max_speed()
print "Max", a.get_max_speed(), b.get_max_speed()
print "Pos", a.get_position(), b.get_position()
print "Tacho", a.get_tacho_count(), b.get_tacho_count()


print "Stalled?", a.is_stalled(), b.is_stalled()
a.set_speed(850)
b.set_speed(800)


print "testing forward a"
a.forward()

print "testing forward b"
b.forward()

time.sleep(5)
print "stopping both"
b.stop()
a.stop()

# motor.forward()
# motor.rotate(360, True)

# time.sleep(5)
# motor.rotate(360, True)
# time.sleep(5)

