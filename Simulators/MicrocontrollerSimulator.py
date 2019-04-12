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

        self.speeds = {}
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
                startSpeed = values['startSpeed']
                endSpeed = values['endSpeed']

                displacement = deltaTime * startSpeed
                # self.results[submachine][motor] = displacement


                if targetValue == None:
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
                    else:
                        if self.speeds.get(submachine).get(motor) is None:
                            self.speeds[submachine][motor] = startSpeed

                    prevSpeed = self.speeds[submachine][motor]
                    newSpeed = prevSpeed + accel * deltaTime
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
        status = statusMap['complete']
        for submachine, motors in self.targets.items():
            for motor, values in motors.items():
                if values['status'] != statusMap['complete']:
                    status = statusMap['started']
        return status