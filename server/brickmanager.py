# -*- coding: utf-8 -*-
import json
import ev3
import socket
import functools
from collections import defaultdict
from lib.simplewebsocketserver import WebSocket, SimpleWebSocketServer


class SubscriptionSocket(WebSocket):
    def __init__(self, brick_manager, server, sock, address):
        super(SubscriptionSocket, self).__init__(server, sock, address)
        self.brick_manager = brick_manager

    def handleMessage(self):
        if self.data is None:
            self.data = ''

        brick_id = str(self.data)
        if self.brick_manager.is_brick_connected(brick_id):
            self.brick_manager.add_new_subscriptions_to_brick(brick_id, self)
        else:
            self.close()

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


class BrickManager(object):
    def __init__(self):
        self._connected_brick = {}
        self._subscriptions_servers = {}
        self._subscription_clients = defaultdict(list)
        self._subscription_objects = {}

    def is_brick_connected(self, address):
        return address in self._connected_brick

    def _is_there_a_subscription_address(self, address):
        return address in self._subscriptions_servers

    def add_new_subscriptions_to_brick(self, address, client):
        self._subscription_clients[address].append(client)

        if address not in self._subscription_objects:
            sub = ev3.Subscription(False, True)
            sub.subscribe_on_samples(functools.partial(self._callback_on_samples, address))
            self._connected_brick[address].set_subscription(sub)
            self._subscription_objects[address] = sub

    def _callback_on_samples(self, address, samples):
        for client in list(self._subscription_clients[address]):
            try:
                data = {}
                brick = self._connected_brick[address]
                for port in ev3.SENSOR_PORTS:
                    if port in brick.get_opened_ports:
                        sensor = brick.get_opened_ports[port]
                        mode = sensor.get_selected_mode()
                        data[port] = {'sensor': sensor.get_name(),
                                      'mode': mode.get_name(),
                                      'sample': samples[port - 1]}
                client.sendMessage(json.dumps(data))
            except socket.error:
                self._subscription_clients[address].remove(client)

    def add_brick(self, address):
        if not self.is_brick_connected(address):
            try:
                brick = ev3.connect_to_brick(address)
                self._connected_brick[address] = brick
            except ev3.BrickNotFoundException:
                pass  # care

    def get_bricks(self):
        return self._connected_brick.keys()

    def get_brick(self, address):
        return self._connected_brick[address]

