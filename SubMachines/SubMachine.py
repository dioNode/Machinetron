from Motors.SpinMotor import SpinMotor


class SubMachine:
    """The machines that combine to create MACHINETRON.
    
    These are Handler, Drill, Mill, Lathe. The purpose of this class is to add
    any kind of connections required to each submachine microcontroller and 
    ensure the communication settings and consistent.
    
    """
    def __init__(self, controller):
        self.controller = controller
        self.spinMotor = SpinMotor(1)
        self.name = "SubMachine"

    def reset(self):
        print('Reset not defined')
