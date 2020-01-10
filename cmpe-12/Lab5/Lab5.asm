##########################################################################################
# Created by: Nguyen, Andrew
# anguy224
# 7 December 2018
#
# Assignment: Lab 3: Loopinp in MIPS
# CMPE 012, Computer Systems aLab 5: Subroutinesnd Assembly Language
# UC Santa Cruz, Fall 2018
#
# Description: This program is used in tandem with Lab5Test.asm and is the 
#              implementations of the subroutines called.
#
#              give_type_prompt:         gives the prompt to type and also takes the time
#                                        that it was printed
#              checks_user_input_string: checks time and takes user input. Then 
#                                        calls compare_strings. Returns 0 if lost, 1
#                                        if won.
#              compare_strings:          compares two strings - calls compare_chars - 
#                                        returns 0 if not the same, returns 1 if the same
#              compare_chars:            compares two chars - returns 0 if not the same, 
#                                        returns 1 if they are
#
# Notes: This program is intended to be run from the MARS IDE.
##########################################################################################


# REGISTER USAGE
# $t0: stores address for compare_chars address
# $t1: stores address for compare_string address
#    : stores user input before moving to $a1
# $t2: holds the time value when user finishes their string
# $t3: holds the time value of when system printed out prompt
# $t4: holds address of type prompt given to user
# $t5: 
# $t6: holds value of next element in the string for $a0 - checks if void or not
# $t7: holds value of next element in the string for $a1 - checks if void or not 
# $t8: holds address of $a0 - to manipulate the address and move to next element
# $t9: holds address of $a1 - to manipulate the address and move to next element

.text
give_type_prompt:
  #pushing to stack $ra
  subi $sp $sp 4
  sw   $ra ($sp)
  
  #saves the value of $a0 in $sp
  subi $sp $sp 4
  sw   $a0 ($sp)
  
  #prints out "Type Prompt: "
  li   $v0 4
  la   $a0 typePrompt
  syscall
  
  #reloads the value of $a0
  lw   $a0 ($sp)
  addi $sp $sp 4
  
  #prints out what to type
  li   $v0 4
  syscall
  
  #takes current time of system and moves it to $a0
  li   $v0 30
  syscall 
  
  #popping off the stack $ra
  lw   $ra ($sp)
  addi $sp $sp 4
  jr   $ra
  
check_user_input_string:
  #pushing to the stack $ra
  subi $sp $sp 4
  sw   $ra ($sp)
  
  #saves address of type prompt given to user and the time the type prompt was given to the user
  move $t4 $a0
  move $t3 $a1
  
  #takes in user input and moves the string to $t1
  la   $a0 inputSpace
  li   $a1 128
  li   $v0 8
  syscall
  move $t1 $a0
  
  #gets current system time and moves it to $t2
  li   $v0 30
  syscall
  move $t2 $a0
  
  #checks if $t2 - $t3 is greater than the allotted time 
  sub  $t2 $t2 $t3
  bgt  $t2 $a2 timeOver
  b    moveon
  
  #sets $v0 to 0 and sends the user to the ending
  timeOver:
    li $v0 0
    b  ending
  
  #if allotted time isn't moved over - moves user input from $t1 to $a1 and the address of the prompt back to $a0
  moveon:
    move $a1 $t1
    move $a0 $t4
  
  #jumps to compare_strings subroutine
  la   $t1 compare_strings
  jalr $t1
  
  ending:
    #pops $ra off the stack
    lw   $ra ($sp)
    addi $sp $sp 4
    jr   $ra

compare_strings:
  #pushing $ra to the stack
  subi $sp $sp 4
  sw   $ra ($sp)
  
  #pushing the values of $a0 and $a1 to the stack
  subi $sp $sp 8
  sw   $a0 ($sp)
  sw   $a1 4($sp)
  
  #sets $t8 and $t9 to addresses of $a0 and $a1
  la   $t8 ($a0)
  la   $t9 ($a1)
  
  #loop to compare characters in the string
  stringLoop:
    #sets $a0 and $a1 to the value at address of $t8 and $t9
    lb   $a0 ($t8)
    lb   $a1 ($t9)
    
    #jumps to compare_chars subroutine
    la   $t0 compare_chars
    jalr $t0
    
    #if $v0 is 0, then the strings aren't equal
    beq  $v0  0  notEqualString
    
    #increments the addresses by 1 
    add  $t8 $t8 1
    add  $t9 $t9 1
    lb   $t7 ($t8)
    lb   $t6 ($t9)
    #checks if the next value in $a0 is void - if it isn't, restart loop
    beq  $t7 0x0 string0
    b    stringLoop
    
    #checks if next value in $a1 is also void - if it isn't restart loop
    string0:
      beq  $t6 0x0 endStringLoop
      li   $v0 0
      b    notEqualString
      
  endStringLoop:
    
  notEqualString:
  #pops values of $a0 and $a1 off the stack
  lw   $a0 ($sp)
  lw   $a1 4($sp)
  addi $sp $sp 8
  
  #pops value of $ra off the stack
  lw   $ra ($sp)
  addi $sp $sp 4
  jr   $ra

compare_chars:
  #pushes value of $ra to the stack
  subi $sp $sp 4
  sw   $ra ($sp)
  
  #checks if the characters are the same
  beq  $a0 $a1 isEqual
  bne  $a0 $a1 notEqual
  #$v0 is 1 if they are
  isEqual:
    li $v0 1 
    b  finished
  
  #$v0 is 0 if they aren't
  notEqual:
    li $v0 0
    b finished
  
  finished:
    #pops $ra off the stack
    lw   $ra ($sp)
    addi $sp $sp 4
    jr   $ra
  
.data
  typePrompt:  .asciiz  "Type Prompt: "
  inputSpace:  .space   128

