import traceback
from typing import List, Dict
import time
import os
from colored import fg, bg, attr
import shlex # https://docs.python.org/3/library/shlex.html

import pickledb # used for async disk based screen updates # https://pythonhosted.org/pickleDB/

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
    DEBUG_LEVEL = 0 
    EXPORT = True # this is related to the vm_export variable; ships info out of vm for display/analysis elsewhere. 
    EXPORT_PATH = './vm_pickle.db'
    SPEED = 1
    memory = []
    registers = {}

    BASE_ADDRESS = 0x1000
    
    
     
 
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

        'R1': 0xa, # general purpose
        'R2': 0xb,
        'R3': 0xc,
        'R4': 0xd, # this is the target for the sig 13 function (print to screen)
    }
    # # bottom 16 units of memory are reserved for registers 

    # }
    # REMOVE - No londer required; registers are part of the memory dict


    def __init__(self, ram_size=1024, debug=True, speed=1, export_path=None):
        # This is the 'RAM' where our program will live
        self.DEBUG = debug
        self.SPEED = speed
        self.RAM_SIZE = ram_size
        self.BASE_ADDRESS = 0x1000
        
        # def memory_init(self):
        #this needs to be a function. 
        self.memory_init(ram_size)
        if export_path == None:
            export_path = '../vm_pickle.db'
        
        self.vm_export = pickledb.load(export_path, True) # this is used to export data about the vm for some additional application to render visualizations or whatnot. may switch to redis if disk performance becomes an issue. Maybe set auto_dump to false and only run it in a batch mode at the end of a run cycle.


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

            0x99: (self.hlt, 'nullbyte'),

        }


        # memory can be a dict; keys just have to be unique. 
        # almost like accessing a list mem[0] will access the value associated with key 0

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




    def memory_init(self, ram_size):
        # self.memory = [0 for _ in range(ram_size)]

        # TODO let's convert this to a dict

        self.memory = {idx:None for idx in range(ram_size)}

   
    def mov(self, where, what):
        """places the value of what in memory[where]"""
        if self.DEBUG:
            print(f'mov instruction: 0x{where:04x} 0x{what:02x}')
        where = self.mem_map(int(where))
        
        self.memory[where] = int(what)
        
        self.memory['IP'] += 3 

    def jmp(self, where):
        """ sets IP to where"""
        where = self.mem_map(int(where))
        self.memory['IP'] = where

    def jif(self, where):
        """jump if TF is 1"""
        if self.memory['TF'] == 1:
            if self.DEBUG:
                print('Test Flag is set is jumping')
            where = int(where) + self.BASE_ADDRESS
            self.memory['IP'] = int(where)
        else:
            if self.DEBUG:
                print("Test Flag is not set so not jumping")
            self.memory['IP'] += 1
        

    def ret(self, where):
        """set IP to where"""
        if self.DEBUG:
            print('Test Flag is set is jumping')
        where = int(where) #+ self.BASE_ADDRESS
        self.memory['IP'] = int(where)
    

    def cmp(self, this, that):
        """compare this to that; sets TF to 1 if they equal; something else if they aren't """
        this = self.mem_map(this)
        that = self.mem_map(that) 

        
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
        by = int(by)
        where = self.mem_map(int(where))

        if self.DEBUG:
            print(f"incrementing value at memory 0x{where:04x} by {by}; currently {self.memory[where]}")
        
        self.memory[where] += int(by)
        if self.DEBUG:
            print(f'value at memory 0x{where:04x} is now {self.memory[where]}')


        self.memory['IP'] += 1

    def dec(self, where, by):
        """DECrement the value at where by some value"""
        by = int(by)
        where = self.mem_map(int(where))

        if self.DEBUG:
            print(f"decrementing value at memory 0x{where:04x} by {by}; currently {self.memory[where]}")
        
        self.memory[where] -= int(by)
        if self.DEBUG:
            print(f'value at memory 0x{where:04x} is now {self.memory[where]}')

        self.memory['IP'] += 1
        
        

    def mul(self, where, by):
        """multiply the value at where x by and store in where integers only please"""
        by = int(by)
        where = self.mem_map(int(where))

        if self.DEBUG:
            print(f"incrementing {where:0#x}")
        
       
        self.memory[where] = self.memory[where] * by

        self.memory['IP'] += 2
        

    def div(self, where, by):
        """div the value at where / by and store in where ; integers only please"""
        by = int(by)
        where = self.mem_map(int(where))
        # integer division
        self.memory[where] = self.memory[where] // by 
        self.memory['IP'] += 2

    def sig(self, signum):
        """SIG as in SIGNAL; this is how we signal that an action should occur; such as print to the screen
        valid signals
        Register memory 0xd is very important 

        0x0d = print char at address located in register D on to screen; putchar
        0x0e = print char at address located in register D on to screen, incrementing address until address contains a null byte; putstring
        0x0f = print char at address located in register D on to screen, decrementing address until address contains a null byte; putstring but reversed

        # much, much later. 
        26 = open a file? 
        27 = write a byte to a file handle?
        
        90 = open a socket?
        91 = write to a socket handle
        92 = read from a socket handle. 
        """
     
        if signum == 0x0d: # putchar 
            # print('printing something')
            R4_val = self.memory[0xd]
            addr_val = self.memory[R4_val] 

            addr_val = self.mem_map(int(addr_val))

            if self.DEBUG:
                print(f"printing char at address in memory 0xd :{R4_val:#04x} value: {addr_val:c}", )

            print(f'{fg("green")}{chr(self.memory[self.memory[0xd] + self.BASE_ADDRESS] )}{attr("reset")}', end='')

            if self.EXPORT:
                self.vm_export.set('screen_output', chr(self.memory[self.memory[0xd]+ self.BASE_ADDRESS]))

            # with open('test_pipe', 'w') as SCREEN: # vm_export replaces this. 
            #     SCREEN.write(f'{fg("green")}{chr(self.memory[self.memory[0xd]])}{attr("reset")}')

        elif signum == 0x0e: # putstring until nullbyte; increasing
            if self.DEBUG:
                print(f"printing string starting at address in memory 0xd :{self.memory[0xd]:#04x} value: {self.memory[self.memory[0xd]+ self.BASE_ADDRESS]:c}", )
            target = self.memory[0xd] + self.BASE_ADDRESS
            while self.memory[target] != 0x00:
                print(f'{fg("green")}{chr(self.memory[target])}{attr("reset")}', end='')

                if self.EXPORT:
                    self.vm_export.set('screen_output', chr(self.memory[self.memory[target]]))
                
                target += 1

        elif signum == 0x0f: # putstring until nullbyte; decreasing (reversed strings)
            if self.DEBUG:
                print(f"printing string ending at address in memory 0xd:{self.memory[0xd]:#04x} value: {self.memory[self.memory[0xd]]:c}", )
            target = self.memory[0xd] + self.BASE_ADDRESS
            while self.memory[target] != 0x00:
                print(f'{fg("green")}{chr(self.memory[target])}{attr("reset")}', end='')

                if self.EXPORT:
                    self.vm_export.set('screen_output', chr(self.memory[self.memory[target]]))

                target -= 1

        else:
            print('unhandled signum', hex(signum))

        self.memory['IP'] += 2

    def lds(self, where, a_string):
        """put a_string at where followed by a 0x00 byte"""
        # where = where + self.BASE_ADDRESS # this one doesn't need to add it because mov() is alreading adding the self.BASE_ADDRESS
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
        
        return used_mem


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
            print('\tregister',k, '=', v)
            # print(f'\tregister {k} = 0x{v:02x}')
        return regs

    def fetch_debug_level(self):
        try:
            dbg_level = int(open('debug_level').read())
            return dbg_level # 0 or higher
        except FileNotFoundError:
            return 0 #no extra debugging

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

            try:
                cmd = line[0].lower()
                param_1 = int(line[1], 16)
                param_2 = int(line[2], 16)
            except IndexError as e:
                print("index error: there probably isn't a second paramer")
                print(e)
            except BaseException as e:
                print(e)
                
            if cmd == 'mov':
                compiled.append(0x01)
                if self.is_register(param_1): # leave registers unmapped
                    compiled.append(param_1)
                else: # remap nonregister addresses
                    # compiled.append(self.mem_map(param_1))
                    compiled.append(param_1) # trying to resolve who should be addressing things... I feel like it should be the run method not the assemble method... 
                
                compiled.append(param_2)

                # assemble the rest of the code
            elif cmd == 'jmp':
                compiled.append(0x02)
                compiled.append(param_1)
           
            elif cmd == 'jif':
                compiled.append(0x03)
                compiled.append(param_1)
            
            elif cmd == 'ret':
                compiled.append(0x04)
                compiled.append(param_1)
           
            elif cmd == 'cmp':
                compiled.append(0x05)
                compiled.append(param_1)
                compiled.append(param_2)
           
            elif cmd == 'inc':
                compiled.append(0x06)
                compiled.append(param_1)
                compiled.append(param_2)
           
            elif cmd == 'dec':
                compiled.append(0x07)
                compiled.append(param_1)
                compiled.append(param_2)
           
            elif cmd == 'mul':
                compiled.append(0x08)
                compiled.append(param_1)
                compiled.append(param_2)
            
            elif cmd == 'div':
                compiled.append(0x09)
                compiled.append(param_1)
                compiled.append(param_2)
           
            elif cmd == 'ldd':
                # like lds but for raw bytes
                pass
            elif cmd == 'sig':
                compiled.append(0x0b)
                compiled.append(param_1)

            elif cmd == 'lds':
                pass
           
            elif cmd == 'hlt':
                # the developer may not have to add the null byte to the end in their sourcecode, because the compiler can add it here. 
                compiled.append(0x99)
                compiled.append(0x00)
            
            elif cmd == 'another_instruction':
                # some new feature
                pass
            else:
                print(f"unknown instruction: {line} ")
                exit()


            if self.DEBUG:
                print([f'0x{x:02x}' for x in compiled])
                print('returning', compiled)
        
        return compiled

    def mem_map(self, requested_address):
        """ applies the self.BASE_ADDRESS (default 0x1000) to a requested address as long as the requested address is not a register address
        """

        if self.is_register(requested_address) == False: # not a register address so add the offset
            requested_address += self.BASE_ADDRESS
        return requested_address     

    def is_register(self, value):
        """determines if an value is one of the register addresses"""
        regs = [self.register_addresses[k] for k in self.registers.keys() if 'R' in k]
        print('**'* 20)
        print(regs)
        if value in regs:
            return True
        return False

    def regsync(self):
        for idx, reg in enumerate(['R1', 'R2', 'R3', 'R4'], start=0xa):
            self.memory[reg] = self.memory[idx]

    def run(self, compiled_code):
        """this is the thing that does the stuff"""
        
        #PROGRAMMER MEMORY VS CODE SPACE... 

        # THERE IS A COLLISION WHERE I WILL OVERWRITE MY OWN INSTRUCTIONS IN MEMORY... 

        # I NEED A BASE_ADDRESS TO START LOADING CODE.

        

        # we need a way to translate the requested memory address to a mapped memory address... unless it's a register, then leave it unmodified. 

        # THIS PROBLEM NEEDS TO BE RESOLVED IN THE COMPILER. 

        ENTRYPOINT = 0x10

        self.memory['IP'] = ENTRYPOINT # memory address 0x10 is the entrypoint and the location of the next instruction.
        
        for idx, data in enumerate(compiled_code):
            if self.DEBUG:
                print(f'loading 0x{data:02x} to memory 0x{ENTRYPOINT + idx:04x}')
            self.memory[ENTRYPOINT + idx] = data
        
        if self.DEBUG:
            self.dumpreg()
            self.dumpmem()
            print("==================")

        

        while self.memory.get('HF') == 0 :
            t_start = time.time()
            self.DEBUG_LEVEL = self.fetch_debug_level()
            
            ### TODO fix this idea. there is a better way. 
            # self.thaw_registers() # I need a moment of clarity on this... this is too much of a hack... 

            self.memory['PC'] += 1
            # self.dumpmem()
            # get instruction from memory
            # print('')
            opcode = self.memory[self.memory['IP']]
            
            try:
                op = self.instructions[opcode]
            except KeyError:
                self.dumpmem()
                self.dumpreg()
                print('illegal operation: IP set to invalid instruction')
                exit()
            if self.DEBUG:
                self.dumpmem()
                print(f'opcode = 0x{opcode:02x}')
                # print("op info:", op, type(op))

            if opcode == None:
                self.memory['HF'] = 1
                print('CRITICAL ERROR: Invalid opcode: None'   )
                continue

            how_many_params = len(op) - 1
            
            # cmd_lens = [len(x) - 1 for x in self.instructions.values()]
            # print(cmd_lens)
            if self.DEBUG:
                print(f'requires {how_many_params=}')
            
            # do the instruction ; make sure 'self' is the first parameter

            params = []
            for i in range(1,how_many_params+1):
                params.append(self.memory[self.memory['IP'] + i ] ) 

            if self.DEBUG:
                print(f'calling {op} with params {[hex(x) for x in params]}')

            # TODO this might need to be refactored to come in-line with the compile ; in particular where/how register access is achieved in the compiled code. 

            self.instructions[opcode][0](*params) # unpack the list as positional args

            if self.DEBUG:
                # self.dumpreg()
                # self.dumpmem()
                # self.dumpmemrange(start=0, end=255)
                if self.DEBUG_LEVEL == 1:
                    input("press enter to continue...")
                
            self.regsync() # this is to update the GP registers with their associated memory address' value.    
            ### 
            if self.EXPORT:
                self.vm_export.set('registers', self.dumpreg())
                self.vm_export.set('memory', self.dumpmem())
                self.vm_export.dump() # see line 40 for more info

            t_end = time.time()
            t_delta = t_end - t_start
            while t_delta < self.SPEED: # slow it down    
                time.sleep(self.SPEED / 1000)
                t_end = time.time()
                t_delta = t_end - t_start
            

        print("CPU Halted successfully")
        if self.DEBUG:
            self.dumpreg()
            self.dumpmem()
            # self.dumpmemrange(start=0, end=255)
