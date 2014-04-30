# -*- coding: utf-8 -*-
import json
import requests

#TODO: error fixes
class JsonRPCClient(object):
    def __init__(self, path):
        self.url = path
        self.headers = {'content-type': 'application/json'}
        self.payload = {
            'jsonrpc': '2.0',
            'id': 1
        }

    def call_method(self, name, *params):
        self.payload['method'] = name
        self.payload['params'] = params
        return requests.post(self.url, data=json.dumps(self.payload), headers=self.headers).json()
