# -*- coding: utf-8 -*-
import logging
import sys
# create logger
logger = logging.getLogger('manager')  # Top module logger
# logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(levelname)s - %(asctime)s - %(name)s - %(funcName)s - %(message)s')

channel = logging.StreamHandler()
channel.setLevel(logging.DEBUG)
channel.setFormatter(formatter)

logger.addHandler(channel)

# import asynchronous
# import brick
# sys.modules['ev3.brick'] = sys.modules.pop('manager.brick')
