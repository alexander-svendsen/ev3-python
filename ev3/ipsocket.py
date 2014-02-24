# -*- coding: utf-8 -*-
import socket
import struct
import error
import communication


class IpSocket(communication.Communication):
    def __init__(self):
        communication.Communication.__init__(self)

    @staticmethod
    def get_nearby_devices(port, hostname='', immediate_return=True):
        # Receive multicast data
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind(('', port))
        mreq = struct.pack("4sl", socket.inet_aton('239.255.255.250'), socket.INADDR_ANY)
        udp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        udp.settimeout(0.5)  # only give it a short period of time to find a package

        devices = {}
        for _ in range(0, 10):  # retry to find the device 10 times
            try:
                data, address = udp.recvfrom(1024)  # this will block until the timeout happens
                devices[address[0]] = data
                if immediate_return and data.lower() == hostname.lower():
                    return devices.items()

            except socket.timeout:
                pass  # got a time out, lets try again
        return devices.items()

    def connect_by_hostname(self, hostname, port):
        devices = self.get_nearby_devices(port, hostname)
        for ip_address, name in devices:
            if name.lower() == hostname.lower():
                break
        else:
            raise error.BrickNotFoundException("No brick by name {0} found".format(hostname))
        self.connect(ip_address, port)