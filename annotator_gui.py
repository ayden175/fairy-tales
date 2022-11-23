import sys

from PyQt5.QtWidgets import QApplication
import tkinter

from annotator import AnnotatorWindow
import annotator.config as cfg

if __name__ == '__main__':
    tkinter.Tk().withdraw()

    app = QApplication(sys.argv)

    cfg.main_window = AnnotatorWindow()
    cfg.main_window.show()

    app.exec()
