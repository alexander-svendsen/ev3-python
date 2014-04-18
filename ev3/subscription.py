# -*- coding: utf-8 -*-
import collections
import Queue
import threading
import logging

_MODULE_LOGGER = logging.getLogger('ev3.subscription')


class Subscription(object):
    """
    Subscription module. It starts a subscription for events at the brick and all the provided callback the user has
    provided.

    NOTE: usage is a little different from how the modules usually interacts with the brick, since the brick
    must take it in instead of the other way
    """
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

    def _send_subscribe(self, command):
        cmd = {"cla": "subscribe", "cmd": command}
        self._message_handler.send(data=cmd, immediate_return=True)

    def start_subscriptions(self, message_handler):
        """
        Starts the subscriptions at the brick

        Meant to be used directly by the brick, not the user. The brick setups the appropriate communication parameters
        and such since the subscription module need direct access so it can change the communication callback
        @param message_handler: which communication module should be used
        @type message_handler: MessageHandler
        """
        self._thread.start()
        self._message_handler = message_handler
        self._message_handler.set_callback(self.add_event)

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
            for callback in self.stream_callback[port + 1]:  # Since port is one of
                callback(sample=sample)

    def _brick_got_disconnected(self):
        for callback in self.callbacks["disconnect"]:
            callback()

    def subscribe_on_brick_disconnect(self, callback):
        self.callbacks["disconnect"].append(callback)

    def subscribe_on_samples(self, callback):
        """
        Subscribe on samples. Will call the provided function with a list of samples on all ports. The samples look like
        this: [[sample1], [sample2], [sample3], [sample4]], since each sample may consist of multiple samples.
        @param callback: function to call when streams is received. Must either take in arguments **kwargs or samples
        """
        self.callbacks["samples"].append(callback)

    def subscribe_on_samples_in_port(self, port, callback):
        """
        Subscribe on a single stream of sample in the provided port. The sample looks like this: [sample]
        @param port: sensor port to subscribe on
        @param callback: function to call when stream is received. Must either take in arguments **kwargs or sample
        """
        self.stream_callback[port].append(callback)

    def subscribe_on_new_sensor(self, callback):
        """
        Subscribe on a message when a new sensor is connected. The name of the sensor is returned to the callback. It is
        not yet opened, so it's left to the user to decide what they want to do with the information. Note some
        sensor may not exists at this side yet, or in some cases it simply does not know what sensor it is, only the
        type. Like the case of most analog sensors.
        @param callback: function to call when sensor is connected. Must either take in arguments **kwargs or
        sensor_name, port

        """
        self.callbacks["new_sensor"].append(callback)

    def subscribe_on_no_sensor(self, callback):
        """
        Subscribe on a message when there is no sensor connected. A message is sent to the callback, providing
        information on the port, like if there is a sensor there, or if a sensor is connected, but has been wrongly
        connected.
        @param callback: function to call when there is no sensor at the port. Must either take in arguments **kwargs or
        msg, port
        """
        self.callbacks["no_sensor"].append(callback)

    def add_event(self, data):
        self.queue.put_nowait(data)

    def _run_events(self):
        while self.running:
            data = self.queue.get(block=True)  # Will wait until data is available
            self._parse_event(data)

    def _parse_event(self, data):
        try:
            if data is None:  # means the connection with the brick went down, sto running
                self.running = False
                self._brick_got_disconnected()
            elif data["msg"] == "sensor_info":
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

    def close(self):
        if self.running:  # fail safe
            self._send_subscribe("close")
        self.running = False

    def __del__(self):
        self.close()
