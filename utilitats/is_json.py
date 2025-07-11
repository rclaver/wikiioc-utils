#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 11:08:02 2025
@author: rafael
@description: evalua si un objecte és un objecte json
"""

import json

def isJson(value):
   if (isinstance(value, dict)):
      return "json_object"
   elif (isinstance(value, int)):
      return "json error"
   elif (value.isnumeric()):
      return "json error"
   else:
      try:
         json.loads(value)
      except (ValueError, TypeError):
         return "json error"
      return "json_object"

def isDict(value):
   return "És dict" if type(value) is dict  else "NO és dict"

dada = "22222222222"
print("valor: string \"", dada, "\":", isJson(dada), isDict(dada))

dada = "texto"
print("valor: string \"", dada, "\":", isJson(dada), isDict(dada))

dada = "[]"
print("valor: array buit", dada, ":", isJson(dada), isDict(json.loads(dada)))

dada = "[{\"m\\u00f2dul\":\"--\",\"itinerariRecomanatS1\":\"1\",\"itinerariRecomanatS2\":\"1\"}]"
print("valor: array [....]:", isJson(dada), isDict(json.loads(dada)))

dada = "{\"bloc\":\"2\",\"unitat formativa\":\"2\",\"nom\":\"Disseny modular\",\"hores\":50,\"ponderacio\":50,\"ordreImparticio\":2}"
print("valor: json {...}:", isJson(dada), isDict(json.loads(dada)))
