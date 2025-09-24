import argparse
import os
import sys
sys.path.insert(0, '../components')
from ALU import *
from ControlUnit import *
from ImmGen import *
from NextPc import *
from PC import *
from RAM import *
from RegisterFile import *
from IFID import *
from IDEX import *
from EXMEM import *
from MEMWB import *
from ForwardingUnit import *
from Hazards import *



class Processor:


    class ClockEvent:
        cycles = 1
        #IF stage
        @classmethod
        def fetch(cls):
            PC.next_pc()
            RAM.InstructionMemory.address = PC.pc
            
            RAM.InstructionMemory.fetch()
            IFID.inst = RAM.InstructionMemory.inst
            IFID.pc = PC.pc
            IFID.pc_curr = PC.pc
            

        # Decode stage
        @classmethod
        def Decode(cls):
            if Hazards.IF_Flush == 1:
                IFID.pc = "0"*8
                IFID.inst = "0"*32
                IFID.pc_curr = "0"*8
            Hazards.memread = IDEX.MemRead
            Hazards.rd = IDEX.rd
            Hazards.inst = IFID.inst
            Hazards.loaduse()
            if Hazards.PCWrite == 1:
                PC.pc = hex(int(PC.pc,16) - 4)[2:].zfill(8)
                Hazards.PCWrite = 0
            #Hazard detection unit
            if Hazards.IF_Flush == 1:
                IFID.pc = "0"*8
                IFID.inst = "0"*32
                IFID.pc_curr = "0"*8
            
            

            IDEX.pc_curr = IFID.pc_curr
            IDEX.pc = IFID.pc
            ControlUnit.inst = IFID.inst
            ControlUnit.generatesignal()
            IDEX.RegWrite = ControlUnit.RegWrite
            IDEX.MemtoReg = ControlUnit.MemtoReg
            IDEX.Branch = ControlUnit.branch
            IDEX.MemWrite = ControlUnit.MemWrite
            IDEX.MemRead = ControlUnit.MemRead
            IDEX.ALUop = ControlUnit.ALUop
            IDEX.ALUsrc = ControlUnit.ALUSrc

            
            RegisterFile.rs1 = int(IFID.inst[-20:-15],2)
            RegisterFile.rs2 = int(IFID.inst[-25:-20],2)
            RegisterFile.readrs1()
            RegisterFile.readrs2()
            IDEX.rs1v = RegisterFile.rs1v
            IDEX.rs2v = RegisterFile.rs2v
            IDEX.rd = int(IFID.inst[-12:-7], 2)
            IDEX.rs1 = RegisterFile.rs1
            IDEX.rs2 = RegisterFile.rs2
            IDEX.inst = IFID.inst

            ImmGen.instruction = IFID.inst
            ImmGen.generate()
            IDEX.imm = ImmGen.imm

            
        

        #Execute
        @classmethod
        def execute(cls):
            if Hazards.ID_Flush == 1:
                IDEX.RegWrite = 0
                IDEX.MemtoReg = 0
                IDEX.MemWrite = 0
                IDEX.Branch = 0
                IDEX.ALUop = "NOP"
                IDEX.ALUsrc = 0
                IDEX.pc = "0"*8
                IDEX.rs1v = 0
                IDEX.rs2v = 0
                IDEX.imm = 0
                IDEX.rd = 0
                IDEX.rs1 = 0
                IDEX.rs2 = 0
                IDEX.inst = "0"*32
                IDEX.pc_curr = "0"*8

            EXMEM.pc_curr = IDEX.pc_curr
            EXMEM.RegWrite = IDEX.RegWrite
            EXMEM.MemtoReg = IDEX.MemtoReg
            EXMEM.MemRead = IDEX.MemRead
            EXMEM.MemWrite = IDEX.MemWrite
            EXMEM.branch = IDEX.Branch
            EXMEM.inst = IDEX.inst
            EXMEM.pc = IDEX.pc
            EXMEM.imm = IDEX.imm
            
            

            if ForwardingUnit.forwardA == 2:
                ALU.op1 = EXMEM.alu_result
            elif ForwardingUnit.forwardA == 1:
                ALU.op1 = RegisterFile.rd_val
            else:
                ALU.op1 = IDEX.rs1v


            if IDEX.ALUsrc == 1:
                ALU.op2 = IDEX.imm
            else:    
                if ForwardingUnit.forwardB == 2:
                    ALU.op2 = EXMEM.alu_result
                elif ForwardingUnit.forwardB == 1:
                    ALU.op2 = RegisterFile.rd_val
                else:
                    ALU.op2 = IDEX.rs2v
                

            ALU.pc = int(IDEX.pc,16)
            ALU.ALUop = IDEX.ALUop
            ALU.calculate()
            EXMEM.alu_result = ALU.alu_result
            EXMEM.zero = ALU.zero
            EXMEM.ALUop = ALU.ALUop
            NextPc.pc = IDEX.pc
            NextPc.imm = EXMEM.imm
            NextPc.calculate()
            EXMEM.NextPc = NextPc.nextpc
            
            EXMEM.rs2v = IDEX.rs2v
            EXMEM.rd = IDEX.rd
            EXMEM.rs1 = IDEX.rs1
            EXMEM.rs2 = IDEX.rs2

        
        #memeory
        @classmethod
        def memory(cls):
            ForwardingUnit.rs1 = IDEX.rs1
            ForwardingUnit.rs2 = IDEX.rs2
            ForwardingUnit.exmemsignal = EXMEM.RegWrite
            ForwardingUnit.memwbsignal = MEMWB.RegWrite
            ForwardingUnit.exmemrd = EXMEM.rd
            ForwardingUnit.memwbrd = MEMWB.rd
            ForwardingUnit.ForwardA()
            ForwardingUnit.ForwardB()
            
            MEMWB.pc_curr = EXMEM.pc_curr
            Hazards.branch = EXMEM.branch
            Hazards.zero = EXMEM.zero
            Hazards.branchinst()
            PC.pcwrite = Hazards.PCWrite
            PC.pcimm = EXMEM.NextPc
            EXMEM.pc = PC.pcimm
            
            MEMWB.RegWrite = EXMEM.RegWrite
            MEMWB.MemtoReg = EXMEM.MemtoReg

            RAM.DataMemory.address = EXMEM.alu_result
            RAM.DataMemory.write_data = EXMEM.rs2v
            RAM.DataMemory.mem_write = EXMEM.MemWrite
            RAM.DataMemory.mem_read = EXMEM.MemRead
            RAM.DataMemory.execute()
            MEMWB.read_data = RAM.DataMemory.read_data
            MEMWB.inst = EXMEM.inst
            MEMWB.rd = EXMEM.rd
            MEMWB.alu_result = EXMEM.alu_result
            MEMWB.ALUop = EXMEM.ALUop
            MEMWB.imm = EXMEM.imm
            MEMWB.nextpc = EXMEM.NextPc
            MEMWB.rs1 = EXMEM.rs1
            MEMWB.rs2 = EXMEM.rs2
            MEMWB.pc = EXMEM.pc

        #writeback
        @classmethod
        def writeback(cls):
            RegisterFile.rd = MEMWB.rd
            MEMWB.write_data = RAM.DataMemory.write_data
            RegisterFile.reg_write = MEMWB.RegWrite
            RegisterFile.rd_val = MEMWB.read_data if MEMWB.MemtoReg == 1 else MEMWB.alu_result
            RegisterFile.write_data()

            cls.print_output(MEMWB.pc_curr)

        @classmethod
        def print_output(cls,pc):
                global stalls
                opcode = MEMWB.inst[-7:]
                if opcode == "0110011" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, x{MEMWB.rs1}, x{MEMWB.rs2}\t => x{MEMWB.rd}={hex(RegisterFile.rd_val)}")
                elif opcode == "0010011" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, x{MEMWB.rs1}, 0x{hex(MEMWB.imm)[2:].zfill(8)}\t => x{MEMWB.rd}={hex(RegisterFile.rd_val)}")
                elif opcode == "0000011" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, {MEMWB.imm}(x{MEMWB.rs1})\t => x{MEMWB.rd}={hex(RegisterFile.rd_val)}" )
                elif opcode == "0100011" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, {MEMWB.imm}(x{MEMWB.rs1})\t => mem 0x{hex(MEMWB.alu_result)[2:].zfill(8)} = 0x{hex(int(RegisterFile.rd_val,2))[2:].zfill(8)}")
                elif opcode == "1100011" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rs1}, x{MEMWB.rs2} , 0x{MEMWB.nextpc}")
                elif opcode == "1101111" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, 0x{hex(MEMWB.imm)[2:].zfill(8)}\t => pc = {MEMWB.nextpc}")
                elif opcode == "1100111" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, 0x{hex(MEMWB.imm)[2:].zfill(8)}\t => pc = {MEMWB.nextpc}")
                elif opcode == "0110111" or opcode == "0010111" :
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, 0x{hex(MEMWB.imm)[2:].zfill(8)}\t => x{MEMWB.rd}= {hex(RegisterFile.rd_val)}")
                else:
                    print(f"{cls.cycles}:\t0x{pc}:\t0x{hex(int(MEMWB.inst,2))[2:].zfill(8)}:\t{MEMWB.ALUop} x{MEMWB.rd}, x{MEMWB.rs1}, x{MEMWB.rs2}")
                    stalls += 1
                cls.cycles = cls.cycles + 1

        @classmethod
        def pipelines(cls):
            cls.writeback()
            cls.memory()
            cls.execute()
            cls.Decode()
            cls.fetch()



    @classmethod
    def binary_text(cls,file_path1):
        bin_text = []
        with open(file_path1, 'rb') as f:
            byte = f.read(4)
            while byte:
                bytestr1 = format(int.from_bytes(byte, byteorder='little'), '032b')
                bin_text.append(bytestr1)
                byte = f.read(4)
        RAM.InstructionMemory.inst_memory = bin_text

    @classmethod
    def binary_data(cls,file_path2):
        bin_data = []
        with open(file_path2, 'rb') as f:
            byte = f.read(4)
            while byte:
                bytestr2 = format(int.from_bytes(byte, byteorder='little'), '032b')
                bin_data.append(bytestr2)
                byte = f.read(4)
        RAM.DataMemory.data_memory = bin_data


    @classmethod
    def main(cls):
        global stalls
        parser = argparse.ArgumentParser(description="Process binary files.")
        parser.add_argument("file_name", help="Name of the binary file (without path)")
        parser.add_argument("--start", type=str, default="0x80000000", 
                            help="The address of the first instruction (default: 0x80000000)")
        parser.add_argument("--num_insts", type=int, default=1000000,
                            help="Number of instructions to simulate (default: 1000000)")
        parser.add_argument("--stats", type=str, default="run.stats", 
                        help="Name and location of the statistics file (default: run.stats)")
    
        args = parser.parse_args()
        
        base_path = '/home/152402013/cs3160/pr5/programs/bins/'
        text_file_path = os.path.join(base_path, f"{args.file_name}.text.bin")
        data_file_path = os.path.join(base_path, f"{args.file_name}.data.bin")
        
        RAM.InstructionMemory.start_address = args.start[2:]
        PC.pc = hex(int(args.start[2:],16) - 4)[2:]
        cls.binary_text(text_file_path)
        cls.binary_data(data_file_path)

        for i in range(args.num_insts):
            cls.ClockEvent.pipelines()

        #stats file

        total_cycles = args.num_insts  

        stats_file_path = os.path.abspath(args.stats)
        command_used = f"python3 {' '.join(sys.argv)}"  
        with open(stats_file_path, 'w') as stats_file:
            stats_file.write(f"{command_used}\n\n")  
            stats_file.write(f"Total cycles: {total_cycles}\n")
            stats_file.write(f"Total instructions: {total_cycles-stalls}\n")
    
        print(f"Statistics written to {stats_file_path}")
    
global stalls
stalls = 0
if __name__ == "__main__":
    Processor.main()