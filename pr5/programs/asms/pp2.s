.section .text
.globl main
main:
	li x1, 50
	li x2, 30
	li x3, 70
	bgt x1, x2, next1
	bgt x2, x3, next2
	
next1:
	blt x1, x3, next3
	mv x4, x1
	j halt
next2:
	mv x4, x2
   	j halt
next3:
	mv x4, x3
   	j halt
halt:
	j halt
	
