from PyQt5.QtWidgets import QColorDialog, QPushButton
from PyQt5.QtGui import QColor

import annotator.config as cfg

class ColorButton(QPushButton):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(25, 25)
        self.color = color
        self.setStyleSheet(f'background-color: {color}')
        self.clicked.connect(self.changeColor)

    def changeColor(self):
        color = QColorDialog.getColor(initial=QColor(self.color))

        if not color.isValid():
            return
        
        self.setStyleSheet("background-color: {}".format(color.name()))
        self.color = color.name()

        for char in cfg.char_lists:
            if char['color'] == self:
                for button in char['buttons']:
                    button.updateColor()

    def remove_text(self):
        found = True

        while found:
            found = False
            for char in cfg.char_lists:
                if char['color'] == self:
                    for button in char['buttons']:
                        char['buttons'].remove(button)
                        button.removeInfo()
                        found = True
                        cfg.unsaved_changes = True
