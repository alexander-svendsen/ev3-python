# -*- coding: utf-8 -*-
import socket


class IpSocket():
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr, port, timeout=None):
        self._socket.settimeout(timeout)
        self._socket.connect((addr, port))

    def close(self):
        self._socket.close()

    def send(self, data):
        self._socket.send(data)

    def receive(self, length, timeout=None):
        self._socket.settimeout(timeout)
        return self._socket.recv(length)

    def getsockname(self):
        return self._socket.getsockname()

    @property
    def connection(self):
        return self._socket

    @property
    def gethostname(self):
        return socket.gethostname()
