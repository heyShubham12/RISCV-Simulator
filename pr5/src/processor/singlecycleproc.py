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

class Processor:
    cycles = 1
    @classmethod
    def print_output(cls):
            opcode = RAM.InstructionMemory.inst[-7:]
            if opcode == "0110011" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, x{RegisterFile.rs1}, x{RegisterFile.rs2}")
            elif opcode == "0010011" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, x{RegisterFile.rs1}, 0x{hex(ImmGen.imm)[2:].zfill(8)}\t => x{RegisterFile.rd}={hex(RegisterFile.rd_val)}")
            elif opcode == "0000011" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, {ImmGen.imm}(x{RegisterFile.rs1})\t => x{RegisterFile.rd}={hex(RegisterFile.rd_val)}" )
            elif opcode == "0100011" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, {ImmGen.imm}(x{RegisterFile.rs1})\t => mem 0x{hex(ALU.alu_result)[2:].zfill(8)} = 0x{hex(int(RAM.DataMemory.write_data,2))[2:].zfill(8)}")
            elif opcode == "1100011" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rs1}, x{RegisterFile.rs2} , 0x{hex(int(PC.pc,16) + ImmGen.imm)[2:].zfill(8)}\t => pc = {NextPc.nextpc}")
            elif opcode == "1101111" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, 0x{hex(ImmGen.imm)[2:].zfill(8)}\t => pc = {NextPc.nextpc}")
            elif opcode == "1100111" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, 0x{hex(ImmGen.imm)[2:].zfill(8)}\t => pc = {NextPc.nextpc}")
            elif opcode == "0110111" or opcode == "0010111" :
                print(f"{cls.cycles}\t0x{PC.pc}\t0x{hex(int(RAM.InstructionMemory.inst,2))[2:].zfill(8)}\t{ALU.ALUop} x{RegisterFile.rd}, 0x{hex(ImmGen.imm)[2:].zfill(8)}\t => x{RegisterFile.rd}= {hex(RegisterFile.rd_val)}")
           
            cls.cycles = cls.cycles + 1
    @classmethod
    def clock_event(cls):
        RAM.InstructionMemory.address = PC.pc
        RAM.InstructionMemory.fetch()
        ControlUnit.inst = RAM.InstructionMemory.inst
        RegisterFile.rs1 = int(RAM.InstructionMemory.inst[-20:-15],2)
        RegisterFile.rs2 = int(RAM.InstructionMemory.inst[-25:-20],2)
        RegisterFile.rd = int(RAM.InstructionMemory.inst[-12:-7],2)
        ControlUnit.generatesignal()
        RegisterFile.reg_write = ControlUnit.RegWrite
        ImmGen.instruction = RAM.InstructionMemory.inst
        ImmGen.generate()
        RegisterFile.readrs1()
        RegisterFile.readrs2()
        ALU.op1 = RegisterFile.rs1v
        ALU.op2 = ImmGen.imm if ControlUnit.ALUSrc == 1 else RegisterFile.rs2v
        ALU.pc = int(PC.pc,16)
        ALU.ALUop = ControlUnit.ALUop
        ALU.calculate()
        NextPc.pc = PC.pc
        NextPc.imm = ImmGen.imm
        NextPc.branch = ControlUnit.branch
        NextPc.zero = ALU.zero
        NextPc.calculate()
        RAM.DataMemory.address = ALU.alu_result
        RAM.DataMemory.write_data = RegisterFile.rs2v
        RAM.DataMemory.mem_write = ControlUnit.MemWrite
        RAM.DataMemory.mem_read = ControlUnit.MemRead
        RAM.DataMemory.execute()
        RegisterFile.rd_val = RAM.DataMemory.read_data if ControlUnit.MemtoReg == 1 else ALU.alu_result
        RegisterFile.write_data()
        cls.print_output()
    
        PC.pc = NextPc.nextpc

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
        parser = argparse.ArgumentParser(description="Process binary files.")
        parser.add_argument("file_name", help="Name of the binary file (without path)")
        parser.add_argument("--start", type=str, default="0x80000000", 
                            help="The address of the first instruction (default: 0x80000000)")
        parser.add_argument("--num_insts", type=int, default=1000000,
                            help="Number of instructions to simulate (default: 1000000)")
        
        args = parser.parse_args()
        
        base_path = '/home/152402013/cs3160/pr5/programs/bins/'
        text_file_path = os.path.join(base_path, f"{args.file_name}.text.bin")
        data_file_path = os.path.join(base_path, f"{args.file_name}.data.bin")
        
        # Convert start address from string to integer
        PC.pc = args.start[2:]
        RAM.InstructionMemory.start_address = PC.pc
        Processor.binary_text(text_file_path)
        Processor.binary_data(data_file_path)
        for i in range(args.num_insts):
            Processor.clock_event()


if __name__ == "__main__":
    Processor.main()