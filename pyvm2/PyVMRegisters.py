class PyVMRegisters(dict):
    """ These registers are mapped to memory as Josh suggested. 

    """ 
    def __init__(self, vm):
        self.vm = vm

    # https://stackoverflow.com/a/6391979 ; this person answered the question of how to access the outer class variables 


    # intercept the call to set a value by overriding the __setitem__ method for the Dict class.
    def __setitem__(self, reg, value):
        # select the correct memory address for the register. 
        target = self.vm.register_addresses[reg]
        print('setting', reg, target)
        # put the value there. 
        print('setting', id(self.vm.memory)) # make sure they are the same object
        print(len(self.vm.memory))
        self.vm.memory[target] = value
        # pass it along to the stock Dict to set the item. 
        super().__setitem__(reg, value)