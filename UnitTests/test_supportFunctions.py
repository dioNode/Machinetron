from unittest import TestCase


class TestSupportFunctions(TestCase):
    def test_posListMatches(self):
        from support.supportFunctions import posListMatches
        # Test basic case
        self.assertTrue(posListMatches([(1, 2)], [(1, 2)]))
        # Test basic fail case
        self.assertFalse(posListMatches([(2, 1)], [(1, 2)]))
        # Test different sizes
        self.assertFalse(posListMatches([(2, 1), (1, 2)], [(1, 2)]))
        self.assertFalse(posListMatches([(2, 1), (1, 2)], [(1, 2)]))
        # Test reversed
        self.assertTrue(posListMatches([(1, 2), (3, 4)], [(3, 4), (1, 2)]))
        # Test decimal rounding
        self.assertTrue(posListMatches([(1.15, 2), (3, 4)], [(3, 4), (1, 2.1)], 0.2))