# SPDX-License-Identifier: GPL-2.0-only
#
# Copyright (C) 2020 Olivier Dion <olivier.dion@polymtl.ca>

import logging
import os
import threading
import time

import gpiozero

import Adafruit_DHT as dht

from flask import Flask

logging.basicConfig(level=logging.INFO)

vcc = gpiozero.LED(23)
vcc.on()

app          = Flask(__name__)
sensors_lock = threading.Lock()

average_humidity, average_temperature = dht.read_retry(dht.DHT22, 24)

alpha = 0.95

def update_sensors_values():

    global average_humidity, average_temperature

    while True:

        H, T = dht.read_retry(dht.DHT22, 24)

        if H is None or T is None:
            logging.warning("failed to read device")
            continue

        H = average_humidity    * alpha + (1 - alpha) * H
        T = average_temperature * alpha + (1 - alpha) * T

        with sensors_lock:
            average_humidity    = H
            average_temperature = T

        time.sleep(5)

threading.Thread(target=update_sensors_values,
                 daemon=True).start()

@app.route("/sensors", methods=["GET"])
def get_sensors_values():

    with sensors_lock:
        return {
            "humidity"    : average_humidity,
            "temperature" : average_temperature,
        }
