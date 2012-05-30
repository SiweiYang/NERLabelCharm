#!/usr/bin/env python
from functools import partial
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QModelIndex
from PyQt4.QtGui import QFileDialog
from LabelModel import LabelModel
from Preprocessor import pack, loadData, splitSentences, saveData, concatenateSentences, saveTrainingData
from PackViewerControl import PackControl
from main import Ui_MainWindow
from sentenceCorrectionModel import sentenceCorrectionModel
from sentenceModel import sentenceModel

class LabelView(QtGui.QMainWindow):
    def __init__(self, fileName, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.sentenceList, QtCore.SIGNAL("clicked(QModelIndex)"), self.updateSentence)
        QtCore.QObject.connect(self.ui.browseResultPath, QtCore.SIGNAL("clicked()"), partial(self.setFilePath, 'RESULT'))
        QtCore.QObject.connect(self.ui.browseTrainingSetPath, QtCore.SIGNAL("clicked()"), partial(self.setFilePath, 'TRAIN'))
        QtCore.QObject.connect(self.ui.browseCorrectSetPath, QtCore.SIGNAL("clicked()"), partial(self.setFilePath, 'CORRECT'))
        QtCore.QObject.connect(self.ui.browseWrongSetPath, QtCore.SIGNAL("clicked()"), partial(self.setFilePath, 'WRONG'))
        QtCore.QObject.connect(self.ui.startButton, QtCore.SIGNAL("clicked()"), self.loadFiles)
        QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"), self.saveFiles)

        QtCore.QObject.connect(self.ui.goodButton, QtCore.SIGNAL("clicked()"), partial(self.resolveSentence, 'GOOD'))
        QtCore.QObject.connect(self.ui.correctButton, QtCore.SIGNAL("clicked()"), partial(self.resolveSentence, 'CORRECT'))
        QtCore.QObject.connect(self.ui.badButton, QtCore.SIGNAL("clicked()"), partial(self.resolveSentence, 'BAD'))


    def setFilePath(self, type):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        filePath = dialog.getOpenFileName()
        if type == 'RESULT':
            self.ui.testResultPath.setText(filePath)
            if len(self.ui.trainingSetPath.text()) == 0:
                self.ui.trainingSetPath.setText(filePath + '_train')
            if len(self.ui.correctSetPath.text()) == 0:
                self.ui.correctSetPath.setText(filePath + '_correct')
            if len(self.ui.wrongSetPath.text()) == 0:
                self.ui.wrongSetPath.setText(filePath + '_wrong')
        elif type == 'TRAIN':
            self.ui.trainingSetPath.setText(filePath)
        elif type == 'CORRECT':
            self.ui.correctSetPath.setText(filePath)
        elif type == 'WRONG':
            self.ui.wrongSetPath.setText(filePath)

    def loadFiles(self):
        testResultPath = self.ui.testResultPath.text()
        correctSetPath = self.ui.correctSetPath.text()
        wrongSetPath = self.ui.wrongSetPath.text()

        #Start only if all 3 are specified
        if testResultPath and correctSetPath and wrongSetPath:
            #load results set
            entries = loadData(testResultPath)
            self.packedSentences = splitSentences(entries)

            #load correct set
            correctEntries = loadData(correctSetPath)
            self.packedCorrectSentences = splitSentences(correctEntries)

            #load wrong set
            wrongEntries = loadData(wrongSetPath)
            self.packedWrongSentences = splitSentences(wrongEntries)

            self.overrideFromPackedSentences(self.packedSentences, self.packedCorrectSentences)
            self.updateSentences()
            self.smartUpdateSentence()

            return

    def saveFiles(self):
        testResultPath = self.ui.testResultPath.text()
        trainSetPath = self.ui.trainingSetPath.text()
        correctSetPath = self.ui.correctSetPath.text()
        wrongSetPath = self.ui.wrongSetPath.text()

        #Start only if all 3 are specified
        if testResultPath and trainSetPath and correctSetPath and wrongSetPath:
            saveData(testResultPath, concatenateSentences(self.packedSentences))
            saveTrainingData(trainSetPath, concatenateSentences(self.packedSentences))

            saveData(correctSetPath, concatenateSentences(self.packedCorrectSentences))
            saveData(wrongSetPath, concatenateSentences(self.packedWrongSentences))
            pass

    def containsPackedSentence(self, packedSentences, packedSentence):
        for sentence in packedSentences:
            if sentence.rawSentence() == packedSentence.rawSentence():
                return True
        return False

    def overrideFromPackedSentence(self, slaveSet, masterSentence):
        for slaveSentence in slaveSet:
            if masterSentence.rawSentence() == slaveSentence.rawSentence():
                masterSentence.override(slaveSentence)

    def overrideFromPackedSentences(self, slaveSet, masterSet):
            for masterSentence in masterSet:
                self.overrideFromPackedSentence(slaveSet, masterSentence)

    #Update sentence sets regarding the action taken
    #Update sentence set view
    def resolveSentence(self, action):
        if action == 'GOOD':
            self.sentenceInCorrection.unify('LEFT')

            self.updateSentence(self.sentenceInCorrectionIndex)

        elif action == 'CORRECT':
            self.sentenceInCorrection.unify('RIGHT')
            if not self.containsPackedSentence(self.packedCorrectSentences, self.sentenceInCorrection):
                self.packedCorrectSentences.append(self.sentenceInCorrection)
            else:
                self.overrideFromPackedSentence(self.packedCorrectSentences, self.sentenceInCorrection)

            self.updateSentence(self.sentenceInCorrectionIndex)

        elif action == 'BAD':
            if not self.containsPackedSentence(self.packedWrongSentences, self.sentenceInCorrection):
                self.packedWrongSentences.append(self.sentenceInCorrection)

        #print 'Correct: %d' % len(self.packedCorrectSentences)
        #print 'Wrong: %d'% len(self.packedWrongSentences)

        if action == 'GOOD' or action == 'CORRECT':
            #Update if already in set
            #Append otherwise
            if not self.containsPackedSentence(self.packedCorrectSentences, self.sentenceInCorrection):
                self.packedCorrectSentences.append(self.sentenceInCorrection)
            else:
                self.overrideFromPackedSentence(self.packedCorrectSentences, self.sentenceInCorrection)

            #Refresh sentenceList
            self.updateSentences()

        self.smartUpdateSentence(self.sentenceInCorrectionIndex.row() + 1)

    def smartUpdateSentence(self, startingRow = 0):
        for rowNum in range(startingRow, self.sentenceModel.rowCount()):
            #print rowNum
            #print self.sentenceModel.sentences[rowNum][sentenceModel.COLUMN_CONFLICT]
            if self.sentenceModel.sentences[rowNum][sentenceModel.COLUMN_CONFLICT]:
                index = self.sentenceModel.index(rowNum, 0)
                self.updateSentence(index)
                return

    def updateSentences(self):
        sentenceList = [(sentence.rawSentence(), sentence.hasConflict(), self.containsPackedSentence(self.packedCorrectSentences, sentence)) for sentence in self.packedSentences]
        self.sentenceModel = sentenceModel(sentenceList)
        self.ui.sentenceList.setModel(self.sentenceModel)

    #Update the correction view with a sentence
    def updateSentence(self, QModelIndex):
        self.sentenceInCorrectionIndex = QModelIndex
        self.sentenceInCorrection = self.packedSentences[QModelIndex.row()]
        sentenceModel = sentenceCorrectionModel(self.sentenceInCorrection.getTokens())
        self.ui.sentenceCorrectionView.setModel(sentenceModel)

        self.ui.sentenceList.scrollTo(QModelIndex)
        self.ui.sentenceIndex.setText(QString(str(QModelIndex.row())))
        #print self.sentenceInCorrection

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    label = LabelView('siwei.music.label')
    label.show()
    sys.exit(app.exec_())