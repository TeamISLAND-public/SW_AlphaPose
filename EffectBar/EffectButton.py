from PyQt5.QtWidgets import QSlider, QDialog, QLabel, QHBoxLayout

from PyQt5.QtCore import Qt, pyqtSignal

class EffectBar(QDialog):
    changedValue = pyqtSignal(int)  # 발생하는 int type 시그널을 저장하는 시그널 객체

    def __init__(self):
        super(EffectBar, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Creating a label

        sliderLabel = QLabel('Slider:', self)

        # Creating a slider and setting its maximum and minimum value

        # self.slider.setMinimum(0)

        # self.slider.setMaximum(100)

        # self.slider.setOrientation(Qt.Horizontal)

        self.slider = QSlider(Qt.Horizontal)

        self.slider.setRange(0, 100)

        self.slider.valueChanged.connect(self.on_changed_value)

        # Creating a horizontalBoxLayout

        hboxLayout = QHBoxLayout(self)  # Adding the widgets

        hboxLayout.addWidget(sliderLabel)

        hboxLayout.addWidget(self.slider)

        # Setting main layout

        self.setLayout(hboxLayout)

        self.setWindowTitle("Dialog with a Slider")

        self.show()

    def on_changed_value(self, val):  # 슬라이더를 움직일시 발생하는 시그널을

        self.changedValue.emit(val)