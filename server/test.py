

##CODE for testing in the web browser

class AvoidColliding(Behavior):
    def __init__(self):
        self._brick = ev3.connect_to_brick('10.0.1.1')
        self.left_motor = ev3.Motor(self._brick, ev3.MOTOR_PORTS.PORT_D)
        self.right_motor = ev3.Motor(self._brick, ev3.MOTOR_PORTS.PORT_A)
        self.ultrasonic = ev3.EV3UltrasonicSensor(self._brick, ev3.SENSOR_PORTS.PORT_1).get_distance_mode()
        self.ignore_test = True

    def check(self):
        distance = self.ultrasonic.fetch_sample()[0]
        if distance < 0.25 and distance != -1:  # returns meter
            return True
        return False

    def action(self):
        self.left_motor.rotate(600, immediate_return=True)
        self.right_motor.rotate(-600)

    def suppress(self):
        pass

class DriveAround(Behavior):
    def __init__(self):
        self.brick = ev3.connect_to_brick('10.0.1.1')
        self.left_motor = ev3.Motor(self.brick, ev3.MOTOR_PORTS.PORT_D)
        self.right_motor = ev3.Motor(self.brick, ev3.MOTOR_PORTS.PORT_A)
        self._running = True

    def check(self):
        return True

    def action(self):
        self._running = True
        self.right_motor.forward()
        self.left_motor.forward()
        while self._running:
            pass
        self.right_motor.stop(immediate=True)
        self.left_motor.stop()

    def suppress(self):
        self._running = False