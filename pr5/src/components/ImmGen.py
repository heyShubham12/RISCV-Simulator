class ImmGen:
    #input

    instruction = "0"*32

    #output

    imm = "0"*32

    @classmethod
    def twos_complement_to_int(cls,binary_str):
        n = len(binary_str)  # Number of bits
        value = int(binary_str, 2)  # Interpret as unsigned integer

        # Check if the value is negative in two's complement
        if (value & (1 << (n - 1))) != 0:
            value -= (1 << n)  # Adjust for two's complement negative value

        return value


    @classmethod
    def generate(cls):
        opcode = cls.instruction[-7:]
        if(opcode in ["0010011","0000011","1100111","1110011"]):
            cls.imm = cls.instruction[-32:-20]

        elif(opcode == "0100011"):
            cls.imm = cls.instruction[-32:-25] + cls.instruction[-12:-7]

        elif(opcode == "1100011"):
            cls.imm = cls.instruction[-32:-31] + cls.instruction[-8:-7] + cls.instruction[-31:-25] + cls.instruction[-12:-8] + "0"

        elif(opcode == "1101111"):
            cls.imm = cls.instruction[-32:-31] + cls.instruction[-20:-12] + cls.instruction[-21:-20] + cls.instruction[-31:-21] + "0"
        
        else:
            cls.imm = "0"*32
        cls.imm = cls.twos_complement_to_int(cls.imm)

        if(opcode in ["0110111","0010111"]):
            cls.imm = cls.instruction[-32:-12] + "0"*12
            cls.imm = int(cls.imm,2)
        
        
