#!/usr/bin/env python
# __author__ = 'Siwei Yang'
from PyQt4.QtCore import QAbstractTableModel, QString, Qt, QVariant
from PyQt4.QtGui import QColor

class sentenceModel(QAbstractTableModel):
    COLUMN_NUM = 1
    COLUMN_SENTENCE = 0
    COLUMN_CONFLICT = 1
    COLUMN_CORRECT = 2

    HEADER = ['Sentence']

    def __init__(self, sentences=[]):
        QAbstractTableModel.__init__(self)
        self.sentences = sentences

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Horizontal and int_role == Qt.DisplayRole:
            return QVariant(sentenceModel.HEADER[p_int])
        if Qt_Orientation == Qt.Vertical and int_role == Qt.DisplayRole:
            return QVariant(p_int)
        return QVariant()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.sentences)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return sentenceModel.COLUMN_NUM

    def data(self, QModelIndex, int_role=None):
        rowNum = QModelIndex.row()
        #colNum = QModelIndex.column()

        if int_role == Qt.DisplayRole:
            return QString(self.sentences[rowNum][sentenceModel.COLUMN_SENTENCE])
        if int_role == Qt.BackgroundColorRole:
            if self.sentences[rowNum][sentenceModel.COLUMN_CONFLICT]:
                if self.sentences[rowNum][sentenceModel.COLUMN_CORRECT]:
                    return QColor(Qt.yellow)
                return QColor(Qt.red)
            return QColor(Qt.green)

        return QVariant()
