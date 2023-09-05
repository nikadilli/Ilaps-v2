import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from imgMS import MSData as msd
from imgMS import MSStats as mss

from widgets.interactive_graph_window import GraphWindow


class Imaging(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.mainLayout.setAlignment(Qt.AlignTop)

        self.settingsGroup = QGroupBox('')
        layout = QFormLayout()

        self.dx = QLineEdit()
        layout.addRow(QLabel("Delta x: "), self.dx)
        self.dy = QLineEdit()
        layout.addRow(QLabel("Delta y: "), self.dy)
        self.background = QComboBox()
        self.background.addItems(['beginning', 'all'])
        layout.addRow('Background: ', self.background)
        layout.addRow(QLabel(""),)
        self.minz = QLineEdit()
        layout.addRow(QLabel("Min z: "), self.minz)
        self.maxz = QLineEdit()
        layout.addRow(QLabel("Max z: "), self.maxz)
        layout.addRow(QLabel(""), )
        self.intercept = QLineEdit()
        layout.addRow(QLabel("Intercept: "), self.intercept)
        self.slope = QLineEdit()
        layout.addRow(QLabel("Slope: "), self.slope)
        layout.addRow(QLabel(""), )
        self.units = QLineEdit()
        layout.addRow(QLabel("Units: "), self.units)
        self.title = QLineEdit()
        layout.addRow(QLabel("Title: "), self.title)
        layout.addRow(QLabel(""), )
        self.interpolation = QComboBox()
        self.interpolation.addItems(['nearest', 'bilinear', 'bicubic', 'spline16',
                                     'spline36', 'quadric', 'gaussian', 'lanczos'])

        layout.addRow('Interpolation: ', self.interpolation)
        self.cmap = QComboBox()
        self.cmap.addItems(['jet', 'grey', 'binary', 'viridis', 'plasma', 'inferno', 'magma', 'cividis',
                            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'
                            ])

        layout.addRow('Colour map: ', self.cmap)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.settingsGroup.setLayout(layout)
        self.mainLayout.addWidget(self.settingsGroup)

        self.settingsGroup2 = QGroupBox('')
        layout2 = QVBoxLayout()
        layout2.addStretch(5)

        self.matrixBtn = QPushButton('Create matrix')
        layout2.addWidget(self.matrixBtn)
        self.matrixBtn.clicked.connect(self.matrix)
        layout2.addStretch(1)

        self.element = QComboBox()
        layout2.addWidget(self.element)

        self.imageBtn = QPushButton('Image')
        layout2.addWidget(self.imageBtn)
        self.imageBtn.clicked.connect(self.image)

        self.rotateBtn = QPushButton('Rotate')
        layout2.addWidget(self.rotateBtn)
        self.rotateBtn.clicked.connect(self.rotate)

        self.VFlipBtn = QPushButton('VFlip')
        layout2.addWidget(self.VFlipBtn)
        self.VFlipBtn.clicked.connect(self.vflip)

        self.HflipBtn = QPushButton('HFlip')
        layout2.addWidget(self.HflipBtn)
        self.HflipBtn.clicked.connect(self.hflip)

        self.AreaStatsBtn = QPushButton('Area Stats')
        layout2.addWidget(self.AreaStatsBtn)
        self.AreaStatsBtn.clicked.connect(self.areastats)

        layout2.addStretch(1)

        self.quantifyBtn = QPushButton('Quantify')
        layout2.addWidget(self.quantifyBtn)
        self.quantifyBtn.clicked.connect(self.quantify)

        self.quantifyAllBtn = QPushButton('Quantify all')
        self.quantifyAllBtn.clicked.connect(self.quantify_all)
        layout2.addWidget(self.quantifyAllBtn)

        layout2.addStretch(1)

        self.importMatrixBtn = QPushButton('Import Matrix')
        layout2.addWidget(self.importMatrixBtn)
        self.importMatrixBtn.clicked.connect(self.import_matrix)

        self.exportMatrixBtn = QPushButton('Export Matrix')
        layout2.addWidget(self.exportMatrixBtn)
        self.exportMatrixBtn.clicked.connect(self.export_matrix)

        self.exportQuantifiedBtn = QPushButton('Export Quantified')
        self.exportQuantifiedBtn.clicked.connect(self.export_quantified)
        layout2.addWidget(self.exportQuantifiedBtn)

        layout2.addStretch(5)

        self.settingsGroup2.setLayout(layout2)
        self.mainLayout.addWidget(self.settingsGroup2)

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

    def get_page(self):
        """
        Returns Page for bulk analysis for main stack of gui
        Returns
        -------
        mainWidget : QWidget
            The widget that the houses the bulk analysis screen.
        """
        return self.mainWidget

    def matrix(self):
        # get values
        dx = int(self.dx.text())
        dy = int(self.dy.text())

        # create maps
        self.parent.Data.create_maps(
            despiked=False, bcgcor_method=self.background.currentText(), dx=dx, dy=dy)

    def image(self, quantified=False):
        # check if maps are created
        if not self.parent.Data.isotopes[self.parent.Data.isotope_names[0]].elmap:
            msg_dialog = QMessageBox()
            msg_dialog.setIcon(QMessageBox.Information)
            msg_dialog.setText('No matrix to plot.')
            msg_dialog.exec_()
            return

        # get values
        elem = self.element.currentText()
        interpolation = self.interpolation.currentText()
        cmap = self.cmap.currentText()
        title = self.title.text()
        units = self.units.text()

        s = self.minz.text()
        if s.replace('.', '', 1).isdigit():
            vmin = float(self.minz.text())
        else:
            vmin = None

        s = self.maxz.text()
        if s.replace('.', '', 1).isdigit():
            vmax = float(self.maxz.text())
        else:
            vmax = None

        # clear figure
        self.fig.clear()
        self.ax = self.fig.subplots()
        self.ax.figure.canvas.draw_idle()

        # show image
        self.parent.Data.isotopes[elem].elmap(fig=self.fig, ax=self.ax, units=units, title=title,
                                              clb=True, quantified=quantified, vmin=vmin, vmax=vmax,
                                              interpolation=interpolation, cmap=cmap)

        self.ax.figure.canvas.draw_idle()

    def rotate(self):
        elem = self.element.currentText()
        self.parent.Data.isotopes[elem].elmap.rotate()
        self.image()

    def vflip(self):
        elem = self.element.currentText()
        self.parent.Data.isotopes[elem].elmap.flip(axis=0)
        self.image()

    def hflip(self):
        elem = self.element.currentText()
        self.parent.Data.isotopes[elem].elmap.flip(axis=1)
        self.image()

    def areastats(self):
        window_to_open = GraphWindow(self)
        window_to_open.setAttribute(Qt.WA_DeleteOnClose)
        window_to_open.show()      

    def import_matrix(self):
        # get file
        filename, filters = QFileDialog.getOpenFileName(self, caption='Open file', dir='.',
                                                        filter="Excel files (*.xlsx)")
        if not filename:
            return

        # create empty MSData
        self.parent.Data = msd.MSData()
        self.parent.Data.logger = self.parent.logger

        # create isotopes from names of sheets
        file = pd.ExcelFile(filename)
        self.parent.Data.isotope_names = file.sheet_names
        for el in self.parent.Data.isotope_names:
            self.parent.Data.isotopes[el] = msd.Isotope(el)
            self.parent.Data.isotopes[el].elmap = msd.ElementalMap()

        # import maps
        self.parent.Data.import_matrices(filename)

        # add elements to combo box
        elems = self.parent.Data.isotope_names
        self.element.addItems(elems)
        self.parent.show_data.elem.addItems(elems)

    def export_matrix(self):
        # check if maps exists and get file to save
        if self.parent.Data.isotopes[self.parent.Data.isotope_names[0]].elmap:
            filename, filters = QFileDialog.getSaveFileName(
                self, caption='Save file', dir='.')
        else:
            msg_dialog = QMessageBox()
            msg_dialog.setIcon(QMessageBox.Information)
            msg_dialog.setText('No data to save.')
            msg_dialog.exec_()
            return

        # save data
        if filename:
            self.parent.Data.export_matrices(filename)

    def quantify(self):
        # get values
        if self.intercept.text().isdigit():
            intercept = int(self.intercept.text())
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Missing intercept.')
            error_dialog.exec_()
            return
        if self.slope.text().isdigit():
            slope = int(self.slope.text())
        else:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Missing slope.')
            error_dialog.exec_()
            return
        elem = self.element.currentText()

        # quantify maps
        self.parent.Data.isotopes[elem].elmap.quantify_map(
            intercept=intercept, slope=slope)

        # replot quantified
        self.image(quantified=True)

    def quantify_all(self):
        msg_dialog = QMessageBox()
        msg_dialog.setIcon(QMessageBox.Information)
        msg_dialog.setText('Not supported yet.')
        msg_dialog.exec_()

    def export_quantified(self):

        filename, filters = QFileDialog.getSaveFileName(
            self, caption='Open file', dir='.')

        if filename:
            self.parent.Data.export_matrices(filename, quantified=True)
