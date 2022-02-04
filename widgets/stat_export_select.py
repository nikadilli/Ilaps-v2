
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from style import IlapsStyle


class DataTableWindow(QMainWindow):
    def __init__(self, parent):
        super(DataTableWindow, self).__init__(parent)

        self.parent = parent

        # self.setGeometry(250, 250, 250, 250)
        self.setWindowTitle("Data selection for statistical export")
        self.setStyleSheet(IlapsStyle)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        groupbox = QGroupBox("Select data table")
        self.mainLayout.addWidget(groupbox)

        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)

        self.quantifiedRBtn = QRadioButton("Quantified")
        vbox.addWidget(self.quantifiedRBtn)
        self.TSCorrectedRBtn = QRadioButton("Corrected - Total sum")
        vbox.addWidget(self.TSCorrectedRBtn)
        self.ISCorrectedRBtn = QRadioButton("Corrected - Internal standard")
        vbox.addWidget(self.ISCorrectedRBtn)

        # control buttons
        self.buttonWidget = QWidget()
        self.buttonLayout = QHBoxLayout(self.buttonWidget)
        self.mainLayout.addWidget(self.buttonWidget)

        self.buttonLayout.addStretch(1)
        self.cancelBtn = QPushButton('Cancel')
        self.buttonLayout.addWidget(self.cancelBtn, alignment=Qt.AlignRight)
        self.cancelBtn.clicked.connect(self.cancel)

        self.selectBtn = QPushButton('Apply')
        self.buttonLayout.addWidget(self.selectBtn, alignment=Qt.AlignRight)
        self.selectBtn.clicked.connect(self.action)

    def action(self):

        if self.quantifiedRBtn.isChecked():
            self.parent.stat_export_table = 'quantified'
        elif self.TSCorrectedRBtn.isChecked():
            self.parent.stat_export_table = 'TScorrected'
        elif self.ISCorrectedRBtn.isChecked():
            self.parent.stat_export_table = 'IScorrected'

        self.close()

    def cancel(self):
        self.close()
