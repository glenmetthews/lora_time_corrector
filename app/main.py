import time

import websocket
import json
import re
import rel
import os
import logging
from websocket import WebSocket
from datetime import datetime

import utils

def on_open(ws: WebSocket):
    request = {
        "cmd": "auth_req",
        "login": os.getenv('USER'),
        "password": os.getenv('PASSWORD')
    }

    ws.send(json.dumps(request))


def on_message(ws: WebSocket, message):
    msg_json = json.loads(message)

    if 'data' in msg_json:
        if re.match(r'^03\w{8}$', msg_json["data"]):
            logging.info(f"Запрос времени от {msg_json['devEui']}, с датой {datetime.fromtimestamp(int(msg_json['data'][2:], 16))}")
            if utils.check_request_time(request_time=msg_json["data"][2:]):
                utils.send_time_package(ws, dev_eui=msg_json['devEui'], request_time=msg_json["data"][2:])
                logging.info(f"Время скорректировано. DevEui = {msg_json['devEui']}.")
            logging.info(f"Диапазон корректировки не превышен. Корректировка не требуется.")
        if re.match(r'^03$', msg_json["data"]):
            logging.info(f"Запрос времени от {msg_json['devEui']}.")
            utils.send_time_package(ws, dev_eui=msg_json['devEui'])
            logging.info(f"Время скорректировано. DevEui = {msg_json['devEui']}")


def on_error(ws: WebSocket, error):
    print(error)


def on_close(ws: WebSocket):
    print("Connection closed")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(asctime)s | %(message)s")

    ws = websocket.WebSocketApp(
        url=f"ws://{os.getenv('HOST')}:{os.getenv('PORT')}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    logging.info(f"Time corrector is running")
    ws.run_forever(dispatcher=rel, reconnect=5)

    rel.signal(2, rel.abort)
    rel.dispatch()

