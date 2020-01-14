import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.center = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, event.pos(), QtCore.Qt.LeftButton, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier)
            self.center = event.pos()
            self.update()
            QtWidgets.QMainWindow.mousePressEvent(self, event)

    def paintEvent(self, event):
        if self.center:
            painter = QtGui.QPainter(self)
            painter.setPen(QtCore.Qt.red)
            painter.drawEllipse(self.center, 11, 11)
        QtWidgets.QMainWindow.paintEvent(self, event)