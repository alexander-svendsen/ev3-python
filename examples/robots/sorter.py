# -*- coding: utf-8 -*-
import ev3
from ev3 import SENSOR_PORTS, MOTOR_PORTS
import time


class Sorter():
    def __init__(self, ip, port):
        self.brick = ev3.connect_to_brick(ip, port)
        self.belt_motor = ev3.Motor(self.brick, MOTOR_PORTS.PORT_D)
        self.throw_out_motor = ev3.Motor(self.brick, MOTOR_PORTS.PORT_A)
        self.throw_out_motor.set_speed(640)

        ev3_color_sensor = ev3.EV3ColorSensor(self.brick, SENSOR_PORTS.PORT_3)
        ev3_touch_sensor = ev3.EV3TouchSensor(self.brick, SENSOR_PORTS.PORT_1)

        self.color = ev3_color_sensor.get_color_id_mode()
        self.touch = ev3_touch_sensor.get_touch_mode()

        self.color_movement = {
            'blue': self.move_to_blue_position,
            'green': self.move_to_green_position,
            'yellow': self.move_to_yellow_position,
            'red': self.move_to_red_position
        }

    def move_to_blue_position(self):
        self.belt_motor.rotate(0)

    def move_to_green_position(self):
        self.belt_motor.rotate(200)

    def move_to_yellow_position(self):
        self.belt_motor.rotate(350)

    def move_to_red_position(self):
        self.belt_motor.rotate(550)

    def move_belt_to_start_position(self):
        self.belt_motor.backward()
        while not self.touch.is_pressed():
            pass
        self.belt_motor.stop()
        self.belt_motor.rotate(30)  # move a little away from the touch sensor

    def throw_a_lego_piece_out(self):  # the lego piece should be at the start position, as in the manual.
        self.throw_out_motor.rotate(180)
        self.throw_out_motor.rotate(-180)

    def move_to_color_position(self, color):
        self.color_movement[color]()

    def scan_for_valid_lego_piece(self):
        color = self.color.get_color_id()
        while color not in self.color_movement:
            color = self.color.get_color_id()
        return color

    def run_sorter(self):
        # first we need to scan in all the lego pieces
        self.brick.beep()
        color_list = []
        for _ in xrange(8):
            color = self.scan_for_valid_lego_piece()
            color_list.append(color)

            self.brick.beep()
            print "Read complete:", color
            time.sleep(1)  # wait a second between each time

        self.brick.beep()
        self.brick.beep()
        time.sleep(2)

        for color in color_list:
            self.move_belt_to_start_position()
            self.color_movement[color]()
            self.throw_a_lego_piece_out()

        self.brick.buzz()

        print "complete!"

if __name__ == "__main__":
    print "Initialize the sorter"
    sorter = Sorter('10.0.1.1', 9200)
    print "Sorter is starting"
    sorter.run_sorter()

