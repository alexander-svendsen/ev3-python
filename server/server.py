# -*- coding: utf-8 -*-
import ev3
import flask
import sys
import tools
import flask_jsonrpc
import brickmanager
from behaviors import subsumption


# controller = subsumption.Controller(False)
brick = ev3.connect_to_brick('10.0.1.1')
app = flask.Flask(__name__)


def status(code):
    response = flask.make_response()
    response.status_code = code
    response.data = response.status
    return response


@app.route('/')
def index():
    return flask.redirect(flask.url_for('static', filename='index.html'))


flask_jsonrpc.register('/jsonrpc/<identifier>', brickmanager.BrickManager(), app)


def main():
    # tools.delete_tmp()  review: uncomment when done
    app.run(host='127.0.0.1', port=80)

if __name__ == "__main__":
    sys.exit(main())