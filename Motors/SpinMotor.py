from Motors.Motor import Motor

class SpinMotor(Motor):
    """Motor object for controlling spinning actuators that deal with angles.

    """

    def __init__(self, displacementPerRotation, numRotationSteps=None):
        super().__init__(displacementPerRotation, numRotationSteps)

    def currentAngle(self):
        return (self.currentDisplacement / self.displacementPerRotation) % 360

