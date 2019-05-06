

class Microcontroller:

    def processCommand(self, command):
        targets = command.generateTargets()
        instructions = self._targetsDictToInstruction(targets, True)
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
        return False

    def getTargets(self):
        return {}

    def getLocationResults(self):
        return {}

    def pause(self):
        pass

    def resume(self):
        pass



    def _targetsDictToInstruction(self, targets, inSteps=False):
        """Generate a list of instruction dictionaries to be sent off"""
        instructions = []
        if type(targets) is dict:
            for submachine, motors in targets.items():
                address = configurationMap[submachine]['id']
                if type(motors) is dict:
                    for motor, targetVals in motors.items():
                        motorID = configurationMap['motorMap'][motor]
                        targetValue = targetVals['targetValue']
                        targetValue = targetValue if targetValue is not None else configurationMap['other']['infVal']
                        startSpeed = targetVals['startSpeed']
                        endSpeed = targetVals['endSpeed']
                        direction = 1 if targetValue >= 0 else 0
                        # Set initByte configurations
                        initByte = 0
                        initByte |= motorID << 5
                        initByte |= direction << 4

                        if inSteps:
                            targetValue = motor.displacementToSteps(targetValue)
                            startSpeed = motor.displacementToSteps(startSpeed)
                            endSpeed = motor.displacementToSteps(endSpeed)

                        # Set data values
                        data = [abs(targetValue), startSpeed, endSpeed]

                        currentInstruction = {
                            'address': address,
                            'initByte': initByte,
                            'data': data
                        }

                        instructions.append(currentInstruction)

        return instructions
