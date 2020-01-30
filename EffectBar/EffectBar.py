from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QGroupBox
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
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
        comboList[3].clicked.connect(self.button3_clicked_change_value)
        comboList[4].clicked.connect(self.button4_clicked_change_value)

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(200)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()

    def button0_clicked_change_value(self):
        self.type = 0
        self.sentValue.emit(self.val, self.type)
        self.val += 1

    def button1_clicked_change_value(self):
        self.type = 1
        self.sentValue.emit(self.val, self.type)
        self.val += 1

    def button2_clicked_change_value(self):
        self.type = 2
        self.sentValue.emit(self.val, self.type)
        self.val += 1

    def button3_clicked_change_value(self):
        self.type = 3
        self.sentValue.emit(self.val, self.type)
        self.val += 1

    def button4_clicked_change_value(self):
        self.type = 4
        self.sentValue.emit(self.val, self.type)
        self.val += 1

# This line is for EffectStatusBar to EffectBar connection
    def return_connection(self, class_object):
        class_object.returnValue.connect(self.EffectStatusBar_Inter_EffectBar)

    @pyqtSlot(int)
    def EffectStatusBar_Inter_EffectBar(self, val):
        self.val = val
