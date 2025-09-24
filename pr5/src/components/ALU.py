class ALU:
    #input
    op1 = 0
    op2 = 0
    ALUop = "NOP"
    pc = 0
    #output
    zero = 0
    alu_result = 0
    
    @classmethod
    def calculate(cls):
        cls.zero = 0
        if(cls.ALUop == "ADD"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "SUB"):
            cls.alu_result = cls.op1 - cls.op2
        elif(cls.ALUop == "XOR"):
            cls.alu_result = cls.op1 ^ cls.op2
        elif(cls.ALUop == "OR"):
            cls.alu_result = cls.op1 | cls.op2
        elif(cls.ALUop == "AND"):
            cls.alu_result = cls.op1 & cls.op2
        elif(cls.ALUop == "SLL"):
            cls.alu_result = cls.op1 << cls.op2
        elif(cls.ALUop == "SRL"):
            cls.alu_result = cls.op1 >> cls.op2
        elif(cls.ALUop == "SRA"):
            cls.alu_result = cls.op1 >> cls.op2
        elif(cls.ALUop == "SLT"):
            cls.alu_result = 1 if (cls.op1 < cls.op2) else 0
        elif(cls.ALUop == "SLTU"):
            cls.alu_result = 1 if (cls.op1 < cls.op2) else 0

    

        elif(cls.ALUop == "ADDI"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "XORI"):
            cls.alu_result = cls.op1 ^ cls.op2
        elif(cls.ALUop == "ORI"):
            cls.alu_result = cls.op1 | cls.op2
        elif(cls.ALUop == "ANDI"):
            cls.alu_result = cls.op1 & cls.op2
        elif(cls.ALUop == "SLLI"):
            cls.alu_result = cls.op1 << (cls.op2 & 31)
        elif(cls.ALUop == "SRLI"):
            cls.alu_result = cls.op1 >> (cls.op2 & 31)
        elif(cls.ALUop == "SRAI"):
            cls.alu_result = cls.op1 >> (cls.op2 & 31)
        elif(cls.ALUop == "SLTI"):
            cls.alu_result = 1 if (cls.op1 < cls.op2) else 0
        elif(cls.ALUop == "SLTIU"):
            cls.alu_result = 1 if (cls.op1 < cls.op2) else 0



        elif(cls.ALUop == "LB"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "LH"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "LW"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "LBU"):
            cls.alu_result = cls.op1 + cls.op2
        elif(cls.ALUop == "LHU"):
            cls.alu_result = cls.op1 + cls.op2



        elif(cls.ALUop == "BEQ"):
            cls.zero = 1 if (cls.op1 == cls.op2) else 0
        elif(cls.ALUop == "BNE"):
            cls.zero = 1 if (cls.op1 != cls.op2) else 0
        elif(cls.ALUop == "BLT"):
            cls.zero = 1 if (cls.op1 < cls.op2) else 0
        elif(cls.ALUop == "BGE"):
            cls.zero = 1 if (cls.op1 >= cls.op2) else 0
        elif(cls.ALUop == "BLTU"):
            cls.zero = 1 if (cls.op1 < cls.op2) else 0
        elif(cls.ALUop == "BGEU"):
            cls.zero = 1 if (cls.op1 >= cls.op2) else 0



        elif(cls.ALUop == "JAL"):
            cls.alu_result = cls.pc+4
            cls.zero = 1

        elif(cls.ALUop == "JALR"):
            cls.alu_result = cls.pc+4
            cls.pc = cls.op1
            cls.zero = 1
        
        elif(cls.ALUop == "LUI"):
            cls.alu_result = cls.op2

        elif(cls.ALUop == "AUIPC"):
            cls.alu_result = cls.pc + cls.op2


        elif(cls.ALUop == "MUL"):
            cls.alu_result = cls.op1 * cls.op2
        elif(cls.ALUop == "MULH"):
            cls.alu_result = cls.op1 * cls.op2
        elif(cls.ALUop == "MULSU"):
            cls.alu_result = cls.op1 * cls.op2
        elif(cls.ALUop == "MULU"):
            cls.alu_result = cls.op1 * cls.op2
        elif(cls.ALUop == "DIV"):
            cls.alu_result = cls.op1 / cls.op2
        elif(cls.ALUop == "DIVU"):
            cls.alu_result = cls.op1 / cls.op2
        elif(cls.ALUop == "REM"):
            cls.alu_result = cls.op1 % cls.op2
        elif(cls.ALUop == "REMU"):
            cls.alu_result = cls.op1 % cls.op2

        
