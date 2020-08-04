#!/usr/bin/env python3

import flask
from search import search
from flask import *
import pathlib
name = 'foo'
app = Flask(__name__)


@app.route("/<query>")
def main(query=""):
    return render_template("index.html", this=list(search(query)))


app.run()
