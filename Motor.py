class Motor(object):
    """Motor object for controlling actuators.
    
    """
    def __init__(self, displacementPerStep, totalSteps=200, stepSize = 1):
        self.currentStep = 0
        self.currentDisplacement = 0
        self.stepAngle = 360 / totalSteps
        self.totalSteps = totalSteps
        self.displacementPerStep = displacementPerStep
        self.stepSize = stepSize

    def currentAngle(self):
        return self.currentStep * self.stepAngle

    def step(self, direction=1):
        if direction >= -1 and direction <=1:
            self.currentStep += direction*self.stepSize
            self.currentDisplacement += direction*self.stepSize*self.displacementPerStep

        while self.currentStep < 0:
            self.currentStep += self.totalSteps

        while self.currentStep >= self.totalSteps:
            self.currentStep -= self.totalSteps

