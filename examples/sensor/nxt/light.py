import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1')

light_sensor = ev3.NXTLightSensor(brick, 1)

print "red"
red = light_sensor.get_red_mode()
print red.fetch_sample()
time.sleep(4)
print "ambient"
ambient = light_sensor.get_ambient_mode()
print ambient.fetch_sample()
