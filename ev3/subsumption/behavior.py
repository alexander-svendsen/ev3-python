# -*- coding: utf-8 -*-


class Behavior(object):
    """
    This is an abstract class. Should embody an specific behavior belonging to a robot. Each Behavior must define three
    things and should be implemented by the user:
    1. check: Under what circumcises should this behavior take control.
    2. action: What should this behavior do while it has control.
    3. suppress: Should give up control immediately when this method is called. Will be called when a behavoir with a
    higher priority gets called.
    """

    def check(self):
        """
        Method to check whether if this behavior should be started or not.
        @return: Should return a true value if this behavior should take control or not
        """
        raise NotImplementedError("Should have implemented this")

    def action(self):
        """
        The code in action should represent what the behavior should do while it's active. When this method returns
        the action is complete and the robot should be in a complete safe state, ie the motors are shut down and such,
        so the next behavior can take safely take control of the robot
        """
        raise NotImplementedError("Should have implemented this")

    def suppress(self):
        """
        Should immediately cause the behavior to exits it execution and put the state in safe mode. In other words it
        should cause the action() method to stop it's execution
        """
        raise NotImplementedError("Should have implemented this")