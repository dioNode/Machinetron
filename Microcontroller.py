from config import configurationMap
from support.supportFunctions import splitNumberHex

import time

class Microcontroller:

    def setupBus(self):
        import smbus
        self.bus = smbus.SMBus(1)


    def processCommand(self, command):
        print('process command')
        targets = command.generateTargets(True)
        instructions = self._targetsDictToInstruction(targets)
        print(instructions)
        for instruction in instructions:
            address = instruction['address']
            commandByte = instruction['commandByte']
            motorInstructions = instruction['motorInstructions']
            self.bus.write_i2c_block_data(address, commandByte, motorInstructions)
            time.sleep(0.1)
            # Start instruction
            self.bus.write_i2c_block_data(address, 1, motorInstructions)

    def isComplete(self):
        # TODO Work for all submachines
        READ_MACHINE_STATE = 0x0A
        address = 0x2A
        retreivedata = self.bus.read_i2c_block_data(address, READ_MACHINE_STATE, 2)
        return retreivedata[1] == 1

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
        address = configurationMap['lathe']['id']
        motorInstructions = []
        for i in range(21):
            motorInstructions.append(0)
        self.bus.write_i2c_block_data(address, configurationMap['instructions']['PAUSE_INST'], motorInstructions)

    def resume(self):
        address = configurationMap['lathe']['id']
        motorInstructions = []
        for i in range(21):
            motorInstructions.append(0)
        self.bus.write_i2c_block_data(address, configurationMap['instructions']['START_INST'], motorInstructions)

    def sendStartCommand(self):
        print('START_INST')

    def _targetsDictToInstruction(self, targets):
        """Generate a list of instruction dictionaries to be sent off"""
        instructions = []
        if type(targets) is dict:
            for submachine, motors in targets.items():
                address = configurationMap[submachine]['id']

                # Process motors to have all three motors inside
                unusedMotorsNum = [1, 2, 3]
                for motorName in motors:
                    unusedMotorsNum.pop(configurationMap['motorMap'][motorName] - 1)


                motorInstructions = []

                for motorNum in range(1,4):
                    if motorNum in unusedMotorsNum:
                        # Generate unused motor code
                        motorInstructions.append(motorNum << 6 | 1 << 5)    # Shift motor ID and direction bit
                        for i in range(6):
                            motorInstructions.append(0)
                    else:
                        # Add proper motor
                        for motor, targetVals in motors.items():
                            if configurationMap['motorMap'][motor] == motorNum:
                                motorRun = 1
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
                                homeBit = 0
                                motorByte = 0
                                motorByte |= motorID << 6
                                motorByte |= direction << 5
                                motorByte |= motorRun << 4
                                motorByte |= homeBit << 3
                                motorByte |= infSpin << 2

                                motorInstructions.append(motorByte)
                                (targetPosMSbit, targetPosLSBit) = splitNumberHex(targetValue)
                                (startSpeedMSbit, startSpeedLSBit) = splitNumberHex(startSpeed)
                                (endSpeedMSbit, endSpeedLSBit) = splitNumberHex(endSpeed)
                                motorInstructions.extend([targetPosMSbit, targetPosLSBit,
                                                          startSpeedMSbit, startSpeedLSBit,
                                                          endSpeedMSbit, endSpeedLSBit])

                commandByte = configurationMap['instructions']['NORM_INST']
                currentInstruction = {
                    'address': address,
                    'commandByte': commandByte,
                    'motorInstructions': motorInstructions
                }

                instructions.append(currentInstruction)





                # # Add in dummy empty variables TODO Remove
                # motorInstructions.append(0b01000000 | 1 << 5)
                # for i in range(6):
                #     motorInstructions.append(0)
                # motorInstructions.append(0b10000000 | 1 << 5)
                # for i in range(6):
                #     motorInstructions.append(0)
                #
                #
                # Legit code
                # for motor, targetVals in motors.items():
                #     motorRun = 1
                #     infSpin = 0
                #     motorID = configurationMap['motorMap'][motor]
                #     targetValue = targetVals['targetValue']
                #     if targetValue is None:
                #         targetValue = 0
                #         infSpin = 1
                #     startSpeed = targetVals['startSpeed']
                #     endSpeed = targetVals['endSpeed']
                #     direction = 1 if targetValue >= 0 else 0
                #     # Set motorByte configurations
                #     homeBit = 0
                #     motorByte = 0
                #     motorByte |= motorID << 6
                #     motorByte |= direction << 5
                #     motorByte |= motorRun << 4
                #     motorByte |= homeBit << 3
                #     motorByte |= infSpin << 2
                #
                #
                #     motorInstructions.append(motorByte)
                #     (targetPosMSbit, targetPosLSBit) = splitNumberHex(targetValue)
                #     (startSpeedMSbit, startSpeedLSBit) = splitNumberHex(startSpeed)
                #     (endSpeedMSbit, endSpeedLSBit) = splitNumberHex(endSpeed)
                #     motorInstructions.extend([targetPosMSbit, targetPosLSBit,
                #                               startSpeedMSbit, startSpeedLSBit,
                #                               endSpeedMSbit, endSpeedLSBit])
                #
                #
                # commandByte = configurationMap['instructions']['NORM_INST']
                # currentInstruction = {
                #     'address': address,
                #     'commandByte': commandByte,
                #     'motorInstructions': motorInstructions
                # }
                #
                # instructions.append(currentInstruction)

        return instructions
