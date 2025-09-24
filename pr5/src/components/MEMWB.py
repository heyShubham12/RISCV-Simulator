class MEMWB:
    RegWrite = 0
    MemtoReg = 0
    read_data = "0"*32
    alu_result = 0
    rd = 0
    ForwardingUnit = 0
    rs1 = 0
    rs2 = 0
    inst = "0"*32
    ALUop = "NOP"
    imm = 0
    nextpc = 0
    pc = "0"*8
    write_data = 0
    pc_curr = "0"*8
    