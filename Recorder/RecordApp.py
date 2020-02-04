import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QMessageBox, QApplication, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import threading


class RecordApp(QMainWindow):
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def getInstance(cls):
        cls.__instance = cls()
        cls.getInstance = cls.__getInstance
        return cls.__instance

    def __init__(self):
        super().__init__()

        self.running = False
        self.recording = False
        self.recordButton = QPushButton("Record")
        self.stopButton = QPushButton("Stop")
        self.videoStream = QLabel()
        self.timer = QTimer()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Record Video")

        self.recordButton.clicked.connect(self.record)
        self.stopButton.clicked.connect(self.stop)

        layout = QVBoxLayout()
        layout.addWidget(self.videoStream)
        layout.addWidget(self.recordButton)
        layout.addWidget(self.stopButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.resize(640, 500)
        self.show()

    def start(self):
        # if user tries to open webcam when webcam is already opened
        if self.running:
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "Webcam is already opened.", QMessageBox.Ok)
            return

        self.cap = cv2.VideoCapture(0)
        self.run()

        # self.videoCaptureThread = threading.Thread(target=self.run)
        # self.videoCaptureThread.daemon = True
        # self.videoCaptureThread.start()

    def stop(self):
        # self.running = False
        # self.videoCaptureThread.join()
        self.cap.release()
        self.timer.stop()
        self.close()

    def run(self):
        self.timer.timeout.connect(self.stream)
        self.timer.start(50)
        # self.cap = cv2.VideoCapture(0)
        # self.running = True
        #
        # while self.running:
        #     ret, frame = self.cap.read()
        #     if ret:
        #         img = frame
        #         qImg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
        #         pixMap = QPixmap.fromImage(qImg)
        #         self.videoStream.setPixmap(pixMap)
        #
        #         if self.recording:
        #             try:
        #                 self.video_writer.write(frame)
        #             except Exception as ex:
        #                 print(ex)
        #     else:
        #         errorbox = QMessageBox()
        #         errorbox.warning(self, "Error Message", "Cannot read frame.", QMessageBox.Ok)
        #         self.running = False
        #         self.cap.release()
        #         self.close()
        #         break

    def stream(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        flipImg = cv2.flip(frame, 1)
        qImg = QImage(flipImg.data, flipImg.shape[1], flipImg.shape[0], QImage.Format_BGR888)
        pixMap = QPixmap.fromImage(qImg)
        self.videoStream.setPixmap(pixMap)

        if self.recording:
            self.video_writer.write(flipImg)

    def record(self):
        self.timer.stop()
        self.recording = True
        self.recordButton.setEnabled(False)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name = QFileDialog.getSaveFileName(self, "Save File", "output.avi", "Videos(*.avi)")
        self.video_writer = cv2.VideoWriter(name[0], fourcc, 20, (640, 480))
        self.timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    recordWindow = RecordApp.getInstance()
    recordWindow.show()
    recordWindow.start()
    sys.exit(app.exec_())
