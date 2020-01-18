import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QMessageBox, QApplication
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
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Record Video")

        self.recordButton.clicked.connect(self.record)
        self.stopButton.setEnabled(False)
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
        if self.running:
            errorbox = QMessageBox()
            errorbox.warning(self, "Error Message", "Webcam is already opened.", QMessageBox.Ok)
            return

        self.videoCaptureThread = threading.Thread(target=self.run)
        self.videoCaptureThread.daemon = True
        self.videoCaptureThread.start()

    def stop(self):
        try:
            self.running = False
            self.videoCaptureThread.join()
            self.cap.release()
            self.close()
        except Exception as ex:
            print(ex)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                img = frame
                qImg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_BGR888)
                pixMap = QPixmap.fromImage(qImg)
                self.videoStream.setPixmap(pixMap)

                if self.recording:
                    try:
                        self.video_writer.write(frame)
                    except Exception as ex:
                        print(ex)
            else:
                errorbox = QMessageBox()
                errorbox.warning(self, "Error Message", "Cannot read frame.", QMessageBox.Ok)
                self.running = False
                self.cap.release()
                self.close()
                break

    def record(self):
        self.recording = True
        self.stopButton.setEnabled(True)
        self.recordButton.setEnabled(False)
        try:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter("output.avi", fourcc, 20, (640, 480))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    recordWindow = RecordApp.getInstance()
    recordWindow.show()
    recordWindow.start()
    sys.exit(app.exec_())
