import sys
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QAction, QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt

from VideoPlayer.VideoStreamer import VideoStreamer


class VideoList(QTableWidget):

    def __init__(self):
        super().__init__()

        self.fileNameList = []
        self.setRowCount(0)
        self.setColumnCount(0)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cell_right_clicked()
        self.show()

    def cell_right_clicked(self):
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Delete", self)
        self.addAction(delete_action)
        delete_action.triggered.connect(self.delete_video)

    def delete_video(self, videoStreamer: VideoStreamer):
        for i in self.selectedItems():
            self.fileNameList.remove(self.item(i.row(), 0).text())
            self.removeRow(i.row())
            if videoStreamer.name == self.item(i.row(), 0).text():
                videoStreamer.delete_mediaPlayer()

    def add_video(self, name):
        self.fileNameList.append(name)
        currentRowCount = self.rowCount()
        self.insertRow(currentRowCount)
        self.setItem(0, currentRowCount, QTableWidgetItem(name))
        self.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoList()
    sys.exit(app.exec_())
