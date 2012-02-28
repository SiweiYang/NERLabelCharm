#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
from LabelModel import LabelModel
from Preprocessor import pack
from PackViewerControl import PackControl
from main import Ui_MainWindow

class LabelView(QtGui.QMainWindow):
    def __init__(self, fileName, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelModel = LabelModel(fileName)
        self.loadText(self.labelModel.entries)
        self.loadCloudFlowerLabel(self.labelModel.tagMap())

        self.packViewer = PackControl(self.ui.MaluubaNER)

        QtCore.QObject.connect(self.ui.textEdit, QtCore.SIGNAL("cursorPositionChanged()"), self.updateSentence)

    def updateSentence(self):
        currentLine = self.ui.textEdit.textCursor().blockNumber()
        segment = self.labelModel.getSegment(currentLine)
        print segment

        decoratedSegment = self.labelModel.decorateSegment(segment)

        print decoratedSegment
        #print self.labelModel.tagMap()
        self.packViewer.showPack(pack(decoratedSegment))

    def loadText(self, entries):
        textBlob = '\n'.join(['\t'.join(line) for line in entries])
        self.ui.textEdit.setText(textBlob)

    def loadCloudFlowerLabel(self, tagMap):
        tags = ["%s => %d" %(tag, index) for tag, index in tagMap.items()]
        self.ui.CloudFlowerNER.setText('\n'.join(tags))



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    label = LabelView('siwei.music.label')
    label.show()
    sys.exit(app.exec_())