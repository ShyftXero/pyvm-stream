from typing import List, Dict
import time

from colored import fg, bg, attr
import shlex # https://docs.python.org/3/library/shlex.html

from .helpers import *

# from instructions import * 


# from .PyVMRegisters import PyVMRegisters

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
    
    

 
    # REMOVE - No londer required; registers are part of the memory dict; not true... for compiling I need to be able to assign a predictable spot
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

        'RC': 0xa, # general purpose
        'RB': 0xb,
        'RC': 0xc,
        'RD': 0xd, # this is the target for the sig 13 function (print to screen)
    }
    # # bottom 16 units of memory are reserved for registers 

    # }
    # REMOVE - No londer required; registers are part of the memory dict


    def __init__(self, ram_size=1024, debug=True, speed=1):
        # This is the 'RAM' where our program will live
        self.DEBUG = debug
        self.SPEED = speed
        self.RAM_SIZE = ram_size
        
        # def memory_init(self):
        #this needs to be a function. 
        self.memory_init(ram_size)


        # using the opcodes as the key
        self.instructions = {
            0x01: (self.mov, 'where', 'what'), # instruction name is the key and a tuple of a hanself.dle to the functions and placeholders the parameters they requireself.
            0x02: (self.jmp, 'where'),
            0x03: (self.jif, 'where'),
            0x04: (self.ret, 'where'),
            0x05: (self.cmp, 'this', 'that'),
            0x06: (self.inc, 'where', 'by'),
            0x07: (self.dec, 'where', 'by '),
            0x08: (self.mul, 'where', 'by'),
            0x09: (self.div, 'where', 'by'),
            0x0a: (self.inc, 'where'),
            0x0b: (self.sig, 'signum'),
            0x0c: (self.lds, 'a_string'),
            0x11: (self.mr1, 'what'),
            0x12: (self.mr2, 'what'),
            0x13: (self.mr3, 'what'),
            0x14: (self.mr4, 'what'),
            0x21: (self.cr1, 'what'),
            0x22: (self.cr2, 'what'),
            0x23: (self.cr3, 'what'),
            0x24: (self.cr4, 'what'),
            0x31: (self.ir1, 'by'),
            0x99: (self.hlt, 'nullbyte'),

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
        if self.DEBUG:
            print(f'mov instruction: 0x{where:04x} 0x{what:02x}')
        
        # self.memory['PC'] += 1
        
    
        where = int(where)
        self.memory[where] = int(what)
        self.memory['IP'] += 3 

    # is this required?
    def mr1(self, what):
        self.memory['R1'] = int(what)
        self.memory['IP'] += 2

    def mr2(self, what):
        self.memory['R2'] = int(what)
        self.memory['IP'] += 2

    def mr3(self, what):
        self.memory['R3'] = int(what)
        self.memory['IP'] += 2
        
    def mr4(self, what):
        self.memory['R4'] = int(what)
        self.memory['IP'] += 2
        

    def jmp(self, where):
        """ sets IP to where"""
        where = int(where)
        self.memory['IP'] = int(where)

    def jif(self, where):
        """jump if TF is 1"""
        if self.memory['TF'] == 1:
            if self.DEBUG:
                print('Test Flag is set is jumping')
            where = int(where)
            self.memory['IP'] = int(where)
        else:
            if self.DEBUG:
                print("Test Flag is not set so not jumping")
            self.memory['IP'] += 1
        

    def ret(self, where):
        """set IP to where"""
        if self.DEBUG:
            print('Test Flag is set is jumping')
        where = int(where)
        self.memory['IP'] = int(where)
    

    def cmp(self, this, that):
        """compare this to that; sets TF to 1 if they equal; something else if they aren't """
        if self.memory[this] == self.memory[that]:
            if self.DEBUG:
                print(f"cmp: the are equal")
            self.memory['TF'] = 1
        else:
            if self.DEBUG:
                print('cmp: they are not equal')
            self.memory['TF'] = 0

        self.memory['IP'] += 1

    def inc(self, where, by):
        """INCrement the value at where by somevalue"""
        if self.DEBUG:
            print(f"incrementing value at memory 0x{where:04x} by {by}; currently {self.memory[where]}")
        
        self.memory[where] += int(by)
        if self.DEBUG:
            print(f'value at memory 0x{where:04x} is now {self.memory[where]}')


        self.memory['IP'] += 1

    def dec(self, where, by):
        """DECrement the value at where by some value"""
        if self.DEBUG:
            print(f"decrementing value at memory 0x{where:04x} by {by}; currently {self.memory[where]}")
        
        self.memory[where] -= int(by)
        if self.DEBUG:
            print(f'value at memory 0x{where:04x} is now {self.memory[where]}')

        self.memory['IP'] += 1
        
        

    def mul(self, where, by):
        """multiply the value at where x by and store in where integers only please"""
        if self.DEBUG:
            print(f"incrementing {where:0#x}")
        
        by = int(by)
        where = int(where)

        self.memory[where] = self.memory[where] * by

        self.memory['IP'] += 2
        

    def div(self, where, by):
        """div the value at where / by and store in where ; integers only please"""
        by = int(by)
        where = int(where)
        # integer division
        self.memory[where] = self.memory[where] // by 
        self.memory['IP'] += 2

    def sig(self, signum):
        """SIG as in SIGNAL; this is how we signal that an action should occur; such as print to the screen
        valid signals
        Register R4 is very important 

        0x0d = print char at address located in r4 on to screen; putchar
        0x0e = print char at address located in r4 on to screen, incrementing address until address contains a null byte; putstring
        0x0f = print char at address located in r4 on to screen, decrementing address until address contains a null byte; putstring but reversed

        # much, much later. 
        26 = open a file? 
        27 = write a byte to a file handle?
        
        90 = open a socket?
        91 = write to a socket handle
        92 = read from a socket handle. 
        """
     
        if signum == 0x0d: # putchar 
            # print('printing something')
            if self.DEBUG:
                print(f"printing char at address in R4 :{self.memory['R4']:#04x} value: {self.memory[self.memory['R4']]:c}", )
            print(f'{fg("green")}{chr(self.memory[self.memory["R4"]])}{attr("reset")}', end='')
        elif signum == 0x0e: # putstring until nullbyte; increasing
            if self.DEBUG:
                print(f"printing string starting at address in R4 :{self.memory['R4']:#04x} value: {self.memory[self.memory['R4']]:c}", )
            target = self.memory['R4']
            while self.memory[target] != 0x00:
                print(f'{fg("green")}{chr(self.memory[target])}{attr("reset")}', end='')
                target += 1
        elif signum == 0x0f: # putstring until nullbyte; decreasing (reversed strings)
            if self.DEBUG:
                print(f"printing string ending at address in R4 :{self.memory['R4']:#04x} value: {self.memory[self.memory['R4']]:c}", )
            target = self.memory['R4']
            while self.memory[target] != 0x00:
                print(f'{fg("green")}{chr(self.memory[target])}{attr("reset")}', end='')
                target -= 1
        else:
            print('unhandled signum', hex(signum))

        self.memory['IP'] += 2

    def lds(self, where, a_string):
        """put a_string at where followed by a 0x00 byte"""

        for char in a_string:
            self.mov(where, char)
            where += 1 
        self.memory[where+1] = 0x00 # null terminated string. 

        self.memory['IP'] = self.memory['ip'] + len(a_string) + 1 # plus 1 for the null byte at the end of the str 

    def hlt(self, nullbyte):
        """Halt the VM and stop all processing
        hlt requires a nullbyte; should be 0x99 then 0x00 in memory

        this is because of the way the instructions are handled in the self.instructions dict. 

        everything needs at least one parameter.
        """
        if self.DEBUG:
            print("CPU instructed to halt; setting HF to 1")
        self.memory['HF'] = 1

    def dumpmem(self):
        print("dumping allocated memory")
        used_mem = {k:v for (k,v) in self.memory.items() if v != None and not isinstance(k,str)}

        for k,v in used_mem.items():
            print(f"\taddress 0x{k:04x} : 0x{v:02x}")


    def dumpmemrange(self,start=0, end=0):
        print("dumping memory range")
        if end == 0:
            end = self.RAM_SIZE
 
        for i in range(start, end):
            print(f"\taddress 0x{i:4x} : {self.memory[i]}")


    def dumpreg(self):
        print("dumping registers")
        regs = {k: v for k, v in self.memory.items() if isinstance(k, str)} # select all of the keys that are strings (not a memory address)

        for k,v in regs.items():
            # print('\tregister',k, '=', v)
            print(f'\tregister {k} = 0x{v:02x}')

    def assemble(self, assembly_src):
        """this is the thing that makes the stuff"""
        compiled = []

        assembly_src = assembly_src.strip()# remove leading and trailing whitespace
        if self.DEBUG:
            print(f'Got src:\n{assembly_src}')
            print('-----')

        #come up with a better tokenizer. 
        for line in assembly_src.split('\n'):
            if line.startswith(';'):
                if self.DEBUG:
                    print('skipping comment: ', line)
                    
                continue 
            if self.DEBUG:
                print('Compiling line:', line)
            

            line = shlex.split(line)
            if self.DEBUG:
                print(f'{line=}')


            # TODO this huge if block might be the result of that moment of clarity referenced below. 

            if line[0].lower() == 'mov':
                if 'r' in line[1].lower():
                    #dealing with a register
                    # leverage mr1-4 functions
                    if line[1].lower() == 'r1':
                        compiled.append(0x11)
                    elif line[1].lower() == 'r2':
                        compiled.append(0x12)
                    elif line[1].lower() == 'r3':
                        compiled.append(0x13)
                    elif line[1].lower() == 'r4':
                        compiled.append(0x14)
                    # finally add what the register should be 
                    compiled.append(line[2])
                else:
                    #not a register so use the default mov func
                    compiled.append(int(line[1], 16))
                    compiled.append(int(line[2], 16))

                # assemble the rest of the code
            elif line[0].lower() == 'jmp':
                pass
            elif line[0].lower() == 'jif':
                pass
            elif line[0].lower() == 'ret':
                pass
            elif line[0].lower() == 'cmp':
                pass
            elif line[0].lower() == 'inc':
                pass
            elif line[0].lower() == 'dec':
                pass
            elif line[0].lower() == 'mul':
                pass
            elif line[0].lower() == 'div':
                pass
            elif line[0].lower() == 'sig':
                pass
            elif line[0].lower() == 'lds':
                pass
            elif line[0].lower() == 'hlt':
                # the developer may not have to add the null byte to the end in their sourcecode, because the compiler can add it here. 
                compiled.append(0x99)
                compiled.append(0x00)
                pass
            elif line[0].lower() == 'another_instruction':
                # some new feature
                pass
            else:
                print(f"unknown instruction: {line} ")
                exit()


            # # TODO I NEED A MOMENT OF CLARITY TO RESOLVE THIS ISSUE IN A MORE ELAGANT FASION... 

            # ###

            # for opcode, obj in self.instructions.items():
            #     if obj[0].__name__ == cmds[0]:   # search for the name of the function and if it is the same as the line being asked for add opcode. 
            #         compiled.append(opcode) # once found, add it
            #         # if len(cmds) >= 2: # func +  two params
            #         if 'R' in cmds[1].upper():    # dealing with a register?
            #             for k,v in self.register_addresses.items():
            #                 if cmds[1].upper() == k:
            #                     # not all register commands have two params... 
            #                     compiled.append(int(v, 16))
            #                     break
                            
            #         else:
            #             compiled.append(int(cmds[1], 16))
                    
            #         try:
            #             if cmds[2][0] in ['\'', '"']: # beginning of a string
            #                 for char in cmds[2][1:-1]:
            #                     compiled.append(ord(char))
            #                 compiled.append(0x00) # null byte for a string
            #             else:
            #                 compiled.append(int(cmds[2], 16))
            #         except IndexError:
            #             if self.DEBUG:
            #                 print('index error looking for cmd[2][0] in ', cmds)
            #         break # no need to continue this loop
                        
            # ###
            # #      

            if self.DEBUG:
                print([f'0x{x:02x}' for x in compiled])
                print('returning', compiled)
        
        return compiled
    

    def run(self, compiled_code):
        """this is the thing that does the stuff"""
        
        self.memory['IP'] = 0x10 # memory address 0x10 is the entrypoint and the location of the next instruction.

        entrypoint = 0x10
        for idx, data in enumerate(compiled_code):
            if self.DEBUG:
                print(f'loading 0x{data:02x} to memory 0x{entrypoint + idx:04x}')
            self.memory[entrypoint + idx] = data

        self.dumpreg()
        self.dumpmem()
        print("==================")

        

        while self.memory.get('HF') == 0 :
            
            ### TODO fix this idea. there is a better way. 
            # self.thaw_registers() # I need a moment of clarity on this... this is too much of a hack... 

            self.memory['PC'] += 1
            # self.dumpmem()
            # get instruction from memory
            print('')
            opcode = self.memory[self.memory['IP']]
            
            op = self.instructions.get(opcode)
            if self.DEBUG:
                print(f'opcode = 0x{opcode:02x}')
                print("op info:", op, type(op))

            if opcode == None:
                self.memory['HF'] = 1
                print('CRITICAL ERROR: Invalid opcode: None'   )

            how_many_params = len(op) - 1
            
            # cmd_lens = [len(x) - 1 for x in self.instructions.values()]
            # print(cmd_lens)
            if self.DEBUG:
                print(f'requires {how_many_params=}')
            
            # do the instruction ; make sure 'self' is the first parameter

            params = []
            for i in range(1,how_many_params+1):
                params.append(self.memory[self.memory['IP']+ i ] ) 

            if self.DEBUG:
                print(f'calling {op} with params {[hex(x) for x in params]}')

            # TODO this might need to be refactored to come in-line with the compile ; in particular where/how register access is achieved in the compiled code. 

            self.instructions[opcode][0](*params) # unpack the list as positional args

            if self.DEBUG:
                # self.dumpreg()
                # self.dumpmem()
                # self.dumpmemrange(start=0, end=255)
                # input("press enter to continue...")
                pass
                
            ### 
            # time.sleep(1 * self.SPEED)


        print("CPU Halted successfully")
        if self.DEBUG:
            self.dumpreg()
            self.dumpmem()
            # self.dumpmemrange(start=0, end=255)
