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
        self._subscriptions_servers = {}
        self._subscription_clients = defaultdict(list)
        self._subscription_objects = {}

    def is_brick_connected(self, address):
        return address in self._connected_brick

    def _is_there_a_subscription_address(self, address):
        return address in self._subscriptions_servers

    def remove_old_subscription_from_brick(self, address, client):
        self._subscription_clients[address].remove(client)

    def remove_brick(self, address):
        print "brick got disconnected ", address  #todo: COMPLETE IT

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
            except Exception as e:  # todo: remove in the future
                print "STRANGE EXCEPTION ON WEBSOCKET", type(e)
                print e

    def add_brick(self, address):
        if not self.is_brick_connected(address):
            try:
                brick = ev3.connect_to_brick(address)
                self._connected_brick[address] = brick
            except ev3.BrickNotFoundException:
                pass  # care

    def get_bricks(self):  # review: name as well ?
        return self._connected_brick.keys()