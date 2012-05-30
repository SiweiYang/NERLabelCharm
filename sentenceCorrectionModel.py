#!/usr/bin/env python
# __author__ = 'Siwei Yang'
from PyQt4.QtCore import QAbstractTableModel, QString, Qt, QVariant
from PyQt4.QtGui import QColor

class sentenceCorrectionModel(QAbstractTableModel):
    COLUMN = 3
    HEADER = ['Token', 'CF', 'CRF']

    def __init__(self, tokens=[]):
        QAbstractTableModel.__init__(self)
        self.tokens = tokens

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if Qt_Orientation == Qt.Horizontal and int_role == Qt.DisplayRole:
            return QVariant(sentenceCorrectionModel.HEADER[p_int])
        if Qt_Orientation == Qt.Vertical and int_role == Qt.DisplayRole:
            return QVariant(p_int)
        return QVariant()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.tokens)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return sentenceCorrectionModel.COLUMN

    def data(self, QModelIndex, int_role=None):
        rowNum = QModelIndex.row()
        colNum = QModelIndex.column()

        token = self.tokens[rowNum]
        hasConflict = not token[1] == token[2]

        if int_role == Qt.DisplayRole:
            return QString(self.tokens[rowNum][colNum])

        if int_role == Qt.BackgroundColorRole:
            if hasConflict:
                return QColor(Qt.red)
            return QColor(Qt.green)

        return QVariant()
