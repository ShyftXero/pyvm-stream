import pyvm2

# vm = pyvm2.PyVM(ram_size=2048, debug=False)
vm = pyvm2.PyVM(ram_size=2048)

some_assy = """
mr1 0xa
mov 0x20, 0x41 
mr4 0x20
sig 0x0d
hlt 0x00
"""

some_assy = """
mr1 0xa ; 
mov 0x20 0x41 
mr4 0x20
sig 0x0d
mov 0x20 0x42 
mr4 0x20
sig 0x0d
mov 0x20 0x43 
mr4 0x20
sig 0x0d
mov 0x20 0x44 
mr4 0x20
sig 0x0d
mov 0x20 0x45 
mr4 0x20
sig 0x0d
mov 0x20 0x46 
mr4 0x20
sig 0x0d
hlt 0x00
"""


some_assy = """
; this is a continuous loop printing A
mov 0xa 0xa
mov 0x20 0x41 
mr4 0x20
sig 0x0d
jmp 0x10
hlt
"""
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