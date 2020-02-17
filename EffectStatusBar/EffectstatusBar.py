from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QAction, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor
from EffectStatusBar.RangeSlider import QRangeSlider


class EffectStatusBar(QTableWidget):
    sent_fix = pyqtSignal(bool, int, list)
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        super().__init__()

        self.setRowCount(0)
        self.setColumnCount(3)  #Setting this value because of effect_type and QRangeSlider

        self.setShowGrid(True)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        self.action_name = "Off Track"
        self.cell_right_clicked()

        self.stateList = []
        self.cellClicked.connect(self.test)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
            self.sent_fix.emit(True, i.row(), [False])
            del self.stateList[i.row()]
            self.removeRow(i.row())

    # This line is for EffectBar to EffectStatusBar connection
    def effectbar_to_effectstatusbar(self, class_object):
        class_object.sent_type.connect(self.EffectBar_Inter_EffectStatusBar)

    # pyqtSlot for getting information about which effect was getting as a signal
    @pyqtSlot(str, int, int)
    def EffectBar_Inter_EffectStatusBar(self, type, current_frame, total_frame):
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        self.stateList.append(True)
        # Inserting item and cellwidget
        self.setItem(currentRowCount, 0, QTableWidgetItem("{}".format(type)))
        self.setItem(currentRowCount, 1, QTableWidgetItem())
        self.item(currentRowCount, 1).setBackground(QColor(34,139,34))
        self.setCellWidget(currentRowCount, 2, QRangeSlider(None, currentRowCount, current_frame, total_frame))
        self.horizontalHeader().setStretchLastSection(True)

    @pyqtSlot(int, int)
    def test(self, row, col):
        if col == 1:
            if self.stateList[row] == True:
                self.stateList[row] = False
                self.item(row, col).setBackground(QColor(139,0,0))
                # self.item(self.rowCount(), 1).setBackground(QColor(155,0,0))
            else:
                self.stateList[row] = True
                self.item(row, col).setBackground(QColor(34,139,34))
                # self.item(self.rowCount(), 1).setBackground(QColor(0,0,0))
            self.sent_fix.emit(False, row, self.stateList)
        return