from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal

from Library.test import test

class EffectBar(QDialog):

    sentValue = pyqtSignal(int)
    no_effect = 5

    def __init__(self):
        super(EffectBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        formLayout =QFormLayout()
        groupBox = QGroupBox("Effect")
        labelLisName = ["Wipe Out Effect", "Sparkling GIF", "Scanning", "Extra", "IDK", "A"]
        labelLis = []
        EffectList = []

        for i in  range(self.no_effect):
            labelLis.append(QLabel("{}".format(labelLisName[i])))
            EffectList.append(QPushButton(""))
            formLayout.addRow(EffectList[i], labelLis[i])

        # for the future code this can be abstracted as putting into a list
        EffectList[0].clicked.connect(self.effect0_clicked)
        EffectList[1].clicked.connect(self.effect1_clicked)
        EffectList[2].clicked.connect(self.effect2_clicked)
        EffectList[3].clicked.connect(self.effect3_clicked)
        EffectList[4].clicked.connect(self.effect4_clicked)

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()

    #This definition of effect's might be changed through such as while or for statement in the future
    def effect0_clicked(self):
        self.type = 0
        self.sentValue.emit(self.type)
        test()
        print(10001)

    def effect1_clicked(self):
        self.type = 1
        self.sentValue.emit(self.type)

    def effect2_clicked(self):
        self.type = 2
        self.sentValue.emit(self.type)

    def effect3_clicked(self):
        self.type = 3
        self.sentValue.emit(self.type)

    def effect4_clicked(self):
        self.type = 4
        self.sentValue.emit(self.type)