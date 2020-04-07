import pyvm2

vm = pyvm2.PyVM(ram_size=2048)

some_assy = """
mov 0x20, 65 
ld 0x45, "some string here"
sig 13
"""

vm.run('asdfasdf')