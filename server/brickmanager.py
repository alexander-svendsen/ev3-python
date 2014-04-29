# -*- coding: utf-8 -*-
import json
import socket
import functools
import threading
import copy
import inspect
import traceback
from collections import defaultdict

import ev3
from behaviors import subsumption
from lib.simplewebsocketserver import WebSocket


class SubscriptionSocket(WebSocket):
    def __init__(self, brick_manager, server, sock, address):
        super(SubscriptionSocket, self).__init__(server, sock, address)
        self.brick_manager = brick_manager
        self.sub_address = None
        self._send_lock = threading.Lock()

    def remove_from_old_subscription(self):
        if self.sub_address:
            self.brick_manager.remove_old_subscription_from_brick(self.sub_address, self)

    def on_message(self):
        try:
            json_data = json.loads(str(self.data))
            if json_data['cmd'] == 'subscribe':

                brick_id = json_data['brick_address']

                if self.sub_address == brick_id:  # no need to resubscribe on same brick
                    return

                self.remove_from_old_subscription()
                if self.brick_manager.is_brick_connected(brick_id):
                    self.brick_manager.add_new_subscriptions_to_brick(brick_id, self)
                    self.sub_address = brick_id
                else:
                    # basically means the clients want subscribe messages to a brick not connected, so we close it
                    self.close()
            elif json_data['cmd'] == 'code':
                self.brick_manager.add_code(self.sub_address, json_data['title'], json_data['code'], self)
            elif json_data['cmd'] == 'bulk_code':
                self.brick_manager.add_code_bulk(self.sub_address, json_data['data'], self)
            elif json_data['cmd'] == 'remove_code':
                self.brick_manager.remove_code(self.sub_address, json_data['title'], self)
            elif json_data['cmd'] == 'run':
                self.brick_manager.run(self.sub_address)
            elif json_data['cmd'] == 'stop':
                self.brick_manager.stop(self.sub_address)
            else:
                print "Strange json data received:", json_data
        except (ValueError, KeyError):
            print "Invalid json data received:", self.data
            print traceback.format_exc()
        except:
            print traceback.format_exc()

    def on_open(self):
        print self.address, 'connected'

    def on_close(self):
        try:
            self.remove_from_old_subscription()
        except:
            print traceback.format_exc()
        print self.address, 'closed'

    def send(self, msg):  # wrapper to ensure that only one message is sent at a time
        with self._send_lock:
            super(SubscriptionSocket, self).send(msg)


class CodeManager(object):
    """manages the code instances"""

    def __init__(self):
        self.subsumption_controller = subsumption.Controller(return_when_no_action=False)
        self.raw_code = {}
        self.behaviors_names_list = []

        self.expressions = {'Behavior': subsumption.Behavior, 'ev3': ev3}
        self.default = {'Behavior': subsumption.Behavior, 'ev3': ev3}

        exec '' in self.expressions
        exec '' in self.default

    def update_behavior(self, behavior_name, behavior):
        if behavior_name in self.behaviors_names_list:
            index = self.behaviors_names_list.index(behavior_name)
            self.subsumption_controller.update(behavior, index)
        else:
            self.subsumption_controller.add(behavior)
            self.behaviors_names_list.append(behavior_name)

    def add_behaviors(self, title, code):
        self.raw_code[title] = code
        try:
            exec code in self.expressions
        except Exception as e:
            return e
        for instance in set(self.expressions) - set(self.default):
            if inspect.isclass(self.expressions[instance]):
                self.update_behavior(title, self.expressions[instance]())
                break
        self.expressions = copy.copy(self.default)
        return None

    def remove_behavior(self, title):
        if title in self.behaviors_names_list:
            index = self.behaviors_names_list.index(title)
            self.subsumption_controller.remove(index)
            del self.behaviors_names_list[index]
            del self.raw_code[title]
        else:
            print "Strange bug since a non-existed behavior tried to be removed"

    def code_package(self):
        data = []
        for index, behavior_name in enumerate(self.behaviors_names_list):
            data.append({
                'title': behavior_name,
                'code': self.raw_code[behavior_name],
                'running': self.subsumption_controller.active_behavior_index == index
            })
        return json.dumps({'cmd': 'code_data', 'data': data})


