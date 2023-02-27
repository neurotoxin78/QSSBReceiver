import sys
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget)
from collections import deque
from handlers.receiver import SDRHandler
from tools import extended_exception_hook, get_config
from widgets.graphs import GraphScreen
from widgets.tuner import Tuner


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI Page
        self.config = get_config()
        uic.loadUi('ui/receiver.ui', self)
        self.setWindowTitle("QSSB")

        # UPLOAD PLOT
        self.graphscreen = GraphScreen()
        self.centralLayout.addWidget(self.graphscreen, 0, 0)
        self.tuner = Tuner()
        self.centralLayout.addWidget(self.tuner, 0, 1, 2, 2)
        self.tuner.tuneDial.valueChanged.connect(self.Tune)
        self.thread = QThread()
        self.configureThread()



    @pyqtSlot(object, object)
    def updatePlot(self, sr, sample):

        self.graphscreen.imag.setData(sample.real)
        # pass

    def Tune(self):
        self.sdrHandler.sdr.frequency = self.tuner.tuneDial.value()
        self.tuner.freqLabel.setText(str(self.tuner.tuneDial.value()))

    def configureThread(self):
        # create object which will be moved to another thread
        self.sdrHandler = SDRHandler()
        # move object to another thread
        self.sdrHandler.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        self.sdrHandler.update_sample.connect(self.updatePlot)
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.sdrHandler.run)
        # start thread
        self.thread.start()




def main():
    config = get_config()
    sys._excepthook = sys.excepthook
    sys.excepthook = extended_exception_hook
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    main_window = MainWindow()
    monitor = QDesktopWidget().screenGeometry(config['display']['output_display'])
    main_window.move(monitor.left(), monitor.top())
    #main_window.showFullScreen()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()