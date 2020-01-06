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

        self.errorLabel = QLabel()
        self.positionSlider = QSlider(Qt.Horizontal)
        self.playButton = QPushButton()
        self.videoButton = QPushButton()
        self.videoWidget = QVideoWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.initUI()

    def initUI(self):
        self.resize(300, 300)
        self.menu()
        self.statusBar()

        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.videoButton.setEnabled(False)
        self.videoButton.clicked.connect(self.close_video)

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlBox)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.videoButton)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def open_video(self):
        filename = QFileDialog.getOpenFileName(self, "Open file", os.getcwd(), "Video files(*.mp4 *.mkv *.avi)")
        # self.cap = cv2.VideoCapture(filename[0])
        self.playButton.setEnabled(True)
        self.videoButton.setEnabled(True)
        self.videoButton.setText("Click to close the video")
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename[0])))
        self.videoPlayer()

    def close_video(self):
        self.videoWidget.close()
        self.videoButton.setEnabled(False)
        self.videoButton.setText("")
        self.playButton.setEnabled(False)
        self.positionSlider.setRange(0, 0)

    def videoPlayer(self):
        self.playButton.clicked.connect(self.play)

        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

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
