# -*- coding: utf-8 -*-

import ev3
import pygame

pygame.init()
brick = ev3.connect_to_brick('00:16:53:3D:E4:77')
screen = pygame.display.set_mode((200, 200))
brick.buzz()
left_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_D)
right_motor = ev3.Motor(brick, ev3.MOTOR_PORTS.PORT_A)
left_motor.set_speed(700)
right_motor.set_speed(700)


def event_loop():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                left_motor.forward()
                right_motor.forward()
            elif event.key == pygame.K_RIGHT:
                left_motor.forward()
                right_motor.backward()

            elif event.key == pygame.K_LEFT:
                left_motor.backward()
                right_motor.forward()
            elif event.key == pygame.K_DOWN:
                left_motor.backward()
                right_motor.backward()
            elif event.key == pygame.K_SPACE:
                left_motor.stop(True)
                right_motor.stop()

while True:
    event_loop()


