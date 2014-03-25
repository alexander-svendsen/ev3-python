# -*- coding: utf-8 -*-
import ev3, time
from ev3 import subscription

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)


def print_func(*args):
    print "Got a callback with args", args

sub = subscription.Subscription()
brick.set_subscription(sub)
# sub.subscribe_on_new_sensor(print_func)
print "ev1"
ev3_touch1 = ev3.EV3TouchSensor(brick, 1)  # should not raise an exception
print "first sensor connected"
nxt_touch = ev3.NXTTouchSensor(brick, 4)
print "second sensor connected"
time.sleep(5)
print "Complete"

#
# # while True:
# #     start = time.time()
# #     ev3_touch.get_raw_data()
# #     end = time.time() - start
# #     print "took: ", end
# # brick.close()
#
# # battery = brick.get_battery()
# # print battery.get_level()
# # print battery.get_message()
# # print battery.milli_voltage
# # time.sleep(5)
#
# mode = ev3_touch1.get_touch_mode()
# print mode.is_pressed()
# ev3_touch1.set_cache_data([1])
# print mode.is_pressed() # should be true noe
# print ev3_touch1.get_name()
# class MyClass(object):
#     def __init__(self, i):
#         print i
#         print "never called in this case"
#
#     def __new__(cls, *args, **kwargs):
#         print "HAHAHA"
#         return super(MyClass, cls).__new__(cls)
#
#     def haha(self):
#         print "muhhahaha"
#
# obj = MyClass(1)
# print obj
# obj.haha()