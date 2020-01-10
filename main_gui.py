import sys
import cv2
import threading
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.fileNameList = []
        self.videoTable = QTableWidget()
        self.positionSlider = QSlider(Qt.Horizontal)
        self.playButton = QPushButton()
        self.volumeSlider = QSlider(Qt.Vertical)
        self.volumeText = QLabel()
        self.videoWidget = QVideoWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.initUI()

    def initUI(self):
        self.resize(1100, 500)
        self.menu()
        self.statusBar()

        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.positionSlider.setRange(0, 0)
        self.volumeSlider.setRange(0, 0)

        # setting of file list
        self.videoTable.setRowCount(0)
        self.videoTable.setColumnCount(0)
        self.videoTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # event when cell of file list is right clicked
        self.cell_right_clicked()

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.positionSlider)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.videoWidget)
        vLayout.addLayout(controlBox)

        volumeBox = QVBoxLayout()
        volumeBox.addWidget(self.volumeSlider)
        volumeBox.addWidget(self.volumeText)

        layout = QHBoxLayout()
        # layout.addLayout(self.fileList)
        layout.addWidget(self.videoTable)
        layout.addLayout(volumeBox)
        layout.addLayout(vLayout)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def open_video(self):
        # if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        #     self.mediaPlayer.stop()
        filename = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), "Video files(*.mp4 *.mkv *.avi)")
        self.videoTable.setColumnCount(1)

        # if Video is already opened
        if filename[0] in self.fileNameList:
            errorbox = QMessageBox()
            errorbox.question(self, "Error Message", "Video is already opened", QMessageBox.Ok)
            return

        # if user doesn't select the video
        if not filename[0]:
            return

        self.playButton.setEnabled(True)

        # set video
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename[0])))
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # add video file in table
        self.fileNameList.append(filename[0])
        currentRowCount = self.videoTable.rowCount()
        try:
            self.videoTable.insertRow(currentRowCount)
            self.videoTable.setItem(0, currentRowCount, QTableWidgetItem(filename[0]))
            self.videoTable.resizeColumnsToContents()
            self.videoTable.doubleClicked.connect(self.change_video)
        except Exception as ex:
            print(ex)

        # set max volume of video
        self.maxVolume = self.mediaPlayer.volume()

        self.videoPlayer()

    def cell_right_clicked(self):
        self.videoTable.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction("Delete", self.videoTable)
        self.videoTable.addAction(delete_action)
        delete_action.triggered.connect(self.delete_video)

    def delete_video(self):
        for i in self.videoTable.selectedItems():
            self.fileNameList.remove(self.videoTable.item(i.row(), 0).text())
            self.videoTable.removeRow(i.row())

    def change_video(self, row):
        self.playButton.setEnabled(True)

        # set video
        for i in self.videoTable.selectedItems():
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(i.text())))
            self.mediaPlayer.setVideoOutput(self.videoWidget)

        # set max volume of video
        self.maxVolume = self.mediaPlayer.volume()

        self.videoPlayer()

    def videoPlayer(self):
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

        # video controller
        self.playButton.clicked.connect(self.play)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.controlVideo)
        self.mediaPlayer.durationChanged.connect(self.videoDuration)

        # audio controller
        self.volumeSlider.sliderMoved.connect(self.setVolume)
        self.mediaPlayer.volumeChanged.connect(self.controlVolume)
        self.volumeDuration(self.mediaPlayer.volume())

        self.mediaPlayer.error.connect(self.handleError)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def controlVolume(self, volume):
        self.volumeSlider.setValue(volume)
        self.volumeText.setText("{:.1f}%".format((volume / self.maxVolume) * 100))

    def volumeDuration(self, duration):
        self.volumeSlider.setRange(0, duration)
        self.volumeSlider.setValue(self.mediaPlayer.volume())
        self.volumeText.setText("100.0%")

    def setVolume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def controlVideo(self, position):
        self.positionSlider.setValue(position)

    def videoDuration(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.positionSlider.setRange(0, 0)
        self.volumeSlider.setRange(0, 0)
        self.volumeText.clear()
        self.setStatusTip("Error: " + self.mediaPlayer.errorString())
        print(self.mediaPlayer.errorString())

    # def saveVideo(self):
    #     fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    #     filename = QFileDialog.getOpenFileName(self, "Save file", os.getcwd())
    #     out = cv2.VideoWriter(filename[0], fourcc, 25.0, (640, 480))
    #     while True:
    #         ret, frame = self.cap.read()
    #         out.write(frame)
    #
    #     self.cap.release()
    #     out.release()
    #     cv2.destroyAllWindows()

    def menu(self):
        menu = self.menuBar()
        menu_file = menu.addMenu("&File")
        menu_edit = menu.addMenu("&Edit")

        video_open = QAction("Open", self)
        video_open.setShortcut("Ctrl+O")
        video_open.setStatusTip("Open the video file")
        video_open.triggered.connect(self.open_video)

        file_exit = QAction("Exit", self)
        file_exit.setShortcut("Ctrl+Q")
        file_exit.setStatusTip("Exit")
        file_exit.triggered.connect(QCoreApplication.instance().quit)

        file_save = QAction("Save", self)
        file_save.setShortcut("Ctrl+S")
        file_save.setStatusTip("Save the video file")
        # file_save.triggered.connect(self.saveVideo)

        menu_file.addAction(video_open)
        menu_file.addAction(file_exit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
