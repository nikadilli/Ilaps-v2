from PySide2.QtWidgets import *


class MatrixTable(QWidget):
    def __init__(self, parent, tabs):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabLst = {}
        for i,tab in enumerate(tabs):
            self.tabLst[i] = tab
        self.tabs = QTabWidget()
        self.tab = [QWidget() for _ in range(len(self.tabLst.keys()))]
        self.table = {}

        for i, txt in self.tabLst.items():
            self.tabs.addTab(self.tab[i], "Tab {}".format(i))
            self.tabUI(i, txt)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def tabUI(self, i, tabtext):
        layout = QVBoxLayout()
        self.table[self.tabLst[i]] = QTableView()
        layout.addWidget(self.table[self.tabLst[i]])
        self.tabs.setTabText(i, tabtext)
        self.tab[i].setLayout(layout)

    def return_tab(self):
        return self.tabLst[self.tabs.currentIndex()]

    def update_tabs(self, tabs):
        for i, tab in enumerate(tabs):
            self.tabLst[i] = tab

        self.tab = [QWidget() for _ in range(len(self.tabLst.keys()))]

        for i, txt in self.tabLst.items():
            self.tabs.addTab(self.tab[i], "Tab {}".format(i))
            self.tabUI(i, txt)



