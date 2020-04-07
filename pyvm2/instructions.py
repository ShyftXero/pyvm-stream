def mov(self, where, what):
    """places the value of what in memory[where]"""
    if self.debug:
        print('mov instruction:', where, what)
    
    self.registers['PC'] += 1
    where = int(where)
    self.memory[where] = byte(where)
    

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
