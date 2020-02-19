class Toggle_Button(QPushButton):
    sent_fix = pyqtSignal(bool, int, bool)
    def __init__(self, currentRowCount):
        QPushButton.__init__(self, "ON")
        # self.setFixedSize(100, 100)
        self.currentRowCount = self.rowCount()
        self.setStyleSheet("background-color: green")
        self.setCheckable(True)
        self.toggled.connect(self.slot_toggle)

    # when toggled connect initial state is True in order to make first click as OFF then True state must be red and OFF
    @pyqtSlot(bool)
    def slot_toggle(self, state):
        print(self.currentRowCount, state)
        self.sent_fix.emit(False, self.currentRowCount, state)
        self.setStyleSheet("background-color: %s" % ({True: "red", False: "green"}[state]))
        self.setText({True: "OFF", False: "ON"}[state])
