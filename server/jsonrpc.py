# -*- coding: utf-8 -*-
import flask


def create_valid_response(response_id=None, result=None, error=None, jsonrpc_version='2.0'):
    response = {}
    if response_id is not None:
        response['id'] = response_id
    if error is not None:  # always return an error
        response['error'] = error
    elif result is not None:
        response['result'] = result

    response['jsonrpc'] = jsonrpc_version
    return flask.jsonify(response)


def register_remote_object(path, obj, app):

    @app.route(path, methods=['POST'])
    def jsonrpc(**kwargs):
        req = flask.request.json
        try:
            name = req['method']
            method = getattr(obj, name)

            params = req.get('params', [])
            if isinstance(params, dict):
                params.update(kwargs)
                result = method(**params)
            else:
                result = method(*params, **kwargs)

            if not isinstance(result, (list, dict, str, unicode, int, float, bool)):
                result = str(result)

            print "jsonrpc -", result
            return create_valid_response(req.get('id'), result)

        except AttributeError as e:
            error = {'code': -32601, 'message': 'Method not found'}
            return create_valid_response(req.get('id'), error=error)

        except TypeError as e:
            error = {'code': -32602, 'message': 'Invalid params'}
            return create_valid_response(req.get('id'), error=error)

        except Exception as e:
            error = {'code': -32000, 'message': e.message}
            return create_valid_response(req.get('id'), error=error)

