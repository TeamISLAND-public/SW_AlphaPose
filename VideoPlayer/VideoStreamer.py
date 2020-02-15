import sys
import cv2
# from ffpyplayer.player import MediaPlayer
# from imutils.video import FileVideoStream
from PyQt5.QtWidgets import QStyle, QPushButton, QSlider,  QLabel, QHBoxLayout, QWidget, QApplication, QGridLayout, QMessageBox, QProgressBar, QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from VideoPlayer.Playbar import PlayBar
from VideoSave.VideoSave import VideoSave


class VideoStreamer(QWidget):

    sent_position = pyqtSignal(list)

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
        self.position_list = []

        self.initUI()

    def initUI(self):
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.timeBox.changeRange(0, 0, 0)
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

        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        pix = QPixmap.fromImage(img)
        resized_pix = pix.scaled(640, 480)
        self.video.setPixmap(resized_pix)

    def nextFrameSlot(self):
        self.showFrame()

        self.setTime()

    def setTime(self):
        self.time += 1
        self.timeBox.controlVideo(self.time)

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

            self.list.append((ret, frame))

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
        self.timeBox.changeRange(0, duration, self.fps)

    def setPosition(self, position):
        self.time = position
        self.timeBox.controlVideo(position)
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

        videoSave = VideoSave(self.name, self.list, self.fps, self.cap.get(4), self.cap.get(3))
        videoSave.show()
        videoSave.saveVideo()

    def mouseDoubleClickEvent(self, pos):
        # if video doesn't exist
        if not self.name:
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "There is no video", QMessageBox.Ok)
            return

        x = pos.x() - self.video.pos().x()
        y = pos.y() - self.video.pos().y()
        if not (0 <= x <= 640 and 0 <= y <= 480):
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "Out of boundary!", QMessageBox.Ok)
            return

        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        weight = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)

        # real position in video
        real_x = int(x / 640 * weight)
        real_y = int(y / 480 * height)

        position = (real_x, real_y)

        self.position_list.append(position)
        self.sent_position.emit(self.position_list)

    def effectbar_to_videostreamer(self, class_object):
        class_object.sent_video.connect(self.EffectBar_Inter_VideoStreamer)

    def effectstatusbar_to_videostreamer(self, class_object):
        class_object.sent_fix.connect(self.EffectStatusBar_Inter_VideoStreamer)


    # Sending result of video visualization
    @pyqtSlot(list, int)
    def EffectBar_Inter_VideoStreamer(self, result_list, current_frame):
        if self.time < len(self.list):
            for i in range(29):
                self.list[current_frame+i] = result_list[i]
        else:
            self.ret = None
        # if video finishes
        if not self.ret:
            self.play()
            return

        self.position_list.clear()

    #RangeSilder value update is expected
    @pyqtSlot(bool, int, bool)
    def EffectStatusBar_Inter_VideoStreamer(self, deletion, current_row, on_off):
        print(deletion, current_row, on_off)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = VideoStreamer()
    sys.exit(app.exec_())
