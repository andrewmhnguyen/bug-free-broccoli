
import random

def solve_csp(nodes, arcs, max_steps):
    #populating values for each node
    values = []
    conflict = []
    for i in range(5):
        values.append(random.randint(1,9))
    
    for i in range(max_steps):
        if conflicts(nodes, arcs, values) == 0:
            return values
        #find all conflicting variables
        
        for j in range(len(nodes)):
            if nodes[j] == 'Y':
                if yellow(nodes,arcs,values) == 1:
                    conflict.append(j)
            elif nodes[j] == 'G':
                if green(nodes, arcs, values) == 1:
                    conflict.append(j)
            elif nodes[j] == 'B':
                if blue(nodes,arcs,values) == 1:
                    conflict.append(j)
            elif nodes[j] == 'V':
                if violet(nodes,arcs,values) == 1:
                    conflict.append(j)
        #take one conflicting variable - takes the index at which it occurs  
        var1 = random.choice(conflict)
        init = conflicts(nodes, arcs, values)
        best = values[var1]
        temp = 0
        for k in range(1,10):
            values[var1] = k
            temp = conflicts(nodes, arcs, values)
            if temp <= init:
                init = temp
                best = k
        values[var1] = best
        conflict=[]
    node_values = []
    return node_values

def conflicts(nodes, arcs, values):
    return yellow(nodes, arcs, values) + green(nodes, arcs, values) + blue(nodes, arcs, values) + violet(nodes, arcs, values)
    
def yellow(nodes, arcs, values):
    yellow = []
    #grab all index of nodes that are yellow
    i = 0
    while i < len(nodes):
        if nodes[i] == 'Y':
            yellow.append(i)
        i = i + 1

    #grab all index of arcs that have yellow nodes - to determine neighbors
    neighbors1 = []
    neighbors2 = []
    neighbors3 = []
    neighbors4 = []
    neighbors5 = []
    
    i = 0
    while i < len(arcs):
        for j in yellow:
            if arcs[i][0] == j:
                if j == 0:
                    neighbors1.append(arcs[i][1])
                if j == 1:
                    neighbors2.append(arcs[i][1])
                if j == 2:
                    neighbors3.append(arcs[i][1])
                if j == 3:
                    neighbors4.append(arcs[i][1])
                if j == 4:
                    neighbors5.append(arcs[i][1])
            elif arcs[i][1] == j:
                if j == 0:
                    neighbors1.append(arcs[i][0])
                if j == 1:
                    neighbors2.append(arcs[i][0])
                if j == 2:
                    neighbors3.append(arcs[i][0])
                if j == 3:
                    neighbors4.append(arcs[i][0])
                if j == 4:
                    neighbors5.append(arcs[i][0])
        i = i + 1
    conflicts = 0
    #checking the amount of conflicts
    for j in yellow:
        if j == 0:
            #check value of neighbor1 and then compare it to value of yellow
            total = 1
            for i in neighbors1:
                total = total * values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 1:
            total = 1
            for i in neighbors2:
                total = total * values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 2:
            total = 1
            for i in neighbors3:
                total = total * values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 3:
            total = 1
            for i in neighbors4:
                total = total * values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 4:
            total = 1
            for i in neighbors5:
                total = total * values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
    return conflicts

def green(nodes, arcs, values):
    green = []
    #grab all index of nodes that are green
    i = 0
    while i < len(nodes):
        if nodes[i] == 'G':
            green.append(i)
        i = i + 1

    #grab all index of arcs that have green nodes - to determine neighbors
    neighbors1 = []
    neighbors2 = []
    neighbors3 = []
    neighbors4 = []
    neighbors5 = []
    i = 0
    while i < len(arcs):
        for j in green:
            if arcs[i][0] == j:
                if j == 0:
                    neighbors1.append(arcs[i][1])
                if j == 1:
                    neighbors2.append(arcs[i][1])
                if j == 2:
                    neighbors3.append(arcs[i][1])
                if j == 3:
                    neighbors4.append(arcs[i][1])
                if j == 4:
                    neighbors5.append(arcs[i][1])
            elif arcs[i][1] == j:
                if j == 0:
                    neighbors1.append(arcs[i][0])
                if j == 1:
                    neighbors2.append(arcs[i][0])
                if j == 2:
                    neighbors3.append(arcs[i][0])
                if j == 3:
                    neighbors4.append(arcs[i][0])
                if j == 4:
                    neighbors5.append(arcs[i][0])
        i = i + 1
    conflicts = 0
    #checking the amount of conflicts
    for j in green:
        if j == 0:
            #check value of neighbor1 and then compare it to value of green
            total = 0
            for i in neighbors1:
                total = total + values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 1:
            total = 0
            for i in neighbors2:
                total = total + values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 2:
            total = 0
            for i in neighbors3:
                total = total + values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 3:
            total = 0
            for i in neighbors4:
                total = total + values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
        if j == 4:
            total = 0
            for i in neighbors5:
                total = total + values[i]
            rightmost = total%10
            if values[j] != rightmost:
                conflicts = conflicts + 1
    return conflicts

