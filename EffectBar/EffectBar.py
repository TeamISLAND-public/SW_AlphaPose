from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from Library.detectron2.demo.run_demo import run_demo

class EffectBar(QDialog):

    sent_type = pyqtSignal(int, int, int)
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
        self.sent_type.emit(self.type, self.current_frame, self.total_frame)
        print(self.video_name)
        self.demo = run_demo(self.video_name, self.type)
        # print(self.current_frame)
        # test()

    def effect1_clicked(self):
        self.type = 1
        self.sent_type.emit(self.type, self.current_frame, self.total_frame)
        self.demo = run_demo(self.video_name, self.type)

    def effect2_clicked(self):
        self.type = 2
        self.sent_type.emit(self.type, self.current_frame, self.total_frame)
        self.demo = run_demo(self.video_name, self.type)

    def effect3_clicked(self):
        self.type = 3
        self.sent_type.emit(self.type, self.current_frame, self.total_frame)
        self.demo = run_demo(self.video_name, self.type)

    def effect4_clicked(self):
        self.type = 4
        self.sent_type.emit(self.type, self.current_frame, self.total_frame)
        self.demo = run_demo(self.video_name, self.type)

    def playbar_to_effectbar(self, class_object):
        class_object.sent_current_frame.connect(self.PlayBar_Inter_EffectBar)

    def main_to_effectbar(self, class_object):
        class_object.sent_video_name.connect(self.MainGui_Inter_EffectBar)

    @pyqtSlot(str)
    def MainGui_Inter_EffectBar(self, video_name):
        self.video_name = video_name

    @pyqtSlot(int, int)
    def PlayBar_Inter_EffectBar(self, current_frame, total_frame):
        self.current_frame = current_frame
        self.total_frame = total_frame