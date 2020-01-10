####################################################################################
# Created by: Nguyen, Andrew
# anguy224
# 9 November 2018
#
# Assignment: Lab 3: Loopinp in MIPS
# CMPE 012, Computer Systems and Assembly Language
# UC Santa Cruz, Fall 2018
#
# Description: This program prompts use for an integer and will print out integers 
#              starting from 0 up to the prompted integer. If the printed integer
#              is evenly divisble by 5, it will print "Flux". If the printed integer
#              is evenly divisble by 7, it will print "Bunny". If evenly divisible 
#              by both, it will print "Flux Bunny".
#
# Notes: This program is intended to be run from the MARS IDE.
####################################################################################


# REGISTER USAGE
# $t0: user input
# $t1: loop counter
# $t2: holds the number 5
# $t3: holds the number 7
# $t4: holds remainder of counter/5
# $t5: holds remainder of counter/7
# $t6: adds $t4 and $t5 together
# $t7: loop boolean

.text
  #prompts user for number
  li   $v0, 4
  la   $a0, prompt
  syscall

  #reads the number and stores it in $t0
  li   $v0, 5
  syscall
  move $t0, $v0

  li   $t1, 0 #gives value of 0 to $t1
  li   $t2, 5 #gives value of 5 to $t2
  li   $t3, 7 #gives value of 7 to $t3

  start_loop: 
    sle  $t7, $t1, $t0
    beqz $t7, end_loop
    
    #checks to see if evenly divisible by 5 and moves the remainder to $t4
    div  $t1, $t2 
    mfhi $t4
  
    #checks to see if evenly divisible by 7 and moves the remainder to $t5
    div  $t1, $t3 
    mfhi $t5
    
    #adds $t4 and $t5 to see if evenly divisible by both
    add  $t6, $t4, $t5
  
    #if block
      beqz $t6, both75         #checks if $t6 is equal to 0, means that number is evenly divisible by 5 and 7   
      beqz $t4, only5          #checks if $t4 is equal to 0, means that number is evenly divisible by 5
      beqz $t5, only7          #checks if $t5 is equal to 0, means that number is evenly divisible by 7
      sge  $t6, $t6,   0       #checks if $t6 is greater than 0, means that some remainder exists
      beq  $t6, 1,     else    #if a remainder does exist, then it goes to the else statement
      b end_if
    both75:
      #prints out Flux Bunny if $t1 is evenly divisible by 5 and 7
      li   $v0, 4
      la   $a0, even75
      syscall
      b end_if
    only5:
      #prints out Flux Bunny if $t1 is evenly divisible by 5
      li   $v0, 4
      la   $a0, even5
      syscall
      b end_if
    only7:
      #prints out Flux Bunny if $t1 is evenly divisible by 7
      li   $v0, 4
      la   $a0, even7
      syscall
      b end_if
    else:
      #prints out value of number stored in $t1
      li   $v0, 1 
      move $a0, $t1
      syscall
      b end_if

    end_if:
    
    #prints new line
    li   $v0, 4
    la   $a0, newLine
    syscall
    
    #adds to counter
    addi $t1, $t1, 1
    b start_loop
    
  end_loop:
  
  #program exit
  li   $v0, 10
  syscall
  
.data
  
  prompt:  .asciiz "Please input a positive integer: "
  even5:   .asciiz "Flux"
  even7:   .asciiz "Bunny"
  even75:  .asciiz "Flux Bunny"
  newLine: .asciiz "\n"
