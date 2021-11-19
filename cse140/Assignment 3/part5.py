import random
import copy

iterations = int(input("Iterations? "))
probability = float(input("Uphill step probability? "))
size = 5
def rjm(size):
    rows, cols = (size, size) 
    arr=[] 
    col = 1
    for i in range(cols): 
        col1 = [] 
        row = 1
        for j in range(rows): 
            rand = random.randint(1, max(((size)-row), (row - 1), ((size)-col), (col-1)))
            col1.append(rand)
            row += 1 
        arr.append(col1) 
        col += 1
    arr[size-1][size-1] = 0
    return arr
arr = rjm(size)

for r in arr:
    for c in r:
        print(c,end = " ")
    print()

def eval_RJM(arr):

    #second 2d array filled with values
    rows, cols = (len(arr), len(arr)) 
    arr2=[] 
    for i in range(cols): 
        col = [] 
        for j in range(rows): 
            col.append(100000) #set a high value for depths 
        arr2.append(col) 
    row = 0
    col = 0
    depth = 0

    #creation of queue
    def bfs_path(arr, arr2, row, col, depth):
        queue = [(row,col,depth)]
        arr2[row][col] = depth
    
        while (len(queue) != 0):
            tak = queue.pop(0)
            row = tak[0]
            col = tak[1]
            depth = tak[2]
            val = arr[row][col]
            if (col + val < size):
                if arr2[row][col+val] > depth+1:
                    queue.append((row, col+val, depth+1))
                    arr2[row][col+val] = depth+1
            if (row + val < size):
                if arr2[row+val][col] > depth+1:
                    queue.append((row+val, col, depth+1))
                    arr2[row+val][col] = depth+1
            if (col - val >= 0):
                if arr2[row][col-val] > depth+1:
                    queue.append((row,col-val,depth+1))
                    arr2[row][col-val] = depth+1
            if (row - val >= 0):
                if arr2[row-val][col] > depth+1:
                    queue.append((row-val,col,depth+1))
                    arr2[row-val][col] = depth+1

    bfs_path(arr, arr2, row, col, depth)

    moves = arr2[size-1][size-1]
    if moves != 100000:
        moves = -1*moves
    for r in arr2:
        hold = ""
        for c in r:
            if c == 100000:
                c = "--"
                hold = hold + c + " "
            elif c < 10:
                hold = hold + " "+ str(c) + " "
            else:
                hold = hold + str(c) + " "
        #print (hold)
    #print(moves)
    return moves
eval_RJM(arr)

best_board = arr
for i in range(iterations):
    #step function - changing one value
    new_board = copy.deepcopy(arr)
    goal = False
    while goal == False:
        rand1 = random.randint(0,4)
        rand2 = random.randint(0,4)
        if ((rand1 == 4) and (rand2 == 4)):
            continue
        new_board[rand1][rand2] = random.randint(1, max(((size)-rand1), (rand1 - 1), ((size)-rand2), (rand2-1)))
        goal = True
    #using eval to compare
    if ((eval_RJM(new_board) <= eval_RJM(arr)) or (random.randint(1,100)<=probability*100)):
        arr = new_board
        if (eval_RJM(new_board) <= eval_RJM(best_board)):
            best_board = arr

def print_eval_RJM(arr):

    #second 2d array filled with values
    rows, cols = (len(arr), len(arr)) 
    arr2=[] 
    for i in range(cols): 
        col = [] 
        for j in range(rows): 
            col.append(100000) #set a high value for depths 
        arr2.append(col) 
    row = 0
    col = 0
    depth = 0

    #creation of queue
    def bfs_path(arr, arr2, row, col, depth):
        queue = [(row,col,depth)]
        arr2[row][col] = depth
    
        while (len(queue) != 0):
            tak = queue.pop(0)
            row = tak[0]
            col = tak[1]
            depth = tak[2]
            val = arr[row][col]
            if (col + val < size):
                if arr2[row][col+val] > depth+1:
                    queue.append((row, col+val, depth+1))
                    arr2[row][col+val] = depth+1
            if (row + val < size):
                if arr2[row+val][col] > depth+1:
                    queue.append((row+val, col, depth+1))
                    arr2[row+val][col] = depth+1
            if (col - val >= 0):
                if arr2[row][col-val] > depth+1:
                    queue.append((row,col-val,depth+1))
                    arr2[row][col-val] = depth+1
            if (row - val >= 0):
                if arr2[row-val][col] > depth+1:
                    queue.append((row-val,col,depth+1))
                    arr2[row-val][col] = depth+1

    bfs_path(arr, arr2, row, col, depth)

    print("Moves from start:")
    moves = arr2[size-1][size-1]
    if moves != 100000:
        moves = -1*moves
    for r in arr2:
        hold = ""
        for c in r:
            if c == 100000:
                c = "--"
                hold = hold + c + " "
            elif c < 10:
                hold = hold + " "+ str(c) + " "
            else:
                hold = hold + str(c) + " "
        print (hold)
    print(moves)

print_eval_RJM(best_board)
