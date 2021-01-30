# SPDX-License-Identifier: GPL-2.0-only
#
# Copyright (C) 2020 Olivier Dion <olivier.dion@polymtl.ca>

import datetime
import logging

import gpiozero

from flask import Flask, request

app = Flask(__name__)

fans = gpiozero.LED(25)

fans.source       = None
fans.source_delay = 60

start_time = None
end_time   = None

@app.route("/air-exchanger", methods=["GET", "POST", "PUT", "DELETE"])
def air_exchanger():

        global fans
        global start_time
        global end_time

        response = {}

        logging.info(request.method);

        if "PUT" == request.method:
                fans.toggle()

        elif "POST" == request.method:

                begin = request.form["fbegin"]
                end   = request.form["fend"]

                try:
                        begin_hh, begin_mm = begin.split(':')
                        end_hh, end_mm     = end.split(':')

                        fans.source = gpiozero.TimeOfDay(datetime.time(int(begin_hh), int(begin_mm)),
                                                         datetime.time(int(end_hh), int(end_mm)), utc=False)
                except Exception as E:
                        logging.exception(E)
                        fans.source = None
                        start_time  = None
                        end_time    = None
                else:
                        start_time = begin
                        end_time   = end

        elif "DELETE" == request.method:
                fans.source = None
                start_time  = None
                end_time    = None

        response["start_time"] = start_time
        response["end_time"]   = end_time
        response["status"]     = "on" if fans.is_lit else "off",

        return response
