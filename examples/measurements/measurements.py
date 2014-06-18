# -*- coding: utf-8 -*-
import ev3
import time

print "setup"
brick = ev3.connect_to_brick(address='10.0.1.1')

# sub = ev3.Subscription(subscribe_on_sensor_changes=False, subscribe_on_sample_data=True)
# brick.set_subscription(sub)
# ultrasonic_1 = ev3.EV3UltrasonicSensor(brick, 1)
# touch = ev3.EV3TouchSensor(brick, 2)
# gyro = ev3.EV3GyroSensor(brick, 3)
# ultrasonic_2 = ev3.EV3UltrasonicSensor(brick, 4)

print brick.ping()
print "starting"
requests = []
for i in range(1000):
    # time.sleep(10)
    start = time.time()
    brick.ping()
    end = time.time() - start
    print "Time " + str(i) + " took:", end
    # requests.append(str(end) + '\n')

# print "writing to file"
# with open('request.csv', 'w') as fp:
#     fp.writelines(requests)

print "Complete"