class PC:
    pc = "0"*8
    pcwrite = 0
    pcimm = "0"*8
    @classmethod
    def next_pc(cls):
        if cls.pcwrite == 0:
            cls.pc = hex(int(cls.pc,16) + 4)[2:].zfill(8)
        else:
            cls.pc = cls.pcimm
