# -*- coding: utf-8 -*-
import functools
import sys
import threading

import flask

import ev3
import jsonrpc
import brickmanager
from lib.simplewebsocketserver import SimpleWebSocketServer


_brick_manager = brickmanager.BrickManager()

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # todo remove in the future


def status(code):
    response = flask.make_response()
    response.status_code = code
    response.data = response.status
    return response


@app.route('/')
def index():
    return flask.redirect(flask.url_for('static', filename='index.html'))


jsonrpc.register_remote_object('/brick_manager', _brick_manager, app)


def main():
    # brick = ev3.connect_to_brick('10.0.1.1')
    # ultrasonic = ev3.EV3UltrasonicSensor(brick, 1)
    # touch = ev3.EV3TouchSensor(brick, 4)
    # _brick_manager.add_brick('10.0.1.1')
    print "Starting websocket server"
    web_socket = functools.partial(brickmanager.SubscriptionSocket, _brick_manager)
    server = SimpleWebSocketServer('', 9999, web_socket)
    _thread = threading.Thread(name="receive_thread", target=server.serveforever, args=())
    _thread.daemon = True
    _thread.start()

    print "Starting flask main server"
    app.run(host='127.0.0.1', port=80)


if __name__ == "__main__":
    sys.exit(main())