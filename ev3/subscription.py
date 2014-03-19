# -*- coding: utf-8 -*-
import collections


class Subscription(object):
    def __init__(self):
        self._events = {
            'sensor_added': "woot",
            'sensor_left': "woot1",
            'streams': "woot3"
        }
        self.callbacks = collections.defaultdict(list)
        self.connected_sensors = {
            "sensor": {"port": 1, "sample": [0.0]}
        }

    def _sensor_added(self, msg):
        sensor = msg["sample_string"]
        port = msg["data"]
        self.connected_sensors[sensor] = {"port": port, }
        for callbacks in self.callbacks["sensor_added"]:
            print "mtf"

    def subscribe_on_data_stream_from_port(self, port, callback):
        pass

    def subscribe_on_streams(self, callback):
        self.callbacks["streams"].append(callback)

    def subscribe_on_sensor_added(self, callback):
        self.callbacks["sensor_added"].append(callback)

    def subscribe_on_sensor_removed(self, callback):
        self.callbacks["sensor_left"].append(callback)

    def run_event(self, event, msg):
        if event in self._events:
            self._events[event](msg)
