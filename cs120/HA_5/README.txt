Canvas Group Name:Group 100             Student 1:Andrew Nguyen          Student 2: Allen Yabut

We compiled the code using: gcc -O3 matmul.c -o Matmul

Which then created an executable file named: Matmul

Then we ran it using ./Matmul

In the program itself, we first initialize the arrays in Main
Then we test out the first matmul with no changes and the time it takes

Afterwards, we test out the transposed matmul and the time it takes

Finally, we test out the tile matmul with each power of 2, going from 1 to 1024.
During these runs, we also need to reset the array E in between each test so the results don't carry over.

The results are printed sequentially and we test each array with verify before moving to the next one