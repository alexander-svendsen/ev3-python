# -*- coding: utf-8 -*-


def falling_fuzzy(small_value, big_value, value):
    return 1.0 - rising_fuzzy(small_value, big_value, value)


def rising_fuzzy(small_value, big_value, value):
    if value <= small_value:
        return 0.0
    elif value >= big_value:
        return 1.0
    return float(value + abs(small_value)) / float(big_value + abs(small_value))


class State(object):  # should control everything
    def __init__(self):  # should be configurable how much the behavior should control the control block
        self.behaviors = []

    def setup(self):
        raise NotImplementedError("You should implement this yourself")

    def add(self, behavior):
        self.behaviors.append(behavior)

    def check(self):  # checks whether this state should be active or not
        raise NotImplementedError("You should implement this yourself")

    def update(self):
        if self.check():
            for behavior in self.behaviors:
                behavior.update()
            return True
        return False


class Behavior(object):
    def __init__(self, actuator_dict_with_effect):
        self.actuator_dict_with_effect = actuator_dict_with_effect

    def update(self):
        raise NotImplementedError("You should implement this yourself")

    def fuzzy_if(self, truth_value, actuator, update_value):
        real_update_value = self.actuator_dict_with_effect[actuator] * update_value
        actuator.update(truth_value, real_update_value)


class Actuator(object):  #wrapper for the actuators. most cases a motor, anything else is even possible
    def __init__(self, actuator):
        self.actuator = actuator
        self.max_truth_value = 0
        self.future_updates = []
        self.move = 0.0

    def update(self, truth_value, update_value):
        self.move = 0.0
        self.max_truth_value += truth_value
        self.future_updates.append((truth_value, update_value))

    def clear_and_sum(self):
        for truth, update_value in self.future_updates:
            try:
                self.move += truth / self.max_truth_value * update_value
            except ZeroDivisionError:
                print "Strange division bug"
        self.max_truth_value = 0
        self.future_updates = []

    def action(self):
        # self.move should be used
        raise NotImplementedError("You should implement this yourself")

