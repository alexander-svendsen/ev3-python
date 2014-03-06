# -*- coding: utf-8 -*-

# All genereic sensor types should go here.
# In other words the actual sensors don't go here as this is only a catagorization of all the available

# These method has a two step communication procedure for discovery and assignment of the correct sensortype.
# you can be more efficent by using the correct sensor type from the beginning instead of these generics ones.


class Gyro:
    def __init__(self):
        pass


class Touch():
    def __init__(self):
        #Evry Compatable sensor inside Touch, point to correct one
        pass


class Ultrasonic:
    pass

class Sound:
    pass

class Light:
    pass

class Color:
    pass
