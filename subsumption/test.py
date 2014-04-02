# -*- coding: utf-8 -*-
from fuzzy import *


class AvoidColliding(Behavior):
    def update(self):
        self.fuzzy_if("blocking", 'drive', 25)
        self.fuzzy_if("blocking", 'drive', 25)

        self.fuzzy_if("blocking", 'rotate', 0)
        self.fuzzy_if("blocking", 'rotate', 0)


class Drive(Behavior):
    def update(self):
        self.fuzzy_if("nothing blocking", 'drive', 0)
        self.fuzzy_if("nothing blocking", 'drive', 0)

        self.fuzzy_if("nothing blocking", 'rotate', -10)
        self.fuzzy_if("nothing blocking", 'rotate', 10)


class WanderState(State):
    def setup(self):
        left_motor = WheelMotor("motor_A")
        right_motor = WheelMotor("motor_B")

        self.add(Drive({left_motor: 1.0, right_motor: 1.0}))

    def check(self):
        return True  # this state should never end


class WheelMotor(Actuator):
    def action(self):
        print "{0} rotate = {1}".format(self.actuator, self.move)


if __name__ == "__main__":
    pass
