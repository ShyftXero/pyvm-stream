import pyvm2

vm = pyvm2.PyVM(ram_size=16**4)
vm.SPEED =  0 # time for 1 cycle; in MILLIS ; 0 = no delay in execution
vm.DEBUG = True
vm.DEBUG_LEVEL = 0

some_assy = """
mr1 0xa
mov 0x20, 0x41 
mr4 0x20
sig 0x0d
hlt 0x00
"""

some_assy = """
mov 0xa 0xa  
mov 0x20 0x41 
mov 0xd 0x20
sig 0x0d
mov 0x20 0x42 
mov 0xd 0x20
sig 0x0d
mov 0x20 0x43 
mov 0xd 0x20
sig 0x0d
mov 0x20 0x44 
mov 0xd 0x20
sig 0x0d
mov 0x20 0x45 
mov 0xd 0x20
sig 0x0d
mov 0x20 0x46 
mov 0xd 0x20
sig 0x0d
hlt 0x00
"""


some_assy = """
; this is a continuous loop printing A
mov 0xa 0xa
mov 0x20 0x41 
mov 0xd 0x20
sig 0x0d
jmp 0x10
hlt
"""

# some_assy = """
# ; Print 5 letters starting at A
# mov 0xa 0x5
# mov 0x20 0x41
# mov 0xd 0x20
# sig 0xd 
# inc 0x20 0x1
# dec 0xa 0x1
# cmp 0xa 0x0
# jif 0xa
# hlt 0x00
# """
compiled_code = vm.assemble(some_assy)

# compiled_code = [
#     # hand-jammed assembly
#     0x01, # mov
#     0x20, # mem index i32
#     0x41, # ascii A
#     0x14, # mr4 
#     0x20, # value to mov into R4; (in this case, the address of char to print
#     0x0b, # sig
#     0x0d, # sig #14 # pulls from R4? or self.memory[0x20]
#     0x99, # hlt
#     0x00, # required nullbyte for hlt
# ]
# print("running", [f'{x:02x}' for x in compiled_code])
# exit()
vm.run(compiled_code)