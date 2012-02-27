#!/usr/bin/env python
__author__ = 'syang'

from Preprocessor import loadData
class LabelModel:
    def __init__(self, fileName):
        self.entries = loadData(fileName)

    def getSegment(self, lineNumber):
        top = lineNumber
        while top > 0:
            if len(self.entries) > top and not self.entries[top] == []:
                top -= 1
            else:
                break

        bottom = lineNumber
        while len(self.entries) > bottom:
            if len(self.entries) > bottom and not self.entries[bottom] == []:
                bottom += 1
            else:
                break
        return self.entries[top:bottom]