import sys
from PyQt5.QtWidgets import QStyle, QPushButton, QSlider,  QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class VideoStreamer(QWidget):

    def __init__(self):
        super().__init__()

        self.positionSlider = QSlider(Qt.Horizontal)
        self.playButton = QPushButton()
        self.volumeSlider = QSlider(Qt.Vertical)
        self.volumeText = QLabel()
        self.videoWidget = QVideoWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.initUI()

    def initUI(self):
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.positionSlider.setRange(0, 0)
        self.volumeSlider.setRange(0, 0)

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
        layout.addLayout(volumeBox)
        layout.addLayout(vLayout)

        self.setLayout(layout)
        self.show()

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

    def set_maxVolume(self):
        self.maxVolume = self.mediaPlayer.volume()

    def set_video(self, name):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(name)))
        self.mediaPlayer.setVideoOutput(self.videoWidget)

    def change_playButtonStatus(self):
        if self.playButton.isEnabled():
            self.playButton.setEnabled(False)
        else:
            self.playButton.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoStreamer()
    sys.exit(app.exec_())
