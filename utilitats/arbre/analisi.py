#!/usr/bin/python3
# -*- coding: UTF8 -*-
# Created on : 4 jul. 2023, 14:04:25
# Author     : rafael
# Classes per a la resolució dels valors de funcions complexes

import sys, re

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
        self.param = param
        #while self.param:
        for rslvr in self.resolvers:
            instance = globals()[rslvr]()
            print("Resolver:", rslvr, "- param:", self.param)
            if (instance.match(self.param)):
                instance.extract(self.param)
                self.param = instance.getToParse()
                if (instance.isSeparator()):
                    if (instance.getMainParam() is not None):
                        self.pila.append(instance.getValue())
                    if (self.isTerminator(instance.getDelimiter())):    #alternativa: instance.isTerminator()
                        return self.param      #eliminar, de los parámetros restantes, la parte ya tratada
                else:
                    self.param = instance.parse(self.param)
                    self.pila.append(instance.getValue())

                #print(rslvr)
                #break

        #return [instance.getMainParam(), instance.getDelimiter(), instance.getToParse()]
        return self.pila


class ResolveValues(stackResolveValues):

    def resolve(self, param):
        result = stackResolveValues().parse(param)
        print(result)

    def isTerminator(self, delimiter=""):
        return (delimiter != ",")   # versió sense paràmetre: (self.getDelimiter() != ",")



class rslvResolveFunction(stackResolveValues):
    className = "rslvResolveFunction"
    pattern = '^(\w+)(\()(.*)'

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

        #result = eval(funcName + "(self.pila)")
        return 55   #result

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
        print("rslvExtractQString:",param)
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


print("====================================")
print("Classes per a ResolveValues")
print("====================================")

def suma(a):
#    print(r"suma:")
#    print(a)
    return 1003

def actualParams():
    global arg
    arg = input("Escriu una funció: ")    #arg = 'suma("Casa"+"Una")'

# Tratamiento de los argumentos de la línea de comandos
arg = sys.argv[1:]
if (len(arg) == 0):
    actualParams()

result = ResolveValues().resolve(arg)
