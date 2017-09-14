# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 16:01:15 2017

@author: cleroy
"""

from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys

int_cycle_number = int(0)
parameters = {'powerSupply': {'type': 'value', 'value': 1, 'label': 'Power Supply',
                              'min': 0, 'max': 10},
              'powerSupply1': {'type': 'value', 'value': 0, 'label': 'NOT CONNECTED - 1',
                               'min': 0, 'max': 10},
              'randomText': {'type': 'text', 'label': 'Something', 'text': 'hello'},
              'interlockActive': dict(type='checkbox', label='Interlock Active', state=2),
              'cycle_number': dict(type='label', label='Cycle # ' + str(int_cycle_number))}


class ParameterTemplate(QtWidgets.QWidget):
    def __init__(self, name):
        super(ParameterTemplate, self).__init__()
        self.name = name
        data = parameters[self.name]

        hbox = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(data['label'])
        hbox.addWidget(self.label)

        if data['type'] == 'value':
            self.value = QtWidgets.QSpinBox()
            self.value.setMinimum(data['min'])
            self.value.setMaximum(data['max'])
            self.value.valueChanged.connect(self.valueChanged)
            self.value.setValue(data['value'])
            hbox.addWidget(self.value)
        elif data['type'] == 'text':
            self.line = QtWidgets.QLineEdit()
            self.line.textChanged.connect(self.textChanged)
            self.line.setText(data['text'])
            hbox.addWidget(self.line)
        elif data['type'] == 'checkbox':
            self.check = QtWidgets.QCheckBox()
            self.check.stateChanged.connect(self.checkstateChanged)
            self.check.setCheckState(data['state'])
            hbox.addWidget(self.check)

        self.setLayout(hbox)

    def valueChanged(self, value):
        parameters[self.name]['value'] = value
        print(parameters)

    def textChanged(self, text):
        parameters[self.name]['text'] = text
        print(parameters)

    def checkstateChanged(self, checkbox):
        parameters[self.name]['state'] = checkbox
        print(parameters)
        print(bool(checkbox))


class Example(QtWidgets.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.parametersUIFactory()

        self.show()

    def parametersUIFactory(self):
        vbox = QtWidgets.QVBoxLayout()
        for param in parameters:
            print(param)
            widget = ParameterTemplate(param)
            vbox.addWidget(widget)
        self.setLayout(vbox)


def main():
    #    app = QWidget(sys.argv)
    #    app.show()
    #    #ex = Example()
    #    sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
