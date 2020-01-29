from PyQt5.QtWidgets import QPushButton, QProgressBar, QScrollArea, QSlider, QListWidgetItem, QRadioButton, QAction
from PyQt5.QtWidgets import QTableWidget, QFormLayout, QAction, QGroupBox, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from EffectStatusBar.RangeSlider import QRangeSlider

class EffectStatusBar(QDialog):
    effect_queue_list = []
    delete_button_list = []
    returnValue = pyqtSignal(int)
    val = 0
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.formLayout =QFormLayout()
        groupBox = QGroupBox("EffectStatusBar")
        groupBox.setLayout(self.formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(200)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()

    def delete_button_finding(self, delete_list):
        for delete_button in delete_list:
            delete_button.clicked.connect(self.test)

    def cell_right_clicked(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Delete", self)
        self.addAction(delete_action)
        delete_action.triggered.connect(self.button0_clicked_change_value)

    def test(self):
        print('a')

    def button0_clicked_change_value(self):
        if self.delete_button_list == []:
            self.returnValue.emit(self.val)
        else:
            self.formlayout.removeRow(self.val)
            del self.delete_button[self.val]
            del self.effect_queue[self.val]
            print(self.delete_button)
            self.returnValue.emit(self.val)
            if self.val == 0:
                self.val = self.val
            else:
                self.val = self.val - 1
        print(self.val)

# This line is for EffectBar to EffectStatusBar connection
    def make_connection(self, class_object):
        class_object.sentValue.connect(self.EffectBar_Inter_EffectStatusBar)

    @pyqtSlot(int, int)
    def EffectBar_Inter_EffectStatusBar(self, val, type, effect_queue_list = effect_queue_list,
                                        delete_button_list = delete_button_list):
        # self.val = val
        # self.type = type
        # currentRowCount = self.rowCount()
        effect_queue_list.append(QRangeSlider())
        # delete_button_list.append(QPushButton("D"))
        # self.insertRow(currentRowCount)
        # self.setItem(0, currentRowCount, QTableWidgetItem)
        # self.effect_queue_list[val].setValue(val)
        # print(self.formlayout.itemAt(val))
        # self.layou
        self.formLayout.addWidget(effect_queue_list[val])
        A = 1