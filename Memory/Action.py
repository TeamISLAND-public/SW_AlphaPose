import sys
from PyQt5.QtWidgets import QUndoStack, QUndoCommand, QUndoView, QApplication, QDialog, QGridLayout

from EffectBar.EffectBar import EffectBar
import EffectStatusBar.EffectstatusBar
import EffectStatusBar.RangeSlider


# maybe be called in EffectBar
# I have to solve how to remember generated effect
class EffectActionCommand(QUndoCommand):

    def __init__(self, name, deletion, type):
        super().__init__()
        self.name = name
        # type of deletion is bool
        self.deletion = deletion
        self.type = type

    def undo(self):
        if self.deletion:
            if self.type == 0:
                EffectBar.effect0_clicked()
            if self.type == 1:
                EffectBar.effect1_clicked()
            if self.type == 2:
                EffectBar.effect2_clicked()
            if self.type == 3:
                EffectBar.effect3_clicked()
            if self.type == 4:
                EffectBar.effect4_clicked()
        else:
            for i in EffectStatusBar.EffectstatusBar.EffectStatusBar.items():
                if i.text() == self.name:
                    EffectStatusBar.EffectstatusBar.EffectStatusBar.removeRow(i.row())

    def redo(self):
        if self.deletion:
            for i in EffectStatusBar.EffectstatusBar.EffectStatusBar.items():
                if i.text() == self.name:
                    EffectStatusBar.EffectstatusBar.EffectStatusBar.removeRow(i.row())
        else:
            if self.type == 0:
                EffectBar.effect0_clicked()
            if self.type == 1:
                EffectBar.effect1_clicked()
            if self.type == 2:
                EffectBar.effect2_clicked()
            if self.type == 3:
                EffectBar.effect3_clicked()
            if self.type == 4:
                EffectBar.effect4_clicked()


# maybe be called in QRangeSlider
class TrackActionCommand(QUndoCommand):

    def __init__(self, start, end, change, slider):
        super().__init__()
        self.old_start = start
        self.old_end = end
        self.change = change
        self.slider = slider

        if self.change > self.old_end:
            self.setText("Change the end {} to {}".format(self.old_end, self.change))
        else:
            self.setText("Change the start {} to {}".format(self.old_start, self.change))

    def undo(self):
        if self.change > self.old_end:
            self.slider._setEnd(self.old_end)
        else:
            self.slider._setStart(self.old_start)

    def redo(self):
        if self.change > self.old_end:
            self.slider._setEnd(self.change)
        else:
            self.slider._setStart(self.change)

    def set_change(self, new):
        self.change = new


class UndoAction(QUndoStack):

    def __init__(self):
        super().__init__()

    # def push(self, QUndoCommand):
        # if type(self.command(self.index())) == type(QUndoCommand):
        #     if type(QUndoCommand) == type(TrackActionCommand):
        #         lastCommand = self.command(self.index())
        #         if (lastCommand.change > lastCommand.old_end and QUndoCommand.change > QUndoCommand.old_end) or (lastCommand.change < lastCommand.old_end and QUndoCommand.change < QUndoCommand.old_end):
        #             lastCommand.set_change(QUndoCommand.change)
        # else:
        #     self.push(QUndoCommand)

        # if type(QUndoCommand) == TrackActionCommand:
        #     if QUndoCommand.old_end == QUndoCommand.change or QUndoCommand.old_start == QUndoCommand.change:
        #         print(QUndoCommand.old_end, QUndoCommand.old_start, QUndoCommand.change)
        #         self.command(self.index()).set_change(QUndoCommand.change)
        #         return
        # else:
        #     self.push(QUndoCommand)


class UndoList(QDialog):
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
        self.setWindowTitle("Command List")
        self.stack = UndoAction()

        self.view = QUndoView()
        self.view.setStack(self.stack)

        layout = QGridLayout()
        layout.addWidget(self.view)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = UndoList()
    sys.exit(app.exec_())
