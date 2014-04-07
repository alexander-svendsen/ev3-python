# -*- coding: utf-8 -*-
import os
import importlib


def delete_tmp():
    path = "./tmp/"
    [os.remove(path + f) for f in os.listdir(path) if f.endswith(".py")]


def load_module(name):
    name = "driver"
    mod = importlib.import_module(name)
    loaded_class = getattr(mod, 'DriveAround')
    instance = loaded_class()
    print instance.check()
    return instance




