from PySide2.QtWidgets import *
from PySide2.QtCore import Qt


class SelectTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.names = {0: 'treshold', 1: 'iolite', }

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tab1UI()
        self.tab2UI()

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tab1UI(self):
        layout = QFormLayout()
        self.bcg = QLineEdit()
        self.mltp = QLineEdit()
        layout.addRow("Background time", self.bcg)
        layout.addRow("SD multiply", self.mltp)
        self.tabs.setTabText(0, "Treshold")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        self.start = QLineEdit()
        layout.addRow("Start time", self.start)
        self.tabs.setTabText(1, "Iolite")
        self.namesCheckBox = QCheckBox('')
        self.namesCheckBox.setChecked(False)
        layout.addRow("Set names from iolite", self.namesCheckBox)
        self.tab2.setLayout(layout)

    def return_tab(self):
        return self.names[self.tabs.currentIndex()]
