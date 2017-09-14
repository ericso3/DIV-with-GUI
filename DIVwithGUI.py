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
# import os
# from PIL import Image

# ser=serial.Serial()
# ser.baudrate = 57600
# ser.port = 'COM5'
# ser.timeout = 1
# SAVENAME = ""

class UI_MainWindow(QtWidgets.QWidget):

    def __init__(self) -> None:
        super(UI_MainWindow, self).__init__()

        self.measure = Measurements()
        self.measure.measurement_sig.connect(self.change_ui)
        # self.measure.save_sig.connect(self.save_data)

        # self.measure.start()

        self.setObjectName("mainWindow")
        self.resize(800,600)

        horizontal_layout1 = QtWidgets.QHBoxLayout()
        horizontal_layout1.setObjectName("horizontal_layout1")

        vertical_layout1 = QtWidgets.QVBoxLayout()
        vertical_layout1.setObjectName("vertical_layout1")

        vertical_layout2 = QtWidgets.QVBoxLayout()
        vertical_layout2.setObjectName("vertical_layout2")

        operator = QtWidgets.QVBoxLayout()
        operator.setObjectName("operator")
        self.operator_label = QtWidgets.QLabel()
        self.operator_label.setObjectName("operator_label")
        operator.addWidget(self.operator_label)
        self.operator_edit = QtWidgets.QLineEdit()
        self.operator_edit.setObjectName("operator_edit")
        operator.addWidget(self.operator_edit)
        vertical_layout1.addLayout(operator)

        sample = QtWidgets.QVBoxLayout()
        sample.setObjectName("sample")
        self.sample_label = QtWidgets.QLabel()
        self.sample_label.setObjectName("sample_label")
        sample.addWidget(self.sample_label)
        self.sample_edit = QtWidgets.QLineEdit()
        self.sample_edit.setObjectName("sample_edit")
        sample.addWidget(self.sample_edit)
        vertical_layout1.addLayout(sample)

        filepath = QtWidgets.QVBoxLayout()
        filepath.setObjectName("filepath")
        self.filepath_label = QtWidgets.QLabel()
        self.filepath_label.setObjectName("filepath_label")
        filepath.addWidget(self.filepath_label)
        self.filepath_edit = QtWidgets.QLineEdit()
        self.filepath_edit.setText('C:\\Users\\python\\Desktop\\DIV Results')
        self.filepath_edit.setObjectName("filepath_edit")
        filepath.addWidget(self.filepath_edit)
        vertical_layout1.addLayout(filepath)

        btn_measure = QtWidgets.QPushButton()
        btn_measure.setEnabled(True)
        btn_measure.setObjectName("btn_measure")
        btn_measure.setFixedSize(450, 60)
        btn_measure.clicked.connect(self.click)
        vertical_layout1.addWidget(btn_measure)

        sample_measured = QtWidgets.QVBoxLayout()
        sample_measured.setObjectName("sample_measured")
        self.sample_measuredLabel = QtWidgets.QLabel()
        self.sample_measuredLabel.setObjectName("sample_measuredLabel")
        sample_measured.addWidget(self.sample_measuredLabel)
        self.sample_measuredText = QtWidgets.QLabel()
        self.sample_measuredText.setObjectName("sample_measuredText")
        sample_measured.addWidget(self.sample_measuredText)
        vertical_layout2.addLayout(sample_measured)

        rs_measured = QtWidgets.QVBoxLayout()
        rs_measured.setObjectName("rs_measured")
        self.rs_measuredLabel = QtWidgets.QLabel()
        self.rs_measuredLabel.setObjectName("rs_measuredLabel")
        rs_measured.addWidget(self.rs_measuredLabel)
        self.rs_measuredText = QtWidgets.QLabel()
        self.rs_measuredText.setObjectName("rs_measuredText")
        rs_measured.addWidget(self.rs_measuredText)
        vertical_layout2.addLayout(rs_measured)

        rsh_measured = QtWidgets.QVBoxLayout()
        rsh_measured.setObjectName("rsh_measured")
        self.rsh_measuredLabel = QtWidgets.QLabel()
        self.rsh_measuredLabel.setObjectName("rsh_measuredLabel")
        rsh_measured.addWidget(self.rsh_measuredLabel)
        self.rsh_measuredText = QtWidgets.QLabel()
        self.rsh_measuredText.setObjectName("rsh_measuredText")
        rsh_measured.addWidget(self.rsh_measuredText)
        vertical_layout2.addLayout(rsh_measured)


        div = QtWidgets.QVBoxLayout()
        self.div_graph = QtWidgets.QLabel()
        # self.div_graph_pix = QtGui.QPixmap('C:/Users/eso/Documents/Python Scripts/Python Project DIV/Test')
        self.div_graph_pix = QtGui.QPixmap(None)
        self.div_graph.resize(688, 473)
        self.div_graph.setPixmap(self.div_graph_pix)
        self.div_graph.setObjectName("div_graph")
        div.addWidget(self.div_graph)
        vertical_layout2.addLayout(div)

        horizontal_layout1.addLayout(vertical_layout1)
        horizontal_layout1.addLayout(vertical_layout2)

        self.setLayout(horizontal_layout1)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainWindow", "DIV Testing Window"))
        self.operator_label.setText(_translate("mainWindow", "Operator:"))
        self.sample_label.setText(_translate("mainWindow", "Sample:"))
        self.filepath_label.setText(_translate("mainWindow", "Filename:"))
        btn_measure.setText(_translate("mainWindow", "Measure"))
        self.sample_measuredLabel.setText(_translate("mainWindow", "Measured Sample: "))
        self.sample_measuredText.setText(_translate("mainWindow", "Waiting for Measurement Data"))
        self.rs_measuredLabel.setText(_translate("mainWindow", "Measured Rs: "))
        self.rs_measuredText.setText(_translate("mainWindow", "Waiting for Measurement Data"))
        self.rsh_measuredLabel.setText(_translate("mainWindow", "Measured Low Current dV/dI: "))
        self.rsh_measuredText.setText(_translate("mainWindow", "Waiting for Measurement Data"))
        self.show()

    def change_ui(self, n: list) -> None:
        _translate = QtCore.QCoreApplication.translate
        print(1)
        measurements = n[0]
        RS_MIN = measurements[0]
        RSH_MEAN = measurements[1]
        date_time = str(datetime.now())
        DIVoutput = n[1]
        self.rs_measuredText.setText(_translate("mainWindow", str(RS_MIN)))
        self.rsh_measuredText.setText(_translate("mainWindow", str(RSH_MEAN)))
        self.sample_measuredText.setText(_translate("mainWindow", self.sample_edit.text()))
        # print(DIVoutput)

        def WriteToFile(message, OutputFile):
            file = open(OutputFile + '.txt', 'a')
            file.write(message)
            file.close()

        operator = self.operator_edit.text()
        rootdir= self.filepath_edit.text()
        savename = operator + '_' + self.sample_edit.text()

        font = {'family': 'sans-serif',
                'weight': 'bold',
                'size': 16}
        title_font = {'fontname': 'Arial', 'size': '12', 'color': 'black', 'weight': 'normal',
                      'verticalalignment': 'bottom'}  # Bottom vertical alignment for more space
        matplotlib.rc('font', **font)

        fig, ax1 = plt.subplots()

        ax1.plot(DIVoutput[:, 0], DIVoutput[:, 1], 'b.')
        ax1.set_xlabel('V (V)')
        # Make the y-axis label and tick labels match the line color.
        ax1.set_ylabel('I (A)', color='b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')

        ax2 = ax1.twinx()
        # s2 = np.sin(2*np.pi*t)
        ax2.plot(DIVoutput[1:, 0], DIVoutput[1:, 2], 'r.')
        ax2.set_ylabel('Rs (Ohms)', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
        plt.title(savename)
        ##plt.show()
        output = str(savename) + "," + str(RS_MIN) + "," + str(RSH_MEAN) + "," + str(date_time) + "\n"
        ##WriteToFile("SampleID, Rs_min (mohm), Rsh_mean (ohm)\n",rootdir + '\\data\\SummaryFile')
        WriteToFile(output, rootdir + '\\data\\SummaryFile')
        fig.savefig(rootdir + '\\data\\' + savename + '.png', bbox_inches='tight')
        np.savetxt(rootdir + '\\data\\' + savename + '.txt', DIVoutput)
        self.div_graph_pix = QtGui.QPixmap(rootdir + '\\data\\' + savename)

    def click(self) ->None :
        print(2)
        self.measure.start()

    # def save_data(self, data) -> None:
    #
    #     def WriteToFile(message, OutputFile):
    #         file = open(OutputFile + '.txt', 'a')
    #         file.write(message)
    #         file.close()
    #     rootdir= 'C:\\Users\\python\\Desktop\\DIV Results'
    #     savename = self.sample_edit.text()



class Measurements(QThread):

    measurement_sig = pyqtSignal(list)

    def __init__(self) -> None:
        super(Measurements, self).__init__()

    def take_measurement(self) -> list:

        ser = serial.Serial()
        ser.baudrate = 57600
        ser.port = 'COM5'
        ser.timeout = 1

        serArduino = serial.Serial()
        serArduino.baudrate = 9600
        serArduino.port = 'COM6'
        serArduino.timeout = 1

        timestamp = time.time()
        # date_time = str(datetime.now())
        first_time_seconds = str(math.floor(timestamp))

        start_current = str(5)
        stop_current = str(4)
        current_step = str(-1e-1)
        start_current_shunt = str(0.00011)
        stop_current_shunt = str(0.00001)
        current_step_shunt = str(-1e-5)
        voltage_protection = str(10)
        number_steps = str(11)  # 21 or fewer
        number_steps_int = int(number_steps)
        source_delay = str(0.01)  # choose 10 ms for this to reduce heating
        timeout_sec = str(float(number_steps) * float(source_delay) + 1)

        serArduino
        serArduino.open()
        time.sleep(0.1)
        serArduino.write(str.encode('2O3O4O5O\n'))

        time.sleep(0.1)

        ser
        ser.open()

        ser.write(str.encode('*IDN?\n'))
        ident = ser.read(200)
        print(ident)

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        time.sleep(0.001)

        ser.write(str.encode(':ROUT:TERM FRON\n'))
        ser.write(str.encode(':ROUT:TERM?\n'))
        print(ser.read(10))

        ser.write(str.encode(':SENS:FUNC:CONC OFF\n'))
        ser.write(str.encode(':SYST:RSEN ON\n'))  # chooses 4wire measurement setting
        ser.write(str.encode(':SOUR:FUNC CURR\n'))
        ser.write(str.encode(":SENS:FUNC 'VOLT:DC'\n"))
        ser.write(str.encode(':SENS:VOLT:PROT ' + voltage_protection + '\n'))
        ser.write(str.encode(':SOUR:CURR:START ' + start_current_shunt + '\n'))  # start current
        ser.write(str.encode(':SOUR:CURR:STOP ' + stop_current_shunt + '\n'))  # stop current
        ser.write(str.encode(':SOUR:CURR:STEP ' + current_step_shunt + '\n'))  # increment
        ser.write(str.encode(':SOUR:CURR:MODE SWE\n'))
        ser.write(str.encode(':SOUR:SWE:RANG AUTO\n'))
        ser.write(str.encode(':SOUR:SWE:SPAC LIN\n'))
        ser.write(str.encode(':TRIG:COUN ' + number_steps + '\n'))  # number of points to measure
        ser.write(str.encode(':SOUR:DEL ' + source_delay + '\n'))  # source delay in sec
        ser.write(str.encode(':OUTP ON\n'))  # starts the sweep
        ser.write(str.encode(':READ?\n'))  # requests the data from the 2440

        # get all of the data out
        b = bytes.decode(
            ser.readline())  # super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
        # print (b)
        b = b.split(',')  # turns this into an array instead of a string with a bunch of commas
        print(len(b))
        ##print b
        DIVoutput = np.zeros((int(len(b)) // 5, 6))
        Header = ['Rs Voltage (V)', 'Rs Current (A)', 'Series Resistance (mohm)', 'Rsh Voltage (V)', 'Rsh Current (A)',
                  'Shunt Resistance (ohm)']

        for i in range(len(b) // 5):
            DIVoutput[i, 3] = b[i * 5]  # voltages
            DIVoutput[i, 4] = b[i * 5 + 1]  # current

        for i in range(len(b) // 5 - 1):
            DIVoutput[i + 1, 5] = (DIVoutput[i + 1, 3] - DIVoutput[i, 3]) / (DIVoutput[i + 1, 4] - DIVoutput[i, 4])

        RSH_MEAN = sum(DIVoutput[1:-1, 5]) / float(len(DIVoutput[1:-1, 5]))
        # print(savename)
        print("Rsh Mean")
        print(RSH_MEAN)

        ##ser
        ##ser.open()

        ##ser.write(str.encode('*IDN?\n')
        ##ident = ser.read(200)
        ##print ident
        time.sleep(0.25)

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        time.sleep(0.001)

        ser.write(str.encode(':ROUT:TERM FRON\n'))
        ser.write(str.encode(':ROUT:TERM?\n'))
        print(ser.read(10))

        ser.write(str.encode(':SENS:FUNC:CONC OFF\n'))
        ser.write(str.encode(':SYST:RSEN ON\n'))  # chooses 4wire measurement setting
        ser.write(str.encode(':SOUR:FUNC CURR\n'))
        ser.write(str.encode(":SENS:FUNC 'VOLT:DC'\n"))
        ser.write(str.encode(':SENS:VOLT:PROT ' + voltage_protection + '\n'))
        ser.write(str.encode(':SOUR:CURR:START ' + start_current + '\n'))  # start current
        ser.write(str.encode(':SOUR:CURR:STOP ' + stop_current + '\n'))  # stop current
        ser.write(str.encode(':SOUR:CURR:STEP ' + current_step + '\n'))  # increment
        ser.write(str.encode(':SOUR:CURR:MODE SWE\n'))
        ser.write(str.encode(':SOUR:SWE:RANG AUTO\n'))
        ser.write(str.encode(':SOUR:SWE:SPAC LIN\n'))
        ser.write(str.encode(':TRIG:COUN ' + number_steps + '\n'))  # number of points to measure
        ser.write(str.encode(':SOUR:DEL ' + source_delay + '\n'))  # source delay in sec
        ser.write(str.encode(':OUTP ON\n'))  # starts the sweep
        ser.write(str.encode(':READ?\n'))  # requests the data from the 2440

        # get all of the data out
        a = bytes.decode(
            ser.readline())  # super important because it reads the entire buffer rather than just the number of bytes you specify in the read() command
        a = a.split(',')  # turns this into an array instead of a string with a bunch of commas

        # clean up the 2440 and the port (turn off output and close port)
        ser.write(str.encode(':OUTP OFF\n'))
        ser.close()

        Header = ['Rs Voltage (V)', 'Rs Current (A)', 'Series Resistance (mohm)', 'Rsh Voltage (V)', 'Rsh Current (A)',
                  'Shunt Resistance (mohm)']

        for i in range(len(a) // 5):
            DIVoutput[i, 0] = a[i * 5]  # voltages
            DIVoutput[i, 1] = a[i * 5 + 1]  # current

        for i in range(len(a) // 5 - 1):
            DIVoutput[i + 1, 2] = 1000 * (DIVoutput[i + 1, 0] - DIVoutput[i, 0]) / (
            DIVoutput[i + 1, 1] - DIVoutput[i, 1])

        RS_MIN = min(DIVoutput[1:-1, 2])
        print("Rs min (m-ohm)")
        print(RS_MIN)
        print("")

        time.sleep(0.25)

        serArduino.write(str.encode('2C3C4C5C\n'))

        time.sleep(0.1)
        serArduino.close()
        print(6)
        # savename = UI_MainWindow.sample_edit.text()
        # print(savename)
        measure = []
        measure.append(RS_MIN)
        measure.append(RSH_MEAN)
        n = [measure, DIVoutput]
        print(7)
        return n

    def run(self) -> None:
        print(3)
        measurements = self.take_measurement()
        # for measurement in measurements:
        #     print(8)
        #     value = measurement
        #     print(4)
        #     self.measurement_sig.emit(str(value))
        #     time.sleep(2)
        print(5)
        self.measurement_sig.emit(measurements)
        time.sleep(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UI_MainWindow()
    sys.exit(app.exec_())





