# -*- coding: utf-8 -*-
import json
import socket
import functools
from collections import defaultdict

import ev3
from lib.simplewebsocketserver import WebSocket


class SubscriptionSocket(WebSocket):
    def __init__(self, brick_manager, server, sock, address):
        super(SubscriptionSocket, self).__init__(server, sock, address)
        self.brick_manager = brick_manager
        self.sub_address = None

    def remove_from_old_subscription(self):
        if self.sub_address:
            self.brick_manager.remove_old_subscription_from_brick(self.sub_address, self)

    def handleMessage(self):
        brick_id = str(self.data)

        if self.sub_address == brick_id:  # no need to resubscribe on same brick
            return

        self.remove_from_old_subscription()
        if self.brick_manager.is_brick_connected(brick_id):
            self.brick_manager.add_new_subscriptions_to_brick(brick_id, self)
        else:
            # basically means the clients want subscribe messages to a brick not connected, so we close it
            self.close()

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        self.remove_from_old_subscription()
        print self.address, 'closed'


class BrickManager(object):
    def __init__(self):
        self._connected_brick = {}
        self._subscription_clients = defaultdict(list)
        self._subscription_objects = {}
        self._old_msg = defaultdict(lambda: {1: '', 2: '', 3: '', 4: ''})

    def is_brick_connected(self, address):
        return address in self._connected_brick

    def remove_old_subscription_from_brick(self, address, client):
        self._subscription_clients[address].remove(client)
        self._old_msg.remove(client)

    def remove_brick(self, address):  # review: should allow for both the connected party removing it, and sudden close
        print "brick got disconnected ", address
        for client in self._subscription_clients[address]:
            client.close()

        self._subscription_clients[address] = []
        del self._subscription_objects[address]

        self._connected_brick[address].close()
        del self._connected_brick[address]

    def add_new_subscriptions_to_brick(self, address, client):
        self._subscription_clients[address].append(client)

        if address not in self._subscription_objects:
            sub = ev3.Subscription(False, True)
            sub.subscribe_on_samples(functools.partial(self._callback_on_samples, address))
            sub.subscribe_on_brick_disconnect(functools.partial(self.remove_brick, address))
            self._connected_brick[address].set_subscription(sub)
            self._subscription_objects[address] = sub

    def _callback_on_samples(self, address, samples):
        for client in list(self._subscription_clients[address]):
            try:
                data = []
                brick = self._connected_brick[address]
                for port in ev3.SENSOR_PORTS:
                    if port in brick.get_opened_ports:
                        sensor = brick.get_opened_ports[port]
                        mode = sensor.get_selected_mode()
                        msg = {'sensor': sensor.get_name(),
                               'mode': mode.get_name(),
                               'port': port,
                               'sample': samples[port - 1]}
                        if self._old_msg[client][port] != msg:
                            data.append(msg)
                            self._old_msg[client][port] = msg
                if data:
                    client.sendMessage(json.dumps(data))
            except socket.error:
                self._subscription_clients[address].remove(client)
            except Exception as e:  # todo: remove in the future
                print "STRANGE EXCEPTION ON WEBSOCKET", type(e)
                print e

    def add_brick(self, address):
        if not self.is_brick_connected(address):
            try:
                brick = ev3.connect_to_brick(address)
                self._connected_brick[address] = brick
                return True
            except ev3.BrickNotFoundException:
                pass  # care
        return False

    def get_bricks(self):  # review: name as well ?
        return self._connected_brick.keys()