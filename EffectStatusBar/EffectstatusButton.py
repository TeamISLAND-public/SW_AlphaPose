from PyQt5.QtWidgets import QDialog, QProgressBar, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

class EffectStatusBar(QDialog):

    def __init__(self):
        super(EffectStatusBar, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Creating a label

        progressLabel = QLabel('Progress Bar:', self)

        # Creating a progress bar and setting the value limits

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)

        # Creating a Horizontal Layout to add all the widgets

        self.hboxLayout = QHBoxLayout(self)  # Adding the widgets
        self.hboxLayout.addWidget(progressLabel)
        self.hboxLayout.addWidget(self.progressBar)
        # Setting the hBoxLayout as the main layout

        self.setLayout(self.hboxLayout)
        self.show()

    def make_connection(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value)

    @pyqtSlot(int)  # pyqtSlot 이 있을때만 실행된다
    def get_slider_value(self, val):
        self.progressBar.setValue(val)