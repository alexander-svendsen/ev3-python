# -*- coding: utf-8 -*-
import error


class BrickNotConnectedException(Exception):
    pass


class Brick:
    def __init__(self, socket):
        self.socket = socket

    def send_command(self, cmd):
        try:
            self.socket.send(cmd + '\n')
        except:
            raise BrickNotConnectedException("Could not send command as the brick is no longer connected")

    def close(self):  # Note should be recommended to the user
        pass