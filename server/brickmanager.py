# -*- coding: utf-8 -*-
import threading
import ev3
import socket
from collections import defaultdict

class Server():
    def __init__(self, addr, port, brick_identifier):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((addr, port))
        self._sock.listen(20)

        self.brick_identifier = brick_identifier
        self.callback = None

        self.active = True
        self._thread = threading.Thread(name="subscription_thread", target=self.accept_connection(), args=())
        self._thread.daemon = True

    def accept_connection(self):
        while self.active:
            client, address = self._sock.accept()
            self.callback(self.brick_identifier, client)

    def close(self, connection):
        connection._close()

    def send(self, connection, data):
        connection.send(data)

    def receive(self, connection, length, timeout=None):
        connection.settimeout(timeout)
        return connection.recv(length)

    @property
    def getsockname(self):
        return self._sock.getsockname()


class BrickManager(object):
    def __init__(self):
        self._connected_brick = {}
        self._subscriptions_servers = {}
        self._subscription_clients = defaultdict(list)

    def _is_brick_connected(self, address):
        return address in self._connected_brick

    def _is_there_a_subscription_address(self, address):
        return address in self._subscriptions_servers

    def _add_new_subscriptions_to_brick(self, address, client):
        self._subscription_clients[address].append(client)

    def add_brick(self, address):
        if not self._is_brick_connected(address):
            try:
                brick = ev3.connect_to_brick(address)
                self._connected_brick[address] = brick
            except ev3.BrickNotFoundException:
                pass  # care

    def get_bricks(self):
        return self._connected_brick.keys()

    def get_subscription_address(self, brick_identifier):
        if not self._is_there_a_subscription_address(brick_identifier):
            server = Server('', 0, brick_identifier)
            server.callback = self._add_new_subscriptions_to_brick
            self._subscriptions_servers[brick_identifier] = server
        return {
            'address': self._subscriptions_servers[brick_identifier].getsockname[0],
            'port': self._subscriptions_servers[brick_identifier].getsockname[1]
        }

    def get_brick(self, address):
        return self._connected_brick[address]

