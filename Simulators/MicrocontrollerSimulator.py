import datetime
from support.supportMaps import statusMap

class MicrocontrollerSimulator:
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

        self.targets = {}

    def displaceActuator(self, submachine, motor, displacement):
        self.results[submachine][motor] += displacement

    def addTarget(self, submachine, motor, targetValue, startSpeed, endSpeed):
        self.targets[submachine] = {
            motor : {
                'targetValue': targetValue,
                'startSpeed': startSpeed,
                'endSpeed': endSpeed,
                'status': statusMap['started']
            }
        }

    def setTargets(self, targets):
        self.targets = targets

    def clearTargets(self):
        self.targets = {}

    def update(self):
        newTime = datetime.datetime.now()
        deltaTime = newTime - self.currentTime
        deltaTime = deltaTime.total_seconds()
        for submachine, motors in self.targets.items():
            for motor, values in motors.items():
                currentValue = self.results[submachine][motor]
                targetValue = values['targetValue']
                # Need to change to accommodate variable speed
                speed = values['startSpeed']
                displacement = speed * deltaTime

                if targetValue == None:
                    # Spinning motor no end
                    newValue = (currentValue + displacement)
                    self.targets[submachine][motor]['status'] = statusMap['complete']
                else:
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
        status = statusMap['complete']
        for submachine, motors in self.targets.items():
            for motor, values in motors.items():
                if values['status'] != statusMap['complete']:
                    status = statusMap['started']
        return status