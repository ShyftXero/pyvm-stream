import pyvm2

# vm = pyvm2.PyVM(ram_size=2048, debug=False)
vm = pyvm2.PyVM(ram_size=2048)

some_assy = """
mov 0x20, 0x41 
mr4 0x20
sig 0x0d
hlt 0x00
"""

compiled_code = vm.compile(some_assy)

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
print("running", [hex(x) for x in compiled_code])

vm.run(compiled_code)