# -*- coding: utf-8 -*-
import collections
import Queue
import threading
import logging

_MODULE_LOGGER = logging.getLogger('ev3.subscription')


class Subscription(object):
    def __init__(self, subscribe_on_sensor_changes=True, subscribe_on_stream_data=True):
        self._subscribe_on_sensor_changes = subscribe_on_sensor_changes
        self._subscribe_on_stream_data = subscribe_on_stream_data

        self.callbacks = collections.defaultdict(list)
        self.stream_callback = collections.defaultdict(list)

        self._message_handler = None  # Should be changed to a appropriate message handler

        self.queue = Queue.Queue()
        self.running = True

        self._thread = threading.Thread(name="subscription_thread", target=self._run_events, args=())
        self._thread.daemon = True
        self._thread.start()

    def _send_subscribe(self, command):
        cmd = {"cla": "subscribe", "cmd": command}
        self._message_handler.send(data=cmd, immediate_return=True)

    def send_subscribe_commands_to(self, message_handler):
        self._message_handler = message_handler
        self._message_handler.set_callback(self._add_event)

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
            callback(msg=msg["sample_string"], port=port)

    def _samples(self, msg):
        samples = msg["samples"]
        for callback in self.callbacks["samples"]:
            callback(samples=samples)

        for port, sample in enumerate(samples):
            for callback in self.stream_callback[port + 1]:
                callback(sample=sample)

    def subscribe_on_streams(self, callback):
        self.callbacks["samples"].append(callback)

    def subscribe_on_stream_on_port(self, port, callback):
        self.stream_callback[port].append(callback)

    def subscribe_on_new_sensor(self, callback):
        self.callbacks["new_sensor"].append(callback)

    def subscribe_on_no_sensor(self, callback):
        self.callbacks["no_sensor"].append(callback)

    def _add_event(self, data):
        self.queue.put_nowait(data)

    def _run_events(self):
        while self.running:
            data = self.queue.get(block=True)  # Will wait until data is available
            self._parse_event(data)

    def _parse_event(self, data):
        try:
            _MODULE_LOGGER.debug("Parsing event: %s", data)
            if data["msg"] == "sensor_info":
                if data["sample_string"] != "None":
                    self._new_sensor(data)
                else:
                    self._no_sensor(data)
            elif data["msg"] == "samples":
                self._samples(data)
            else:
                _MODULE_LOGGER.warning("Strange event received msg=%s", data["msg"])
        except:
            _MODULE_LOGGER.exception("Something went wrong in a callback")

    def close(self):  # TODO close the active subscriptions
        self.running = False