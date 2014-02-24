# -*- coding: utf-8 -*-
import error


class BrickNotConnectedException(Exception):
    pass


class Brick:
    def __init__(self, socket):
        """
        @type socket: communication.Communication
        @param socket: Socket used for communicating with the brick
        """
        self.socket = socket

    def send_command(self, cmd):
        try:
            self.socket.send(cmd + '\n')
            return self.socket.receive(1024)  # TODO: revice on a better number
        except:
            raise BrickNotConnectedException("Brick not connected")

    def close(self):  # Note should be recommended to the user
        pass
