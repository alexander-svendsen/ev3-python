# -*- coding: utf-8 -*-
import time
import ev3
from ev3 import subsumption


class DriveAround(subsumption.Behavior):
    def __init__(self, brick):
        self.left_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_D)
        self.right_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_A)
        self._running = True

    def check(self):
        return True

    def action(self):
        self._running = True
        self.right_motor.forward()
        self.left_motor.forward()
        while self._running:
            time.sleep(1)
        self.right_motor.stop(immediate=True)
        self.left_motor.stop()

    def suppress(self):
        self._running = False


class AvoidColliding(subsumption.Behavior):
    def __init__(self, brick):
        self._brick = brick
        self.left_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_D)
        self.right_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_A)
        self.ultrasonic = ev3.EV3UltrasonicSensor(brick, ev3.SENSOR_PORTS.PORT_1).get_distance_mode()
        self.ignore_test = True

    def check(self):
        print "DISTANCE:", self.ultrasonic.fetch_sample()[0]
        distance = self.ultrasonic.fetch_sample()[0]
        if distance < 0.25 and distance != -1:  # returns meter
            return True
        return False

    def action(self):
        self.left_motor.rotate(600, immediate_return=True)
        self.right_motor.rotate(-600)

    def suppress(self):
        pass


if __name__ == "__main__":
    brick = ev3.connect_to_brick('00:16:53:3D:E4:77')
    brick.buzz()
    conjecture = subsumption.Controller(True)

    avoid = AvoidColliding(brick)
    drive = DriveAround(brick)

    conjecture.add(avoid)
    conjecture.add(drive)
    conjecture.start()

    brick.beep() # we are complete