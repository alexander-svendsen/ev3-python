# -*- coding: utf-8 -*-

# import manager
# import ev3
# import time
#
# #When a bricks has been connected, the server should be active
# ev3.connect_to_brick('10.0.1.1')
#
# print "Waiting"
# time.sleep(100)  # server should be up until this is complete
# print "The End"


import requests
import json


def main():
    url = "http://127.0.0.1:80/jsonrpc/10"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "get_battery",
        "params": ["er feit"],
        "jsonrpc": "2.0",
        "id": 1
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    # assert response["id"] == 0
    print response

if __name__ == "__main__":
    main()