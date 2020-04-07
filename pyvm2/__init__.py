from typing import List, Dict
import time

from .helpers import *

# from instructions import * 


from .PyVMRegisters import PyVMRegisters

import importlib

class PyVM():
    """
    Python based virtual machine

    all of this is made up and the points don't matter. 

    think of it like a set of dominoes; once you set iem over, it's a loem over, it's a long flowing chain-reaction. 

    """
    importlib.import_module('.instructions', 'pyvm2')
    # print(__name__)
    # exit()
    # from .instructions import  mov, hlt, sig
    # this should bring all of the cpu instructions into the PyVM class namespace. right? I should have to preface all of the function calls with 'self.'

    DEBUG = True
    SPEED = 1
    memory = []
    registers = {}
    
    print('outer', id(memory)) # see  id(PyVM.memory))


    # I don't know how this works just yet... we'll figure it out.; It should be a list of all the supported instructions by the cpu

    # all of the instructions are 2 or less parameters. . 


 

    register_addresses = {
            # realmem , val
        'PC': 0x0, # program counter; incremented at each instruction.
            # PC gets 2 register (0x0 and 0x1) slots for counting up to 65535

        'IP': 0x2, # instruction pointer; where the NEXT instruction is located in memory

            # IP gets two slots (0x2 and 0x3) so it can address up to 65535 addresses in the ram

        'LI': 0x4, # last instruction pointer
        
        'JF': 0x5, # did the last instruction trigger a jump? 1 if so. 
        'TF': 0x6, # test flag; the result of CMP instruction is stored here. 
        'HF': 0x7, # halt flag; stop all processing. set to value > 0

        'R1': 0x8, # general purpose
        'R2': 0x9,
        'R3': 0xa,
        'R4': 0xb, # this is the target for the sig 13 function (print to screen)

    # bottom 16 units of memory are reserved for registers 

    }



    def __init__(self, ram_size=1024, debug=True, speed=1):
        # This is the 'RAM' where our program will live
        self.DEBUG = debug
        self.SPEED = speed
        self.RAM_SIZE = ram_size
        
        # def memory_init(self):
        #this needs to be a function. 
        self.memory_init(ram_size)

        self.instructions = {
        'mov': (0x01, self.mov, 'where', 'what'), # instruction name is the key and a tuple of a hanself.dle to the functions and placeholders the parameters they requireself.
        'jmp': (0x02, self.jmp, 'where'),
        'jif': (0x03, self.jif, 'where'),
        'ret': (0x04, self.ret, 'where'),
        'cmp': (0x05, self.cmp, 'this', 'that'),
        'inc': (0x06, self.inc, 'where'),
        'dec': (0x07, self.dec, 'where'),
        'mul': (0x08, self.mul, 'where', 'by'),
        'div': (0x09, self.div, 'where', 'by'),
        'inc': (0x0a, self.inc, 'where'),
        'sig': (0x0b, self.sig, 'signum'),
        'lds': (0x0c, self.lds, 'a_string'),
        'hlt': (0x99, self.hlt) 
    }


        # memory can be a dict; keys just have to be unique. 
        # almost like accessing a list mem[0] will access the value associated with key 0

        # mem['r1'] will get/set that value too. 

        # you lose relative indexing and slices. e.g. mem[idx+2]

   

        # Special registers are special; They instruct the cpu on what to do or inform it of the result of the last operation

        # General Purpose registers (Rx) are like short-term memory; you can assign stuff to them.

        # Maybe we can make our life simpler by pointing them to the first N memory slots?


        # self.registers = PyVMRegisters(self)
        # self.registers.update({
        self.memory.update({
            # realmem , val
            'PC': 0, # program counter; incremented at each instruction.
                # PC gets 2 register (0x0 and 0x1) slots for counting up to 65535
                # no longer true... just lie about the max for registers
            'IP': 0, # instruction pointer; where the NEXT instruction is located in memory

                # IP gets two slots (0x2 and 0x3) so it can address up to 65535 addresses in the ram
                # no longer true... just lie about the max for registers

            'LI': 0, # last instruction pointer
            
            'JF': 0, # did the last instruction trigger a jump? 1 if so. 
            'TF': 0, # test flag; the result of CMP instruction is stored here. 
            'HF': 0, # halt flag; stop all processing. set to value > 0 to stop the program

            'R1': 0, # general purpose
            'R2': 0,
            'R3': 0,
            'R4': 0, # this is the target for the sig 13 function (print to screen)

        # bottom 16 units of memory are reserved for registers 

        }) 

        # we need to provide a way to render to the screen. 
        # via "in
        # I don't know how this works just yet... we'll figure it out.; It should be a list of all the supported instructions by the cpu

        # all of the instructions are 2 or less parameters. . 


        ### TODO remove this code

        self.memory[0x10] = 0x00 # mov
        self.memory[0x11] = 0x20 # mem index i32
        self.memory[0x12] = 0x41 # ascii A
        self.memory[0x13] = 0x0b # sig
        self.memory[0x14] = 0x0c # sig #13 # pulls from R4? or self.memory[0x05]
        self.memory[0x15] = 0x99 # hlt

    def memory_init(self, ram_size):
        # self.memory = [0 for _ in range(ram_size)]

        # TODO let's convert this to a dict

        self.memory = {idx:None for idx in range(ram_size)}

    # def thaw_registers(self):
    #     # print(type(self.registers.values()))
    #     print("thaw", self.registers.items())
    #     for k, v in self.registers.items():
    #         self.registers[k] = self.memory[v]

    # def freeze_registers(self):
    #     print("freeze", self.register_addresses.items())
    #     for k, v in self.register_addresses.items():
    #         self.memory[v] = self.registers[k]

    # def modreg(self, reg, val):
    #     target = self.register_addresses[reg]

    #     self.memory[target] = val
   
    def mov(self, where, what):
        """places the value of what in memory[where]"""
        if self.debug:
            print('mov instruction:', where, what)
        
        self.registers['PC'] += 1
        where = int(where)
        self.memory[where] = int(what)
        

    def jmp(self, where):
        """ sets IP to where"""
        pass

    def jif(self, where):
        """jump if TF is 1"""
        pass

    def ret(self, where):
        """set IP to where"""
        pass

    def cmp(self, this, that):
        """compare this to that; sets TF to 1 if they equal; something else if they aren't """
        pass

    def inc(self, where):
        """INCrement the value at where by 1"""
        pass

    def dec(self, where):
        """DECrement the value at where by 1"""
        pass

    def mul(self, where, by):
        """multiply the value at where x by and store in where integers only please"""
        pass

    def div(self, where, by):
        """div the value at where / by and store in where ; integers only please"""
        pass

    def sig(self, signum):
        """SIG as in SIGNAL; this is how we signal that an action should occur; such as print to the screen
        valid signals

        13 = print on to screen

        
        # much, much later. 
        26 = open a file? 
        27 = write a byte to a file handle?
        
        90 = open a socket?
        91 = write to a socket handle
        92 = read from a socket handle. 
        """

        if signum == 13: # print 
            print('printing something')
            print(self.registers['R4'])
        pass

    def lds(self, where, a_string):
        """put a_string at where followed by a 0x00 byte"""

        pass

    def hlt(self):
        """Halt the VM and stop all processing"""
        self.memory['HF'] = 0

    def dumpmem(self):
        print("dumping allocated memory")
        used_mem = {k:v for (k,v) in self.memory.items() if v != None and not isinstance(k,str)}

        for k,v in used_mem.items():
            print(f"\taddress {k:#0{4}x} : {v}")


    def dumpmemrange(self,start=0, end=0):
        print("dumping memory range")
        if end == 0:
            end = self.RAM_SIZE
 
        for i in range(start, end):
            print(f"\taddress {i:4x} : {self.memory[i]}")


    def dumpreg(self):
        print("dumping registers")
        regs = {k: v for k, v in self.memory.items() if isinstance(k, str)} # select all of the keys that are strings (not a memory address)

        for k,v in regs.items():
            print('\tregister',k, '=', v)

    def compile(self, assembly_src):
        """this is the thing that makes the stuff"""
        compiled = []
        #come up with a better tokenizer. 
        for line in assembly_src.split('\n'):
            if self.DEBUG:
                print('Compiling', line)

            cmds = line.split(' ')
            for cmd in cmds: 
                self.intstructions
            compiled.append()

        pass
    



    def run(self, compiled_code):
        """this is the thing that does the stuff"""
        # while self.registers.get('HF') == 0 : # see conversion to dictionary
        self.memory['IP'] = 0x10 # memory address 0 is the entrypoint and the location of the next instruction.

        while self.memory.get('HF') == 0 :
            
            ### TODO fix this idea. there is a better way. 
            # self.thaw_registers() # I need a moment of clarity on this... this is too much of a hack... 

            self.memory['PC'] += 1

            # get instruction from memory
            print('')
            opcode = self.memory[self.memory['IP']]
            cmd_lens = [len(x) - 2 for x in self.instructions.values()]
            print(cmd_lens)
            print(f'{opcode=}')

            
            # do the instruction ; make sure 'self' is the first parameter

            self.memory['IP'] += 1

            if self.DEBUG:
                self.dumpreg()
                # self.dumpmem()
                # self.dumpmemrange(start=0, end=255)


            ### 
            time.sleep(1 * self.SPEED)


        print("CPU Halted")
        if self.DEBUG:
            self.dumpreg()
            self.dumpmem()
            # self.dumpmemrange(start=0, end=255)