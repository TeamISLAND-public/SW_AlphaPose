import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QGroupBox, QCheckBox
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QGroupBox, QCheckBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

lst = [u"On", u"Off"]

class EffectBar(QWidget):
    def __init__(self):
        super(EffectBar, self).__init__()
        # window_width = 1200
        # window_height = 600
        # self.setFixedSize(window_width, window_height)
        self.initUI()

    def createLayout_group(self, number):
        sgroupbox = QGroupBox("Effect No.{}:".format(number), self)
        layout_groupbox = QVBoxLayout(sgroupbox)
        effect_button = QPushButton('Activate',sgroupbox)
        layout_groupbox.addWidget(effect_button)
        effect_button.clicked.connect(self.on_click)
        # effect_2 = QPushButton('b', sgroupbox)
        # layout_groupbox.addWidget(effect_2)

        # for i in range(len(lst)):
        #     item = QCheckBox(lst[i], sgroupbox)
        #     layout_groupbox.addWidget(item)
        #     item.stateChanged.connect(self.CheckBoxState)
            # print(item)
        layout_groupbox.addStretch(1)
        return sgroupbox

    @pyqtSlot()
    def on_click(self):
        sender = self.sender()
        print(sender.text())

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self)
        # self.scrollarea.setFixedHeight(150)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        for i in range(2):
            self.layout_SArea.addWidget(self.createLayout_group(i))
        self.layout_SArea.addStretch(1)

    def initUI(self):
        self.createLayout_Container()
        self.layout_All = QGridLayout(self)
        self.layout_All.addWidget(self.scrollarea)
        self.show()