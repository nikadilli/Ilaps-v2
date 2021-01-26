from PySide2.QtWidgets import *
from PySide2.QtCore import Qt


class StandardSelect(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout(self.mainWidget)
        self.btns = QWidget()
        self.layout2 = QVBoxLayout(self.btns)
        self.layout2.setAlignment(Qt.AlignCenter)

        self.stdList = QListWidget()
        self.addBtn = QPushButton('Add')
        self.addBtn.clicked.connect(self.add)
        self.removeBtn = QPushButton('Remove')
        self.removeBtn.clicked.connect(self.remove)
        self.showLst = QListWidget()

        self.layout2.addWidget(self.addBtn)
        self.layout2.addWidget(self.removeBtn)
        self.layout.addWidget(self.stdList)
        self.layout.addWidget(self.btns)
        self.layout.addWidget(self.showLst)

        self.setLayout(self.layout)

    def add(self):
        std = self.stdList.currentItem().text()
        self.showLst.addItem(std)

    def remove(self):
        for item in self.showLst.selectedItems():
            self.showLst.takeItem(self.showLst.row(item))

    def return_all(self):
        return [str(self.showLst.item(i).text()) for i in range(self.showLst.count())]