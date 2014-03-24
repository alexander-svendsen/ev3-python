# -*- coding: utf-8 -*-
import collections


class Subscription(object):
    def __init__(self, callbacks=None, subscribe_on_sensor_changes=True, subscribe_on_stream_data=True):
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

    def _new_sensor(self, msg):
        port = int(msg["data"]) + 1
        sensor = msg["sample_string"]
        for callback in self.callbacks["new_sensor"]:
            callback(sensor_name=sensor, port=port)

    def _no_sensor(self, msg):
        port = int(msg["data"]) + 1
        for callback in self.callbacks["no_sensor"]:
            callback(port=port)

    def _samples_received(self, msg):
        pass  # TODO: Wait on this one

    def subscribe_on_data_stream_from_port(self, port, callback):
        pass # TODO: wait to do this one

    def subscribe_on_streams(self, callback):
        self.callbacks["data_stream"].append(callback)

    def subscribe_on_sensor_added(self, callback):
        self.callbacks["new_sensor"].append(callback)

    def subscribe_on_sensor_removed(self, callback):
        self.callbacks["no_sensor"].append(callback)

    def run_event(self, data):  #TODO: DATA?
        try:
            print data
            if data["msg"] == "sensor_info":
                if data["sample_string"] != "None":
                    return self._new_sensor(data)
                else:
                    return self._no_sensor(data)
            elif data["msg"] == "samples":
                return self._samples_received(data)

            print "Strange event received: ", data["msg"]
        except Exception as e:
            print "Strange exception", e
        print "it got finished"

    def close(self): # TODO close the active subscriptions
        pass