class BrickManager(object):
    def __init__(self):
        self._connected_brick = {}
        self._subscription_clients = defaultdict(list)
        self._subscription_objects = {}
        self._old_msg = defaultdict(lambda: {1: '', 2: '', 3: '', 4: ''})
        self.code_managers = {}

    def tell_others_about_it(self, address, data, client):
        for other_clients in self._subscription_clients[address]:
            if other_clients != client:
                other_clients.send(data)

    def runnable_callback(self, address, index):
        print "New running", index
        data = json.dumps({'cmd': 'running', 'title': self.code_managers[address].behaviors_names_list[index]})
        for client in self._subscription_clients[address]:
            client.send(data)

    def _run(self, address):
        try:
            self.code_managers[address].subsumption_controller.start()
        except Exception as e:
            self.tell_others_about_it(address, json.dumps({'cmd': 'error', 'data': str(e)}), None)

    def run(self, address):
        thread = threading.Thread(name="Continuous behavior checker",
                                  target=self._run, args=(address,))
        thread.daemon = True
        thread.start()

    def stop(self, address):
        self.code_managers[address].subsumption_controller.stop()

    def add_code_bulk(self, address, bulk, client):
        for code_module in bulk:
            exception = self.code_managers[address].add_behaviors(code_module['title'], code_module['code'])
            if exception:
                client.send(
                    json.dumps({'cmd': 'error', 'data': 'In module ' + code_module['title'] + ' -> ' + str(exception)}))
            return
        self.tell_others_about_it(address, json.dumps({'cmd': 'code_data', 'data': bulk}), client)

    def add_code(self, address, name, code, client):
        exception = self.code_managers[address].add_behaviors(name, code)
        if exception:
            client.send(json.dumps({'cmd': 'error', 'data': 'In module ' + name + ': ' + str(exception)}))
        self.tell_others_about_it(address,
                                  json.dumps({'cmd': 'code_data', 'data': [{'title': name, 'code': code}]}),
                                  client)

    def remove_code(self, address, name, client):
        self.code_managers[address].remove_behavior(name)
        self.tell_others_about_it(address,
                                  json.dumps({'cmd': 'remove_code', 'title': name}),
                                  client)

    def is_brick_connected(self, address):
        return address in self._connected_brick

    def remove_old_subscription_from_brick(self, address, client):
        self._subscription_clients[address].remove(client)
        del self._old_msg[client]

    def remove_brick(self, address):
        print "brick got disconnected ", address
        for client in self._subscription_clients[address]:
            client.close()

        self._subscription_clients[address] = []
        del self._subscription_objects[address]

        self._connected_brick[address].close()
        del self._connected_brick[address]

    def add_new_subscriptions_to_brick(self, address, client):
        if address not in self.code_managers:
            code_manager = CodeManager()
            self.code_managers[address] = code_manager
            code_manager.subsumption_controller.callback = functools.partial(self.runnable_callback, address)
        else:
            client.send(self.code_managers[address].code_package())

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
                    client.send(json.dumps({'cmd': 'sensor_data', 'data': data}))
            except socket.error:
                self._subscription_clients[address].remove(client)
            except Exception as e:
                print "Strange exception on websockets", type(e)
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

    def get_bricks(self):
        return self._connected_brick.keys()

    def open_sensor(self, brick_address, sensor_name, port):
        if brick_address in self._connected_brick:
            brick = self._connected_brick[brick_address]
            sensor_class = getattr(ev3, sensor_name)
            try:
                # simply try to construct sensor will automatically be pushed to client afterwords
                sensor_class(brick, int(port))
                return True
            except (ev3.InvalidSensorPortException, ev3.SensorNotConnectedException):
                pass
        return False