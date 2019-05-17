import datetime
from support.supportMaps import statusMap
from Microcontroller import Microcontroller

class MicrocontrollerSimulator(Microcontroller):
    """Class that simulates what the microcontrollers in the sub machines should do.

    This class is designed to be easily swapped out with the actual microcontrollers.Note it only tracks the
    displacement since the motor steps can be inferred from the displacement.

    """
    def __init__(self, speedMultiplier=1):
        super().__init__()
        # These results are purely to simulate endeffactor movement
        # Actual STM microcontroller will need to monitor steps too
        self.currentTime = datetime.datetime.now()
        self.speedMultiplier = speedMultiplier
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

    def setupBus(self):
        print('Nothing for bus')

    def processCommand(self, command):
        self._clearTargets()
        targets = command.generateTargets()
        self._setTargets(targets)

    def isComplete(self):
        return self._getCommandStatus() == statusMap['complete']

    def getTargets(self):
        return self.targets

    def getLocationResults(self):
        self._update()
        return self.results

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def _setTargets(self, targets):
        """Sets the current target locations and speeds.

        Args:
            targets(dict): The target locations and speeds.

        """
        self.targets = targets

    def _clearTargets(self):
        """Clears all the targets to get ready for the next command."""
        self.targets = {}
        self.accel = {}
        self.speeds = {}

    def _update(self):
        """Updates the current locations of the microcontroller.

        This function uses the time that has passed so far to calculate the amount of movement that the motors have
        done.

        """
        newTime = datetime.datetime.now()
        deltaTime = (newTime - self.currentTime) * self.speedMultiplier
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

    def _getCommandStatus(self):
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
