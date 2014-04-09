# -*- coding: utf-8 -*-


def falling_fuzzy(small_value, big_value, value):
    """
    Will return how true the provided value is depending on the small and big numbers. The closer the value is to
    small_value the more true it is. The closer it is to the big_value the less true it is.

    @type small_value: float
    @type big_value: float
    @type value: float
    @return: How true is the provided value
    @rtype: float
    """
    return 1.0 - rising_fuzzy(small_value, big_value, value)


def rising_fuzzy(small_value, big_value, value):
    """
    Will return how true the provided value is depending on the small and big numbers. The closer the value is to
    big_value the more true it is. The closer it is to the small_value the less true it is.

    @type small_value: float
    @type big_value: float
    @type value: float
    @return: How true is the provided value
    @rtype: float
    """
    if value <= small_value:
        return 0.0
    elif value >= big_value:
        return 1.0
    return float(value + abs(small_value)) / float(big_value + abs(small_value))


class State(object):
    """
    Control almost everything related to fuzzy behaviors. Fuzzy behaviors are split into states, where the sum of all
    the fuzzy behaviors is what the state tries to achieve. Each state has total control over its active components
    and will mange things like updating and calculating the correct actions depending on calculated values in the
    behavior
    """
    def __init__(self):
        self.controllers = []
        self.behaviors = []
        self.actuators = []
        self.setup()

    def setup(self):
        """
        Should setup the behavior properly. Each active component should be added here. Like the different behaviors,
        active actuators and the proper control blocks.
        """
        raise NotImplementedError("You should implement this yourself")

    def add_behavior(self, behavior):
        """
        Add a behavior to the state
        @type behavior: Behavior
        """
        self.behaviors.append(behavior)

    def add_active_actuators(self, actuator):
        """
        Add an actuator to the state
        @type actuator: Actuator
        """
        self.actuators.append(actuator)

    def add_controller(self, controller):
        """
        Add a controller to the state
        @type controller: Controller
        """
        self.controllers.append(controller)

    def check(self):
        """
        Checks whether this state should be active or not. This method should be overwritten by the implementer.
        Used natively in update since there is no point to update the state if it is not active
        """
        raise NotImplementedError("You should implement this yourself")

    def update(self):
        """
        Updates all of the components in the state if the state is active
        """
        if self.check():
            for actuators in self.actuators:
                actuators.reset()
            for behavior in self.behaviors:
                behavior.update()
            for controller in self.controllers:
                controller.calculate_movement()
                controller.update_actuators()
            return True
        return False

    def action(self):
        """
        Apply the update to the actuators. In most cases make the robot move.
        """
        for action in self.actuators:
            action.action()


class Behavior(object):
    """
    A single behavior. A behavior should effect multiple controllers to achieve their goal. Say you want a behavior
    which avoid collisions by rotating. Then this behavior must affect rotation more and more the closer the robot is
    to the colliding object, but at the same time it must effect the drive forward control block as the robot needs to
    drive less and less quickly forward to avoid colliding.
    """
    def __init__(self, controllers):
        self.controllers = controllers

    def update(self):
        """
        Should add your fuzzy logic here. Utilize the fuzzy_if function for full effect
        """
        raise NotImplementedError("You should implement this yourself")

    def fuzzy_if(self, truth_value, controller, update_value):
        """
        Updates the controller with the update value depending on how true the update is, in the sum of all truths.

        @param truth_value: how true is this update
        @param controller: name of the controller
        @param update_value: update value

        @type truth_value: float
        @type controller: str
        @type update_value: float
        """
        self.controllers[controller].update(truth_value, update_value)


class Actuator(object):
    """
    Wrapper for the actuators, most cases a motor. Depends if anything else is even possible, if it has movement or
    something that can be translated to movement is should work.
    """
    def __init__(self, actuator):
        self.move = 0.0
        self.actuator = actuator

    def reset(self):
        """
        Reset the stored movement, usually called between each update by the state
        """
        self.move = 0.0

    def update(self, value):
        """
        Updates the move value for the actuator
        @type value: int|float
        """
        self.move += value

    def action(self):
        """
        Should be overwritten. Depends on what type of actuator this wrapper has and what kind of operation should be
        done on that actuator. Remember to use the self.move variable as the updated value is stored there.
        """
        raise NotImplementedError("You should implement this yourself")


class Controller(object):
    """
    Class that should encapsulate the different control aspects of the actuators. Examples can be rotation or regular
    forward movement.
    """
    def __init__(self):
        self.move = 0.0
        self.max_truth_value = 0.0
        self.future_updates = []

    def update_actuators(self):
        """
        Update the actuators as you want here. Maybe one actuator should go forward while one other goes back. It
        depends, that's why you must implement the logic yourself. Note: you should use self.move as updates has been
        stored in here
        """
        raise NotImplementedError("You should implement this yourself")

    def update(self, truth_value, update_value):
        """
        Updates the controller with the update value depending on how true the update is, in the sum of all truths.
        Temporally stores the movement until all updates has been added and calculated_movement is called.

        @type truth_value: float
        @type update_value: float
        """
        self.move = 0.0
        self.max_truth_value += truth_value
        self.future_updates.append((truth_value, update_value))

    def calculate_movement(self):
        """
        Calculate the sum of all updates and clear the stored value
        """
        for truth, update_value in self.future_updates:
            try:
                self.move += truth / self.max_truth_value * update_value
            except ZeroDivisionError:
                pass  # means there is nothing to update this iteration
        self.max_truth_value = 0
        self.future_updates = []