#!/usr/bin/python3
# -*- coding: UTF8 -*-
# Created on : 4 jul. 2023, 14:04:25
# Author     : rafael
# Classes per a la resolució dels valors de funcions complexes

import re

class abstractResolveValues:

    def setParams(self, mainParam, delimiter, toParse):
        self.mainParam = mainParam
        self.delimiter = delimiter
        self.toParse = toParse

    def getMainParam(self):
        return self.mainParam

    def getDelimiter(self):
        return self.delimiter

    def getToParse(self):
        return self.toParse


class stackResolveValues(abstractResolveValues):

    resolvers = ['rslvResolveFunction',
                 'rslvExtractQString',
                 'rslvExtractString',
                 'rslvResolveArray',
                 'rslvResolveObject',
                 'rslvResolveTerminator'
                ]
    pila = []

    def parse(self, param):
        while param:
            for rslvr in self.resolvers:
                instance = globals()[rslvr]()
                if (instance.match(param)):
                    instance.extract(param)
                    param = instance.getToParse()
                    if (instance.isSeparator()):
                        if (instance.getMainParam() is not None):
                            self.pila.append(instance.getValue())
                        if (self.isTerminator(instance.getDelimiter())):    #alternativa: instance.isTerminator()
                            return param      #eliminar, de los parámetros restantes, la parte ya tratada
                    else:
                        param = instance.parse(param)
                        self.pila.append(instance.getValue())

        return self.pila


class ResolveValues(stackResolveValues):

    def resolve(self, param):
        result = self.parse(param)
        print(result)

    def isTerminator(self, delimiter=""):
        return (delimiter != ",")   # versió sense paràmetre: (self.getDelimiter() != ",")


class rslvResolveFunction(stackResolveValues):
    className = "rslvResolveFunction"
    pattern = '^(\w+)(\()(.*)'
    pila = []

    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        funcName = self.getMainParam()
        parsedParams = []
        for param in self.pila:
            if isinstance(param, (list, tuple, set)):
                parsedParams.append(param)
            elif param:
                parsedParams.append(param)

        result = eval(funcName + "(self.pila)")
        return result

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(match.group(1), match.group(2), match.group(3))

    def isSeparator(self):
        return False

    def isTerminator(self, delimiter=""):
        return (delimiter == ")")   # versió sense paràmetre: (self.getDelimiter() == ")")


class rslvResolveArray(stackResolveValues):
    className = "rslvResolveArray"
    pattern = '^(\[)(.*)'
    pila = []

    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        return self.pila

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(match.group(1), match.group(1), match.group(2))

    def isSeparator(self):
        return False

    def isTerminator(self, delimiter=""):
        return (delimiter == "]")   # versió sense paràmetre: (self.getDelimiter() == "]")


class rslvResolveObject(stackResolveValues):
    className = "rslvResolveObject"
    pattern = '^({)(.*)'
    pila = []

    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        return self.pila

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(match.group(1), match.group(1), match.group(2))

    def isSeparator(self):
        return False

    def isTerminator(self, delimiter=""):
        return (delimiter == "")   # versió sense paràmetre: (self.getDelimiter() == "")


class rslvResolveTerminator(stackResolveValues):
    className = "rslvResolveTerminator"
    pattern = '^(,|}|\]|\))(.*)'

    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        return self.getMainParam()

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(None, match.group(1), match.group(2))

    def isSeparator(self):
        return True

    def isTerminator(self, delimiter=""):
        return (delimiter != ",")   # versió sense paràmetre: (self.getDelimiter() != ",")


class rslvExtractQString(stackResolveValues):
    #extrae, del inicio, textos entre comillas (incluye las comillas escapadas \")
    className = "rslvExtractQString"
    pattern = '^(".*?[^\\\\]")(,|\)|\]|\})?(.*)'

    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        return self.getMainParam()

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(match.group(1), match.group(2), match.group(3))

    def isSeparator(self):
        return True

    def isTerminator(self, delimiter=""):
        return (delimiter != ",")   # versió sense paràmetre: (self.getDelimiter() != ",")


class rslvExtractString(stackResolveValues):
    #extrae, del inicio, palabras sin comillas y números enteros y decimales
    className = "rslvExtractString"
    pattern = '^(\w+(?:\.\d+)?)(,|\)|\]|})?(.*)'  #Aquest inclou noms de funcions: "nom("
                                                  #per tant s'ha d'executar després
    def match(self, param):
        return bool(re.match(self.pattern, param))

    def getValue(self):
        return self.getMainParam()

    def extract(self, param):
        match = re.fullmatch(self.pattern, param)
        self.setParams(match.group(1), match.group(2), match.group(3))

    def isSeparator(self):
        return True

    def isTerminator(self, delimiter=""):
        return (self.delimiter != ",")   # versió sense paràmetre: (self.getDelimiter() != ",")


def suma(param):
   result = 0
   for elem in param:
      result += int(elem)
   return result

def init():
    arg = input("Escriu una funció: ")    #arg = 'suma(4,7)'
    return ResolveValues().resolve(arg)

print("====================================")
print("Classes per a ResolveValues")
print("====================================")

init()
