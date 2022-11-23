import os

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from tkinter import filedialog

import annotator.config as cfg

class AnnotatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.alignments = ['good', 'neutral', 'bad']
        self.path = None
        self.initUI()
        self.show()


    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
        uic.loadUi('annotator/annotator.ui', self)
        self.add_character_clicked()

        self.load_fairy_tale.clicked.connect(self.load_fairy_tale_clicked)
        self.previous_fairy_tale.clicked.connect(self.previous_fairy_tale_clicked)
        self.next_fairy_tale.clicked.connect(self.next_fairy_tale_clicked)
        self.add_character.clicked.connect(self.add_character_clicked)

        self.load_annotations.triggered.connect(self.load_annotations_clicked)
        self.save_annotations.triggered.connect(self.save_annotations_clicked)

    def load_annotations_clicked(self):
        path = filedialog.askopenfilename(defaultextension='.yaml', filetypes=[('YAML files', '*.yaml')])
        if path == '':
            return
        # TODO: load annotations from file

    def save_annotations_clicked(self):
        path = filedialog.asksaveasfilename(defaultextension='.yaml', filetypes=[('YAML files', '*.yaml')])
        if path == '':
            return False

        # TODO: save annotations to file
        return True


    def add_character_clicked(self):
        hbox = QtWidgets.QHBoxLayout()

        name = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        hbox.addWidget(name)

        alignment = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        alignment.setMaximumSize(QtCore.QSize(100, 16777215))
        alignment.addItems(self.alignments)
        alignment.setCurrentText('neutral')
        hbox.addWidget(alignment)

        remove = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        remove.setMinimumSize(QtCore.QSize(70, 0))
        remove.setMaximumSize(QtCore.QSize(70, 16777215))
        remove.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        remove.setText('Remove')
        remove.clicked.connect(lambda: self.clear_item(hbox))
        hbox.addWidget(remove)

        hbox.setStretch(0, 2)
        hbox.setStretch(1, 1)
        self.characters_layout.insertLayout(self.characters_layout.count()-1, hbox)

    def clear_item(self, item):
        if hasattr(item, "layout"):
            if callable(item.layout):
                layout = item.layout()
        else:
            layout = None

        if hasattr(item, "widget"):
            if callable(item.widget):
                widget = item.widget()
        else:
            widget = None

        if widget:
            widget.setParent(None)
        elif layout:
            for i in reversed(range(layout.count())):
                self.clear_item(layout.itemAt(i))

    def load_fairy_tale_clicked(self):
        path = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if path == '':
            return
        self.set_fairy_tale_text(path)


    def previous_fairy_tale_clicked(self):
        if self.path is None:
            return
        directory = self.path.rsplit('/', 1)[0]
        filename = self.path.rsplit('/', 1)[1]

        previous_file = None
        for file in sorted(os.listdir(directory)):
            if file == filename:
                if previous_file is None:
                    return
                self.set_fairy_tale_text(directory + '/' + previous_file)
                break
            previous_file = file


    def next_fairy_tale_clicked(self):
        if self.path is None:
            return
        directory = self.path.rsplit('/', 1)[0]
        filename = self.path.rsplit('/', 1)[1]

        for file in sorted(os.listdir(directory)):
            if file > filename:
                self.set_fairy_tale_text(directory + '/' + file)
                break

    def set_fairy_tale_text(self, path):
        self.path = path
        text = open(path, 'r').read()
        self.fairy_tale_text.setText(text)
        self.filename.setText(path.rsplit('/', 1)[1])


    def closeEvent(self, event):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText("You have unsaved changes.")
        msg.setInformativeText("Do you want to save them before closing? Unsaved changes will be lost.")
        msg.setWindowTitle("Unsaved changes")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

        reply = msg.exec_()

        if reply == QtWidgets.QMessageBox.No:
            event.accept()
        elif reply == QtWidgets.QMessageBox.Cancel:
            event.ignore()
        else:
            result = self.save_annotations_clicked()
            if result:
                event.accept()
            else:
                event.ignore()