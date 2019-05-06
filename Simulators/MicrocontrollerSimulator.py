import datetime
from support.supportMaps import statusMap
from Microcontroller import Microcontroller

class MicrocontrollerSimulator(Microcontroller):
    """Class that simulates what the microcontrollers in the sub machines should do.

    This class is designed to be easily swapped out with the actual microcontrollers.Note it only tracks the
    displacement since the motor steps can be inferred from the displacement.

    """
    def __init__(self):
        # These results are purely to simulate endeffactor movement
        # Actual STM microcontroller will need to monitor steps too
        self.currentTime = datetime.datetime.now()
        self.results = {
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

        self.speeds = {}
        self.accel = {}
        self.targets = {}

        self.paused = True

    def processCommand(self, command):
        targets = command.generateTargets()

    def isComplete(self):
        pass


    def displaceActuator(self, submachine, motor, displacement):
        """Offsets the current locations of the cutting tools by the given amount.

        Args:
            submachine (SubMachine): The sub machine being worked on (handler, drill, mill, lathe).
            motor (string): The motor that is being turned (shift, flip, spin, raise, pen).
            displacement (double): The offset to be placed on the current location in mm.

        """
        self.results[submachine][motor] += displacement

    def addTarget(self, submachine, motor, targetValue, startSpeed, endSpeed):
        """Adds a target location with speeds for the given sub machine.

        Note that the start and end speeds are linear relative to time not displacement.

        Args:
            submachine (SubMachine): The sub machine being worked on (handler, drill, mill, lathe).
            motor (string): The motor that is being turned (shift, flip, spin, raise, pen).
            targetValue (double): The target offset to be placed on the current location in mm.
            startSpeed (double): The initial speed of movement (mm/s).
            endSpeed (double): The ending speed of movement (mm/s).

        """
        self.targets[submachine] = {
            motor: {
                'targetValue': targetValue,
                'startSpeed': startSpeed,
                'endSpeed': endSpeed,
                'status': statusMap['started']
            }
        }

    def setTargets(self, targets):
        """Sets the current target locations and speeds.

        Args:
            targets(dict): The target locations and speeds.

        """
        self.targets = targets

    def clearTargets(self):
        """Clears all the targets to get ready for the next command."""
        self.targets = {}
        self.accel = {}
        self.speeds = {}

    def update(self):
        """Updates the current locations of the microcontroller.

        This function uses the time that has passed so far to calculate the amount of movement that the motors have
        done.

        """
        newTime = datetime.datetime.now()
        deltaTime = newTime - self.currentTime
        deltaTime = deltaTime.total_seconds() if not self.paused else 0
        for submachine, motors in self.targets.items():
            for motor, values in motors.items():
                currentValue = self.results[submachine][motor]
                targetValue = values['targetValue']
                startSpeed = values['startSpeed']
                endSpeed = values['endSpeed']

                displacement = deltaTime * startSpeed

                if targetValue is None:
                    # Spinning motor no end
                    newValue = (currentValue + displacement)
                    self.targets[submachine][motor]['status'] = statusMap['complete']
                else:
                    if targetValue - currentValue == 0:
                        accel = 0
                    else:
                        accel = (pow(endSpeed, 2) - pow(startSpeed, 2)) / (2 * (targetValue - currentValue))

                    # Adjust speed and acceleration
                    if self.speeds.get(submachine) is None:
                        self.speeds[submachine] = {motor: startSpeed}
                        self.accel[submachine] = {motor: accel}
                    else:
                        if self.speeds.get(submachine).get(motor) is None:
                            self.speeds[submachine][motor] = startSpeed
                            self.accel[submachine][motor] = accel


                    accel = self.accel[submachine][motor]
                    prevSpeed = self.speeds[submachine][motor]
                    newSpeed = prevSpeed + accel * deltaTime

                    # Account for overaccelerating
                    if accel > 0 and newSpeed > endSpeed or accel < 0 and newSpeed < endSpeed:
                        newSpeed = endSpeed

                    self.speeds[submachine][motor] = newSpeed

                    # s = ut + 0.5at^2
                    displacement = prevSpeed * deltaTime + 0.5 * accel * pow(deltaTime, 2)

                    # Displacement motor
                    if abs(targetValue - currentValue) <= displacement:
                        # You've reached the target
                        newValue = targetValue
                        # Signal complete
                        self.targets[submachine][motor]['status'] = statusMap['complete']
                    else:
                        # Add distance
                        direction = (targetValue - currentValue) / abs(targetValue - currentValue)
                        newValue = currentValue + direction*displacement

                # Update info
                self.results[submachine][motor] = newValue
        self.currentTime = newTime

    def getCommandStatus(self):
        """Returns whether all the commands have been complete.

        Returns:
            Whether the sub machines have completed their instructions and are ready for next command.

        """

        status = statusMap['complete']
        for submachine, motors in self.targets.items():
            for motor, values in motors.items():
                if values['status'] != statusMap['complete']:
                    status = statusMap['started']
        return status
