from config import configurationMap
from support.supportFunctions import splitNumberHex
import smbus
import time

class Microcontroller:

    def setupBus(self):
        print('lol')


    def processCommand(self, command):
        self.bus = smbus.SMBus(1)
        targets = command.generateTargets(True)
        instructions = self._targetsDictToInstruction(targets)
        print(instructions)
        for instruction in instructions:
            address = instruction['address']
            commandByte = instruction['commandByte']
            motorInstructions = instruction['motorInstructions']
            # TODO Liam bus send
            DEVICE_ADDRESS = 0x15  # 7 bit address (will be left shifted to add the read write bit)
            DEVICE_REG_LEDOUT0 = 0x1d
            # Write an array of registers
            ledout_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
            # self.bus.write_i2c_block_data(address, DEVICE_REG_LEDOUT)
            self.bus.write_i2c_block_data(address, commandByte, motorInstructions)
            time.sleep(0.1)
            tempMotorArray = [0b01000000 | 1 << 5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0b10000000 | 1 << 5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0b11000000 | 1 << 5 | 1 << 4, 0x00, 0x00, 0x01, 0x2C, 0x01, 0x2C]
            self.bus.write_i2c_block_data(address, commandByte, tempMotorArray)
            time.sleep(0.1)
            self.bus.write_i2c_block_data(address, 1, motorInstructions)

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
        testInstruction = [0b01000000 | 1 << 5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                          0b10000000 | 1 << 5, 0x00, 0x00, 0x00, 0x32, 0x00, 0x00,
                          0b11000000 | 1 << 5 | 1 << 4, 0x06, 0x40, 0x01, 0x2C, 0x01, 0x2C]
        instructions = []
        if type(targets) is dict:
            for submachine, motors in targets.items():
                address = configurationMap[submachine]['id']


                if type(motors) is dict:
                    motorInstructions = []

                    # Add in dummy empty variables TODO Remove
                    motorInstructions.append(0b01000000 | 1 << 5)
                    for i in range(6):
                        motorInstructions.append(0)
                    motorInstructions.append(0b10000000 | 1 << 5)
                    for i in range(6):
                        motorInstructions.append(0)
                    # dummymotor1 = {'motorByte': 0b10100000, 'data': [0, 0, 0]}
                    # dummymotor2 = {'motorByte': 0b01100000, 'data': [0, 0, 0]}
                    # motorInstructions.append(dummymotor1)
                    # motorInstructions.append(dummymotor2)


                    # Legit code
                    for motor, targetVals in motors.items():
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
                        directionBit = 1
                        homeBit = 0
                        motorByte = 0
                        motorByte |= motorID << 6
                        motorByte |= directionBit << 5
                        motorByte |= motorRun << 4
                        motorByte |= homeBit << 3
                        motorByte |= infSpin << 2


                        # Set data values
                        data = [abs(targetValue), startSpeed, endSpeed]

                        motorInstruction = {
                            'motorByte': motorByte,
                            'data': data,
                        }

                        motorInstructions.append(motorByte)
                        (targetPosMSbit, targetPosLSBit) = splitNumberHex(targetValue)
                        (startSpeedMSbit, startSpeedLSBit) = splitNumberHex(startSpeed)
                        (endSpeedMSbit, endSpeedLSBit) = splitNumberHex(endSpeed)
                        motorInstructions.extend([targetPosMSbit, targetPosLSBit,
                                                  startSpeedMSbit, startSpeedLSBit,
                                                  endSpeedMSbit, endSpeedLSBit])


                        # motorInstructions.append(motorInstruction)

                    commandByte = configurationMap['instructions']['NORM_INST']
                    currentInstruction = {
                        'address': address,
                        'commandByte': commandByte,
                        'motorInstructions': motorInstructions
                    }

                    instructions.append(currentInstruction)

        return instructions
