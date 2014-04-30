# -*- coding: utf-8 -*-
import logging

# create logger
logger = logging.getLogger('ev3')  # Top module logger
# logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(levelname)s - %(asctime)s - %(name)s - %(funcName)s - %(message)s')

channel = logging.StreamHandler()
channel.setLevel(logging.DEBUG)
channel.setFormatter(formatter)

logger.addHandler(channel)

from discover import connect_to_brick, find_brick_by_name, find_all_nearby_devices
import discover

from brick import Brick
from motor import MOTOR_PORTS, Motor
from sensors import *
from subscription import Subscription
from error import *
