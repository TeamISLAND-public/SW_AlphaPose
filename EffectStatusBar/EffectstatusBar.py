from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QAction, QPushButton, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from EffectStatusBar.RangeSlider import QRangeSlider

class EffectStatusBar(QTableWidget):
    sent_fix = pyqtSignal(bool, int, bool)
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        super().__init__()

        self.action_name = "Off Track"
        self.cell_right_clicked()

        self.setRowCount(0)
        self.setColumnCount(3)  #Setting this value because of effect_type and QRangeSlider

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setShowGrid(True)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.show()

    # popup link information
    def cell_right_clicked(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Track Delete", self)
        test_action = QAction("{}".format(self.action_name), self)
        self.addAction(delete_action)
        self.addAction(test_action)
        delete_action.triggered.connect(self.delete_effect_queue_list)

    #deleting effect list in the effectstatusbar
    def delete_effect_queue_list(self):
        for i in self.selectedItems():
            self.sent_fix.emit(True, i.row(), False)
            self.removeRow(i.row())

    # This line is for EffectBar to EffectStatusBar connection
    def effectbar_to_effectstatusbar(self, class_object):
        class_object.sent_type.connect(self.EffectBar_Inter_EffectStatusBar)

    # pyqtSlot for getting information about which effect was getting as a signal
    @pyqtSlot(str, int, int)
    def EffectBar_Inter_EffectStatusBar(self, type, current_frame, total_frame):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        # Inserting item and cellwidget

        self.setItem(currentRowCount, 0, QTableWidgetItem("{}".format(type)))
        self.setCellWidget(currentRowCount, 1, Toggle_Button(currentRowCount))
        self.setCellWidget(currentRowCount, 2, QRangeSlider(None, currentRowCount, current_frame, total_frame))
        self.horizontalHeader().setStretchLastSection(True)

class Toggle_Button(QPushButton):
    def __init__(self, currentRowCount):
        QPushButton.__init__(self, "ON")
        # self.setFixedSize(100, 100)
        self.currentRowCount = currentRowCount
        self.setStyleSheet("background-color: green")
        self.setCheckable(True)
        self.toggled.connect(self.slot_toggle)

    # when toggled connect initial state is True in order to make first click as OFF then True state must be red and OFF
    @pyqtSlot(bool)
    def slot_toggle(self, state):
        print(self.currentRowCount, state)
        self.setStyleSheet("background-color: %s" % ({True: "red", False: "green"}[state]))
        self.setText({True: "OFF", False: "ON"}[state])