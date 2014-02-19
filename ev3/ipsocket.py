# -*- coding: utf-8 -*-
import socket


class IpSocket():
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _get_device_address_by_name(self, hostname, port):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use the Simple Service Discovery Protocol address for discovery
        udp.bind(("239.255.255.250", port))

        while True:
            data, ip_address = udp.recvfrom(1024)  # todo how much data
            if data == hostname:
                return ip_address

    def connect_by_hostname(self, hostname, port):
        ip_address = self._get_device_address_by_name(hostname, port)
        self.connect(ip_address, port)

    def connect(self, addr, port):
        self._socket.connect((addr, port))

    def send(self, data):
        self._socket.send(data)

    def receive(self, length, timeout=None):
        self._socket.settimeout(timeout)
        return self._socket.recv(length)

    def close(self):
        self._socket.close()

