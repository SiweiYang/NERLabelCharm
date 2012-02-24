#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
from main import Ui_MainWindow

class LabelView(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.textEdit, QtCore.SIGNAL("cursorPositionChanged()"), self.updateSentence)

    def updateSentence(self):
        currentLine = self.ui.textEdit.textCursor().blockNumber()

        top = currentLine
        while top > 0:
            if len(self.textList) > top and not self.textList[top] == []:
                top -= 1
            else:
                break

        bottom = currentLine
        while len(self.textList) > bottom:
            if len(self.textList) > bottom and not self.textList[bottom] == []:
                bottom += 1
            else:
                break
        print (currentLine, top, bottom)

    def loadFile(self, fileName):
        self.fileName = fileName
        textList = []

        file = open(self.fileName, 'r')
        while True:
            line = file.readline()
            if line == '':
                break
            textList.append(line.strip().split())
        file.close()

        self.textList = textList
        textBlob = '\n'.join(['\t'.join(line) for line in textList])
        self.ui.textEdit.setText(textBlob)

    def loadMaluubaLabel(self):
        pass

    def loadCloudFlowerLabel(self):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    label = LabelView()
    label.loadFile('siwei.music.label')
    label.show()
    sys.exit(app.exec_())