import sys
import cv2
# from ffpyplayer.player import MediaPlayer
# from imutils.video import FileVideoStream
from PyQt5.QtWidgets import QStyle, QPushButton, QSlider,  QLabel, QHBoxLayout, QWidget, QApplication, QGridLayout, QMessageBox, QProgressBar, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

from VideoPlayer.Playbar import PlayBar
from VideoSave.VideoSave import VideoSave

class VideoStreamer(QWidget):

    def __init__(self):
        super().__init__()

        self.name = None
        self.timeBox = PlayBar()
        self.playButton = QPushButton()
        self.volumeSlider = QSlider(Qt.Vertical)
        self.volumeText = QLabel("0.0%")
        self.video = QLabel()
        self.timer = QTimer()
        self.list = []

        self.initUI()

    def initUI(self):
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.timeBox.changeRange(0, 0)
        self.volumeSlider.setRange(0, 0)

        self.video.setMouseTracking(False)

        controlBox = QHBoxLayout()
        controlBox.addWidget(self.playButton)
        controlBox.addWidget(self.timeBox)

        grid = QGridLayout()
        # grid.addWidget(self.volumeSlider, 0, 0)
        # grid.addWidget(self.volumeText, 1, 0)
        grid.addWidget(self.playButton, 1, 1)
        grid.addWidget(self.video, 0, 2)
        grid.addWidget(self.timeBox, 1, 2)

        self.setLayout(grid)
        self.show()

    def showFrame(self):
        if self.time < len(self.list):
            self.ret, frame = self.list[self.time]
        else:
            self.ret = None
        # audio_frame, val = self.audio.get_frame()

        # if video finishes
        if not self.ret:
            self.play()
            return

        self.video.setPixmap(frame)

    def nextFrameSlot(self):
        self.showFrame()

        self.setTime()

    def setTime(self):
        self.time += 1
        self.timeBox.controlVideo(self.time, self.fps)

    def start(self):
        self.timer.setInterval(1000 / self.fps)
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start()
        # self.timer.start(1000 / self.fps)

    def play(self):
        # if video finishes
        if not self.ret and not self.timer.isActive():
            self.setPosition(0)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        if self.timer.isActive():
            self.timer.stop()
            # self.audio.set_pause(True)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.timer.start()
            # self.audio.set_pause(False)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def set_video(self, name):
        self.time = 0
        self.name = name
        self.cap = cv2.VideoCapture(self.name)
        # self.audio = MediaPlayer(self.name)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        loadingWindow = QMainWindow()

        progress = QProgressBar()
        progress.setMaximum(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress.show()

        loadingWindow.setCentralWidget(progress)
        loadingWindow.show()

        count = 0
        progress.setValue(count)
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
            pix = QPixmap.fromImage(img)
            resized_pix = pix.scaled(640, 480)
            self.list.append((ret, resized_pix))

            count += 1
            progress.setValue(count)

        self.setPosition(0)
        self.videoDuration(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.start()

    def change_video(self, name):
        self.list.clear()
        self.cap.release()
        # self.audio.pause()
        self.killTimer(self.timer.timerId())
        self.timer = QTimer()
        self.set_video(name)

    def videoPlayer(self):
        self.timeBox.slider.sliderMoved.connect(self.setPosition)

    def videoDuration(self, duration):
        self.timeBox.changeRange(0, duration)

    def setPosition(self, position):
        self.time = position
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.showFrame()

    def change_playButtonStatus(self):
        if not self.playButton.isEnabled():
            self.playButton.setEnabled(True)

    def delete_mediaPlayer(self):
        self.cap.release()
        self.playButton.setEnabled(False)
        self.timeBox.changeRange(0, 0)

    def save_video(self):
        # if video doesn't exist
        if not self.name:
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "There is no video", QMessageBox.Ok)
            return

        if self.timer.isActive():
            self.timer.stop()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        videoSave = VideoSave(self.name)
        videoSave.show()
        videoSave.saveVideo()

    def mouseDoubleClickEvent(self, pos):
        # if video doesn't exist
        if not self.name:
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "There is no video", QMessageBox.Ok)
            return

        # coordinate of videos's left top position is (44, 9)
        x = pos.x() - 44
        y = pos.y() - 9
        if not (0 <= x <= 640 and 0 <= y <= 480):
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "Out of boundary!", QMessageBox.Ok)
            return

        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        weight = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        # real position in video
        real_x = int(x / 640 * weight)
        real_y = int(y / 480 * height)

        print(real_x, real_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoStreamer()
    sys.exit(app.exec_())
