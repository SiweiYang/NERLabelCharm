#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
from LabelModel import LabelModel
from main import Ui_MainWindow

class LabelView(QtGui.QMainWindow):
    def __init__(self, fileName, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelModel = LabelModel(fileName)
        self.loadText(self.labelModel.entries)

        QtCore.QObject.connect(self.ui.textEdit, QtCore.SIGNAL("cursorPositionChanged()"), self.updateSentence)

    def updateSentence(self):
        currentLine = self.ui.textEdit.textCursor().blockNumber()

        print self.labelModel.getSegment(currentLine)

    def loadText(self, entries):
        textBlob = '\n'.join(['\t'.join(line) for line in entries])
        self.ui.textEdit.setText(textBlob)

    def loadMaluubaLabel(self):
        #self.ui.maluubaNER
        pass

    def loadCloudFlowerLabel(self):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    label = LabelView('siwei.music.label')
    label.show()
    sys.exit(app.exec_())