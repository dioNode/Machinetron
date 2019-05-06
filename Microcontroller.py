class Microcontroller:

    def processCommand(self, command):
        targets = command.generateTargets()
        instructions = self.targetsDictToInstruction(targets, True)
        print(instructions)
        for instruction in instructions:
            address = instruction['address']
            initByte = instruction['initByte']
            data = instruction['data']
            # TODO Liam bus send
            DEVICE_ADDRESS = 0x15  # 7 bit address (will be left shifted to add the read write bit)
            DEVICE_REG_LEDOUT0 = 0x1d
            # Write an array of registers
            ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
            self.bus.write_i2c_block_data(address, DEVICE_REG_LEDOUT)

    def isComplete(self):
        pass


