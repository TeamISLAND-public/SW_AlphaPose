import sys
import cv2
import time
from PyQt5.QtWidgets import QStyle, QPushButton, QSlider,  QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QImage, QPixmap
from VideoPlayer.Playbar import PlayBar


class VideoStreamer(QWidget):

    def __init__(self):
        super().__init__()

        self.timeBox = PlayBar()
        self.playButton = QPushButton()
        self.volumeSlider = QSlider(Qt.Vertical)
        self.volumeText = QLabel("0.0%")
        # self.videoWidget = QVideoWidget()
        # self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video = QLabel()
        self.timer = QTimer()

        self.initUI()

    def initUI(self):
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.timeBox.changeRange(0, 0)
        self.volumeSlider.setRange(0, 0)
        # self.videoWidget.resize(640, 480)

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.timeBox)

        grid = QGridLayout()
        grid.addWidget(self.volumeSlider, 0, 0)
        grid.addWidget(self.volumeText, 1, 0)
        grid.addWidget(self.playButton, 1, 1)
        # grid.addWidget(self.videoWidget, 0, 2)
        grid.addWidget(self.video, 0, 2)
        grid.addWidget(self.timeBox, 1, 2)

        self.setLayout(grid)
        self.show()

    def nextFrameSlot(self):
        self.ret, frame = self.cap.read()
        if not self.ret:
            self.play()
            return
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        pix = QPixmap.fromImage(img)
        resized_pix = pix.scaled(640, 480)
        self.video.setPixmap(resized_pix)

        self.setTime()

    def setTime(self):
        self.time += 1
        self.timeBox.controlVideo(self.time, self.cap.get(cv2.CAP_PROP_FPS))

    def start(self):
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)

    def play(self):
        if not self.ret and not self.timer.isActive():
            self.setPosition(0)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        if self.timer.isActive():
            self.timer.stop()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.timer.start()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def set_video(self, name):
        self.time = 0
        self.cap = cv2.VideoCapture(name)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.setPosition(0)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        self.videoDuration(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.start()

    def change_video(self, name):
        self.cap.release()
        self.killTimer(self.timer.timerId())
        self.timer = QTimer()
        self.set_video(name)

    def videoPlayer(self):
        self.timeBox.slider.sliderMoved.connect(self.setPosition)

    def videoDuration(self, duration):
        self.timeBox.changeRange(0, duration)

    def setPosition(self, position):
        self.time = position
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)

    def change_playButtonStatus(self):
        if not self.playButton.isEnabled():
            self.playButton.setEnabled(True)

    # def videoPlayer(self):
    #     self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
    #
    #     # video controller
    #     self.playButton.clicked.connect(self.play)
    #     self.timeBox.slider.sliderMoved.connect(self.setPosition)
    #     self.mediaPlayer.positionChanged.connect(self.timeBox.controlVideo)
    #     self.mediaPlayer.durationChanged.connect(self.videoDuration)
    #
    #     # audio controller
    #     self.volumeSlider.sliderMoved.connect(self.setVolume)
    #     self.mediaPlayer.volumeChanged.connect(self.controlVolume)
    #     self.volumeDuration(self.mediaPlayer.volume())
    #
    #     self.mediaPlayer.error.connect(self.handleError)
    #
    # def controlVolume(self, volume):
    #     self.volumeSlider.setValue(volume)
    #     self.volumeText.setText("{:.1f}%".format((volume / self.maxVolume) * 100))
    #
    # def volumeDuration(self, duration):
    #     self.volumeSlider.setRange(0, duration)
    #     self.volumeSlider.setValue(self.mediaPlayer.volume())
    #     self.volumeText.setText("100.0%")
    #
    # def setVolume(self, volume):
    #     self.mediaPlayer.setVolume(volume)
    #
    # def handleError(self):
    #     self.playButton.setEnabled(False)
    #     self.timeBox.changeRange(0, 0)
    #     self.volumeSlider.setRange(0, 0)
    #     self.volumeText.clear()
    #     self.setStatusTip("Error: " + self.mediaPlayer.errorString())
    #
    # def set_maxVolume(self):
    #     self.maxVolume = self.mediaPlayer.volume()
    #
    # def delete_mediaPlayer(self):
    #     self.maxVolume = 0
    #     self.playButton.setEnabled(False)
    #     self.timeBox.changeRange(0, 0)
    #     self.volumeSlider.setRange(0, 0)
    #     self.volumeText.clear()
    #     # self.mediaPlayer.endofmedia()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoStreamer()
    sys.exit(app.exec_())
