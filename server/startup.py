# -*- coding: utf-8 -*-
import ev3


def main():
    brick = ev3.connect_to_brick('10.0.1.1')
    ultrasonic = ev3.EV3ColorSensor(brick, 3)