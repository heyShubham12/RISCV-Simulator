class ControlUnit:
    #input
    inst = "0"*32


    #output

    branch = 0
    MemRead = 0
    MemtoReg = 0
    ALUop = "NOP"
    MemWrite = 0
    ALUSrc = 0
    RegWrite = 0

    # To be checked

    @classmethod
    def generatesignal(cls):
        cls.ALUop = "NOP"
        cls.branch = 0
        cls.MemRead = 0
        cls.MemtoReg = 0
        cls.MemWrite = 0
        cls.ALUSrc = 0
        cls.RegWrite = 0
        opcode = cls.inst[-7:]
        funct3 = hex(int(cls.inst[-15:-12], 2))[2:].zfill(1)
        funct7 = hex(int(cls.inst[-32:-25], 2))[2:].zfill(2)

        #R-Type

        if(opcode=="0110011"):
            cls.branch = 0
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 0
            cls.RegWrite = 1
            if(funct3 == "0" and funct7 == "00"):
                cls.ALUop = "ADD"
            elif(funct3 == "0" and funct7 == "20"):
                cls.ALUop = "SUB"
            elif(funct3 == "4"):
                cls.ALUop = "XOR"
            elif(funct3 == "6" and funct7 == "00"):
                cls.ALUop = "OR"
            elif(funct3 == "7"):
                cls.ALUop = "AND"
            elif(funct3 == "1"):
                cls.ALUop = "SLL"
            elif(funct3 == "5" and funct7 == "00"):
                cls.ALUop = "SRL"
            elif(funct3 == "5" and funct7 == "20"):
                cls.ALUop = "SRA"
            elif(funct3 == "2"):
                cls.ALUop = "SLT"
            elif(funct3 == "3"):
                cls.ALUop = "SLTU"
            elif(funct3 == "0" and funct7 == "01"):
                cls.ALUop = "MUL"
            elif(funct3 == "1" and funct7 == "01"):
                cls.ALUop = "MULH"
            elif(funct3 == "2" and funct7 == "01"):
                cls.ALUop = "MULSU"
            elif(funct3 == "3" and funct7 == "01"):
                cls.ALUop = "MULU"
            elif(funct3 == "4" and funct7 == "01"):
                cls.ALUop = "DIV"
            elif(funct3 == "5" and funct7 == "01"):
                cls.ALUop = "DIVU"
            elif(funct3 == "6" and funct7 == "01"):
                cls.ALUop = "REM"
            elif(funct3 == "7" and funct7 == "01"):
                cls.ALUop = "REMU"

        #I-Type1

        elif(opcode == "0010011"):
            cls.branch = 0
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 1
            cls.RegWrite = 1
            if(funct3 == "0"):
                cls.ALUop = "ADDI"
            elif(funct3 == "4"):
                cls.ALUop = "XORI"
            elif(funct3 == "6"):
                cls.ALUop = "ORI"
            elif(funct3 == "7"):
                cls.ALUop = "ANDI"
            elif(funct3 == "1"):
                cls.ALUop = "SLLI"
            elif(funct3 == "5" and funct7 == "00"):
                cls.ALUop = "SRLI"
            elif(funct3 == "5" and funct7 == "20"):
                cls.ALUop = "SRAI"
            elif(funct3 == "2"):
                cls.ALUop = "SLTI"
            elif(funct3 == "3"):
                cls.ALUop = "SLTIU"

        #I-type2

            
        elif(opcode == "0000011"):
            cls.branch = 0
            cls.MemRead = 1
            cls.MemtoReg = 1
            cls.MemWrite = 0
            cls.ALUSrc = 1
            cls.RegWrite = 1
            if(funct3 == "0"):
                cls.ALUop = "LB"
            elif(funct3 == "1"):
                cls.ALUop = "LH"
            elif(funct3 == "2"):
                cls.ALUop = "LW"
            elif(funct3 == "4"):
                cls.ALUop = "LBU"
            elif(funct3 == "5"):
                cls.ALUop = "LHU"

        #S-Type

        elif(opcode == "0100011"):
            cls.branch = 0
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 1
            cls.ALUSrc = 1
            cls.RegWrite = 0
            if(funct3 == "0"):
                cls.ALUop = "SB"
            elif(funct3 == "1"):
                cls.ALUop = "SH"
            elif(funct3 == "2"):
                cls.ALUop = "SW"

        #B-Type

        elif(opcode == "1100011"):
            cls.branch = 1
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 0
            cls.RegWrite = 0
            if(funct3 == "0"):
                cls.ALUop = "BEQ"
            elif(funct3 == "1"):
                cls.ALUop = "BNE"
            elif(funct3 == "4"):
                cls.ALUop = "BLT"
            elif(funct3 == "5"):
                cls.ALUop = "BGE"
            elif(funct3 == "6"):
                cls.ALUop = "BLTU"
            elif(funct3 == "7"):
                cls.ALUop = "BGEU"

        #J-Type

        elif(opcode == "1101111"):
            cls.branch = 1
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 1
            cls.RegWrite = 0
            cls.ALUop = "JAL"

        #I-Type3

        elif(opcode == "1100111"):
            cls.branch = 1
            cls.MemRead = 1
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 1
            cls.RegWrite = 1
            if(funct3 == "0"):
                cls.ALUop = "JALR"

        #U-Type

        elif(opcode == "0110111"):
            cls.branch = 0
            cls.MemRead = 1
            cls.MemtoReg = 0
            cls.MemWrite = 1
            cls.ALUSrc = 1
            cls.RegWrite = 1
            cls.ALUop = "LUI"
            
        #U-type2

        elif(opcode == "0010111"):
            cls.branch = 0
            cls.MemRead = 0
            cls.MemtoReg = 0
            cls.MemWrite = 0
            cls.ALUSrc = 1
            cls.RegWrite = 1
            cls.ALUop = "AUIPC"
            


