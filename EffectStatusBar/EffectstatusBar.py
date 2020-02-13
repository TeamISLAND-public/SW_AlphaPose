from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QAction, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

from EffectStatusBar.RangeSlider import QRangeSlider

class EffectStatusBar(QTableWidget):
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        super().__init__()
        self.action_name = "Off Track"
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
        delete_action = QAction("Track Delete", self)
        test_action = QAction("{}".format(self.action_name), self)
        self.addAction(delete_action)
        self.addAction(test_action)
        delete_action.triggered.connect(self.delete_effect_queue_list)

    #deleting effect list in the effectstatusbar
    def delete_effect_queue_list(self):
        for i in self.selectedItems():
            self.removeRow(i.row())

    # This line is for EffectBar to EffectStatusBar connection
    def effectbar_to_effectstatusbar(self, class_object):
        class_object.sent_type.connect(self.EffectBar_Inter_EffectStatusBar)

    # pyqtSlot for getting information about which effect was getting as a signal
    @pyqtSlot(int, int, int)
    def EffectBar_Inter_EffectStatusBar(self, type, current_frame, total_frame):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        # Inserting item and cellwidget
        self.setItem(currentRowCount, 0, QTableWidgetItem("{}{}{}".format(type,current_frame,total_frame)))
        self.setCellWidget(currentRowCount, 0, QPushButton())
        self.setCellWidget(currentRowCount, 1, QRangeSlider(None, current_frame, total_frame))
        self.horizontalHeader().setStretchLastSection(True)
