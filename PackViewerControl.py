#!/usr/bin/env python
__author__ = 'syang'

class PackControl:
    def __init__(self, display):
        self.display = display

    def showPack(self, packs):
        text = ''
        for tag, words in packs:
            text += "%s => %s\n" % (tag, '-'.join(words))
        self.display.setText(text)