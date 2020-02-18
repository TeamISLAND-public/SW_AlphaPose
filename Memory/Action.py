from PyQt5.QtWidgets import QUndoStack, QUndoCommand

from EffectBar.EffectBar import EffectBar
from EffectStatusBar.EffectstatusBar import EffectStatusBar
from EffectStatusBar.RangeSlider import QRangeSlider

stack = QUndoStack()


# maybe be called in EffectBar
class EffectAction(QUndoCommand):

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
            for i in EffectStatusBar.items():
                if i.text() == self.name:
                    EffectStatusBar.removeRow(i.row())

    def redo(self):
        if self.deletion:
            for i in EffectStatusBar.items():
                if i.text() == self.name:
                    EffectStatusBar.removeRow(i.row())
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
class TrackAction(QUndoCommand):

    def __init__(self, start, finish, change):
        super().__init__()
        self.old_start = start
        self.old_finish = finish
        self.change = change

    def undo(self):
        if self.change > self.old_finish:
            QRangeSlider._setEnd(self.old_finish)
        else:
            QRangeSlider._setStart(self.old_start)

    def redo(self):
        if self.change > self.old_finish:
            QRangeSlider._setEnd(self.change)
        else:
            QRangeSlider._setStart(self.change)
