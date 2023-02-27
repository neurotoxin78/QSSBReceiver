from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget
from pyqtgraph import PlotWidget, mkPen


class GraphScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super(GraphScreen, self).__init__(*args, **kwargs)
        self.frame = QFrame()
        self.frameLayout = QGridLayout(self.frame)
        self.plot = PlotWidget()
        self.configurePlot()
        self.frameLayout.addWidget(self.plot)
        self.setLayout(self.frameLayout)


    def configurePlot(self):
        self.plot.setGeometry(QRect(0, 0, 10, 10))
        self.plot.setStyleSheet("background-color: transparent; color: #FB9902;")
        self.plot.setObjectName("upload_plot")
        background = QBrush()
        background.setColor(QColor(0x31363b))
        self.plot.setBackground(background)
        self.plot.plotItem.showGrid(x=True, y=True, alpha=0.8)
        self.plot.getPlotItem().addLegend()
        self.plot.getPlotItem().enableAutoRange(axis='y', enable=False)
        # self.plot.getPlotItem().invertY()
        # self.upload_plot.getPlotItem().invertX()
        self.imag = self.plot.plot(
            pen=mkPen('#009637', width=1, name="imag", symbolBrush=(0, 0, 200), symbolPen='w', symbol='o',
                         symbolSize=14,
                         style=Qt.SolidLine))
        self.plot.getPlotItem().hideAxis('bottom')
        self.plot.getPlotItem().hideAxis('left')
        #self.centralLayout.addWidget(self.plot, 0, 0)

