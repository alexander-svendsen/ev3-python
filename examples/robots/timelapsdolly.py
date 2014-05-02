# -*- coding: utf-8 -*-
import ev3
import time


class TimeLapsDolly(object):
    def __init__(self, connected_brick):
        self.brick = connected_brick
        self.motor = ev3.Motor(connected_brick, ev3.MOTOR_PORTS.PORT_A)
        self.touch = ev3.EV3TouchSensor(connected_brick, ev3.SENSOR_PORTS.PORT_1).get_touch_mode()
        self.motor.set_speed(1200)

        self.initialize_position()
        self.pos = 0
        self.max_pos = -31000

    def initialize_position(self):
        self.motor.forward()
        while not self.touch.is_pressed():
            pass
        self.motor.stop()

    def go_to_end(self):
        self.motor.rotate(self.max_pos)

    def go_forward(self, degrees):
        self.pos += degrees
        self.motor.rotate(degrees)

    def is_it_at_the_end(self, pos=0):
        return (self.pos + pos) >= self.max_pos


if __name__ == "__main__":
    brick = ev3.connect_to_brick('10.0.1.1')
    timelaps = TimeLapsDolly(brick)
    # timelaps.go_to_end()
    while True:
        time.sleep(1)
        timelaps.go_forward(-45)
