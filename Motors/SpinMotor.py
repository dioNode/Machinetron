from Motors.Motor import Motor

class SpinMotor(Motor):
    def __init__(self, displacementPerStep):
        super().__init__(displacementPerStep)
