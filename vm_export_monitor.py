import pickledb
import time
from pprint import pprint

vm_import = pickledb.load('vm_pickle.db', False)

# import pyxel



# class App:
#     def __init__(self):
#         pyxel.init(160, 120)
#         self.x = 0
#         pyxel.run(self.update, self.draw)

#     def update(self):
#         self.x = (self.x + 1) % pyxel.width

#     def draw(self):
#         pyxel.cls(0)
#         pyxel.rect(self.x, 0, 8, 8, 9)

# App()




def update():
    registers = vm_import.get('registers')
    if registers:
        pprint(registers)
    memory = vm_import.get('memory')
    if memory:
        pprint(memory)
    screen_output = vm_import.get('screen_output')
    if screen_output:
        pprint(screen_output)

while True:
    update()
    time.sleep(.1)