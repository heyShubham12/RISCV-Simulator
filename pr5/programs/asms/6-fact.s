.section .data
	.align 2
a:
	.word 5

.section .text

.globl main
main:

	la x11, a
	lw x12, 0(x11)
	li x1, 2
	li x2, 1
	addi x14, x12, 0
	addi x13, x12, -1
	bge x12, x1, fact

fact:

	blt x12, x2, halt
	mul x10, x14, x13
	addi x13, x13, -1
	addi x12, x12, -1
	addi x14, x10, 0
	bne x13, x2, fact
halt:
	j halt
