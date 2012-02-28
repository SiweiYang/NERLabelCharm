#!/usr/bin/env python
__author__ = 'syang'

from Preprocessor import loadData, transform
class LabelModel:
    def __init__(self, fileName):
        self.entries = loadData(fileName)

    def tagMap(self):
        map = {'B-SONG': 0,
               'I-SONG': 1,
               'B-ALBUM': 2,
               'I-ALBUM': 3,
               'B-RATING': 4,
               'I-RATING': 5,
               'B-PLAYLIST': 6,
               'I-PLAYLIST': 7,
               'B-ARTIST': 8,
               'I-ARTIST': 9,
               'B-STATION': 10,
               'I-STATION': 11,
               'B-GENRE': 12,
               'I-GENRE': 13,
               'B-ORDER': 14,
               'I-ORDER': 15
        }

        return map

    def decorateSegment(self, segment):
        seq = [line[1] for line in segment]
        newSeq = transform(seq, self.tagMap())

        return zip([line[0] for line in segment], newSeq)

    def getSegment(self, lineNumber):
        top = lineNumber
        while top > 0:
            if len(self.entries) > top and not self.entries[top-1] == []:
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