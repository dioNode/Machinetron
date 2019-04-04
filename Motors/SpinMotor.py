from Motors.Motor import Motor

class SpinMotor(Motor):
    def __init__(self, displacementPerStep, totalSteps=200, stepsPerSecond = 1):
        super().__init__(displacementPerStep, totalSteps, stepsPerSecond)

