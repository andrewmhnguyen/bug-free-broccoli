#! /usr/bin/env python3
import fileinput
import sys

# list of Stmt objects
sList = []

# symbol table stores variable/label mappings
symTable = {}

# used to store a parsed TL expressions which are
# constant numbers, constant strings, variable names, and binary expressions
class Expr :
    def __init__(self,op1,operator,op2=None):
        self.op1 = op1
        self.operator = operator
        self.op2 = op2

    def __str__(self):
        if self.op2 == None:
            return self.operator + " " + self.op1
        else:
            return self.op1 + " " + self.operator + " " +  self.op2

    # evaluate this expression given the environment of the symTable
    def eval(self, symTable):
        if self.operator == "var":
            return symTable[op1]
        elif self.operator == '+':
            return self.op1 + self.op2
        elif self.operator == '-':
            return self.op1 - self.op2                
        elif self.operator == '*':
            return self.op1 * self.op2
        elif self.operator == '/':
            return self.op1 / self.op2
        elif self.operator == '<':
            return 1 if self.op1 < self.op2 else 0
        elif self.operator == '>':
            return 1 if self.op1 > self.op2 else 0
        elif self.operator == '<=':
            return 1 if self.op1 <= self.op2 else 0
        elif self.operator == '>=':
            return 1 if self.op1 >= self.op2 else 0
        elif self.operator == '==':
            return 1 if self.op1 == self.op2 else 0
        elif self.operator == '!=':
            return 1 if self.op1 != self.op2 else 0
        else:
            return 0

# used to store a parsed TL statement
class Stmt :
    def __init__(self,keyword,exprs):
        self.keyword = keyword
        self.exprs = exprs

    def __str__(self):
        others = ""
        for exp in self.exprs:
            others = others + " " + str(exp)
        return self.keyword + others

    # perform/execute this statement given the environment of the symTable
    def perform(self, symTable):
        print ("Doing: " + str(self))

# Parsing each line to a Stmt object
# Currently WIP for let and/or print expressions
line_number = 1

for line in fileinput.input():
    line_strip = line.strip() # trims the left and right whitespaces of a line
    key = line_strip.partition(' ')[0] # get the key
    rest = line_strip.partition(' ')[2] # get the exprs
    restSplit = rest.split('=') # split into an array without the '='; allows us to store var key and key's value

    if key == 'let':
        symTable[restSplit[0].strip()] = restSplit[1].strip()

    # Parse line to a Stmt object (needs fixing)
    state = Stmt(key, rest)

    # Add the Stmt object to sList
    sList.append(state)

    # If this line is labeled:
        # Add (label, current line number) mapping to symTable
    if key[-1:] == ':':
        symTable[key[0:-1]] = line_number

    # Increment line number 
    line_number += 1

    print(symTable)

# Evaluate sList with symTable


#whole bunch of debugging stuff
    #print(restSplit)
    #print(state.__str__())
    #print(y)
    #print(key)
    #print(rest)
    

#print(express.__str__())

# let variableName = expression
# if expression goto label
# print expression1, expression2, ...
# input variableName