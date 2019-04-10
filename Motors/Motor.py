class Motor(object):
    """Motor object for controlling actuators.
    
    """
    def __init__(self, displacementPerRotation):
        self.currentDisplacement = 0
        self.displacementPerRotation = displacementPerRotation

    def currentAngle(self):
        return (self.currentDisplacement / self.displacementPerRotation) * 360

