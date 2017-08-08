import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
import serial
import time
import numpy as np
from pylab import *  # do not import all, (very!) bad practices
import matplotlib.pyplot as plt
from datetime import datetime
import os
from PIL import Image

# the below should be somewhere else
ser = serial.Serial()  # styling
ser.baudrate = 57600
ser.port = 'COM5'
ser.timeout = 1 


class UI_Main(object):
    def setupUI(self, MainWindow):  # mainwindow should start lowercase (uppercase are for classes)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)  # styling

        # no need to have methods below for what they are doing
        def hbox(where):
            return QtWidgets.QHBoxLayout(where)

        def vbox(where):
            return QtWidgets.QVBoxLayout(where)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout1 = hbox(self.centralwidget)
        self.horizontalLayout1.setObjectName("horizontalLayout1")

        self.verticalLayout1 = vbox(self.centralwidget)
        self.verticalLayout1.setObjectName("verticalLayout1")

        self.verticalLayout2 = vbox(self.centralwidget)
        self.verticalLayout2.setObjectName("verticalLayout2")

        self.operator = vbox(self.centralwidget)
        self.operator.setObjectName("operator")
        self.operator_label = QtWidgets.QLabel(self.centralwidget)
        self.operator_label.setObjectName("operator_label")
        self.operator.addWidget(self.operator_label)
        self.operator_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.operator_edit.setObjectName("operator_edit")
        self.operator.addWidget(self.operator_edit)
        self.verticalLayout1.addLayout(self.operator)

        self.sample = vbox(self.centralwidget)
        self.sample.setObjectName("sample")
        self.sample_label = QtWidgets.QLabel(self.centralwidget)
        self.sample_label.setObjectName("sample_label")
        self.sample.addWidget(self.sample_label)
        self.sample_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.sample_edit.setObjectName("sample_edit")
        self.sample.addWidget(self.sample_edit)
        self.verticalLayout1.addLayout(self.sample)

        self.filepath = vbox(self.centralwidget)
        self.filepath.setObjectName("filepath")
        self.filepath_label = QtWidgets.QLabel(self.centralwidget)
        self.filepath_label.setObjectName("filepath_label")
        self.filepath.addWidget(self.filepath_label)
        self.filepath_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.filepath_edit.setObjectName("filepath_edit")
        self.filepath.addWidget(self.filepath_edit)
        self.verticalLayout1.addLayout(self.filepath)

        self.buttons_layout = vbox(self.centralwidget)
        self.buttons_layout.setObjectName("buttons_layout")
        self.btn_measure = QtWidgets.QPushButton(self.centralwidget)
        self.btn_measure.setEnabled(True)
        self.btn_measure.setObjectName("btn_measure")
        self.buttons_layout.addWidget(self.btn_measure)
        self.verticalLayout1.addLayout(self.buttons_layout)

        self.sample_measured = hbox(self.centralwidget)
        self.sample_measured.setObjectName("sample_measured")
        self.sample_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.sample_measuredLabel.setObjectName("sample_measuredLabel")
        self.sample_measured.addWidget(self.sample_measuredLabel)
        self.sample_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.sample_measuredText.setObjectName("sample_measuredText")
        self.sample_measured.addWidget(self.sample_measuredText)
        self.verticalLayout2.addLayout(self.sample_measured)

        self.Rs_measured = hbox(self.centralwidget)  # all attributes must start with lowercase, or underscore
        self.Rs_measured.setObjectName("Rs_measured")
        self.Rs_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.Rs_measuredLabel.setObjectName("Rs_measuredLabel")
        self.Rs_measured.addWidget(self.Rs_measuredLabel)
        self.Rs_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.Rs_measuredText.setObjectName("Rs_measuredText")
        self.Rs_measured.addWidget(self.Rs_measuredText)
        self.verticalLayout2.addLayout(self.Rs_measured)

        self.Rsh_measured = hbox(self.centralwidget)
        self.Rsh_measured.setObjectName("Rsh_measured")
        self.Rsh_measuredLabel = QtWidgets.QLabel(self.centralwidget)
        self.Rsh_measuredLabel.setObjectName("Rsh_measuredLabel")
        self.Rsh_measured.addWidget(self.Rsh_measuredLabel)
        self.Rsh_measuredText = QtWidgets.QLabel(self.centralwidget)
        self.Rsh_measuredText.setObjectName("Rsh_measuredText")
        self.Rsh_measured.addWidget(self.Rsh_measuredText)
        self.verticalLayout2.addLayout(self.Rsh_measured)

        self.DIV = vbox(self.centralwidget)
        self.DIV_graph = QtWidgets.QLabel(self.centralwidget)
        self.DIV_graph_pix = QtGui.QPixmap(None)
        self.DIV_graph.resize(688, 473)
        self.DIV_graph.setPixmap(self.DIV_graph_pix)
        self.DIV_graph.setObjectName("DIV_graph")
        self.DIV.addWidget(self.DIV_graph)
        self.verticalLayout2.addLayout(self.DIV)

        self.horizontalLayout1.addLayout(self.verticalLayout1)
        self.horizontalLayout1.addLayout(self.verticalLayout2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUI(MainWindow)

    # the method above does not really need to here, but can be at the end of __init__
    def retranslateUI(self, MainWindow):  # --> main_window
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DIV Testing Window"))
        self.operator_label.setText(_translate("MainWindow", "Operator:"))
        self.sample_label.setText(_translate("MainWindow", "Sample:"))
        self.filepath_label.setText(_translate("MainWindow", "Filename:"))
        self.btn_measure.setText(_translate("MainWindow", "Measure"))
        self.sample_measuredLabel.setText(_translate("MainWindow", "Measured Sample: "))
        self.sample_measuredText.setText(_translate("MainWindow", "Waiting for Measurement Data"))
        self.Rs_measuredLabel.setText(_translate("MainWindow", "Measured Rs: "))
        self.Rs_measuredText.setText(_translate("MainWindow", "Waiting for Measurement Data"))
        self.Rsh_measuredLabel.setText(_translate("MainWindow", "Measured Rsh: "))
        self.Rsh_measuredText.setText(_translate("MainWindow", "Waiting for Measurement Data"))


class BeginMeasurements(QThread):

    measurement = pyqtSignal(str)  # why do you need two signals?
    finished = pyqtSignal()

    def __init__(self, parent=None):  # styling
        super(BeginMeasurements, self).__init__(parent)

    def TakeMeasurement(self):  # -> take_measurement
        Rs_min = 2.5
        return Rs_min

    def run(self):
        print(y)
        Rs_min = str(self.TakeMeasurement())  # lowercase
        print(yes1)
        self.measurement.emit(Rs_min)
        print(yes2)
        time.sleep(2)
        self.finished.emit()  # this is probably not needed, or if needed, should be explained


class CreateUIThread(QMainWindow, UI_Main):  # could have a better naming such as Window
    def __init__(self, parent=None):
        super(CreateUIThread, self).__init__(parent)
        # what is done here is complicated unless you really understand what you are doing
        # my recomendation would be: keep all things about mainWindow here, and create the 
        # main widget in the UI_Main, something like that:
        #
        # class UI_Main(QtWidgets.Qwidget):  <-- UI_Main is going to be our central widget 
        # ... all UI stuff + signal handling for the thread
        #
        # class CreateUIThread(QMainWindow):
        #     def __init__(self):
        #         super(CreateUIThread, self).__init__()
        #         self.setObjectName("MainWindow")
        #         self.resize(800, 600)
        #         self.central_widget = UI_Main()
        #         self.setCentralWidget(self.central_widget)

        self.setupUI(self)
        self.btn_measure.clicked.connect(self.UpdateUI)  # move this to UI_main
        self.show()

    def UpdateUI(self):  # move this to UI_main
        self.getMeasurement = BeginMeasurements()
        print(str(type(self.getMeasurement)))
        self.sample_measuredText.setText(self.sample_edit.text())
        self.getMeasurement.measurement.connect(self.change)
        self.getMeasurement.finished.connect(self.done)
        self.getMeasurement.start()

    def change(self, word): # UI_main
        print(9)
        _translate = QtCore.QCoreApplication.translate
        print(10)
        self.Rs_measuredText.setText(_translate("MainWindow", "test"))

    def done(self):  # UI_main
        QMessageBox.information(self, "Done!", "Done fetching posts!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CreateUIThread()
    sys.exit(app.exec_())
