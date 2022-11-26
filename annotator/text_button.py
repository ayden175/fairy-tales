from PyQt5.QtWidgets import QPushButton
import string

class TextButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # remove the border
        self.setStyleSheet('border: none;')
        self.entity = False
        self.name = None
        self.alignment = None

    def addClick(self, func):
        self.clicked.connect(lambda: func(self))

    def removeInfo(self):
        self.entity = False
        self.name = None
        self.alignment = None
        self.setStyleSheet('border: none; background-color: none')

    def setInfo(self, name, alignment, color):
        self.entity = True
        self.name = name
        self.alignment = alignment
        self.color = color
        self.updateColor()

    def updateColor(self):
        self.setStyleSheet(f'border: none; background-color: {self.color.color}')

    def getText(self):
        return self.text().translate(str.maketrans('', '', string.punctuation))

    def getName(self):
        return self.name.text()

    def getAlignment(self):
        return self.alignment.currentText()