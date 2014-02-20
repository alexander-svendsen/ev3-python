# -*- coding: utf-8 -*-
import config
import error
import ipsocket
import brick


def connect_to_brick(address, port):
    try:
        import bluetooth
        import bluesocket

        if bluetooth.is_valid_address(address):
            try:
                socket = bluesocket.BlueSocket()
                socket.connect(address, port)
                return brick.Brick(socket)

            except bluetooth.BluetoothError:
                raise error.BrickNotFoundException("Did you provide the correct bluetooth address and port?")

    except ImportError:
        pass

    try:
        socket = ipsocket.IpSocket()
        socket.connect(address, port)
        return brick.Brick(socket)
    except:
        raise error.BrickNotFoundException("Did you provide the correct ip address and port?")


def find_brick(name):
    try:
        socket = ipsocket.IpSocket()
        socket.connect_by_hostname(hostname=name, port=config.IP_SOCKET_PORT)
        return brick.Brick(socket)
    except error.BrickNotFoundException:
        pass

    try:
        import bluesocket
        socket = bluesocket.BlueSocket()
        socket.connect_by_hostname(hostname=name, port=config.BLUETOOTH_PORT)
        return brick.Brick(socket)
    except ImportError, error.BrickNotFoundException:
        pass

    raise error.BrickNotFoundException("Brick with name {0} not found".format(name))


def find_all_nearby_devices():
    devices = []
    devices.extend(ipsocket.IpSocket.get_nearby_devices(port=config.IP_SOCKET_PORT, immediate_return=False))
    try:
        import bluesocket
        devices.extend(bluesocket.BlueSocket.get_nearby_devices())
    except ImportError:
        pass
    return devices


def filter_devices_on_name(devices, name):
    return filter(lambda x: x[1].lower() == name.lower(), devices)


def find_all_bricks_with_name(name):
    devices = find_all_nearby_devices()
    return filter_devices_on_name(devices, name)
