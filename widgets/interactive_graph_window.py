
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from style import IlapsStyle

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from imgMS import MSStats as mss


class EndLoop(Exception):
    pass


class GraphWindow(QMainWindow):
    def __init__(self, parent):
        super(GraphWindow, self).__init__(parent)

        self.parent = parent

        # self.setGeometry(250, 250, 250, 250)
        self.setWindowTitle("Interactive graph")
        self.setStyleSheet(IlapsStyle)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        self.graph = QWidget()
        self.graphLayout = QVBoxLayout(self.graph)
        self.fig = Figure()
        self.ax = self.fig.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet(
            "QWidget {border: None; background-color: white; color: black}")
            
        self.graphLayout.addWidget(self.toolbar)
        self.graphLayout.addWidget(self.canvas)

        self.mainLayout.addWidget(self.graph)
        
        mapa = self.parent.parent.Data.isotopes[self.parent.element.currentText()].elmap
        lasso = mss.interactive_average(mapa)(ax=self.ax)
        
        #self.ax.figure.canvas.draw_idle()

    def cancel(self):
        self.close()
