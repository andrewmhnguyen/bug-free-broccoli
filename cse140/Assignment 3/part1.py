import random
size = int(input("Rook Jumping Maze size (5-10)? "))
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

for r in arr:
    for c in r:
        print(c,end = " ")
    print()
