class IDEX:
    RegWrite = 0
    MemtoReg = 0
    MemRead = 0
    MemWrite = 0
    HazardControl = 0
    Branch = 0
    ALUop = "NOP"
    ALUsrc = 0
    pc = "0"*8
    rs1v = 0
    rs2v = 0
    imm = 0
    rd = 0
    rs1 = 0
    rs2 = 0
    inst = "0"*32
    pc_curr = "0"*8

    