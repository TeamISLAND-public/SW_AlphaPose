from PyQt5.QtWidgets import QPushButton, QProgressBar, QDialog, QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QFormLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSlot

class EffectStatusBar(QDialog):
    effect_queue = []
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.progressbar = QProgressBar()
        # layout = QHBoxLayout()
        # layout.addWidget(self.progressbar)
        # self.setLayout(layout)

        self.box = QVBoxLayout()
        self.setLayout(self.box)

        self.show()

    def make_connection(self, class_object):
        class_object.sentValue.connect(self.EffectBar_Inter_EffectStatusBar)

    @pyqtSlot(int, int)
    def EffectBar_Inter_EffectStatusBar(self, val, type, effect_queue=effect_queue):
        print(val,type)
        effect_queue.append(QProgressBar())
        self.box.addWidget(effect_queue[val])
        self.effect_queue[val].setValue(val)

