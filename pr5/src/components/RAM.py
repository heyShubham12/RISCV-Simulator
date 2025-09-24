class RAM:
    class InstructionMemory:
        #input
        address = "0"*8
        #output
        inst = "0"*32

        start_address = "0"*8

        inst_memory = []
        
        @classmethod
        def fetch(cls):
            try:
                cls.inst = cls.inst_memory[(int(cls.address,16)-int(cls.start_address,16))//4]
            except:
                cls.inst = "0"*32
    
    


    class DataMemory:
        #input
        address = "0"*8
        write_data = 0
        mem_write = 0
        mem_read = 0


        #output
        read_data = 0

        data_memory = []

        @classmethod
        def twos_complement_to_int(cls,binary_str):
            n = len(binary_str)  # Number of bits
            value = int(binary_str, 2)  # Interpret as unsigned integer

            # Check if the value is negative in two's complement
            if (value & (1 << (n - 1))) != 0:
                value -= (1 << n)  # Adjust for two's complement negative value

            return value
    
        @classmethod
        def execute(cls):
            if cls.mem_read == 1:
                try:
                    cls.read_data = cls.twos_complement_to_int(cls.data_memory[(cls.address-int("80008000",16))//4])
                except:
                    cls.read_data = 0
            elif cls.mem_write == 1:
                try:
                    cls.data_memory[(cls.address-int("80008000",16))//4] = format(cls.write_data, "032b")
                except:
                    pass

