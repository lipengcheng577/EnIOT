
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
import sys
import os
from single_meter_widget import single_meter_widget
import configparser
#from main import Ui_Main


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
       

    def init_meter_list(self):
        self.toolBoxDevList.removeItem(0)

        self.read_config()

        for meter in self.meters_dict:
            sm_wdgt = single_meter_widget(meter, self.meters_dict[meter])
            self.toolBoxDevList.addItem(sm_wdgt, meter)


    def read_config(self):
        print('read simu dev config start ...')

        config = configparser.ConfigParser()

        try:
            config.read("./config.ini", encoding='utf-8')
        except IOError:
            print("打开config.ini 失败！")
            return


        self.meters_dict = {}
        meters = config.sections()
        for meter in meters:
            meases = config.items(meter)
            meas_dict = {}
            for meas in meases:
                meas_dict[meas[0]] = meas[1]
            self.meters_dict[meter] = meas_dict

    def start_meter(self):
        if self.meter_state == True:
            self.meter_state = False
            self.toolButtonStart.setIcon( QIcon( "images//start.png" ) );
            self.append_msg('停止通信')
        else:
            self.meter_state = True
            self.toolButtonStart.setIcon( QIcon( "images//stop.png" ) );
            self.append_msg('启动通信')

    def append_msg(self, msg):
        self.textBrowserMsg.append(msg)

            
     
