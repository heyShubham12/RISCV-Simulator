class RegisterFile:
    #input
    rs1 = 0
    rs2 = 0
    rd = 0
    rd_val = 0
    reg_write = 0

    #output
    
    rs1v = 0
    rs2v = 0

    reg_memory = [0]*32

    @classmethod
    def readrs1(cls):
        cls.rs1v = cls.reg_memory[cls.rs1]


    @classmethod 
    def readrs2(cls):
        cls.rs2v = cls.reg_memory[cls.rs2]

    @classmethod
    def write_data(cls):
        if cls.reg_write == 1 and cls.rd != 0:
            cls.reg_memory[cls.rd] = cls.rd_val