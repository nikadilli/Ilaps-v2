import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Qt


class StdRedirector(object):
    def __init__(self, text_widget, out=None):
        self.text_space = text_widget
        self.terminal = sys.stdout
        self.out = None

    def write(self, m):

        self.text_space.moveCursor(QtGui.QTextCursor.End)
        self.text_space.insertPlainText( m )

        if self.out:
            self.out.write(m)

    def flush(self):
        pass


class ErrorLog(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.errText = QTextEdit()
        self.errText.setReadOnly(True)
        self.mainLayout.addWidget(self.errText)

        sys.stderr = StdRedirector(self.errText, sys.stderr)

    def get_page(self):
        """
        Returns Page for bulk analysis for main stack of gui
        Returns
        -------
        mainWidget : QWidget
            The widget that the houses the bulk analysis screen.
        """
        return self.mainWidget
