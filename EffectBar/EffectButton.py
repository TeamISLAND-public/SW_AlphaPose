from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QGroupBox
from PyQt5 import QtGui

from PyQt5.QtCore import pyqtSignal, QSize

class EffectBar(QDialog):
    sentValue = pyqtSignal(int, int)
    val = 0
    def __init__(self):
        super(EffectBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        formLayout =QFormLayout()
        groupBox = QGroupBox("Effect")
        labelLisName = ["Wipe Out Effect", "Sparkling GIF", "Scanning", "Extra", "IDK", "A"]
        labelLis = []
        comboList = []

        for i in  range(5):
            labelLis.append(QLabel("{}".format(labelLisName[i])))
            comboList.append(QPushButton(""))
            # comboList.append(QPushButton.setIcon(QtGui.QIcon('Image/Class diagram/torch_scanning.png')))
            formLayout.addRow(comboList[i], labelLis[i])

        comboList[0].clicked.connect(self.button0_clicked_change_value)
        comboList[1].clicked.connect(self.button1_clicked_change_value)
        comboList[2].clicked.connect(self.button2_clicked_change_value)
        comboList[3].clicked.connect(self.button0_clicked_change_value)
        comboList[4].clicked.connect(self.button0_clicked_change_value)

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(200)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()

    def button0_clicked_change_value(self):
        self.val += 1
        self.type = 0
        self.sentValue.emit(self.val, self.type)

    def button1_clicked_change_value(self):
        self.val += 1
        self.type = 1
        self.sentValue.emit(self.val, self.type)

    def button2_clicked_change_value(self):
        self.val += 1
        self.type = 2
        self.sentValue.emit(self.val, self.type)

