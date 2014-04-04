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
        self.controllers = []
        self.behaviors = []
        self.actuators = []
        self.setup()

    def setup(self):
        raise NotImplementedError("You should implement this yourself")

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def add_active_actuators(self, actuator):
        self.actuators.append(actuator)

    def add_controller(self, actuator):
        self.controllers.append(actuator)

    def check(self):  # checks whether this state should be active or not
        raise NotImplementedError("You should implement this yourself")

    def update(self):
        if self.check():
            for behavior in self.behaviors:
                behavior.update()
            return True
        return False

    def action(self):
        for controller in self.controllers:
            controller.calculate_movement()
            controller.update_actuators()
        for action in self.actuators:
            action.action()


class Behavior(object):
    def __init__(self, actuator_dict):
        self.actuator_dict = actuator_dict

    def update(self):
        raise NotImplementedError("You should implement this yourself")

    def fuzzy_if(self, truth_value, actuator, update_value):
        real_update_value = self.actuator_dict[actuator][1] * update_value
        self.actuator_dict[actuator][0].update(truth_value, real_update_value)


class Actuator(object):
    """
    wrapper for the actuators. most cases a motor, anything else is even possible
    """
    def __init__(self, actuator):
        self.move = 0.0
        self.actuator = actuator

    def update(self, value):
        self.move += value

    def action(self):
        raise NotImplementedError("You should implement this yourself")


class ControlBlock(object):
    def __init__(self):
        self.move = 0.0
        self.max_truth_value = 0.0
        self.future_updates = []

    #remember use the same actuators on the different control blocks
    def update_actuators(self):
        """
        Update the actuators as you want here. Maybe one actuator should go forward while one other goes back. It
        depends, that's why you must implement the logic yourself. Note: you should use self.calculate_movement and
        self.move as updates has been stored in here
        """
        self.calculate_movement()
        raise NotImplementedError("You should implement this yourself")

    def update(self, truth_value, update_value):
        self.move = 0.0
        self.max_truth_value += truth_value
        self.future_updates.append((truth_value, update_value))

    def calculate_movement(self):
        for truth, update_value in self.future_updates:
            try:
                self.move += truth / self.max_truth_value * update_value
            except ZeroDivisionError:
                pass  # means there is nothing to update this iteration
        self.max_truth_value = 0
        self.future_updates = []