import sys
import cv2
# from moviepy.editor import AudioFileClip, VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from PyQt5.QtWidgets import QProgressBar, QMainWindow, QApplication, QVBoxLayout, QWidget, QFileDialog

class VideoSave(QMainWindow):

    def __init__(self, name, frames, fps, h, w):
        super().__init__()

        self.progress = QProgressBar(self)
        self.name = name
        self.frameList = frames
        self.fps = fps
        self.h = h
        self.w = w

        self.resize(350, 60)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.progress)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def saveVideo(self):
        count = 0
        four_cc = cv2.VideoWriter_fourcc(*'DIVX')
        name = QFileDialog.getSaveFileName(self, "Save File", "output.avi", "Videos(*.avi)")
        # if user doesn't select file directory
        if not name[0]:
            return

        out = cv2.VideoWriter(name[0], four_cc, self.fps, (int(self.w), int(self.h)))

        self.progress.setMaximum(len(self.frameList))

        while count < len(self.frameList):
            (ret, frame) = self.frameList[count]

            if ret:
                count += 1
                out.write(frame)
                self.progress.setValue(count)
            else:
                break

        out.release()

        audio = AudioFileClip(self.name)
        video = VideoFileClip(name[0])
        result = video.set_audio(audio)
        result.write_videofile(name[0].replace(".avi", ".mp4"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    videoSave = VideoSave(r'C:\Users\kimda\Desktop\github\Team_Island\VideoSave\input.mp4')
    videoSave.saveVideo()
    sys.exit(app.exec_())
