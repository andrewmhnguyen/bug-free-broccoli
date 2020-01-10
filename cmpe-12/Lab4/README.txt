------------------------
Lab 4: ASCII Decimal to 2SC
CMPE 012 Fall 2018
Nguyen, Andrew
anguy224
-------------------------
What was your approach to converting each decimal number to two’s complement
form?
If this is referring of ASCII to decimal, then I isolated the number that was in
the 10^1 slot. Afterwards, I subtracted by 48 to get the value (0-9) that wasn't an 
ASCII character and multiplied it by 10 to get the correct value.
I repeated the same step for the character in the 10^0 slot but I didn't multiply by
10 at the end. 

If it is referring to decimal to binary, I used the and operation and bit masking.
I started with 0x80000000 and anded it with the value. If it gave a 1, then I'd 
print a one, if it gave a 0, then I'd print a zero. Afterwards, I'd shift right by 1
and repeat the process 32 times.

What did you learn in this lab?
I learned about program arguments and how to take them. I also learned about arrays 
in MIPS and how to implement them. I also deepened my understanding of if statements
in MIPS and how I can use different ones. 

Did you encounter any issues? Were there parts of this lab you found enjoyable?
I was stuck on converting the ASCII to decimal form for a very long time. I was
also stuck on printing out values after I loaded them into an array. I think just
seeing it all work in the end was enjoyable. 

How would you redesign this lab to make it better?
I think I would add more suggestions on what to do, as I only figured out how to 
do everything after I looked through Piazza multiple times and rewatching the 
lectures. 