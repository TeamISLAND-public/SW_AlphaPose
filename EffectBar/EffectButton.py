from PyQt5.QtWidgets import QSlider, QDialog, QLabel, QHBoxLayout, QPushButton, QSizePolicy

from PyQt5.QtCore import Qt, pyqtSignal

class EffectBar(QDialog):
    changedValue = pyqtSignal(int)  # 발생하는 int type 시그널을 저장하는 시그널 객체
    sentValue = pyqtSignal(int, int)
    val = 0
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

        self.button1 = QPushButton('Effect1')
        self.button2 = QPushButton('Effect2')

        self.button1.setSizePolicy(QSizePolicy.MinimumExpanding , QSizePolicy.MinimumExpanding)

        self.button1.clicked.connect(self.button1_clicked_change_value)
        self.button2.clicked.connect(self.button2_clicked_change_value)

        # Creating a horizontalBoxLayout
        hboxLayout = QHBoxLayout(self)  # Adding the widgets
        hboxLayout.addWidget(sliderLabel)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(self.button1)
        hboxLayout.addWidget(self.button2)

        # Setting main layout
        self.setLayout(hboxLayout)
        self.show()

    def on_changed_value(self, val):
        self.changedValue.emit(val)

    def button1_clicked_change_value(self):
        self.val += 1
        self.type = 1
        self.sentValue.emit(self.val, self.type)
        # print(self.val)

    def button2_clicked_change_value(self):
        self.val += 1
        self.type = 2
        self.sentValue.emit(self.val, self.type)
        # print(self.val)
