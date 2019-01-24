#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File Name:meter_mqtt_simu.py
# 模拟采用mqtt通信的电表，与fep_mqtt进行通信
# Python Version:2.7
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import json
import time
import datetime
import queue

from mainwindow import *

def start_window():
    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print('*********************\n  METER SIMU MQTT\n *********************\n')
    start_window()

