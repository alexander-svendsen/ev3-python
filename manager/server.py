# -*- coding: utf-8 -*-
import socket
import threading


class Server(object):
    def __init__(self, address, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((address, port))
        self._sock.listen(20)

        self.running = True

        thread = threading.Thread(name="listen_for_spectators", target=self._listen_for_spectators, args=())
        thread.daemon = True
        thread.start()

        self.spectator_dict = {}
        self.bricks = []

    def add_brick(self, brick):
        self.bricks.append(brick)
        self.spectator_dict[brick] = []

    def accept_connection(self):
        return self._sock.accept()

    def send_to_spectators(self, brick, cmd):
        for spectator in self.spectator_dict[brick]:
            spectator.send(cmd)

    def _listen_for_spectators(self):
        while self.running:
            connection, address = self.accept_connection()
            # find out which brick they are interested in