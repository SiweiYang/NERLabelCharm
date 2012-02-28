#!/usr/bin/env python
from packPrinter import printPack
__author__ = 'syang'
def loadData(fileName):
    entries = []

    file = open(fileName, 'r')
    while True:
        line = file.readline()
        if line == '':
            break

        line = line.strip()
        cols = line.split()
        entries.append(cols)
    return entries

#return: (tag)
def scanner(fileName):
    entries = loadData(fileName)

    dict = set()
    lineNumber = 0
    for cols in entries:
        lineNumber += 1
        if cols == []:
            continue

        #print lineNumber
        for col in cols[1:]:
            if len(col) > 1:
                dict.add(col[2:])

    return dict

def lookup(tag, map):
    for (key, index) in map.items():
        try:
            if int(tag) == index:
                tag = key
                break
        except ValueError:
            break
    return tag

def transform(seq, map):
    newSeq = []
    for tag in seq:
        newSeq.append(lookup(tag, map))
    return newSeq

#input: [[entry]], [index]
#return: [[selectedEntry]]
def selectCols(seq, selectedCols):
    selectedCols.sort()

    newSeq = []
    for cols in seq:
        line = []
        for colNumber in selectedCols:
            if colNumber < len(cols):
                line.append(cols[colNumber])
            else:
                line.append(None)
        newSeq.append(line)

    return newSeq

#return [[cols]]
def splitSentences(entries):
    sentence = []
    sentences = []
    for cols in entries:
        if cols == []:
            if sentence == []:
                pass
            else:
                sentences.append(sentence)
                sentence = []
            continue
        sentence.append(cols)

    return sentences


#expect [[word, tag]]
def pack(sentence):
    packedSentence = []
    lastTag = ''
    for word, tag in sentence:
        if samePack(lastTag, tag):
            wordTag, wordPack = packedSentence[-1]
            wordPack.append(word)
        else:
            packedSentence.append((tag, [word]))
        lastTag = tag

    return packedSentence

def samePack(tagA, tagB):
    if tagA == 'O' and tagB == 'O':
        return True
    if ( tagA.startswith('B-') or tagA.startswith('I-') ) and tagB.startswith('I-'):
        return tagA[2:] == tagB[2:]

    return False

if __name__ == '__main__':
    map = {}
    i = 0
    for tag in scanner('siwei.music.label'):
        map[tag] = i
        i += 1
    print(map)

    entries = transform('siwei.label.done', map)
    myEntries = selectCols(entries, [0, 1])
    cfEntries = selectCols(entries, [0, 2])

    mySentences = splitSentences(myEntries)
    cfSentences = splitSentences(cfEntries)

    packedMySentences = [pack(sentence) for sentence in mySentences]
    print len(packedMySentences)

    #printPack(packedMySentences[100])