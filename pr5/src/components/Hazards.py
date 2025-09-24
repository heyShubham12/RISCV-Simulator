class Hazards:
    memread = 0
    rd = "0"*5
    inst = "0"*32
    rs1 = "0"*5
    rs2 = "0"*5
    IF_Flush = 0
    PCWrite = 0
    branch = 0
    zero = 0
    ID_Flush = 0
    pc = "0"*8
    imm = 0
    @classmethod
    def loaduse(cls):
        cls.rs1 = int(cls.inst[-20:-15], 2)
        cls.rs2 = int(cls.inst[-25:-20], 2)
        cls.IF_Flush = 0
        cls.PCWrite = 0
        if cls.memread == 1:

            if cls.rd != 0 and cls.rs1 == cls.rd or cls.rs2 == cls.rd:
                cls.IF_Flush = 1
                cls.PCWrite = 1
    @classmethod
    def branchinst(cls):
        if cls.branch == 1 and cls.zero == 1:
            cls.PCWrite = 1
            cls.IF_Flush = 1
            cls.ID_Flush = 1
        else:
            cls.PCWrite = 0
            cls.IF_Flush = 0
            cls.ID_Flush = 0

        
        

    
    