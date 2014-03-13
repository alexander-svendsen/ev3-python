# -*- coding: utf-8 -*-
import error


class BrickNotConnectedException(Exception):
    pass


class Brick(object):
    def __init__(self, socket):
        """
        @param socket: Socket used for communicating with the brick
        @type socket: communication.Communication
        """
        self.socket = socket
        self._opened_ports = []

    def set_port_to_used(self, port):
        if port in self._opened_ports:
            return False
        self._opened_ports.append(port)
        return True

    def set_port_to_unused(self, port):
        if port in self._opened_ports:
            self._opened_ports.remove(port)

    def send_command(self, cmd):
        try:
            self.socket.send(cmd + '\n')
            return self.socket.receive(1024)  # TODO: revice on a better number
        except:
            raise BrickNotConnectedException("Brick not connected")

    def close(self):  # Note should be recommended to the user
        pass
