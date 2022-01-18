import sys
from PySide2.QtWidgets import *
from PySide2 import QtGui
from PySide2.QtCore import Qt
from widgets.tab_table import TabTable
from widgets.pandas_model import PandasModel
from widgets.drop_elems_window import ElemWindow

from imgMS import MSData as msd
from imgMS import MSEval as mse
from imgMS.side_functions import *


class BulkAnalysis(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.suma = 1000000
        self.skip_isotopes = []
        self.oxide_form = False

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout(self.mainWidget)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.settingsGroup = QGroupBox('Settings')
        layout = QGridLayout()

        self.lodLbl = QLabel('Detection limit')
        layout.addWidget(self.lodLbl, 0, 0)
        self.lodCombo = QComboBox()
        self.lodCombo.addItems(['beginning', 'end', 'all'])
        layout.addWidget(self.lodCombo, 1, 0)

        self.despikingLbl = QLabel('Despiking')
        layout.addWidget(self.despikingLbl, 0, 1)
        self.despikingCombo = QComboBox()
        self.despikingCombo.addItems(['True', 'False'])
        layout.addWidget(self.despikingCombo, 1, 1)

        self.methodLbl = QLabel('Method')
        layout.addWidget(self.methodLbl, 0, 2)
        self.method = QComboBox()
        self.method.addItems(['integral', 'intensity'])
        layout.addWidget(self.method, 1, 2)

        self.abltimeLbl = QLabel('Peak ablation time:')
        layout.addWidget(self.abltimeLbl, 0, 3)
        self.ablation = QLineEdit()
        layout.addWidget(self.ablation, 1, 3)

        self.standardLbl = QLabel('Standard')
        layout.addWidget(self.standardLbl, 0, 4)
        self.standard = QComboBox()
        self.standard.addItems(['Select standard'])
        layout.addWidget(self.standard, 1, 4)

        self.averageBtn = QPushButton('Average')
        layout.addWidget(self.averageBtn, 0, 5)
        self.averageBtn.clicked.connect(self.average)
        self.quantifyBtn = QPushButton('Quantification')
        layout.addWidget(self.quantifyBtn, 1, 5)
        self.quantifyBtn.clicked.connect(self.quantify)

        self.intStdCor = QPushButton('Internal Std Correction')
        layout.addWidget(self.intStdCor, 0, 6)
        self.intStdCor.clicked.connect(self.correctionIS)
        self.totSumCor = QPushButton('Total Sum Correction')
        layout.addWidget(self.totSumCor, 1, 6)
        self.totSumCor.clicked.connect(self.correctionTS)

        self.tssettingsBtn = QPushButton('TS settings')
        layout.addWidget(self.tssettingsBtn, 1, 7)
        self.tssettingsBtn.clicked.connect(self.elem_window)

        self.reportBtn = QPushButton('Report')
        layout.addWidget(self.reportBtn, 0, 8)
        self.reportBtn.clicked.connect(self.report)
        self.exportBtn = QPushButton('Export')
        layout.addWidget(self.exportBtn, 1, 8)
        self.exportBtn.clicked.connect(self.export)

        layout.setAlignment(Qt.AlignLeft)
        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.settingsGroup.setLayout(layout)

        self.mainLayout.addWidget(self.settingsGroup)

        self.table = TabTable(self)
        self.mainLayout.addWidget(self.table)

    def get_page(self):
        """
        Returns Page for bulk analysis for main stack of gui
        Returns
        -------
        mainWidget : QWidget
            The widget that the houses the bulk analysis screen.
        """
        return self.mainWidget

    def average(self):
        """
        Calculate average of peaks for MSData
        """
        # get values from GUI
        method = self.method.currentText()
        scale = self.lodCombo.currentText()
        despiking = self.despikingCombo.currentText()

        # calculate average
        self.parent.Data.average_isotopes(
            despiked=despiking, bcgcor_method=scale, method=method)

        # check length of names vs peaks
        if len(self.parent.Data.names) != len(self.parent.Data.means.index):
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                f'Number of peaks({len(self.parent.Data.means.index)}) doesnt\
                    match number of given names({len(self.parent.Data.names)}).')
            error_dialog.exec_()
            return

        # show average data
        model = PandasModel(self.parent.Data.means)
        self.table.table['Average'].setModel(model)
        self.table.show_tab(1)

    def quantify(self):
        """
        Calculate quantified values of peaks for MSData
        """

        # get values
        std = self.standard.currentText()
        abltime = self.ablation.text()
        method = self.method.currentText()
        scale = self.lodCombo.currentText()

        # check if abltime not missing
        if abltime == '' and method == 'integral':
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                'Missing ablation time while method is integral.')
            error_dialog.exec_()
            return

        # check if abltime was endered and convert to mumber
        if abltime != '':
            abltime = float(abltime)
        else:
            abltime = None

        # check if selected standard was measured
        if std not in self.parent.Data.names:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('{} not in peak names.'.format(std))
            error_dialog.exec_()
            return

        # quantify data
        self.parent.Data.quantify_isotopes(srm_name=std)

        # calculate detection limit
        self.parent.Data.detection_limit(
            method=method, scale=scale, ablation_time=abltime)

        # show quantified data
        model = PandasModel(self.parent.Data.quantified)
        self.table.table['Quantified'].setModel(model)

        self.table.show_tab(2)

    def correctionIS(self):
        """
        Correct quantified values of MSData using internal standard correction
        """
        # check if parameters were imported and contain coef for IS
        if self.parent.Data.param is None:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                'Missing data for internal standard correction.')
            error_dialog.exec_()
            return
        elif self.parent.Data.param.is_coef is None:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                'Missing data for internal standard correction.')
            error_dialog.exec_()
            return

        # correct data
        self.parent.Data.IS_correction()

        # show data corrected by internal standard
        model = PandasModel(
            self.parent.Data.corrected_IS[self.parent.Data.param.is_coef.columns[0]])
        self.table.table['Internal Std'].setModel(model)
        self.table.show_tab(3)

    def correctionTS(self):
        """
        Correct quantified values of MSData using total sum correction
        """
        # correct data
        self.parent.Data.TS_correction(
            suma=self.suma, skip_isotopes=self.skip_isotopes, return_oxides=self.oxide_form)

        # show data corrected by total sum
        model = PandasModel(self.parent.Data.corrected_TS)
        self.table.table['Total Sum'].setModel(model)
        self.table.show_tab(4)

    def report(self):
        # round all data
        self.parent.Data.report()

        # show all data
        if self.parent.Data.quantified is not None:
            model = PandasModel(self.parent.Data.quantified)
            self.table.table['Quantified'].setModel(model)
        if self.parent.Data.corrected_IS is not None:
            model = PandasModel(
                self.parent.Data.corrected_IS[self.parent.Data.param.is_coef.columns[0]])
            self.table.table['Internal Std'].setModel(model)
        if self.parent.Data.corrected_TS is not None:
            model = PandasModel(self.parent.Data.corrected_TS)
            self.table.table['Total Sum'].setModel(model)

    def export(self):
        # get filename
        filename, filters = QFileDialog.getSaveFileName(
            self, 'Save file', '', 'All files (*.*);;Excel (*.xlsx, *.xls)')

        # save data
        if filename:
            self.parent.Data.export(filename)

    def elem_window(self):
        window_to_open = ElemWindow(self)
        window_to_open.show()
