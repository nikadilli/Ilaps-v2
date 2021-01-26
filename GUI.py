
import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Qt

from layouts.welcome import Welcome
from layouts.data_select import DataSelect
from layouts.bulk_analysis import BulkAnalysis
from layouts.imaging import Imaging
from layouts.show_data import ShowData
from layouts.error_log import ErrorLog
from style import IlapsStyle


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(50, 50, 1500, 1000)
        self.setWindowTitle("Ilaps")
        self.setWindowIcon(QtGui.QIcon('./imgs/ilaps.png'))

        self.init_gui()
        self.setStyleSheet(IlapsStyle)

    def init_gui(self):

        self.Data = None
        self.Iolite = None
        self.logger = None

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # initialize all pages
        self.welcome = Welcome(self)
        self.data_select = DataSelect(self)
        self.bulk_analysis = BulkAnalysis(self)
        self.imaging = Imaging(self)
        self.show_data = ShowData(self)
        self.error_log = ErrorLog(self)

        # create main stack of pages
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.welcome.get_page())
        self.Stack.addWidget(self.data_select.get_page())
        self.Stack.addWidget(self.bulk_analysis.get_page())
        self.Stack.addWidget(self.imaging.get_page())
        self.Stack.addWidget(self.show_data.get_page())
        self.Stack.addWidget(self.error_log.get_page())
        self.Stack.setCurrentIndex(0)

        self.mainLayout.addWidget(self.Stack)

        # toolbar
        close = QAction(QtGui.QIcon('./imgs/quit.png'), 'Exit', self)
        close.setShortcut('Ctrl+Q')
        close.triggered.connect(self.close_application)

        home = QAction(QtGui.QIcon('./imgs/home.png'), 'Home', self)
        home.setShortcut('Ctrl+H')
        home.triggered.connect(lambda: self.change_layout(0))

        data = QAction(QtGui.QIcon('./imgs/graph.png'), 'Data analysis', self)
        data.setShortcut('Ctrl+D')
        data.triggered.connect(lambda: self.change_layout(1))

        bulk = QAction(QtGui.QIcon('./imgs/analysis.png'),
                       'Bulk analysis', self)
        bulk.setShortcut('Ctrl+A')
        bulk.triggered.connect(lambda: self.change_layout(2))

        imaging = QAction(QtGui.QIcon('./imgs/imaging.png'), 'Imaging', self)
        imaging.setShortcut('Ctrl+I')
        imaging.triggered.connect(lambda: self.change_layout(3))

        table = QAction(QtGui.QIcon('./imgs/table.png'), 'Show data', self)
        table.setShortcut('Ctrl+T')
        table.triggered.connect(lambda: self.change_layout(4))

        error = QAction(QtGui.QIcon('./imgs/error.png'),
                        'Show error log', self)
        error.setShortcut('Ctrl+E')
        error.triggered.connect(lambda: self.change_layout(5))

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(home)
        self.toolbar.addAction(data)
        self.toolbar.addAction(bulk)
        self.toolbar.addAction(imaging)
        self.toolbar.addAction(table)
        self.toolbar.addAction(error)
        self.toolbar.addAction(close)

    def change_layout(self, i):
        self.Stack.setCurrentIndex(i)

    def close_application(self):
        choice = QMessageBox.question(self, 'Quit!',
                                            "Are you sure you want to quit?",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
