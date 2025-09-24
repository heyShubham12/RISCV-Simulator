.section .data
	.align 2
n:
	.word 5
l:
	.word 2
	.word -1
	.word 7
	.word 5
	.word 3

.section .text
.globl main
main:
   
	la   x1, l
	lw   x11, n
	li   x10, 0
	li   x2, 0

loop:
	bge  x2, x11, halt
	addi x1, x1, 4
	lw   x4, 0(x1)
	bge  x4, zero, check_even
	j    increment_index

check_even:

	andi x5, x4, 1
	beq  x5, zero, increment_count
	j    increment_index

increment_count:
	addi x10, x10, 1   # x10 = count + 1

increment_index:
	addi x2, x2, 1
	j    loop
halt:
	j halt

