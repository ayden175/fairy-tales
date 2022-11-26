import os

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from tkinter import filedialog

import annotator.config as cfg
from annotator.data_saver import DataSaver
from annotator.text_button import TextButton
from annotator.text_layout import TextLayout
from annotator.color_button import ColorButton

class AnnotatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.alignments = ['good', 'neutral', 'bad']
        self.initUI()
        self.dataSaver = DataSaver()
        self.show()


    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
        uic.loadUi('annotator/annotator.ui', self)
        for color in cfg.colors:
            self.add_character_clicked(color)

        self.textScrollArea.setLayout(TextLayout(self.textScrollArea))
        self.no_char_color.setFixedSize(25, 25)
        self.no_char_color.setStyleSheet("background-color: white;")

        self.load_fairy_tale.clicked.connect(self.load_fairy_tale_clicked)
        self.previous_fairy_tale.clicked.connect(self.previous_fairy_tale_clicked)
        self.next_fairy_tale.clicked.connect(self.next_fairy_tale_clicked)
        self.add_character.clicked.connect(self.add_character_clicked)
        self.checkbox_no_char.clicked.connect(lambda: self.checkbox_clicked(self.checkbox_no_char))

        #self.load_annotations.triggered.connect(self.load_annotations_clicked)
        self.save_annotations.clicked.connect(self.save_annotations_clicked)

    def checkbox_clicked(self, checkbox):
        for j in range(self.characters_layout.count()-4):
            self.characters_layout.itemAt(j+2).itemAt(1).widget().setChecked(False)
        checkbox.setChecked(True)

        print(cfg.char_lists)
        for j in range(self.characters_layout.count()-4):
            if self.characters_layout.itemAt(j+2).itemAt(1).widget() == checkbox:
                name = self.characters_layout.itemAt(j+2).itemAt(2).widget()

                for char in cfg.char_lists:
                    print("-------------")
                    print(char['name'])
                    print(name)
                    if char['name'] == name:
                        print('found')
                        print(char)
                        cfg.active_char = char
                        return

        cfg.active_char = None

    def text_button_clicked(self, button):
        if cfg.active_char is not None and button in cfg.active_char['buttons']:
            return

        if cfg.active_char is None and button.entity is None:
            return

        cfg.unsaved_changes = True

        for char in cfg.char_lists:
            if button in char['buttons']:
                char['buttons'].remove(button)
                button.removeInfo()
                break

        if cfg.active_char is None:
            return
            
        cfg.active_char['buttons'].append(button)
        button.setInfo(cfg.active_char['name'], cfg.active_char['alignment'], cfg.active_char['color'])

    def load_annotations_clicked(self):
        if cfg.unsaved_changes:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("You have unsaved changes.")
            msg.setInformativeText("Loading annotations will discard all unsaved changes. Do you want to continue?")
            msg.setWindowTitle("Unsaved changes")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

            reply = msg.exec_()

            if reply == QtWidgets.QMessageBox.Cancel:
                return

        path = filedialog.askopenfilename(defaultextension='.yaml', filetypes=[('YAML files', '*.yaml')])
        if path == '':
            return
        # TODO: load annotations from file
        self.dataSaver.import_yaml()


    def save_annotations_clicked(self):
        if cfg.path is None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("No fairy tale is loaded.")
            msg.setWindowTitle("No fairy tale loaded")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return

        for char in cfg.char_lists:
            if len(char['buttons']) > 0 and char['name'].text().strip() == '':
                msg = QtWidgets.QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Character name is not set.")
                msg.setInformativeText("There are used characters without a name. Please name all used characters before saving.")
                msg.setWindowTitle("Characters without names")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return

        names = []
        for char in cfg.char_lists:
            if len(char['buttons']) > 0:
                names.append(char['name'].text().lower().strip())

        if len(names) != len(set(names)):
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("There are duplicate names.")
            msg.setInformativeText("All characters must have a unique name. Please give every used charactera a unique name before saving.")
            msg.setWindowTitle("Duplicate names")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return

        self.check_buttons()
        if not cfg.unsaved_changes:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("There are no unsaved changes.")
            msg.setWindowTitle("No unsaved changes")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
            
        self.dataSaver.export_csv()

        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Annotations saved successfully.")
        msg.setWindowTitle("Changes saved")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

        return True


    def add_character_clicked(self, colorname='yellow'):
        hbox = QtWidgets.QHBoxLayout()

        if not colorname:
            colorname = 'yellow'
        color = ColorButton(colorname)
        hbox.addWidget(color)

        active = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        active.setText("Active")
        active.clicked.connect(lambda: self.checkbox_clicked(active))
        hbox.addWidget(active)

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
        remove.setText('Clear')
        remove.clicked.connect(color.remove_text)
        hbox.addWidget(remove)

        hbox.setStretch(2, 2)
        hbox.setStretch(3, 1)
        self.characters_layout.insertLayout(self.characters_layout.count()-2, hbox)

        cfg.char_lists.append({'name': name, 'alignment': alignment, 'color': color, 'buttons': []})

    def load_fairy_tale_clicked(self):
        if self.unsaved_changes():
            return

        path = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if path == '':
            return

        self.set_fairy_tale_text(path)


    def previous_fairy_tale_clicked(self):
        if cfg.path is None:
            return

        if self.unsaved_changes():
            return

        previous_file = None

        files = [f for f in os.listdir(cfg.path) if os.path.isfile(os.path.join(cfg.path, f))]
        for file in sorted(files):
            if file == cfg.story:
                if previous_file is None:
                    return
                self.set_fairy_tale_text(cfg.path + '/' + previous_file)
                break
            previous_file = file


    def next_fairy_tale_clicked(self):
        if cfg.path is None:
            return

        if self.unsaved_changes():
            return

        files = [f for f in os.listdir(cfg.path) if os.path.isfile(os.path.join(cfg.path, f))]
        for file in sorted(files):
            if file > cfg.story:
                self.set_fairy_tale_text(cfg.path + '/' + file)
                break

    def set_fairy_tale_text(self, path):
        # clear textScrollArea
        self.textScrollArea.layout().clear()

        cfg.path = path.rsplit('/', 1)[0]
        cfg.story = path.rsplit('/', 1)[1]

        text = open(path, 'r').read()
        paragraphs = text.split('\n')

        cfg.words = []
        for p in paragraphs:
            words = p.split(' ')
            cfg.words.append([])
            for w in words:
                button = TextButton(w, self.textScrollArea)
                button.addClick(self.text_button_clicked)
                cfg.words[-1].append(button)
        
        # add buttons to textlayout
        self.textScrollArea.layout().setButtons(cfg.words)
        self.filename.setText(path.rsplit('/', 1)[1])

        for char in cfg.char_lists:
            char['name'].clear()
            char['alignment'].setCurrentText('neutral')
            char['buttons'] = []

    
    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.textScrollArea.layout().updateLayout()

    
    def unsaved_changes(self):
        if cfg.story is None:
            return False

        self.check_buttons()
        if cfg.unsaved_changes:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('annotator/unicorn.png'))
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("You have unsaved changes.")
            msg.setInformativeText("Do you want to save them before loading a new fairy tale? Unsaved changes will be lost.")
            msg.setWindowTitle("Unsaved changes")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

            reply = msg.exec_()

            if reply == QtWidgets.QMessageBox.No:
                return False
            elif reply == QtWidgets.QMessageBox.Cancel:
                return True
            else:
                result = self.save_annotations_clicked()
                if result:
                    return False
                else:
                    return True
            
        return False

    def check_buttons(self):
        found_changes = False
        for char in cfg.char_lists:
            if len(char['buttons']) > 0:
                found_changes = True

        if not found_changes:
            cfg.unsaved_changes = False

    def closeEvent(self, event):
        self.check_buttons()
        if cfg.unsaved_changes:
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
                    
        else:
            event.accept()