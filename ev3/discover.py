# -*- coding: utf-8 -*-
import config
import error
import ipsocket
import brick
import logging

_MODULE_LOGGER = logging.getLogger('ev3.discover')


class NoValidCommunicationChosenException(Exception):
    pass


def connect_to_brick(address, by_ip=True, by_bluetooth=True):
    if by_bluetooth:
        try:
            import bluetooth
            import bluesocket

            if bluetooth.is_valid_address(address):
                try:
                    _MODULE_LOGGER.debug("Bluetooth address found, trying to connect to brick")

                    socket = bluesocket.BlueSocket()
                    socket.connect(address, config.BLUETOOTH_PORT)
                    return brick.Brick(socket)

                except bluetooth.BluetoothError:
                    raise error.BrickNotFoundException("Did you provide the correct bluetooth address and port?")

        except ImportError:
            pass

    if by_ip:
        try:
            _MODULE_LOGGER.debug("Connecting to brick by IP")

            socket = ipsocket.IpSocket()
            socket.connect(address, config.IP_SOCKET_PORT)
            return brick.Brick(socket)
        except:
            raise error.BrickNotFoundException("Did you provide the correct ip address and port?")

    raise NoValidCommunicationChosenException("You must choose either ip or bluetooth as a communication option")


def find_brick_by_name(name, by_ip=True, by_bluetooth=True):
    if by_ip:
        try:
            socket = ipsocket.IpSocket()
            socket.connect_by_hostname(hostname=name, port=config.IP_SOCKET_PORT)

            _MODULE_LOGGER.debug("Found brick with IP")

            return brick.Brick(socket)
        except error.BrickNotFoundException:
            pass

    if by_bluetooth:
        try:
            import bluetooth
            import bluesocket

            socket = bluesocket.BlueSocket()
            socket.connect_by_hostname(hostname=name, port=config.BLUETOOTH_PORT)

            _MODULE_LOGGER.debug("Found brick with bluetooth")

            return brick.Brick(socket)
        except (ImportError, error.BrickNotFoundException, IOError, bluetooth.BluetoothError):
            pass

    raise error.BrickNotFoundException(
        "Brick with name '{0}' not found, Searched in ip={1}, bluetooth={2}".format(name, by_ip, by_bluetooth))


def find_all_nearby_devices(by_ip=True, by_bluetooth=True):
    devices = []
    if by_ip:
        devices.extend(ipsocket.IpSocket.get_nearby_devices(port=config.IP_SOCKET_PORT, immediate_return=False))

    if by_bluetooth:
        try:
            import bluesocket
            devices.extend(bluesocket.BlueSocket.get_nearby_devices())
        except (ImportError, IOError):
            pass

    _MODULE_LOGGER.debug("Found devices: %s", devices)
    return devices


def filter_devices_on_name(devices, name):
    return filter(lambda x: x[1].lower() == name.lower(), devices)


def find_all_bricks_with_name(name, by_ip=True, by_bluetooth=True):
    devices = find_all_nearby_devices(by_ip, by_bluetooth)
    return filter_devices_on_name(devices, name)
