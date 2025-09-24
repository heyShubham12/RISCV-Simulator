.section .data
sum:
	.word 0xc001
.section .text
.global main
main:
	la x3, sum
	li x1, 10
	li x2, 20
	add x3, x1, x2
halt:
	j halt
