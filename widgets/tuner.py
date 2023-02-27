from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget, QDial, QLabel


class Tuner(QWidget):
    minimum = 7000000
    maximum = 7300000
    def __init__(self, *args, **kwargs):
        super(Tuner, self).__init__(*args, **kwargs)
        self.frame = QFrame()
        self.frame.setMinimumSize(QSize(160, 160))
        self.frameLayout = QGridLayout(self.frame)
        self.tuneDial = QDial()
        self.tuneDial.setMinimum(self.minimum)
        self.tuneDial.setMaximum(self.maximum)
        self.tuneDial.setMinimumSize(QSize(160, 160))
        self.frameLayout.addWidget(self.tuneDial, 0, 0)
        self.freqLabel = QLabel()
        self.frameLayout.addWidget(self.freqLabel, 1, 0, 2, 1)
        self.freqLabel.setText("700000")
        self.setLayout(self.frameLayout)

