.section .data
	.align 2
myvar1: 
	.word 0xc001

myvar2: 
	.word 0xc0de

	.size myarr, 16
myarr:  
	.word 0xfeed
	.word 0xdeed
	.word 0xdeaf
	.word 0xd00d


.section .text
	.globl main
main:
	la x1, myvar1
	lw x11, 0(x1)

	la x2, myvar2
	lw x12, 0(x2)

	la x3, myarr
	lw x13, 0(x3)
	lw x14, 4(x3)
halt:
	j halt

