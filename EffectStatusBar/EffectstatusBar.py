from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QAction, QApplication, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from EffectStatusBar.RangeSlider import QRangeSlider
import sys

class EffectStatusBar(QTableWidget):
    effect_queue_list = []
    returnValue = pyqtSignal(int)
    val = 0
    def __init__(self):
        super(EffectStatusBar, self).__init__()
        self.init_ui()

    def init_ui(self):
        super().__init__()

        self.effect_queue_list = []
        self.setRowCount(0)
        self.setColumnCount(1)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cell_right_clicked()
        self.show()

    def cell_right_clicked(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Delete Effect", self)
        self.addAction(delete_action)
        delete_action.triggered.connect(self.delete_effect_queue_list)

    def delete_effect_queue_list(self):
        # if self.effect_queue_list == []:
        #     self.returnValue.emit(self.val)
        # else:
        #     print(self.effect_queue_list)
        #     self.returnValue.emit(self.val)
        #     if self.val == 0:
        #         self.val = self.val
        #     else:
        #         self.val = self.val - 1
        #     self.formLayout.itemAt(self.val).widget().setParent(None)
        #     del self.effect_queue_list[self.val]
        #     print(self.effect_queue_list)
        for i in self.selectedItems():
            print(i)
            # self.effect_queue_list.remove(self.item(i.row(), 0).text())
            self.removeRow(i.row())

# This line is for EffectBar to EffectStatusBar connection
    def make_connection(self, class_object):
        class_object.sentValue.connect(self.EffectBar_Inter_EffectStatusBar)

    @pyqtSlot(int, int)
    def EffectBar_Inter_EffectStatusBar(self, val, type, effect_queue_list = effect_queue_list):
        # self.val = val
        # self.type = type
        # effect_queue_list.append(QRangeSlider())
        # self.formLayout.addWidget(effect_queue_list[val])
        # self.formLayout.update()
        # print(val, type)
        #
        effect_queue_list.append(val)
        print(effect_queue_list)
        currentRowCount = self.rowCount()
        print(currentRowCount)
        self.insertRow(currentRowCount)
        self.setItem(0, currentRowCount, QTableWidgetItem("{}".format(currentRowCount)))
        self.setCellWidget(currentRowCount, 0, QRangeSlider())
        self.horizontalHeader().setStretchLastSection(True)

        # self.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EffectStatusBar()
    sys.exit(app.exec_())