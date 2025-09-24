class NextPc:
    #input

    pc = "0"*8
    imm = 0

    #output

    nextpc = "0"*8

    @classmethod
    def calculate(cls):
        cls.nextpc = hex(int(cls.pc,16) + int(cls.imm))[2:].zfill(8)
        