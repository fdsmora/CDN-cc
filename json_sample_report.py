#!/usr/bin/python
import re
import json

def lineStartsWith(pattern, line):
   return re.search("^"+pattern, line) 

fieldsValues = []
with open("testlog_2", "r") as f:
    fieldsNames = []
    for i in range(3):
        currentLine = f.readline()
        if lineStartsWith("#Fields", currentLine):
            fieldsNames = currentLine.split()[1:]
        else:
            fieldsValues = currentLine.split()  

print(json.dumps(dict(zip(fieldsNames, fieldsValues)), indent=4, sort_keys=True))
