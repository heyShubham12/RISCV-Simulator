.section .data
	.align 2
count:
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
marks:
	.word 2
	.word 3
	.word 0
	.word 5
	.word 10
	.word 7
	.word 1
	.word 10
	.word 10
	.word 8
	.word 9
	.word 6
	.word 7
	.word 8
	.word 2
	.word 4
	.word 5
	.word 0
	.word 9
	.word 1
n:
	.word 20

.section .text
.globl main
main:
	la x11, count   
	la x12, marks 
	li x13, 11       
	lw x14, n      
	li x7, 1      
	li x17, 4

loop:
	bge x7, x14, halt

	lw x15, 0(x12)   
	mul x15, x15, x17 
	add x15, x11, x15
	lw x6, 0(x15)      
	addi x6, x6, 1    
	sw x6, 0(x15)     
	addi x12, x12, 4
	addi x7, x7, 1   
	j loop        

halt:
	j halt        

