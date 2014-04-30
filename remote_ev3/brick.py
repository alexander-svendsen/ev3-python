# -*- coding: utf-8 -*-
import logging

from ev3 import battery
from ev3 import error

_MODULE_LOGGER = logging.getLogger('ev3.brick')


class Brick(object):
    def __init__(self, remote_object, address):
        self.remote_object = remote_object
        self.brick_identifier = address

        self._opened_ports = {}
        self.hostname = ""
        self.mute = False  # blocks sound messages
        self.closed = False

        self.battery = battery.Battery()
        self.refresh_battery()

    def get_battery(self):
        return self.battery

    def refresh_battery(self):
        response = self.send_command({"cla": "status"})
        self.battery.milli_voltage = response["data"]
        self.hostname = response["sample_string"]

    @property
    def get_opened_ports(self):
        return self.remote_object.call_method('get_opened_ports', self.brick_identifier)

    def set_port_to_used(self, port, obj_using_port=None):
        if port in self._opened_ports:
            return False
        self._opened_ports[port] = obj_using_port
        return True

    def set_port_to_unused(self, port):
        if port in self._opened_ports:
            del self._opened_ports[port]

    def send_command(self, cmd, immediate_return=False):
        if self.closed:
            raise error.BrickNotConnectedException("Brick closed, you cannot use this object anymore")
        data = self.remote_object.call_method(name='send_command',
                                              params=[self.brick_identifier, cmd, immediate_return])
        return data

    def play_tone(self, frequency, duration):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "play_tone", "frequency": frequency, "time": duration})

    def buzz(self):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "buzz"})

    def beep(self):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "beep"})

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()

        self.closed = True

    def __del__(self):
        self.close()

    def __str__(self):
        return self.hostname