from PyQt5.QtWidgets import QUndoStack, QUndoCommand

from EffectBar.EffectBar import EffectBar
import EffectStatusBar.EffectstatusBar
import EffectStatusBar.RangeSlider

stack = QUndoStack()


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

    def __init__(self, start, finish, change, slider):
        super().__init__()
        self.old_start = start
        self.old_finish = finish
        self.change = change
        self.slider = slider

    def undo(self):
        if self.change > self.old_finish:
            self.slider._setEnd(self.old_finish)
        else:
            self.slider._setStart(self.old_start)

    def redo(self):
        if self.change > self.old_finish:
            self.slider._setEnd(self.change)
        else:
            self.slider._setStart(self.change)
