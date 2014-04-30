# -*- coding: utf-8 -*-
import config
import error
import ipsocket
import brick
import logging

_MODULE_LOGGER = logging.getLogger('ev3.discover')
_LOADED_BRICKS = {}


def _is_brick_already_in_memory(address, port):
    if (address, port) in _LOADED_BRICKS:
        return not _LOADED_BRICKS[(address, port)].closed
    return False


def _stored_brick(address, port):
    _MODULE_LOGGER.debug("Brick found in memory, returning stored instance")
    return _LOADED_BRICKS[(address, port)]


def _store_brick_in_memory(address, port, opened_brick):
    _LOADED_BRICKS[(address, port)] = opened_brick


def connect_to_brick(address, by_ip=True, by_bluetooth=True):
    if by_bluetooth:
        try:
            import bluetooth
            import bluesocket

            if bluetooth.is_valid_address(address):
                try:
                    _MODULE_LOGGER.debug("Bluetooth address found, trying to connect to brick")

                    if _is_brick_already_in_memory(address, config.BLUETOOTH_PORT):
                        return _stored_brick(address, config.BLUETOOTH_PORT)

                    socket = bluesocket.BlueSocket()
                    socket.connect(address, config.BLUETOOTH_PORT)
                    _brick = brick.Brick(socket)

                    _store_brick_in_memory(address, config.BLUETOOTH_PORT, _brick)

                    return _brick

                except bluetooth.BluetoothError:
                    raise error.BrickNotFoundException("Did you provide the correct bluetooth address?")

        except ImportError:
            pass

    if by_ip:
        try:
            _MODULE_LOGGER.debug("Connecting to brick by IP")

            if _is_brick_already_in_memory(address, config.IP_SOCKET_PORT):
                return _stored_brick(address, config.IP_SOCKET_PORT)

            socket = ipsocket.IpSocket()
            socket.connect(address, config.IP_SOCKET_PORT)
            _brick = brick.Brick(socket)

            _store_brick_in_memory(address, config.IP_SOCKET_PORT, _brick)

            return _brick
        except:
            raise error.BrickNotFoundException("Did you provide the correct ip address?")

    raise error.NoValidCommunicationChosenException("You must choose either ip or bluetooth as a communication option")


def find_brick_by_name(name, by_ip=True, by_bluetooth=True):
    if by_ip:
        try:
            socket = ipsocket.IpSocket()
            address = socket.get_address_by_hostname(hostname=name, port=config.IP_SOCKET_PORT)

            _MODULE_LOGGER.debug("Found brick with IP")

            if _is_brick_already_in_memory(address, config.IP_SOCKET_PORT):
                return _stored_brick(address, config.IP_SOCKET_PORT)

            socket.connect(address, config.IP_SOCKET_PORT)
            _brick = brick.Brick(socket)

            _store_brick_in_memory(address, config.BLUETOOTH_PORT, _brick)

            return _brick
        except error.BrickNotFoundException:
            pass

    if by_bluetooth:
        try:
            import bluetooth
            import bluesocket
            try:
                socket = bluesocket.BlueSocket()
                address = socket.get_address_by_hostname(hostname=name)

                _MODULE_LOGGER.debug("Found brick with bluetooth")

                if _is_brick_already_in_memory(address, config.BLUETOOTH_PORT):
                    return _stored_brick(address, config.BLUETOOTH_PORT)

                socket.connect(address, config.BLUETOOTH_PORT)
                _brick = brick.Brick(socket)

                _store_brick_in_memory(address, config.BLUETOOTH_PORT, _brick)

                return _brick
            except (error.BrickNotFoundException, bluetooth.BluetoothError):
                pass
        except (ImportError, IOError):
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
