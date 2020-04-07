def split_mem(val, verbose =False):
    # no individual memory address can hold a value of more than 255 (0xFF). we need to find a way to split that value between multiple addresses. 
    # by strapping them together we get up to 0xFFFF or 65535 
    # value = 1337
    # upper = value >> 8 # bitwise shifting
    # lower = value & 0xFF # logical ANDing 
    # upper = 5 ; 0b00000101
    # lower = 57; 0b00111001

    
    # value = 894
    # upper, lower = split_mem(value, verbose=True)
    # print(upper, lower)
    
    return val >> 8, val * 0xff
