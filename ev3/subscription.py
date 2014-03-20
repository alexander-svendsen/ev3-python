# -*- coding: utf-8 -*-
import collections
from brick import Brick
import sensors


class Subscription(object):
    def __init__(self, bricks):
        self._events = {
            'sensor_connected': self._sensor_added,
            'sensor_disconnected': self._sensor_left,
            'data_stream': self._data_stream_recived
        }
        self.callbacks = collections.defaultdict(list)
        self.subscription_channels = []
        self._bricks = bricks

        for brick in bricks:
            brick.event_callback = self.run_event
            brick.event_callback("MUHAHAH")

    def add_brick(self, brick):
        pass

    def remove_brick(self, brick):
        pass


    #TODO: will store and tell the brick to start sending events on the appropriate streams
    # if there is a subscription
    def send_subscribe_commands_to(self, message_handler):
        cmd = {}  # TODO
        self.subscription_channels.append(message_handler)
        message_handler.send(data=cmd, immediate_return=True)  # subscribe on events

    def _sensor_added(self, msg):
        sensor = msg["sample_string"]
        port = msg["data"]
        for callback in self.callbacks["sensor_added"]:
            callback(sensor=sensor, port=port)

    def _sensor_left(self, msg):
        port = msg["data"]
        for callback in self.callbacks["data_stream"]:
            callback(port=port)

    def _data_stream_recived(self, msg):
        pass  # TODO: Wait on this one

    def subscribe_on_data_stream_from_port(self, port, callback):
        pass # TODO: wait to do this one

    def subscribe_on_streams(self, callback):
        self.callbacks["data_stream"].append(callback)

    def subscribe_on_sensor_added(self, callback):
        self.callbacks["sensor_connected"].append(callback)

    def subscribe_on_sensor_removed(self, callback):
        self.callbacks["sensor_disconnected"].append(callback)

    def run_event(self, data):  #TODO: DATA?
        print "..... woooot?"
        # if event in self._events:
        #     self._events[event](msg)
        # else:
        #     print "Strange event received: ", event
