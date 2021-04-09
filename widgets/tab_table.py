from PySide2.QtWidgets import *


class TabTable(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabLst = {0: 'Raw', 1: 'Average',
                       2: 'Quantified', 3: 'Internal Std', 4: 'Total Sum'}
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

    def show_tab(self, idx):
        self.tabs.setCurrentIndex(idx)
