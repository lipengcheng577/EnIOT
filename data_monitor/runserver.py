"""
This script runs the data_monitor application using a development server.
"""

#from data_monitor import app

#if __name__ == '__main__':
#    app.run('localhost', 5555)


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
