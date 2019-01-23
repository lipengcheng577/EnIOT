from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QTextBrowser, QTableWidgetItem


class single_meter_widget(QtWidgets.QWidget):
    """description of class"""

    def __init__(self, name, meas_dict):
        QtWidgets.QWidget.__init__(self)
        self.name = name
        self.meas_dict = meas_dict
        self.grid = QGridLayout(self)

        self.meas_table = QTableWidget()
        self.meas_table.setRowCount( len(meas_dict))
        self.meas_table.setColumnCount(2)

        header = [ "量测名称", "值"]
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

    
        


