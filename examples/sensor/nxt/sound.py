# -*- coding: utf-8 -*-

import ev3
import time

brick = ev3.connect_to_brick(address='10.0.1.1', port=9200)

sound_sensor = ev3.NXTSoundSensor(brick, 1)

print "db"
db = sound_sensor.get_db_mode()
print db.fetch_sample()
time.sleep(4)
print "dba"
dba = sound_sensor.get_dba_mode()
print dba.fetch_sample()
