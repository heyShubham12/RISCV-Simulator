class ForwardingUnit:
    memwbrd = "0"*5
    exmemrd = "0"*5
    rs1 = "0"*5
    rs2 = "0"*5
    exmemsignal = 0
    memwbsignal = 0
    forwardA = 0
    forwardB = 0

    @classmethod
    def ForwardA(cls):
        if cls.exmemrd != 0 and cls.rs1 == cls.exmemrd and cls.exmemsignal == 1:
            cls.forwardA = 2
        elif cls.memwbrd !=0 and cls.rs1 == cls.memwbrd and cls.memwbsignal == 1:
            cls.forwardA = 1
        else:
            cls.forwardA = 0
    @classmethod        
    def ForwardB(cls):
        if cls.exmemrd != 0 and cls.rs2 == cls.exmemrd and cls.exmemsignal == 1:
            cls.forwardB = 2
        elif cls.memwbrd !=0 and cls.rs2 == cls.memwbrd and cls.memwbsignal == 1:
            cls.forwardB = 1
        else:
            cls.forwardB = 0
