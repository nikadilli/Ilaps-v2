
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from style import IlapsStyle


class EndLoop(Exception):
    pass


class ElemWindow(QMainWindow):
    def __init__(self, parent):
        super(ElemWindow, self).__init__(parent)

        self.parent = parent

        # self.setGeometry(250, 250, 250, 250)
        self.setWindowTitle("Elements selection")
        self.setStyleSheet(IlapsStyle)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        self.elemWidget = QWidget()
        self.elemLayout = QGridLayout(self.elemWidget)
        self.mainLayout.addWidget(self.elemWidget)

        if self.parent.parent.Data is not None:
            elems_nr = len(self.parent.parent.Data.isotope_names)

            self.elemsChBxs = []

            try:
                for i in range(10):
                    for j in range(10):
                        idx = i*10 + j
                        if idx == elems_nr - 1:
                            raise EndLoop
                        self.elemsChBxs.append(
                            QCheckBox(self.parent.parent.Data.isotope_names[idx]))
                        if self.parent.parent.Data.isotope_names[idx] in self.parent.skip_isotopes:
                            self.elemsChBxs[idx].setChecked(True)
                        self.elemLayout.addWidget(self.elemsChBxs[idx], i, j)
            except EndLoop:
                pass
        else:
            self.elemLayout.addWidget(QLabel('Analysis not imported.'))

        # suma settings
        self.sumaWidget = QWidget()
        self.sumaLayout = QHBoxLayout(self.sumaWidget)
        self.mainLayout.addWidget(self.sumaWidget)

        self.sumaLbl = QLabel('Total sum [ppm]: ')
        self.sumaLayout.addWidget(self.sumaLbl, alignment=Qt.AlignLeft)

        self.sumaEntry = QLineEdit(str(self.parent.suma))
        self.sumaLayout.addWidget(self.sumaEntry, alignment=Qt.AlignLeft)

        self.sumaLayout.addStretch(1)

        # oxide form setting
        self.oxideWidget = QWidget()
        self.oxideLayout = QHBoxLayout(self.oxideWidget)
        self.mainLayout.addWidget(self.oxideWidget)

        self.oxideBox = QCheckBox('keep oxide form')
        if self.parent.oxide_form is True:
            self.oxideBox.setChecked(True)
        self.oxideLayout.addWidget(self.oxideBox)

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
        self.parent.skip_isotopes = [el.text()
                                     for el in self.elemsChBxs if el.isChecked()]
        self.parent.suma = float(self.sumaEntry.text())
        self.parent.oxide_form = self.oxideBox.isChecked()

        self.close()

    def cancel(self):
        self.close()
