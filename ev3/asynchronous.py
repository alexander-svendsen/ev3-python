# -*- coding: utf-8 -*-
import socket
import threading
import json
import logging
import error

_MODULE_LOGGER = logging.getLogger('ev3.asynchronous')
_MAX_SEQ = 65000


class Message(object):
    def __init__(self):
        self._msg = None
        self.wait_object = threading.Event()

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value
        self.wait_object.set()

    def wait(self):
        self.wait_object.wait()

    def __nonzero__(self):
        return self.wait_object.isSet()


class MessageHandler(object):
    def __init__(self, communication_obj):
        """
        @param communication_obj: Socket used for communicating with the brick
        @type communication_obj: communication.Communication
        """
        self._callback = lambda x: None
        self._communication_method = communication_obj
        # Can't use file_sockets since bluetooth don't support it, so implement a easy fix for it by using buffers
        self._buffer = ""

        self._message_queue = {}
        self._sequence = 0
        self.exception = False  # exception tracker

        self._running = True

        self._thread = threading.Thread(name="receive_thread", target=self._receive_forever, args=())
        self._thread.daemon = True
        self._thread.start()
        self._send_lock = threading.Lock()

    def set_callback(self, callback):
        self._callback = callback

    def _call_callback(self, data):
        try:
            self._callback(data)  # the subscription module should be the one here,
        except:
            _MODULE_LOGGER.exception("Exception in callback, callback method should run in its own thread")

    def _receive(self):
        raw_data = self._communication_method.receive(1024)
        if raw_data == "":
            raise Exception  # no data means that the connection has been severed

        self._buffer += raw_data
        temp = self._buffer.split("\n")
        self._buffer = temp.pop()
        for line in temp:
            _MODULE_LOGGER.debug("Received: %s", line)

            data = json.loads(line)
            if data["msg"] == "response":
                # If not inside the queue, it means the user was not interested in the response, even tough we got it
                if data["seq"] in self._message_queue:
                    self._message_queue[data["seq"]].msg = data
            else:
                self._call_callback(data)

    def _receive_forever(self):
        while self._running:
            try:
                self._receive()
            except:  # if anything wrong happen it means the brick got disconnected
                self.exception = True
                for key, value in self._message_queue.iteritems():
                    value.msg = {}
                self._call_callback(None)
                self.close()

    def _is_message_available(self, seq):
        return bool(self._message_queue[seq])

    def send(self, data, immediate_return=False):
        with self._send_lock:
            self._sequence = (self._sequence + 1) % _MAX_SEQ
            seq = self._sequence
            if not immediate_return:
                self._message_queue[seq] = Message()

            data["seq"] = seq
            try:
                self._communication_method.send(json.dumps(data) + '\n')
            except socket.error:
                raise error.BrickNotConnectedException("Brick no longer connected")

        del data["seq"]  # to hide seq from the users point of view
        return seq

    def receive(self, seq):
        if seq not in self._message_queue:
            return ""  # prob means the message was not setup to receive a response, so it will return none
        while not self._is_message_available(seq):
            self._message_queue[seq].wait()
        message = self._message_queue[seq].msg
        del self._message_queue[seq]

        if "seq" in message:
            del message["seq"]  # to hide seq from the users point of view
        return message

    def close(self):
        self._running = False
        self._communication_method.close()