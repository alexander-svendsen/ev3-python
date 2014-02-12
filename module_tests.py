import ev3
from ev3 import Motor, MOTOR_PORTS

#TODO do something smart with the port
#ev3.connect_to_brick(ip='10.0.1.1', port=9200)

motor = Motor(None, MOTOR_PORTS.B)



