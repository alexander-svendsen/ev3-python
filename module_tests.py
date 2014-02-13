import ev3
from ev3 import Motor, MOTOR_PORTS

import time

#TODO do something smart with the port
brick = ev3.connect_to_brick(ip='10.0.1.1', port=9200)
motor = Motor(brick, MOTOR_PORTS.A)

time.sleep(5)
print "testing forward"
motor.forward()


time.sleep(15)

print "stopping motors"
motor.stop()


time.sleep(15)
print "testing forward"
motor.forward()
time.sleep(5)
print "stopping motors"
motor.stop()

print "everything ok?"
time.sleep(60)



