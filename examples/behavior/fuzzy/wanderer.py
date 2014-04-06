# -*- coding: utf-8 -*-
import time
from behavior.fuzzy import *
import ev3

MIN_BLOCKING_DISTANCE = 0.20
MAX_BLOCKING_DISTANCE = 0.50

BRICK = ev3.connect_to_brick('10.0.1.1')
distance = ev3.EV3UltrasonicSensor(BRICK, 1).get_distance_mode()


class Cache(object):
    def __init__(self):
        self.value = 0
        self.counter = 0

    def get_distance(self):
        if self.counter <= 0:
            self.value = distance.fetch_sample()[0]
            self.counter = 2
        self.counter -= 1
        if self.value <= -1:  # means infinity, setting it to a high value
            self.value = 1

        return self.value

cache = Cache()


class Forward(Behavior):
    def update(self):
        meter = cache.get_distance()
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'translate', 350)
        self.fuzzy_if(rising_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'rotate', 0)


class AvoidColliding(Behavior):
    def update(self):
        meter = cache.get_distance()
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'translate', 0)
        self.fuzzy_if(falling_fuzzy(MIN_BLOCKING_DISTANCE, MAX_BLOCKING_DISTANCE, meter), 'rotate', 5)


class BigMotor(Actuator):
    def __init__(self, actuator):
        super(BigMotor, self).__init__(actuator)
        self.old_move = 350

    def action(self):
        if self.old_move != self.move:  #cacheing here
            self.actuator.set_speed(self.move)
        self.old_move = self.move
        assert (self.move > 0)


class Rotate(Controller):
    def __init__(self, right):
        super(Rotate, self).__init__()
        self.right = right
        self.actuators = [right]

    def update_actuators(self):
        print "Rotate effect: ", self.move
        self.right.update(self.move)


class Translate(Rotate):
    def update_actuators(self):
        print "Translate effect: ", self.move
        self.right.update(self.move)


class WanderState(State):
    def setup(self):
        right = ev3.Motor(BRICK, "A")
        left = ev3.Motor(BRICK, "D")
        right.set_speed(350)
        right.forward()

        left.set_speed(350)
        left.forward()

        right_motor = BigMotor(right)
        self.add_active_actuators(right_motor)

        rotate = Rotate(right_motor)
        translate = Translate(right_motor)

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
        time.sleep(0.5)  # let it do it's magic for a time

