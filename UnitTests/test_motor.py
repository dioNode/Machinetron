from unittest import TestCase


class TestMotor(TestCase):

    def setUp(self):
        from Motors.Motor import Motor
        from Motors.SpinMotor import SpinMotor
        self.motor = Motor(10)
        self.spinMotor = SpinMotor(10)

    def test_init(self):
        """Test all the initial variables are stored correctly."""
        from config import configurationMap
        motor = self.motor

        # Check each parameter
        self.assertEqual(motor.displacementPerRotation, 10)
        self.assertEqual(motor.currentDisplacement, 0)
        self.assertEqual(motor.numRotationSteps, configurationMap['other']['numRotationSteps'])

    def test_currentAngle(self):
        """Test the current angle function works."""
        motor = self.motor
        # Initial value
        self.assertEqual(motor.currentAngle(), 0)
        # Positive displacement
        motor.currentDisplacement = 10
        self.assertEqual(motor.currentAngle(), 360.0)
        # Negative displacement
        motor.currentDisplacement = -10
        self.assertEqual(motor.currentAngle(), -360.0)

    def test_displacementToSteps(self):
        """Test displacementToSteps function."""
        motor = self.motor
        # Test zero
        self.assertEqual(motor.displacementToSteps(0), 0)
        # Positive value
        self.assertEqual(motor.displacementToSteps(10), 200)
        # Negative value
        self.assertEqual(motor.displacementToSteps(-10), -200)

    def test_SpinMotor(self):
        from config import configurationMap

        motor = self.spinMotor
        # Test initialize inheritence
        self.assertEqual(motor.displacementPerRotation, 10)
        self.assertEqual(motor.currentDisplacement, 0)
        self.assertEqual(motor.numRotationSteps, configurationMap['other']['numRotationSteps'])
        # Test current angle function wraps 360 degrees
        motor.currentDisplacement = 4000
        self.assertEqual(motor.currentAngle(), 40.0)
        # Test wrap negative direction
        motor.currentDisplacement = -10
        self.assertEqual(motor.currentAngle(), 359.0)
