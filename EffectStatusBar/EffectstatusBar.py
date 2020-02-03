from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QAction, QApplication, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from EffectStatusBar.RangeSlider import QRangeSlider
import sys

class EffectStatusBar(QTableWidget):
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        super().__init__()
        self.setRowCount(0)
        self.setColumnCount(2)  #Setting this value because of effect_type and QRangeSlider
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(True)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.cell_right_clicked()
        self.show()

    # popup link information
    def cell_right_clicked(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Delete Effect", self)
        test_action = QAction("Test Action", self)
        self.addAction(delete_action)
        self.addAction(test_action)
        delete_action.triggered.connect(self.delete_effect_queue_list)

    #deleting effect list in the effectstatusbar
    def delete_effect_queue_list(self):
        for i in self.selectedItems():
            self.removeRow(i.row())

    # This line is for EffectBar to EffectStatusBar connection
    def make_connection(self, class_object):
        class_object.sent_type.connect(self.EffectBar_Inter_EffectStatusBar)

    # pyqtSlot for getting information about which effect was getting as a signal
    @pyqtSlot(int, int, int)
    def EffectBar_Inter_EffectStatusBar(self, type, current_frame, total_frame):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        self.setItem(currentRowCount, 0, QTableWidgetItem("{}{}{}".format(type,current_frame,total_frame)))   # Inserting item and cellwidget
        # QRangeSlider = self.QRangeSlider.setMax(total_frame)
        self.setCellWidget(currentRowCount, 1, QRangeSlider())
        self.horizontalHeader().setStretchLastSection(True)