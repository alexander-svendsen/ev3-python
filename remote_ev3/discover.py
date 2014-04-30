# -*- coding: utf-8 -*-
import ev3.error
import brick
import logging
import jsonrpc

_MODULE_LOGGER = logging.getLogger('ev3.discover')
_LOADED_BRICKS = {}


def _is_brick_already_in_memory(path, address):
    if (path, address) in _LOADED_BRICKS:
        return not _LOADED_BRICKS[(path, address)].closed
    return False


def _stored_brick(path, address):
    _MODULE_LOGGER.debug("Brick found in memory, returning stored instance")
    return _LOADED_BRICKS[(path, address)]


def _store_brick_in_memory(path, address, opened_brick):
    _LOADED_BRICKS[(path, address)] = opened_brick


def connect_to_brick(path, address):
    if _is_brick_already_in_memory(path, address):
        return _stored_brick(path, address)

    remote_object = jsonrpc.JsonRPCClient(path)
    if remote_object.call_method('add_brick', address):
        return brick.Brick(remote_object, address)
    raise ev3.error.BrickNotFoundException("Brick not found at that address")


def find_all_nearby_devices(path):
    remote_object = jsonrpc.JsonRPCClient(path)
    return remote_object.call_method('get_bricks')


def filter_devices_on_name(devices, name):
    return filter(lambda x: x[1].lower() == name.lower(), devices)


def find_all_bricks_with_name(path, name):
    remote_object = jsonrpc.JsonRPCClient(path)
    devices = remote_object.call_method('get_bricks_with_name')
    return filter_devices_on_name(devices, name)
