.section .text

matmul:
	li a6, 1
	li t0, 12
	li t1, 3
	li t2, 0 # i=0

loopi:
	beq t2, t1, finish
	li t3, 0 # j=0

loopj:
	beq t3, t1, next_i
	li t4, 0 #sum = 0
	li t5, 0 #k=0
	
loopk:
	beq t5, t1, next_j
	
	mul t6, t0, t2
	slli a3, t5, 2
	add t6, t6, a3
	add t6, t6, a0
	lw a4, 0(t6)
	
	mul t6, t0, t5
	slli a3, t3, 2
	add t6, t6, a3
	add t6, t6, a1
	lw a5, 0(t6)
	
	mul a4, a4, a5
	add t4, t4, a4
	
	addi t5, t5, 1
	j loopk
	
	
next_j:
	mul t6, t0, t2
	slli a3, t3, 2
	add t6, t6, a3
	add t6, t6, a2
	sw t4, 0(t6)
	addi t3, t3, 1
	beqz t4, got
	j loopj

got:
	li a6, 0
	j loopj

next_i:
	addi t2, t2, 1
	j loopi

finish:
	mv a0, a6
	ret		



.globl main
main:
	addi sp, sp, -128
	sw ra, 0(sp)
	sw s0, 4(sp)
	sw a0, 8(sp)
	sw a1, 12(sp)
	sw a2, 16(sp)
	addi s0, sp, 128
	li a0, 4
	sw a0, -72(s0)
	li a0, 2
	sw a0, -68(s0)
	li a0, 6
	sw a0, -64(s0)
	li a0, 1
	sw a0, -60(s0)
	li a0, 4
	sw a0, -56(s0)
	li a0, 2
	sw a0, -52(s0)
	li a0, 0
	sw a0, -48(s0)
	li a0, 0
	sw a0, -44(s0)
	li a0, 0
	sw a0, -40(s0)
	
	li a0, 5
	sw a0, -36(s0)
	li a0, 7
	sw a0, -32(s0)
	li a0, 1
	sw a0, -28(s0)
	li a0, 3
	sw a0, -24(s0)
	li a0, 6
	sw a0, -20(s0)
	li a0, 8
	sw a0, -16(s0)
	li a0, 1
	sw a0, -12(s0)
	li a0, 3
	sw a0, -8(s0)
	li a0, 2
	sw a0, -4(s0)
	
	addi a0, s0, -72
	addi a1, s0, -36
	addi a2, s0, -108
	
	jal matmul
	
	
	lw ra, 0(sp)
	lw s0, 4(sp)
	lw a0, 8(sp)
	lw a1, 12(sp)
	lw a2, 16(sp)
	addi sp, sp, 128
	
	
	
halt:
	j halt
