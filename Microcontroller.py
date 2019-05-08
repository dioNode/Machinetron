from config import configurationMap

class Microcontroller:

    def processCommand(self, command):
        targets = command.generateTargets(True)
        instructions = self._targetsDictToInstruction(targets)
        print(instructions)
        for instruction in instructions:
            address = instruction['address']
            motorInstructions = instruction['motorInstructions']
            # TODO Liam bus send
            DEVICE_ADDRESS = 0x15  # 7 bit address (will be left shifted to add the read write bit)
            DEVICE_REG_LEDOUT0 = 0x1d
            # Write an array of registers
            ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
            self.bus.write_i2c_block_data(address, DEVICE_REG_LEDOUT)

    def isComplete(self):
        return True

    def getTargets(self):
        return {}

    def getLocationResults(self):
        return {
            'drill': {
                'spin': 0,
                'vert': 0,
                'pen': 0,
            },
            'mill': {
                'spin': 0,
                'vert': 0,
                'pen': 0,
            },
            'lathe': {
                'spin': 0,
                'vert': 0,
                'pen': 0,
            },
            'handler': {
                'rail': 0,
                'flip': 0,
                'spin': 0,
            },
        }

    def pause(self):
        pass

    def resume(self):
        pass

    def _targetsDictToInstruction(self, targets):
        """Generate a list of instruction dictionaries to be sent off"""
        instructions = []
        if type(targets) is dict:
            for submachine, motors in targets.items():
                address = configurationMap[submachine]['id']
                if type(motors) is dict:
                    motorInstructions = []
                    for motor, targetVals in motors.items():
                        motorRun = 0
                        infSpin = 0
                        motorID = configurationMap['motorMap'][motor]
                        targetValue = targetVals['targetValue']
                        if targetValue is None:
                            targetValue = 0
                            infSpin = 1
                        startSpeed = targetVals['startSpeed']
                        endSpeed = targetVals['endSpeed']
                        direction = 1 if targetValue >= 0 else 0
                        # Set motorByte configurations
                        motorByte = 0
                        motorByte |= motorID << 6
                        motorByte |= motorRun << 5
                        motorByte |= infSpin << 4


                        # Set data values
                        data = [abs(targetValue), startSpeed, endSpeed]

                        motorInstruction = {
                            'motorByte': motorByte,
                            'data': data,
                        }

                        motorInstructions.append(motorInstruction)

                    commandByte = 'NORM_INST'
                    currentInstruction = {
                        'address': address,
                        'commandByte': commandByte,
                        'motorInstructions': motorInstructions
                    }

                    instructions.append(currentInstruction)

        return instructions
