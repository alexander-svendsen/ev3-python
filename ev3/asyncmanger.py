# -*- coding: utf-8 -*-
from collections import deque
from threading import Thread, Condition
import json
#File of managing the ascynchronous communication between the brick and python program


#avoid sequence number
# request response handler. First request get first response, since they should be asynchronous
# Use msg to differenciate between messages
#todo raise exception if somethign went wrong with the communication

class AsynchManager():
    def __init__(self, communication_obj):
        self.communication = communication_obj
        # Can't use file_sockets since bluetooth don't support it, so implement a easy fix for it by using buffers
        self._buffer = ""

        self.message_queue = deque()
        self.wait_lock = Condition()
        self.send_lock = Condition()

        self.thread = Thread(name="receive_thread", target=self._receive, args=())
        self.thread.daemon = True
        self.thread.start()

    def _receive(self):  # start in thread??
        while True:
            self._buffer += self.communication.receive(1024)
            temp = self._buffer.split("\n")
            self._buffer = temp.pop()
            for line in temp:
                ##TODO: check if this is a message or a event
                self.message_queue.append(json.loads(line))
                self.wait_lock.acquire()
                self.wait_lock.notify() # is there anyone waiting for a message?
                self.wait_lock.release()

    def _is_message_available(self):
        return bool(self.message_queue)

    def send(self, data):  # TODO: send without getting data
        self.send_lock.acquire()
        self.communication.send(json.dumps(data) + '\n')
        self.send_lock.release()

    def send_and_receive(self, data):
        self.wait_lock.acquire()
        self.send(data)
        while not self._is_message_available():
            self.wait_lock.wait()
        message = self.message_queue.popleft()
        self.wait_lock.release()
        return message







