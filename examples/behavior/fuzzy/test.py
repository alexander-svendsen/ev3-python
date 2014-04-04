# -*- coding: utf-8 -*-
from behavior.fuzzy import *


MIN_BLOCKING_DISTANCE = 0.0
MAX_BLOCKING_DISTANCE = 0.20

DISTANCE = 0.25  # in meters


class Forward(Behavior):
    def update(self):
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, DISTANCE), 'translate', 0.25)
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, DISTANCE), 'rotate', 0.0)


class AvoidColliding(Behavior):
    def update(self):
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, DISTANCE), 'translate', 0.0)
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, DISTANCE), 'rotate', -0.7)


class WheelMotor(Actuator):
    def action(self):
        print "{0} rotate = {1}".format(self.actuator, self.move)


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
        left_motor = WheelMotor("motor_A")
        right_motor = WheelMotor("motor_B")
        self.add_active_actuators(left_motor)
        self.add_active_actuators(right_motor)

        rotate = Rotate(left_motor, right_motor)
        translate = Translate(left_motor, right_motor)

        self.add_controller(rotate)
        self.add_controller(translate)

        self.add_behavior(Forward({'rotate': rotate, 'translate': translate}))
        self.add_behavior(AvoidColliding({'rotate': rotate, 'translate': translate}))

    def check(self):
        return True  # this state should never end


if __name__ == "__main__":
    wander = WanderState()
    if wander.update():
        wander.action()

