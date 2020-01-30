import sys
from PyQt5.QtWidgets import QWidget, QApplication, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class PlayBar(QWidget):

    def __init__(self):
        super().__init__()

        self.slider = QSlider(Qt.Horizontal)
        self.time = QLabel("00:00:00")

        self.initUI()

    def initUI(self):
        self.slider.setRange(0, 0)

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.time)

        self.setLayout(layout)

    def changeRange(self, start, finish):
        self.slider.setRange(start, finish)
        if start == 0 and finish == 0:
            self.time.setText("00:00:00")

    def controlVideo(self, position, fps):
        self.slider.setValue(position)
        position = position / fps
        h = position // 3600
        m = (position - h * 360000) // 60
        s = position - h * 3600 - m * 60
        self.time.setText("{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    playBar = PlayBar()
    playBar.show()
    sys.exit(app.exec_())