def blue(nodes, arcs, values):
    blue = []
    #grab all index of nodes that are blue
    i = 0
    while i < len(nodes):
        if nodes[i] == 'B':
            blue.append(i)
        i = i + 1

    #grab all index of arcs that have blue nodes - to determine neighbors
    neighbors1 = []
    neighbors2 = []
    neighbors3 = []
    neighbors4 = []
    neighbors5 = []
    i = 0
    while i < len(arcs):
        for j in blue:
            if arcs[i][0] == j:
                if j == 0:
                    neighbors1.append(arcs[i][1])
                if j == 1:
                    neighbors2.append(arcs[i][1])
                if j == 2:
                    neighbors3.append(arcs[i][1])
                if j == 3:
                    neighbors4.append(arcs[i][1])
                if j == 4:
                    neighbors5.append(arcs[i][1])
            elif arcs[i][1] == j:
                if j == 0:
                    neighbors1.append(arcs[i][0])
                if j == 1:
                    neighbors2.append(arcs[i][0])
                if j == 2:
                    neighbors3.append(arcs[i][0])
                if j == 3:
                    neighbors4.append(arcs[i][0])
                if j == 4:
                    neighbors5.append(arcs[i][0])
        i = i + 1
    conflicts = 0
    #checking the amount of conflicts
    for j in blue:
        if j == 0:
            #check value of neighbor1 and then compare it to value of blue
            total = 0
            for i in neighbors1:
                total = total + values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 1:
            total = 0
            for i in neighbors2:
                total = total + values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 2:
            total = 0
            for i in neighbors3:
                total = total + values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 3:
            total = 0
            for i in neighbors4:
                total = total + values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 4:
            total = 0
            for i in neighbors5:
                total = total + values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
    return conflicts

def violet(nodes, arcs, values):
    violet = []
    #grab all index of nodes that are violet
    i = 0
    while i < len(nodes):
        if nodes[i] == 'V':
            violet.append(i)
        i = i + 1

    #grab all index of arcs that have violet nodes - to determine neighbors
    neighbors1 = []
    neighbors2 = []
    neighbors3 = []
    neighbors4 = []
    neighbors5 = []
    i = 0
    while i < len(arcs):
        for j in violet:
            if arcs[i][0] == j:
                if j == 0:
                    neighbors1.append(arcs[i][1])
                if j == 1:
                    neighbors2.append(arcs[i][1])
                if j == 2:
                    neighbors3.append(arcs[i][1])
                if j == 3:
                    neighbors4.append(arcs[i][1])
                if j == 4:
                    neighbors5.append(arcs[i][1])
            elif arcs[i][1] == j:
                if j == 0:
                    neighbors1.append(arcs[i][0])
                if j == 1:
                    neighbors2.append(arcs[i][0])
                if j == 2:
                    neighbors3.append(arcs[i][0])
                if j == 3:
                    neighbors4.append(arcs[i][0])
                if j == 4:
                    neighbors5.append(arcs[i][0])
        i = i + 1
    conflicts = 0
    #checking the amount of conflicts
    for j in violet:
        if j == 0:
            #check value of neighbor1 and then compare it to value of violet
            total = 1
            for i in neighbors1:
                total = total * values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 1:
            total = 1
            for i in neighbors2:
                total = total * values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 2:
            total = 1
            for i in neighbors3:
                total = total * values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 3:
            total = 1
            for i in neighbors4:
                total = total * values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        if j == 4:
            total = 1
            for i in neighbors5:
                total = total * values[i]
            leftmost = firstDigit(total)
            if values[j] != leftmost:
                conflicts = conflicts + 1
        
    return conflicts

def firstDigit(n) : 
  
    # Remove last digit from number 
    # till only one digit is left 
    while n >= 10:  
        n = n / 10
    # return the first digit 
    return int(n) 
nodes = 'YGVRB'
arcs = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4)]
max_steps = 1000

for _ in range(max_steps):
    sol = solve_csp(nodes, arcs, max_steps)
    if sol != []:
        break
        
all_solutions = [[1, 1, 1, 7, 2],[2, 1, 2, 4, 3],[2, 6, 7, 6, 1],[2, 8, 9, 6, 1],
                 [3, 3, 1, 5, 4],[6, 2, 8, 7, 1],[6, 7, 8, 2, 1],[6, 9, 4, 8, 1]]

if sol == []:
    print('No solution')
else:
    if sol in all_solutions:
        print('Solution found:', sol)
    else:
        print('ERROR: False solution found:', sol)