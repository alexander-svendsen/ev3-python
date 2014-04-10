# -*- coding: utf-8 -*-
class Battery(object):
    def __init__(self):
        # if rechargeable battery used, different values if otherwise
        self.level_min = 7100
        self.level_max = 8200
        self.milli_voltage = 0

        self.messages = {
            0: "critical",
            1: "low",
            2: "ok",
            3: "full"
        }

    def get_level(self):
        if self.milli_voltage > self.level_max:
            return 3
        elif self.milli_voltage > (self.level_min + 100):
            return 2
        elif self.milli_voltage > self.level_min:
            return 1
        else:
            return 0

    def get_message(self, level=None):
        if level is None:
            level = self.get_level()
        return self.messages[level]

    def __str__(self):
        return self.get_message()

