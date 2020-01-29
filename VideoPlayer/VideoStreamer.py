import sys
from PyQt5.QtWidgets import QStyle, QPushButton, QSlider,  QLabel, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from VideoPlayer.Playbar import PlayBar


class VideoStreamer(QWidget):

    def __init__(self):
        super().__init__()

        self.timeBox = PlayBar()
        self.playButton = QPushButton()
        self.volumeSlider = QSlider(Qt.Vertical)
        self.volumeText = QLabel("0.0%")
        self.videoWidget = QVideoWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.initUI()

    def initUI(self):
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.timeBox.changeRange(0, 0)
        self.volumeSlider.setRange(0, 0)
        self.videoWidget.resize(640, 480)

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.timeBox)

        grid = QGridLayout()
        grid.addWidget(self.volumeSlider, 0, 0)
        grid.addWidget(self.volumeText, 1, 0)
        grid.addWidget(self.playButton, 1, 1)
        grid.addWidget(self.videoWidget, 0, 2)
        grid.addWidget(self.timeBox, 1, 2)

        self.setLayout(grid)
        self.show()

    def videoPlayer(self):
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

        # video controller
        self.playButton.clicked.connect(self.play)
        self.timeBox.slider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.timeBox.controlVideo)
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

    def videoDuration(self, duration):
        self.timeBox.changeRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.timeBox.changeRange(0, 0)
        self.volumeSlider.setRange(0, 0)
        self.volumeText.clear()
        self.setStatusTip("Error: " + self.mediaPlayer.errorString())

    def set_maxVolume(self):
        self.maxVolume = self.mediaPlayer.volume()

    def set_video(self, name):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(name)))
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.name = name

    def change_playButtonStatus(self):
        if not self.playButton.isEnabled():
            self.playButton.setEnabled(True)

    def delete_mediaPlayer(self):
        self.maxVolume = 0
        self.playButton.setEnabled(False)
        self.timeBox.changeRange(0, 0)
        self.volumeSlider.setRange(0, 0)
        self.volumeText.clear()
        # self.mediaPlayer.endofmedia()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoStreamer()
    sys.exit(app.exec_())
