# -*- coding: utf-8 -*-
from behavior.fuzzy import *
import ev3
import sys
MIN_BLOCKING_DISTANCE = 0.0
MAX_BLOCKING_DISTANCE = 0.30

BRICK = ev3.connect_to_brick('10.0.1.1')
distance = ev3.EV3UltrasonicSensor(BRICK, 1).get_distance_mode()
CACHE = 0
COUNTER = 0


def get_distance(counter=COUNTER, cache=CACHE):
    if counter == 0:
        cache = distance.fetch_sample()[0]
        counter = 2
    counter -= 1
    return cache


class Forward(Behavior):
    def update(self):
        meter = get_distance()
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'translate', 90)
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'rotate', 0.0)


class AvoidColliding(Behavior):
    def update(self):
        meter = get_distance()
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'translate', 0.0)
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'rotate', 600)


class RightMotor(Actuator):
    def action(self):
        print "rotate right motor by = {0}".format(self.move)
        self.actuator.rotate(self.move, True)


class LeftWheelMotor(Actuator):
    def action(self):
        print "rotate left motor by = {0}".format(self.move)
        self.actuator.rotate(self.move, False)  # only do this to make a synchronous fashion like this


class Rotate(Controller):
    def __init__(self, left, right):
        super(Rotate, self).__init__()
        self.left = left
        self.right = right
        self.actuators = [left, right]

    def update_actuators(self):
        print "Rotate effect: ", self.move
        self.right.update(self.move)
        self.left.update(-self.move)


class Translate(Rotate):
    def update_actuators(self):
        print "Translate effect: ", self.move
        self.right.update(self.move)
        self.left.update(self.move)


class WanderState(State):
    def setup(self):
        right_motor = RightMotor(ev3.Motor(BRICK, "A"))
        left_motor = LeftWheelMotor(ev3.Motor(BRICK, "D"))
        self.add_active_actuators(right_motor)
        self.add_active_actuators(left_motor)

        rotate = Rotate(left_motor, right_motor)
        translate = Translate(left_motor, right_motor)

        self.add_controller(rotate)
        self.add_controller(translate)

        self.add_behavior(Forward({'rotate': rotate, 'translate': translate}))
        self.add_behavior(AvoidColliding({'rotate': rotate, 'translate': translate}))

    def check(self):
        return True  # this state should never end


if __name__ == "__main__":
    BRICK.buzz()
    wander = WanderState()
    while wander.update():
        wander.action()

