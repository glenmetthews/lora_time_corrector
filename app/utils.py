import json
import time
import os


def get_hex_timestamp():
    now_timestamp = int(time.time())
    hex_str = f'{now_timestamp:x}'
    return hex_str


def check_request_time(request_time: str):
    return abs(int(time.time()) - int(request_time, 16)) > int(os.getenv('DELAY'))


def generate_time_package(dev_eui: str, port: int = 60, ack: bool = False, request_time: str = str()):
    return {
        "cmd": "send_data_req",
        "data_list": [
            {
                "devEui": dev_eui,
                "data": f'03{get_hex_timestamp()}{request_time}',
                "port": port,
                "ack": ack
            }
        ]
    }


def send_time_package(ws, dev_eui, request_time: str = None):
    if request_time:
        response = generate_time_package(dev_eui=dev_eui, request_time=request_time)
    else:
        response = generate_time_package(dev_eui=dev_eui)
    ws.send(json.dumps(response))
