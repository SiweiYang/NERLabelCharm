#!/usr/bin/env python
__author__ = 'syang'

def packSize(pack):
    sizes = [len(word) for word in pack[1]]

    return len(sizes) + sum(sizes) + 1

#expect [(tag, [word])]
def printPack(packedSentence):
    for tag, words in packedSentence:
        print tag, ' -> ', words