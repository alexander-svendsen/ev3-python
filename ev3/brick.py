# -*- coding: utf-8 -*-
import error
import asynchronous


class Brick(object):
    def __init__(self, communication_object):
        """
        @param communication_object: Socket used for communicating with the brick
        @type communication_object: communication.Communication
        """
        self._communication = communication_object
        self._message_handler = asynchronous.MessageHandler(communication_object)
        self._opened_ports = {}

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

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()