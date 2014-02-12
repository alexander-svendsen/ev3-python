# -*- coding: utf-8 -*-
from ev3.ipsocket import IpSocket
from ev3.brick import Brick


class BrickNotFoundException(Exception):
    pass


def connect_to_brick(ip, port):
    try:
        socket = IpSocket().connect(ip, port)
        return Brick(socket)
    except:
        raise BrickNotFoundException("Did you provide the correct ip and port?")








# TODO support for bluetooth as well ?
# TODO offer the possibilty of finding it by hostname.... seem to uneccesary
