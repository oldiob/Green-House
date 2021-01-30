# SPDX-License-Identifier: GPL-2.0-only
#
# Copyright (C) 2020 Olivier Dion <olivier.dion@polymtl.ca>

import logging

from flask import Flask

app = Flask(__name__, static_folder="client",
            static_url_path="/client")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_spa(path):
    return app.send_static_file("index.html")
