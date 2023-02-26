import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, pyqtSignal, pyqtSlot, QObject, QThread
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget)
from source.sdrplay import SDRPlaySource
from tools import extended_exception_hook, get_config
from SoapySDR import *
from pyqtgraph import PlotWidget
import pyqtgraph as pg



class SDRHandler(QObject):
    running = False
    update_sample = pyqtSignal(str, object)
    sdr = SDRPlaySource()

    def run(self):
        while True:
            sr, samples = self.sdr.readStream()
            audio = samples.flatten().view('float32')
            self.update_sample.emit(str(sr.timeNs), audio)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Load the UI Page
        self.config = get_config()
        uic.loadUi('ui/receiver.ui', self)
        self.setWindowTitle("QSSB")

        # UPLOAD PLOT
        self.plot = PlotWidget()
        self.plot.setGeometry(QRect(0, 0, 10, 10))
        self.plot.setStyleSheet("background-color: transparent; color: #FB9902;")
        self.plot.setObjectName("upload_plot")
        background = QBrush()
        background.setColor(QColor(0x31363b))
        self.plot.setBackground(background)
        self.plot.plotItem.showGrid(x=True, y=True, alpha=0.8)
        self.plot.getPlotItem().addLegend()
        self.plot.getPlotItem().enableAutoRange(axis='x', enable=True)
        # self.plot.getPlotItem().invertY()
        # self.upload_plot.getPlotItem().invertX()
        self.imag = self.plot.plot(
            pen=pg.mkPen('#009637', width=1, name="imag", symbolBrush=(0, 0, 200), symbolPen='w', symbol='o',
                         symbolSize=14,
                         style=Qt.SolidLine))
        self.plot.getPlotItem().hideAxis('bottom')
        self.plot.getPlotItem().hideAxis('left')
        self.centralLayout.addWidget(self.plot, 0, 0)
        self.thread = QThread()
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

    @pyqtSlot(str, object)
    def updatePlot(self, sr, sample):
        self.imag.setData(sample)







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