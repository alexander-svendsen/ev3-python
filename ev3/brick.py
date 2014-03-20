# -*- coding: utf-8 -*-
import error
import asynchronous


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
        elif self.milli_voltage > (self.level_min - 100):
            return 2
        elif self.milli_voltage > self.level_min:
            return 1
        else:
            return 0

    def get_message(self, level=None):
        if level is None:
            level = self.get_level()
        return self.messages[level]


class Brick(object):
    def __init__(self, communication_object):
        """
        @param communication_object: Communication object used for communicating with the brick
        @type communication_object: communication.Communication
        """
        self._message_handler = asynchronous.MessageHandler(communication_object, self.event_callback)
        self._opened_ports = {}
        self.battery = Battery()
        self.hostname = ""
        self.refresh_battery()

    def get_battery(self):
        return self.battery

    def refresh_battery(self):
        response = self.send_command({"cla": "status"})
        self.battery.milli_voltage = response["data"]
        self.hostname = response["sample_string"]

    @property
    def get_opened_ports(self):
        return self._opened_ports

    def set_port_to_used(self, port, obj_using_port=None):
        if port in self._opened_ports:
            return False
        self._opened_ports[port] = obj_using_port
        return True

    def set_port_to_unused(self, port):
        if port in self._opened_ports:
            del self._opened_ports[port]

    def send_command(self, cmd):
        seq = self._message_handler.send(cmd)
        data = self._message_handler.receive(seq)

        # if anything has gone wrong in the async handler, the exception flag is set to true.
        if self._message_handler.exception:
            raise error.BrickNotConnectedException("Brick not connected")
        return data

    @staticmethod
    def event_callback(data):  # meant to be overwritten
        print "Event happened with data:", data

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()

    def __del__(self):
        self.close()

    def __str__(self):
        return self.hostname