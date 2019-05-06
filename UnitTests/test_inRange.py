from unittest import TestCase


class TestInRange(TestCase):
    def test_inRange(self):
        from support.supportFunctions import inRange
        self.assertTrue(inRange((1,1), (1,3), 3))
