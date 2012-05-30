#!/usr/bin/env python
__author__ = 'syang'

class TaggedSentence:
    def __init__(self, entries):
        self.entities = []

        for entry in entries:
            self.entities.append((entry[0], entry[-2], entry[-1]))

    def __repr__(self):
        return str(self.entities)

    def hasConflict(self):
        for entity in self.entities:
            if not entity[1] == entity[2]:
                return True

        return False

    def unify(self, type):
        if type == 'LEFT':
            self.entities = [(entity[0], entity[-2], entity[-2]) for entity in self.entities]
        if type == 'RIGHT':
            self.entities = [(entity[0], entity[-1], entity[-1]) for entity in self.entities]

    def override(self, slave):
        tokens = []
        for index in range(min(len(self.getTokens()), len(slave.getTokens()))):
            tokens.append((slave.getTokens()[index][0], self.getTokens()[index][-2], slave.getTokens()[index][-1]))

        slave.setTokens(tokens)

    def getTokens(self):
        return self.entities

    def setTokens(self, tokens):
        self.entities = tokens

    def rawSentence(self):
        return ' '.join([entity[0] for entity in self.entities])

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

def packSize(pack):
    sizes = [len(word) for word in pack[1]]

    return len(sizes) + sum(sizes) + 1

#expect [(tag, [word])]
def printPack(packedSentence):
    for tag, words in packedSentence:
        print tag, ' -> ', words