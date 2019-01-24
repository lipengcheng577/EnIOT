
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer
import sys
import os
from single_meter_widget import *
import configparser
import queue, json, time, datetime
from my_mqtt import *


qtCreatorFile = "meter_mqtt.ui" # Enter file here.
ui_widget, QtBaseClass = uic.loadUiType(qtCreatorFile)

class mainwindow(QtWidgets.QWidget, ui_widget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        ui_widget.__init__(self)
        self.setupUi(self)

        self.toolButtonStart.setIcon( QIcon( "images//start.png" ) );
        self.init_meter_list()

        self.meter_state = False
        self.toolButtonStart.clicked.connect(self.start_meter)

        self.counter = 1
        self.timer = QTimer()      
        self.timer.setInterval(100)       
        self.timer.start()
         # 信号连接到槽       
        self.timer.timeout.connect(self.onDelMsgQueue)

        self.mqt = my_mqtt()
       

    def init_meter_list(self):
        self.toolBoxDevList.removeItem(0)

        self.read_config()

        self.sm_widgets = {}
        for meter_id in self.meters_dict:
            sm_wdgt = single_meter_widget(meter_id, self.meters_name[meter_id], self.meters_dict[meter_id])
            self.sm_widgets[meter_id] = sm_wdgt
            self.toolBoxDevList.addItem(sm_wdgt, self.meters_name[meter_id])


    def read_config(self):
        print('read simu dev config start ...')

        config = configparser.ConfigParser()

        try:
            config.read("./config.ini", encoding='utf-8')
        except IOError:
            print("打开config.ini 失败！")
            return


        self.meters_dict = {}
        self.meters_name = {}
        meters = config.sections()
        for meter in meters:
            meases = config.items(meter)
            meas_dict = {}
            id = int(meter)
            for meas in meases:    
                if meas[0] == "name":
                    self.meters_name[id] = meas[1]
                else:
                    meas_dict[meas[0]] = meas[1]

            self.meters_dict[id] = meas_dict        


    def start_meter(self):
        host = self.lineEditHost.text()
        port = int(self.lineEditPort.text())

        if self.meter_state == True:
            self.meter_state = False
            self.toolButtonStart.setIcon( QIcon( "images//start.png" ) );
            self.append_msg('停止通信')

            self.mqt.stop()
        else:
            ret = self.mqt.start(host, port)
            if ret != 0:
                QMessageBox.critical(self,"Error", "请检查host和port是否正确!") 
                return

            self.meter_state = True
            self.toolButtonStart.setIcon( QIcon( "images//stop.png" ) );
            self.append_msg('启动通信')


    def append_msg(self, msg):
        self.textBrowserMsg.append(msg)


    def onDelMsgQueue(self):
        while not MQTT_DOWN_QUEUE.empty():
            msg = MQTT_DOWN_QUEUE.get()
            request = json.loads(msg.payload.decode())

            soc = int(time.time())
            timestruct = time.localtime(soc)
            timestring = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
           
            if "id" in request.keys():
                meter_id = request["id"]
                if meter_id in self.sm_widgets.keys():
                    if 'heart' in request.keys():
                        self.append_msg( "%s 心跳报文, id = %d" % (timestring, meter_id) )
                        self.sm_widgets[meter_id].show_msg( "%s 心跳报文" % (timestring) )
                    else:
                        self.append_msg( "%s 召唤数据, id = %d" % (timestring, meter_id) )
                        self.sm_widgets[meter_id].show_msg( "%s 召唤数据" % (timestring) )
                        self.sm_widgets[meter_id].get_data()

                        #data = {}
                        #data["p"] = curr.minute
                        #data["q"] = curr.second
                        #data['id'] = DEV_ID
                        #data['soc'] = soc
                        #data['date_time'] = timestring
                        #self.client.publish(MQTT_PUB_CHANNEL, json.dumps(data))
                else:
                    self.append_msg( "设备ID不在列表中 id = %d", meter_id )
            else:
                self.append_msg("WWWWWWWWWW")
        
        while not MQTT_UP_QUEUE.empty():
            msg = MQTT_UP_QUEUE.get()
            self.mqt.publish(msg)

        

            
     
