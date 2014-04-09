# -*- coding: utf-8 -*-
import flask
import sys
import tools
from behaviors import subsumption

controller = subsumption.Controller(False)
app = flask.Flask(__name__)


def status(code):
    response = flask.make_response()
    response.status_code = code
    response.data = response.status
    return response


@app.route('/')
def index():
    controller.add(subsumption.Behavior())
    print str(controller.behaviors)
    return flask.redirect(flask.url_for('static', filename='index.html'))


@app.route('/test')
def test():
    return str(controller.behaviors)


def main():
    # tools.delete_tmp()  review: uncomment when done
    app.debug = True
    app.run(host='127.0.0.1', port=80)

if __name__ == "__main__":
    sys.exit(main())