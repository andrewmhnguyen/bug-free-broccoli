#! /usr/bin/env python3
import fileinput
import sys


#for line in fileinput.input():
#   print(line)

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

# Currently working on below

for eachLine in fileinput.input():
    y = eachLine.strip()
    key = y.partition(' ')[0] # get the key
    rest = y.partition(' ')[2] # get the exprs
    state = Stmt(key, rest)
    
    #print(state.__str__())
    #print(y)
    #print(key)
    print(rest)

testEx = Expr('x', '=', '1')
print(testEx.__str__())

# let variableName = expression
# if expression goto label
# print expression1, expression2, ...
# input variableName