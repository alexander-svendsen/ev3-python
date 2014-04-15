# -*- coding: utf-8 -*-
import logging
import error
import asynchronous
import battery


_MODULE_LOGGER = logging.getLogger('ev3.brick')


class Brick(object):
    def __init__(self, communication_object):
        """
        @param communication_object: Communication object used for communicating with the brick
        @type communication_object: communication.Communication
        """
        self.subscription = None
        self._opened_ports = {}
        self.hostname = ""

        self.mute = False  # blocks sound messages
        self.closed = False

        self._message_handler = asynchronous.MessageHandler(communication_object)
        self.battery = battery.Battery()
        self.refresh_battery()

    def get_battery(self):
        return self.battery

    def refresh_battery(self):
        response = self.send_command({"cla": "status"})
        self.battery.milli_voltage = response["data"]
        self.hostname = response["sample_string"]

    @property
    def get_opened_ports(self):
        return self._opened_ports

    def set_port_to_used(self, port, obj_using_port=None):
        if port in self._opened_ports:
            return False
        self._opened_ports[port] = obj_using_port
        return True

    def set_port_to_unused(self, port):
        if port in self._opened_ports:
            del self._opened_ports[port]

    def send_command(self, cmd, immediate_return=False):
        if self.closed:
            raise error.BrickNotConnectedException("Brick closed, you cannot use this object anymore")

        seq = self._message_handler.send(cmd, immediate_return)
        data = self._message_handler.receive(seq)

        # if anything has gone wrong in the async handler, the exception flag is set to true.
        if self._message_handler.exception:
            raise error.BrickNotConnectedException("Brick not connected")
        return data

    def set_subscription(self, subscription):
        """
        @param subscription: subscription module
        @type subscription: Subscription
        """
        self.subscription = subscription
        self.subscription.start_subscriptions(self._message_handler)
        self.subscription.subscribe_on_samples(self._data_stream_cache)

    def _data_stream_cache(self, samples):
        for port, sample in enumerate(samples):
            port += 1
            if sample:
                if port in self._opened_ports:
                    self._opened_ports[port].set_cache_data(sample)
                else:
                    _MODULE_LOGGER.warning("Got a sample for a port not containing a sensor. Port=%s, Sample=%s",
                                           port, sample)

    def remove_subscription(self):
        self.subscription.close()
        for x in xrange(1, 5):
            if x in self._opened_ports:
                self._opened_ports[x].set_cache_data(None)

    def play_tone(self, frequency, duration):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "play_tone", "frequency": frequency, "time": duration})

    def buzz(self):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "buzz"})

    def beep(self):
        if not self.mute:
            self.send_command({"cla": "sound", "cmd": "beep"})

    def close(self):
        open_ports = self._opened_ports.keys()
        for port in open_ports:
            self._opened_ports[port].close()
        if self.subscription:
            self.subscription.close()

        self._message_handler.close()
        self.closed = True

    def __del__(self):
        self.close()

    def __str__(self):
        return self.hostname