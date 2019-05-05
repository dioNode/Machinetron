from config import configurationMap

class Motor(object):
    """Motor object for controlling actuators.
    Test
    """
    def __init__(self, displacementPerRotation, numRotationSteps=None):
        self.currentDisplacement = 0
        self.displacementPerRotation = displacementPerRotation
        self.numRotationSteps = numRotationSteps if numRotationSteps is not None else configurationMap['other']['numRotationSteps']

    def currentAngle(self):
        return (self.currentDisplacement / self.displacementPerRotation) * 360

    def displacementToSteps(self, displacement):
        return (displacement / self.displacementPerRotation) * self.numRotationSteps
