import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
import serial
import time
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
from datetime import datetime
import os
from PIL import Image

ser = serial.Serial()
ser.baudrate = 57600
ser.port = 'COM5'
ser.timeout = 1


class UI_Main(QtWidgets.QWidget):
    def __init__(self, MainWindow):
        super(UI_Main, self).__init__()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.DIV_graph_pix = QtGui.QPixmap(None)
        self.DIV_graph = QtWidgets.QLabel(self.centralwidget)
        self.DIV = vbox(self.centralwidget)
        self.Rsh_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.Rsh_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.Rsh_measured = hbox(self.centralwidget)
        self.Rs_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.Rs_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.Rs_measured = hbox(self.centralwidget)
        self.sample_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.sample_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.sample_measured = hbox(self.centralwidget)
        self.btn_measure = QtWidgets.QPushButton(self.centralwidget)
        self.buttons_layout = vbox(self.centralwidget)
        self.filepath_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.filepath_label = QtWidgets.QLabel(self.centralwidget)
        self.filepath = vbox(self.centralwidget)
        self.sample_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.sample_label = QtWidgets.QLabel(self.centralwidget)
        self.sample = vbox(self.centralwidget)
        self.operator_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.operator_label = QtWidgets.QLabel(self.centralwidget)
        self.operator = vbox(self.centralwidget)
        self.verticalLayout2 = vbox(self.centralwidget)
        self.verticalLayout1 = vbox(self.centralwidget)
        self.horizontalLayout1 = hbox(self.centralwidget)

        self.setupUI(parent)

        self.retranslateUI(parent)
        self.btn_measure.clicked.connect(self.UpdateUI)
        self.show()

    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout1.setObjectName("horizontalLayout1")

        self.verticalLayout1.setObjectName("verticalLayout1")

        self.verticalLayout2.setObjectName("verticalLayout2")

        self.operator.setObjectName("operator")
        self.operator_label.setObjectName("operator_label")
        self.operator.addWidget(self.operator_label)
        self.operator_edit.setObjectName("operator_edit")
        self.operator.addWidget(self.operator_edit)
        self.verticalLayout1.addLayout(self.operator)

        self.sample.setObjectName("sample")
        self.sample_label.setObjectName("sample_label")
        self.sample.addWidget(self.sample_label)
        self.sample_edit.setObjectName("sample_edit")
        self.sample.addWidget(self.sample_edit)
        self.verticalLayout1.addLayout(self.sample)

        self.filepath.setObjectName("filepath")
        self.filepath_label.setObjectName("filepath_label")
        self.filepath.addWidget(self.filepath_label)
        self.filepath_edit.setObjectName("filepath_edit")
        self.filepath.addWidget(self.filepath_edit)
        self.verticalLayout1.addLayout(self.filepath)

        self.buttons_layout.setObjectName("buttons_layout")
        self.btn_measure.setEnabled(True)
        self.btn_measure.setObjectName("btn_measure")
        self.buttons_layout.addWidget(self.btn_measure)
        self.verticalLayout1.addLayout(self.buttons_layout)

        self.sample_measured.setObjectName("sample_measured")
        self.sample_measuredLabel.setObjectName("sample_measuredLabel")
        self.sample_measured.addWidget(self.sample_measuredLabel)
        self.sample_measuredText.setObjectName("sample_measuredText")
        self.sample_measured.addWidget(self.sample_measuredText)
        self.verticalLayout2.addLayout(self.sample_measured)

        self.Rs_measured.setObjectName("Rs_measured")
        self.Rs_measuredLabel.setObjectName("Rs_measuredLabel")
        self.Rs_measured.addWidget(self.Rs_measuredLabel)
        self.Rs_measuredText.setObjectName("Rs_measuredText")
        self.Rs_measured.addWidget(self.Rs_measuredText)
        self.verticalLayout2.addLayout(self.Rs_measured)

        self.Rsh_measured.setObjectName("Rsh_measured")
        self.Rsh_measuredLabel.setObjectName("Rsh_measuredLabel")
        self.Rsh_measured.addWidget(self.Rsh_measuredLabel)
        self.Rsh_measuredText.setObjectName("Rsh_measuredText")
        self.Rsh_measured.addWidget(self.Rsh_measuredText)
        self.verticalLayout2.addLayout(self.Rsh_measured)

        self.DIV_graph.resize(688, 473)
        self.DIV_graph.setPixmap(self.DIV_graph_pix)
        self.DIV_graph.setObjectName("DIV_graph")
        self.DIV.addWidget(self.DIV_graph)
        self.verticalLayout2.addLayout(self.DIV)

        self.horizontalLayout1.addLayout(self.verticalLayout1)
        self.horizontalLayout1.addLayout(self.verticalLayout2)

        self.setCentralWidget(self.centralwidget)

    def retranslateUI(self, MainWindow: object):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DIV Testing Window"))
        self.operator_label.setText(_translate("MainWindow", "Operator:"))
        self.sample_label.setText(_translate("MainWindow", "Sample:"))
        self.filepath_label.setText(_translate("MainWindow", "Filename:"))
        self.btn_measure.setText(_translate("MainWindow", "Measure"))
        self.sample_measuredLabel.setText(_translate("MainWindow", "Measured Sample: "))

    def UpdateUI(self):
        self.getMeasurement = BeginMeasurements()
        print(str(type(self.getMeasurement)))
        self.sample_measuredText.setText(self.sample_edit.text())
        self.getMeasurement.measurement.connect(self.change)
        self.getMeasurement.finished.connect(self.done)
        self.getMeasurement.start()

    def change(self):
        print(9)
        _translate = QtCore.QCoreApplication.translate
        print(10)
        self.Rs_measuredText.setText(_translate("MainWindow", "test"))

    def done(self):
        """
        Show the message that fetching posts is done.
        Disable Stop button enable the Start one and reset progress bar to 0.
        :return:
        """
        QMessageBox.information(self, "Done!")


class BeginMeasurements(QThread):
    measurement = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(BeginMeasurements, self).__init__(parent)

    def __del__(self):
        self.wait()

    def TakeMeasurement(self):

        #For now only put in code for Rs_min to try and start with sending this value
        Rs_min = 2.5
        return Rs_min

    def run(self):
        Rs_min = str(self.TakeMeasurement())
        self.measurement.emit(Rs_min)
        time.sleep(2)
        self.finished.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UI_Main(MainWindow)
    sys.exit(app.exec_())

