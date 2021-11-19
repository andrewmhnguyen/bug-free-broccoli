"""
Pseudocode

//assume in the command prompt the user has entered the argument, tl.txt, the name of
//the text file that contains a TL program in it
create sList, an empty list of Stmt objects
create symTable, an empty symbol table

for each line of statement in tl.txt:
    parse the line to an Stmt object //possibly with satellite Expr objects
    add the Stmt object to sList
    if this line is labeled:
        add (label, current line number) mapping to symTable

evaluate sList with symTable
"""
