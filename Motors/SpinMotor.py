from Motors.Motor import Motor

class SpinMotor(Motor):
    """Motor object for controlling actuators.

    """

    def __init__(self, displacementPerRotation):
        super().__init__(displacementPerRotation)

    def currentAngle(self):
        return (self.currentDisplacement / self.displacementPerRotation) % 360

