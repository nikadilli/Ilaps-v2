from PySide2.QtWidgets import *
from PySide2.QtCore import Qt


class PeakSelect(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout(self.mainWidget)
        self.btns = QWidget()
        self.layout2 = QVBoxLayout(self.btns)
        self.layout2.setAlignment(Qt.AlignCenter)

        self.peakList = QListWidget()
        self.peakList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selectBtn = QPushButton('Select all')
        self.selectBtn.clicked.connect(self.select_all)
        self.deselectBtn = QPushButton('Deselect all')
        self.deselectBtn.clicked.connect(self.deselect_all)
        self.apply = QPushButton('Apply')
        self.apply.clicked.connect(self.return_all)

        self.layout2.addWidget(self.selectBtn)
        self.layout2.addWidget(self.deselectBtn)
        self.layout2.addWidget(self.apply)
        self.layout.addWidget(self.peakList)
        self.layout.addWidget(self.btns)

        self.setLayout(self.layout)

    def select_all(self):
        pass

    def deselect_all(self):
        pass

    def return_all(self):
        return self.peakList.selectedItems()
