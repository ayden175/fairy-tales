from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class TextLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setContentsMargins(0, 0, 0, 0)
        #self.rows = QVBoxLayout(self.widget())
        #self.widget().addLayout(QHBoxLayout(self.widget()))
        self.setAlignment(Qt.AlignTop)
        self.all_buttons = []
        self.sizes = []

    def setButtons(self, buttons):
        self.all_buttons = buttons
        self.updateLayout()

    def updateLayout(self):
        #self.rows = QVBoxLayout()
        max_width = self.parentWidget().frameGeometry().width()

        for paragraph in self.all_buttons:
            self.addRow()

            for button in paragraph:
                row_size = self.sizes[-1]
                button_size = button.sizeHint().width() + 8

                if row_size + button_size > max_width:
                    self.addRow()
                self.itemAt(self.count()-1).layout().addWidget(button)
                self.sizes[self.count()-1] += button_size
            
    def addRow(self):
        layout = QHBoxLayout(self.widget())
        layout.setAlignment(Qt.AlignLeft)
        self.addLayout(layout)
        self.sizes.append(0)

    def clear(self):
        self.clearLayout(self)
        self.all_buttons = []
        self.sizes = []
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())