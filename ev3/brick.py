# -*- coding: utf-8 -*-
import json
import error


class Brick(object):
    def __init__(self, communication_object):
        """
        @param communication_object: Socket used for communicating with the brick
        @type communication_object: communication.Communication
        """
        self._communication = communication_object
        self._opened_ports = {}

        # Can't use file_sockets since bluetooth don't support it, so implement a easy fix for it by using buffers
        self._buffer = ""

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
        try:
            self._communication.send(json.dumps(cmd) + '\n')
            return json.loads(self._communication.receive(1024))  # TODO: revice on a better number
        except:
            raise error.BrickNotConnectedException("Brick not connected")

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()