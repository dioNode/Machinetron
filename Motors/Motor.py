class Motor(object):
    """Motor object for controlling actuators.
    
    """
    def __init__(self, displacementPerStep, totalSteps=200, stepsPerSecond = 1):
        self.currentStep = 0
        self.currentDisplacement = 0
        self.stepAngle = 360 / totalSteps
        self.totalSteps = totalSteps
        self.displacementPerStep = displacementPerStep
        self.stepsPerSecond = stepsPerSecond

    def currentAngle(self):
        return self.currentStep * self.stepAngle

    def step(self, numSteps=1, direction=1):
        if direction >= -1 and direction <=1:
            self.currentStep += direction*numSteps
            self.currentDisplacement += direction*self.displacementPerStep*numSteps

        while self.currentStep < 0:
            self.currentStep += self.totalSteps

        while self.currentStep >= self.totalSteps:
            self.currentStep -= self.totalSteps

    def changeSpeed(self, stepsPerSecond):
        self.stepsPerSecond = stepsPerSecond