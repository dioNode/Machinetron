from unittest import TestCase


class TestMotor(TestCase):

    def setUp(self):
        from Motors.Motor import Motor
        self.motor = Motor(10)

    def test_init(self):

        from config import configurationMap
        motor = self.motor

        # Check each parameter
        self.assertEqual(motor.displacementPerRotation, 10)
        self.assertEqual(motor.currentDisplacement, 0)
        self.assertEqual(motor.numRotationSteps, configurationMap['other']['numRotationSteps'])

    def test_currentAngle(self):
        motor = self.motor
        self.assertEqual(motor.currentAngle(), 0)

    def test_displacementToSteps(self):
        motor = self.motor
        self.assertEqual(motor.displacementToSteps(10), 200)
