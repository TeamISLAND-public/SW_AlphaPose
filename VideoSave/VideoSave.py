import sys
import cv2
from PyQt5.QtWidgets import QProgressBar, QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QBasicTimer


class VideoSave(QMainWindow):

    def __init__(self, name):
        super().__init__()

        self.count = 0
        self.progress = QProgressBar(self)
        self.button = QPushButton("Close", self)
        self.timer = QBasicTimer()
        self.cap = cv2.VideoCapture(name)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, self.cap.get(cv2.CAP_PROP_FPS), (640, 480))

        self.resize(350, 60)
        self.initUI()

    def initUI(self):
        self.progress.setMaximum(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.button.setEnabled(False)
        self.button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.progress)
        layout.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()

    def saveVideo(self):
        self.timer.start(0, self)

    def timerEvent(self, e):
        ret, frame = self.cap.read()
        if (self.count > self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) or not ret:
            self.timer.stop()
            self.button.setEnabled(True)
            self.cap.release()
            self.out.release()
            return

        self.count += 1
        self.progress.setValue(self.count)
        self.out.write(frame)
        cv2.imshow('frame', frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    videoSave = VideoSave('input.mp4')
    videoSave.saveVideo()
    sys.exit(app.exec_())
