.section .data
	.align 2
a:
	.word 6

.section .text

.globl main
main:
    
	la   x11, a
	lw   x1, 0(x11)
	li   x2 , 2
	
loop:
    bge x2, x1, prime
    rem x3, x1, x2
    beqz x3, not_prime
    addi x2, x2, 1
    j loop

not_prime:
	li   x10, -1   
	j    halt       

prime:
	li   x10, 1         
	j    halt 

halt:
	j halt
