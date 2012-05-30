#!/usr/bin/env python
from packPrinter import printPack, pack, TaggedSentence

__author__ = 'syang'
def loadData(fileName):
    entries = []

    try:
        file = open(fileName, 'r')
        while True:
            line = file.readline()
            if line == '':
                break

            line = line.strip()
            cols = line.split()
            entries.append(cols)
        file.close()
    except IOError:
        pass

    return entries

def saveData(fileName, entries):
    try:
        file = open(fileName, 'w')
        lines = [('%s\t%s\t%s' % (entry[0], entry[-2], entry[-1])).strip() for entry in entries]
        lines = ['%s\n' % line for line in lines]
        #print lines
        file.writelines(lines)
        file.close()
    except IOError:
        pass

    return entries

def saveTrainingData(fileName, entries):
    try:
        file = open(fileName, 'w')
        lines = [('%s\t%s' % (entry[0], entry[-2])).strip() for entry in entries]
        lines = ['%s\n' % line for line in lines]
        #print lines
        file.writelines(lines)
        file.close()
    except IOError:
        pass

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

#return [TaggedSentence]
def splitSentences(entries):
    sentence = []
    sentences = []
    for cols in entries:
        if cols == []:
            if sentence == []:
                pass
            else:
                sentences.append(TaggedSentence(sentence))
                sentence = []
            continue
        sentence.append(cols)

    return sentences

def concatenateSentences(sentences):
    entries = []
    for sentence in sentences:
        for token in sentence.getTokens():
            entries.append(token)
        entries.append(('', '', ''))

    return entries

if __name__ == '__main__':
    entries = loadData('siwei.music.label')
    #myEntries = selectCols(entries, [0, 1])
    #cfEntries = selectCols(entries, [0, 2])

    mySentences = splitSentences(entries)

    print(mySentences)
    #packedMySentences = [pack(sentence) for sentence in mySentences]
    #print len(packedMySentences)

    #printPack(packedMySentences[100])