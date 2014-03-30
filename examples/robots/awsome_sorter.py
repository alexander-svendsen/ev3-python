# -*- coding: utf-8 -*-
import itertools
import ev3
from ev3 import SENSOR_PORTS, MOTOR_PORTS
import time


class AwesomeSorter():
    def __init__(self, ip, port):
        self._brick = ev3.connect_to_brick(ip, port)
        self._belt_motor = ev3.Motor(self._brick, MOTOR_PORTS.PORT_D)
        self._throw_out_motor = ev3.Motor(self._brick, MOTOR_PORTS.PORT_A)
        self._throw_out_motor.set_speed(640)
        self._throw_out_motor.rotate(180, True)

        ev3_color_sensor = ev3.EV3ColorSensor(self._brick, SENSOR_PORTS.PORT_3)
        ev3_touch_sensor = ev3.EV3TouchSensor(self._brick, SENSOR_PORTS.PORT_1)

        self._color = ev3_color_sensor.get_color_id_mode()
        self._touch = ev3_touch_sensor.get_touch_mode()

        self._movement = {
            'blue': 0,
            'green': 200,
            'yellow': 350,
            'red': 550,
        }
        self._position = 0

    def move_to_color(self, color):
        movement = self._movement[color] - self._position
        self._position = self._movement[color]
        if movement:  # no point sending a command if there isn't anying to send
            self._belt_motor.rotate(movement)

    def move_belt_to_start_position(self):
        self._belt_motor.backward()
        while not self._touch.is_pressed():
            pass
        self._belt_motor.stop()
        self._belt_motor.rotate(30)  # move a little away from the touch sensor

    def throw_a_lego_piece_out(self, quick_mode=True):
        self._throw_out_motor.rotate(-180)
        self._throw_out_motor.rotate(180, quick_mode)

    def scan_for_valid_lego_piece(self):
        color = self._color.get_color_id()
        while color not in self._movement:
            color = self._color.get_color_id()
        return color

    def run_sorter(self):
        # first we need to scan in all the lego pieces
        self._brick.beep()
        color_list = []
        for _ in xrange(8):
            color = self.scan_for_valid_lego_piece()
            color_list.append(color)

            self._brick.beep()
            print "Read complete:", color
            time.sleep(1)  # wait a second between each time

        self._brick.beep()
        self._brick.beep()
        time.sleep(2)

        self.move_belt_to_start_position()

        peeper, color_iterator = itertools.tee(color_list)
        peeper.next()
        peek = peeper.next()
        for color in color_iterator:
            self.move_to_color(color)
            if color == peek:
                self.throw_a_lego_piece_out(quick_mode=False)
            else:
                self.throw_a_lego_piece_out()

            try:
                peek = peeper.next()
            except StopIteration:
                peek = None
        self._brick.buzz()
        self._throw_out_motor.rotate(-180)
        print "complete!"

if __name__ == "__main__":
    print "Initialize the sorter"
    sorter = AwesomeSorter('10.0.1.1', 9200)
    print "Sorter is starting"
    sorter.run_sorter()
