# -*- coding: utf-8 -*-
import error
import asyncmanger


class Brick(object):
    def __init__(self, communication_object):
        """
        @param communication_object: Socket used for communicating with the brick
        @type communication_object: communication.Communication
        """
        self._communication = communication_object
        self.asynch_msg = asyncmanger.AsynchManager(communication_object)
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
        try:
            return self.asynch_msg.send_and_receive(cmd)
            # self._communication.send(json.dumps(cmd) + '\n')
            # return json.loads(self._communication.receive(1024))
        except:
            raise error.BrickNotConnectedException("Brick not connected")

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()