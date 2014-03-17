# -*- coding: utf-8 -*-
import threading
import json

MAX_SEQ = 65000


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


class AsynchronousMessageHandler(object):
    def __init__(self, communication_obj):
        self.communication = communication_obj
        # Can't use file_sockets since bluetooth don't support it, so implement a easy fix for it by using buffers
        self._buffer = ""

        self.message_queue = {}
        self.sequence = 0
        self.exception = False  # exception tracker

        self.thread = threading.Thread(name="receive_thread", target=self._receive_forever, args=())
        self.thread.daemon = True
        self.thread.start()
        self.send_lock = threading.Lock()

    def _receive(self):
        raw_data = self.communication.receive(1024)
        if raw_data == "":
            raise Exception  # no data means that the connection has been severed

        self._buffer += raw_data
        temp = self._buffer.split("\n")
        self._buffer = temp.pop()
        for line in temp:
            ##TODO: check if this is a message or a event
            data = json.loads(line)
            with self.send_lock:
                if data["seq"] in self.message_queue:
                    self.message_queue[data["seq"]].msg = data
                else:
                    self.message_queue[data["seq"]] = Message()
                    self.message_queue[data["seq"]].msg = data

    def _receive_forever(self):
        while True:
            try:
                self._receive()
            except:  # if anything wrong happen it means the brick got disconnected
                self.exception = True
                for key, value in self.message_queue.iteritems():
                    value.msg = {}
                break

    def _is_message_available(self, seq):
        return bool(self.message_queue[seq])

    def send(self, data):
        with self.send_lock:
            self.sequence = (self.sequence + 1) % MAX_SEQ
            seq = self.sequence
            self.message_queue[seq] = Message()

        data["seq"] = seq
        self.communication.send(json.dumps(data) + '\n')
        return seq

    def receive(self, seq):
        while not self._is_message_available(seq):
            self.message_queue[seq].wait()
        message = self.message_queue[seq].msg
        del self.message_queue[seq]
        return message







