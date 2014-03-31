# -*- coding: utf-8 -*-
import threading


class Controller():
    """
    Runs the main subsumption logic. Controls which behavior will run based on their priority and if they want to become
    active or not. Works as a scheduler, where only one behavior can be active at a time and who is active is decided by
    the sensor data and their priority. The previous active behavior gets suppressed when a behavior with a higher
    priority wants to run.

    There is two usages in this class. One is to make the class take care of scheduler itself, by calling the start()
    method. The other is to take care of the scheduler by yourself, by using the step() method
    """
    def __init__(self, return_when_no_action, behaviors=None):
        """
        Initialize the object. Notice the subsumption module is not bound to a specific brick, the behaviors are. This
        makes it possible to have a subsumption module responsible for multiple bricks at the same time, if desirable.

        @param behaviors: list of behaviors. Their priority is based on their order. The first has the highest, while
        the last has the lowest.
        """
        if behaviors:
            self.behaviors = behaviors
        self.behaviors = []
        self.wait_object = threading.Event()
        self._active_behavior = None

        self._running = True
        self._return_when_no_action = return_when_no_action

    def add(self, behavior):
        """
        Add a behavior to the subsumption module. The order decide which priority they have. First > Second
        @type behavior: Behavior
        """
        self.behaviors.append(behavior)

    def step(self):
        """
        Find the next active behavior and runs it.
        @return: Returns whether it got to run any behavior or not
        """
        behavior = self.find_next_active_behavior()
        if behavior is not None:
            self.behaviors[behavior].action()
            return True
        return False

    def find_next_active_behavior(self):
        """
        Finds the next behavior that wants to run, if any
        @return: Next runnable behavior if any
        @rtype: int
        """
        for priority, behavior in enumerate(self.behaviors):
            if behavior.check():
                return priority
        return None

    def _find_and_set_new_active_behavior(self):
        new_behavior_priority = self.find_next_active_behavior()
        old_behavior_priority = self._active_behavior
        if old_behavior_priority is None or old_behavior_priority > new_behavior_priority:
            self._active_behavior = new_behavior_priority
            if old_behavior_priority is not None:
                self.behaviors[old_behavior_priority].suppress()

    def start(self):  # run the action methods
        """
        Starts finding and running behaviors, suppressing the old behaviors when new behaviors with higher priority
        wants to run.
        """
        self._find_and_set_new_active_behavior()  # force do it ourselves once to find the right onne
        thread = threading.Thread(name="Continuous behavior checker",
                                  target=self._continues_find_new_active_behavior, args=())
        thread.daemon = True
        thread.start()

        while True:
            if self._active_behavior is not None:
                self.behaviors[self._active_behavior].action()
                self._active_behavior = None
            elif self._return_when_no_action:
                break

        #Nothing more to do, so we are shutting down
        self._running = False

    def _continues_find_new_active_behavior(self):
        while self._running:
            self._find_and_set_new_active_behavior()