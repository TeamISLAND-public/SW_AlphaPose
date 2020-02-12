import sys
from PyQt5.QtWidgets import QWidget, QApplication, QSlider, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


class PlayBar(QWidget):
    sent_current_frame = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.slider = QSlider(Qt.Horizontal)
        self.time = QLabel("00:00:00")
        self.total_time = QLabel("00:00:00")

        self.initUI()

    def initUI(self):
        self.slider.setRange(0, 0)
        self.slider.valueChanged.connect(self.current_frame)
        self.total_time.setAlignment(Qt.AlignRight)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.time)
        hLayout.addWidget(self.slider)

        vLayout = QVBoxLayout()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.total_time)

        self.setLayout(vLayout)

    def current_frame(self):
        current_frame = self.slider.value()
        total_frame = self.total_frame
        self.sent_current_frame.emit(current_frame, total_frame)

    def changeRange(self, start, finish, fps):
        self.fps = fps
        self.slider.setRange(start, finish)
        self.slider.setTickPosition(QSlider.TicksBothSides)

        # total time label
        if self.fps != 0:
            last = float(self.slider.maximum() / self.fps)
            m = last // 60
            s = int(last) - m * 60
            c = (last - m * 60 - s) * 100
            self.total_time.setText("{:02d}:{:02d}:{:02d}".format(int(m), int(s), int(c)))

        self.total_frame = finish
        if start == 0 and finish == 0:
            self.time.setText("00:00:00")
            self.total_time.setText("00:00:00")
            return

        self.slider.setTickInterval(self.fps * 5)

    def controlVideo(self, position):
        if self.fps == 0:
            return

        self.slider.setValue(position)
        position = float(position / self.fps)
        m = position // 60
        s = int(position) - m * 60
        c = (position - m * 60 - s) * 100
        self.time.setText("{:02d}:{:02d}:{:02d}".format(int(m), int(s), int(c)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    playBar = PlayBar()
    playBar.show()
    sys.exit(app.exec_())
