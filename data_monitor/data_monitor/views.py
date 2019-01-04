#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from data_monitor import app

import random
import json
import time


@app.route('/')
def data():
    devices = ["ddd1","ddd2", "ddd3"]
    data = []
    soc = int(time.time())*1000 - 5000*10
    for i in range(0, 10):
        utc = soc + i*1000
        val = random.uniform(1.0,10.0)
        data.append([utc, val])
    return render_template( 'curve.html', devs=devices, data=json.dumps(data) )
    #return render_template( 'curve.html', devs=devices)


@app.route('/new',methods=['GET'])
def getnew():
    soc = int(time.time())*1000
    top = [soc, random.uniform(1.0,10.0)]
    print top
    return json.dumps(top)
