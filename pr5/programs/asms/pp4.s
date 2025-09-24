.section .data
    .align 2                  
myvar1:
	.word 0xc001
myarr:
	.space 400

.section .text
	.global main
main:
	la x1, myarr
	la x3, myvar1
	li x4, 100	 
loop:
	lw t1, 0(x3)
	sw t1, 0(x1)
	addi x1, x1, 4
	addi x4, x4, -1
	bnez x4, loop
halt:
	j halt







	
