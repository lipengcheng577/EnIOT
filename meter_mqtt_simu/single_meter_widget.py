from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTextBrowser, QTableWidgetItem

import json, time
import queue

MQTT_UP_QUEUE = queue.Queue(maxsize = 1000)

class single_meter_widget(QtWidgets.QWidget):
    """description of class"""

    def __init__(self, id, name, meas_dict):
        QtWidgets.QWidget.__init__(self)
        self.id = id
        self.name = name
        self.meas_dict = meas_dict
        self.grid = QGridLayout(self)

        self.meas_table = QTableWidget()
        self.meas_table.setRowCount( len(meas_dict))
        self.meas_table.setColumnCount(2)

        header = [ "量测名称", "值" ]
        self.meas_table.setHorizontalHeaderLabels(header)

        self.grid.addWidget(self.meas_table, 0, 0, 1, 1)

        self.frame_show = QTextBrowser()
        self.grid.addWidget(self.frame_show, 0, 1, 1, 1)

        row = 0
        for meas in self.meas_dict:
            item = QTableWidgetItem(meas)
            self.meas_table.setItem(row, 0, item)

            item = QTableWidgetItem(self.meas_dict[meas])
            self.meas_table.setItem(row, 1, item)

            row += 1


    def show_msg(self, msg):
        self.frame_show.append(msg)


    def get_data(self):
        row_count = self.meas_table.rowCount()

        data = {}

        data['id'] = self.id

        soc = int(time.time())
        timestruct = time.localtime(soc)
        timestring = time.strftime("'%Y-%m-%d %H:%M:%S'", timestruct)
        
        data['soc'] = soc
        data['date_time'] = timestring
        for i in range(0, row_count):
            meas_name = self.meas_table.item(i,0).text()
            meas_val = self.meas_table.item(i,1).text()
            data[meas_name] = float(meas_val)

        z = data['ua']*data['ia'] + data['ub']*data['ib'] + data['uc']*data['ic']
        p = data['cos'] * z
        q = data['cos'] * z 
        data['z'] = z
        data['p'] = p
        data['q'] = q
        self.show_msg(json.dumps(data))
        MQTT_UP_QUEUE.put(json.dumps(data))


    
        


