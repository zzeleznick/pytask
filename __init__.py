#!/usr/bin/env python
# coding=UTF-8
import os
from flask import Flask, render_template
# internals
from tasker import *

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/hi/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/')
def base():
    tasks = get(colored = False)
    return render_template('index.html', name = 'ZZ', TL = tasks)

if __name__ == '__main__':
    # app.config.from_object(os.environ['APP_SETTINGS'])
    app.run(debug = True)