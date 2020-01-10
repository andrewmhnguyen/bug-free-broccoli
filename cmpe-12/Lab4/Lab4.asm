####################################################################################
# Created by: Nguyen, Andrew
# anguy224
# 18 November 2018
#
# Assignment: Lab 4: ASCII Decimal to 2SC
# CMPE 012, Computer Systems and Assembly Language
# UC Santa Cruz, Fall 2018
#
# Description: Takes in ASCII decimal number and converts to integer and then adds
#              Prints out the sum in decimal and 2SC form.
#
# Notes: This program is intended to be run from the MARS IDE.
####################################################################################

#Pseudo Code
#Takes in 2 numbers from user 
#Converts 2 numbers to 2SC
#Stores them in register $s1 and $s2
#Adds the 2 numbers together
#Stores the output in register $s0
#Convert the number back to decimal
#Print out both the decimal and 2SC form

# REGISTER USAGE
# $t0: stores the first argument in ASCII
#    : stores the array 
#    : bit mask
# $t1: stores the second argument in ASCII
#    : counter/offset when printing out the sum in ASCII form
#    : counter when printing out the sim in binary form
# $t2: loads in value at  ($t0) for converting args
#    : copies $t0 array
#    : anded value of $t0 and $t1 to determine what to print 
# $t3: loads in value at 1($t0) for converting args
# $t4: stores the first char in the argument
#    : keeps track of if $s0 is negative or positive 
# $t5: stored as 1 or -1 depending if the arg is postive or negative
#    : used to divide by 10 
# $t6: stored remainder of $t9/10 to get the values to store in array
# $t9: copy of $s0 and divided by 10 to get values to divide by 10 again - sets itself as that value 
# $s0: stores the sum of the two numbers 
# $s1: stores the first argument in 2SC
# $s2: stores the second argument in 2SC

