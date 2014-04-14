# -*- coding: utf-8 -*-
import functools
import ev3
import flask
import sys
import tools
import jsonrpc
import brickmanager
from behaviors import subsumption
import startup
import threading

# controller = subsumption.Controller(False)
# brick = ev3.connect_to_brick('10.0.1.1')

_brick_manager = brickmanager.BrickManager()
app = flask.Flask(__name__)


def status(code):
    response = flask.make_response()
    response.status_code = code
    response.data = response.status
    return response


@app.route('/')
def index():
    return flask.redirect(flask.url_for('static', filename='index.html'))


jsonrpc.register_new_remote_object('/jsonrpc', _brick_manager, app)


def main():
    # tools.delete_tmp()  review: uncomment when done
    startup.main()
    print "Starting websocket server"
    server = brickmanager.SimpleWebSocketServer('', 9999, functools.partial(brickmanager.SubscriptionSocket, _brick_manager))
    _thread = threading.Thread(name="receive_thread", target=server.serveforever, args=())
    _thread.daemon = True
    _thread.start()

    print "Starting flask main server"
    app.run(host='127.0.0.1', port=80)

if __name__ == "__main__":
    sys.exit(main())