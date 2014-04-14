# -*- coding: utf-8 -*-

import requests
import json


def main():
    url = "http://127.0.0.1:80/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "add_brick",
        "params": ["10.0.1.1"],
        "jsonrpc": "2.0",
        "id": 1
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print response

if __name__ == "__main__":
    main()