.text
  
  #prints out string decnumbers
  li   $v0, 4
  la   $a0, decnumbers
  syscall
  
  #takes first argument and prints it
  lw   $a0, ($a1)
  move $t0, $a0
  li   $v0, 4
  syscall
  
  #orunts out a space
  li   $a0, 4
  la   $a0, space
  syscall
  
  #takes second argument and prints it
  lw   $a0, 4($a1)
  move $t1, $a0
  li   $v0, 4
  syscall

  #prints new line
  li   $a0, 4
  la   $a0, newline
  syscall 
  
  #prints new line
  li  $v0, 4
  la  $a0, newline
  syscall
  
  #found on Piazza post by Daniel Schilling when he posted his psuedo code in response to another student - post 
  conversionToDecimal:
    firstArg:
      #if block - checks if positive or negative first 
      start:
        li  $t5, 1               #represents positive value 
        lb  $t4, ($t0)           #checks if first value is negative
        beq $t4, 0x2d, negative  #if - sign is present goes to negative
        b   start_loop
      #if there is a negative value - increments by 1 to go to next value
      negative:                 
        li  $t5, -1
        add $t0, $t0, 1
     
      #sees which number it is on and redirects to correct one
      start_loop:             
        lb    $t2,  ($t0)            #loads in character at address ($t0)
        lb    $t3, 1($t0)            #loads in character at address 1($t0)
        bne   $t3, 0x0,    bigchar   #if $t3 isn't void, go to bigchar
        beq   $t3, 0x0,    smallchar #if $t3 is void, go to smallchar
      
      #if numbers are multiples of 10^1 goes here and converts to decimal
      bigchar:
        sub   $t2, $t2, 48          #subtracts 48 to get the correct value in decimal form
        mul   $t2, $t2, 10          #multiply by 10
        add   $s1, $s1, $t2         #add that value to $s1
        add   $t0, $t0, 1           #changes the address
        b     start_loop
      
      #if numbers are multiples of 10^0 goes here and converts to decimal
      smallchar:
        sub   $t2, $t2, 48  #subtracts 40 to get the correct value in decimal form
        add   $s1, $s1, $t2 #adds that value to $s1
        b end_loop
      
      end_loop:
      
      #multiplies with $t5 which gives the number its correct positive or negative value
      mul $s1, $s1, $t5
      
    secondArg:  
      #if block - checks if positive or negative first
      start2:
        li    $t5, 1
        lb    $t4, ($t1)
        beq   $t4, 0x2d, negative2
        b     start_loop2
      #if there is a negative value - increments by 1 to go to next value    
      negative2:
        li    $t5, -1
        add   $t1, $t1, 1
        
      #sees which number it is on and redirects to correct one
      start_loop2: 
        lb    $t2,  ($t1)               #loads in character at address ($t1)
        lb    $t3, 1($t1)               #loads in character at address 1($t1)
        bne   $t3, 0x0,    bigchar2     #if $t3 isn't void, go to bigchar2
        beq   $t3, 0x0,    smallchar2   #if $t3 is void, go to smallchar2
        
      #if numbers are multiples of 10^1 goes here and converts to decimal
      bigchar2:
        sub   $t2, $t2, 48   #subtracts by 48 to get the correct value in decimal form
        mul   $t2, $t2, 10   #multiplies by 10
        add   $s2, $s2, $t2  #adds the value to $s2
        add   $t1, $t1, 1    #changes the address
        b     start_loop2
        
      #if numbers are multiples of 10^0 goes here and converts to decimal
      smallchar2:
        sub   $t2, $t2, 48  #subtracts by 48 to get the correct value in decimal form 
        add   $s2, $s2, $t2 #adds the value to $s2
        b     end_loop2
      
      end_loop2:
      
      #multiplies with $t5 which gives the number its correct positive or negative value
      mul $s2, $s2, $t5
    
    #adds two converted numbers together and stores them in $s0
    add $s0, $s1, $s2
  
  
  #prints out message in decsum - The sum in decimal is:
  li  $v0, 4
  la  $a0, decsum
  syscall
  
  li   $t5, 10     #intializes $t5 to 10 so it can be used to divide with
  li   $t4, 1      #intializes $t4 to 1 - will later be used as a negative checker
  move $t9, $s0    #copies $s0 to $t9 so we can manipulate $t9
  
  
  arrayCreation:
    #creation of array and intialization of counter/offset
    la   $t0, array
    li   $t1, 0
    blt  $s0, 0,     negNumber #checks if number in $s0 is negative 
    move $t2, $t0              
    b loop
    
    #changes $t9 so it is a positive number - also changes $t4 to -1
    negNumber:
      li   $t4, -1
      mul  $t9, $t9,   -1  
      move $t2, $t0
  
  #loops to isolate values in order to convert them to ASCII and then stores them in an array
  #used array from class as inspiration 
  loop:
    div  $t9, $t5
    mflo $t9                 #$t9/10 gives the next value to divide by
    mfhi $t6                 #$t9%10 gives value that needs to be stored
    add  $t6,  $t6,  48      #add 48 to convert to ASCII
    sb   $t6, ($t2)          #stores the value to array at $t2
    addi $t1,  $t1,  1       #increases offset/counter 
    add  $t2,  $t0, $t1      #changes the address
    beq  $t9,   0,   endLoop #ends the loop 
    b    loop
  endLoop:
  
  sb   $zero ($t2)  #adds zero to the array 
  
  #prints the array
  printArray:
    beq $t4, -1, printNeg
    b skipNeg
    #if number is negative, prints out "-" character
    printNeg:
      li $v0, 4
      la $a0, minus
      syscall
    skipNeg:
    
    #checks the counter and determines where the first character to print is 
    beq $t1, 3, printLoop3  #checks if there are 3 characters
    beq $t1, 2, printLoop2  #checks if there are 2 characters
    beq $t1, 1, printLoop1  #checks if there is 1 character
    
    printLoop3:
      beq $t1, 0, endPrintLoop3 #checks if there are any characters left, if not, end
      #prints character at the address
      li $v0 11
      lb $a0 2($t0)
      syscall
      
      sub $t0, $t0, 1 #changes the address
      sub $t1, $t1, 1 #lowers the counter
      b printLoop3
    endPrintLoop3:
    
    printLoop2:
      beq $t1, 0, endPrintLoop2 #checks if there are any characters left, if not, end
      #prints character at the address
      li $v0 11
      lb $a0 1($t0)
      syscall
      
      sub $t0, $t0, 1 #changes the address
      sub $t1, $t1, 1 #lowers the counter
      b printLoop2
    endPrintLoop2:
    
    printLoop1:
      beq $t1, 0, endPrintLoop1 ##checks if there are any characters left, if not, end
      #prints character at the address
      li $v0 11
      lb $a0 ($t0)
      syscall
      
      sub $t0, $t0, 1 #changes the address
      sub $t1, $t1, 1 #lowers the counter 
      b printLoop1
    endPrintLoop1:
  #prints new line 
  li  $v0, 4
  la  $a0, newline
  syscall
  
  #prints new line
  li  $v0, 4
  la  $a0, newline
  syscall

  #found on Piazza post by Daniel Schilling when he posted in response to a student asking how to print binary
  printInBinary:
    startBinary:
      li $t0, 0x80000000            #bit mask
      li $t1, 0                     #counter
      
      #prints out the message: "The sum in binary is:"
      li $v0, 4                     
      la $a0, binsum
      syscall 
    
    #loops through 32 bits and ands them with the bit mask
    binaryLoop:
      and $t2, $t0, $s0            #ands bit mask and value to be printed
      beq $t2, 1, one              #if and returns one, will print "1"
      beq $t2, 0, zero             #if and returns zero, will print "0"
    one:
      #prints a one 
      li  $v0, 4
      la  $a0, printOne
      syscall
       
      srl $t0, $t0, 1             #shifts mask by one
      add $t1, $t1, 1             #adds to counter
      beq $t1, 32,  endBinaryLoop #if counter reaches 32, means a full shift has been completed
      b   binaryLoop  
    zero:
      #prints a zero
      li  $v0, 4
      la  $a0, printZero
      syscall
     
      srl $t0, $t0, 1             #shifts mask by one
      add $t1, $t1, 1             #adds to counter
      beq $t1, 32,  endBinaryLoop #if counter reaches 32, means a full shift has been completed
      b   binaryLoop
  
    endBinaryLoop:
  
  #prints new line
  li  $v0, 4
  la  $a0, newline
  syscall
  
  #program exit
  li  $v0, 10
  syscall
  
.data
  array:      .space   3
  minus:      .asciiz "-"
  printOne:   .asciiz "1"
  printZero:  .asciiz "0"
  decnumbers: .asciiz "You entered the decimal numbers:\n"
  decsum:     .asciiz "The sum in decimal is:\n"
  binsum:     .asciiz "The sum in two's complement binary is:\n"
  space:      .asciiz " "
  newline:    .asciiz "\n"
