from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QScrollArea, QFormLayout, QLabel, QGroupBox, QTabWidget, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from Library.detectron2.demo.run_demo import run_demo

class EffectBar(QDialog):
    sent_type = pyqtSignal(str, int, int)
    sent_video = pyqtSignal(list, int)
    no_effect = 3

    def __init__(self):
        super(EffectBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.clicked_positions = []
        self.demo = []
        self.video_name = []

        self.layout = QVBoxLayout()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "HOT")
        self.tabs.addTab(self.tab2, "2020")
        widget = QWidget()

        # Create first tab
        formLayout1 = QFormLayout(widget)
        self.labelLisName1 = ["Wipe Out Effect", "Sparkling GIF", "Scanning", "Extra", "IDK", "A"]
        labelLis1, EffectList1 = [], []

        for i in range(self.no_effect):
            labelLis1.append(QLabel("{}".format(self.labelLisName1[i])))
            EffectList1.append(QPushButton(""))
            formLayout1.addRow(EffectList1[i], labelLis1[i])

        # for the future code this can be abstracted as putting into a list
        EffectList1[0].clicked.connect(lambda: self.effect_clicked(0))
        EffectList1[1].clicked.connect(lambda: self.effect_clicked(1))
        EffectList1[2].clicked.connect(lambda: self.effect_clicked(2))

        scroll1 = QScrollArea()
        scroll1.setLayout(formLayout1)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(scroll1)
        self.tab1.setLayout(self.tab1.layout)

        #Create second tab
        formLayout2 = QFormLayout(widget)
        labelLisName2 = ["A", "B", "C", "D", "E", "F"]
        labelLis2, EffectList2 = [], []

        for i in range(self.no_effect):
            labelLis2.append(QLabel("{}".format(labelLisName2[i])))
            EffectList2.append(QPushButton(""))
            formLayout2.addRow(EffectList2[i], labelLis2[i])

        # for the future code this can be abstracted as putting into a list
        EffectList2[0].clicked.connect(lambda: self.effect_clicked(0))
        EffectList2[1].clicked.connect(lambda: self.effect_clicked(1))
        EffectList2[2].clicked.connect(lambda: self.effect_clicked(2))


        scroll2 = QScrollArea()
        scroll2.setLayout(formLayout2)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(scroll2)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.show()

    #This definition of effect's might be changed through such as while or for statement in the future
    def effect_clicked(self, index):
        self.type = index
        if not self.video_name:
            print("no Video_name")
            return
        else:
            self.demo = run_demo(self.video_name, self.type, self.current_frame, self.clicked_positions).run()

        if not self.demo:
            print("no Demo")
            self.clicked_positions.clear()
            return
        else:
            self.sent_type.emit(self.labelLisName1[self.type], self.current_frame, self.total_frame)
            self.sent_video.emit(self.demo, self.current_frame)
            self.clicked_positions.clear()

    def playbar_to_effectbar(self, class_object):
        class_object.sent_current_frame.connect(self.PlayBar_Inter_EffectBar)

    def main_to_effectbar(self, class_object):
        class_object.sent_video_name.connect(self.MainGui_Inter_EffectBar)

    def videobar_to_effectbar(self, class_object):
        class_object.sent_position.connect(self.VideoBar_Inter_EffectBar)

    @pyqtSlot(str)
    def MainGui_Inter_EffectBar(self, video_name):
        self.video_name = video_name

    @pyqtSlot(int, int)
    def PlayBar_Inter_EffectBar(self, current_frame, total_frame):
        self.current_frame = current_frame
        self.total_frame = total_frame

    @pyqtSlot(list)
    def VideoBar_Inter_EffectBar(self, clicked_positions):
        self.clicked_positions = clicked_positions
        print(self.clicked_positions)