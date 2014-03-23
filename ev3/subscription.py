# -*- coding: utf-8 -*-
import collections


class Subscription(object):
    def __init__(self, callbacks=None, subscribe_on_sensor_changes=True, subscribe_on_stream_data=True):
        self._events = {
            'sensor_connected': self._sensor_added,
            'sensor_disconnected': self._sensor_left,
            'data_stream': self._data_stream_received
        }
        self.callbacks = collections.defaultdict(list)
        self._subscribe_on_sensor_changes = subscribe_on_sensor_changes
        self._subscribe_on_stream_data = subscribe_on_stream_data
        self._message_handler = None  # Should be changed to a appropriate message handler

    def _send_subscribe(self, command):  # complete!
        cmd = {"cla": "subscribe", "cmd": command}
        self._message_handler.send(data=cmd, immediate_return=True)

    def send_subscribe_commands_to(self, message_handler):  # complete!
        self._message_handler = message_handler
        self._message_handler.set_callback(self.run_event)

        if self._subscribe_on_sensor_changes:
            self._send_subscribe("subscribe_on_sensor_changes")
        if self._subscribe_on_stream_data:
            self._send_subscribe("subscribe_on_stream_data")

    def _sensor_added(self, msg):
        sensor = msg["sample_string"]
        port = msg["data"]
        for callback in self.callbacks["sensor_added"]:
            callback(sensor=sensor, port=port)

    def _sensor_left(self, msg):
        port = msg["data"]
        for callback in self.callbacks["data_stream"]:
            callback(port=port)

    def _data_stream_received(self, msg):
        pass  # TODO: Wait on this one

    def is_event_active(self, event):
        return event in self.callbacks

    def subscribe_on_data_stream_from_port(self, port, callback):
        pass # TODO: wait to do this one

    def subscribe_on_streams(self, callback):
        self.callbacks["data_stream"].append(callback)

    def subscribe_on_sensor_added(self, callback):
        self.callbacks["sensor_connected"].append(callback)

    def subscribe_on_sensor_removed(self, callback):
        self.callbacks["sensor_disconnected"].append(callback)

    def run_event(self, data):  #TODO: DATA?
        print data
        print data["msg"]
        # if event in self._events:
        #     self._events[event](msg)
        # else:
        #     print "Strange event received: ", event

    def close(self): # TODO close the active subscriptions
        pass