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
    data = []
    soc = int(time.time())*1000 - 5000*10
    for i in range(0, 10):
        utc = soc + i*1000
        val = random.uniform(1.0,10.0)
        data.append([utc, val])
    return render_template('curve.html',data=json.dumps(data))


@app.route('/new',methods=['GET'])
def getnew():
    soc = int(time.time())*1000
    top = [soc, random.uniform(1.0,10.0)]
    print top
    return json.dumps(top)
