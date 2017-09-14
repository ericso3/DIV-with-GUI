# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      khan
#
# Created:     25/07/2017
# Copyright:   (c) khan 2017
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import sys, time
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys

i = 0


class MyApp(QtWidgets.QWidget):
    def __init__(self, name):
        super(MyApp, self).__init__()

        self.setGeometry(300, 300, 280, 600)
        self.setWindowTitle('Threads')

        self.layout = QVBoxLayout(self)

        testButton = QPushButton("Test")
        testButton.resize(testButton.sizeHint())
        # self.connect(self.testButton, QtCore.SIGNAL("released()"), self.test)
        listwidget = QListWidget(self)

        # self.layout.addWidget(self.testButton)
        # self.layout.addWidget(self.listwidget)

        threadPool = []
        self.show()

    ##  #Start push button
    ##  self.btnStart = QtGui.QPushButton("Start", self)
    ##  self.btnStart.clicked.connect(self.btnStartClicked)
    ##  self.btnStart.resize(100,45)
    ##  self.btnStart.move(130,10)
    ##
    ##
    ##
    ## def btnStartClicked(self):
    ##  time.sleep(1)

    def add(self, text):
        """ Add item to list widget """
        print("Add: " + text)
        listwidget.addItem(text)
        listwidget.sortItems()

    def addBatch2(self, text="test", iters=6, delay=0.3):
        for i in range(iters):
            time.sleep(delay)  # artificial time delay
            self.emit(QtCore.SIGNAL('add(QString)'), text + " " + str(i))

    def test(self):
        listwidget.clear()

        # generic thread using signal
        threadPool.append(GenericThread)
        #  self.threadPool.append( GenericThread(self.addBatch2,"from generic thread using slow signal ",delay=1.0) )
        self.disconnect()
        self.connect(self, QtCore.SIGNAL("add(QString)"), self.add)
        threadPool[len(self.threadPool) - 1].start()


class GenericThread(QtCore.QThread):
    sig = QtCore.pyqtSignal()

    def __init__(self, name):
        super(GenericThread, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function()
        return


# run
# app = QApplication(sys.argv)
# test1 = MyApp(name)
# test1.show()
# app.exec_()

def main():
        #    app = QWidget(sys.argv)
        #    app.show()
        #    #ex = Example()
        #    sys.exit(app.exec_())
    app = QtWidgets.QApplication(sys.argv)
    ex = GenericThread()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
