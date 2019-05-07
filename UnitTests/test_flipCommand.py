from unittest import TestCase


class TestFlipCommand(TestCase):

    def setUp(self):
        from Commands.FlipCommand import FlipCommand
        from Controller import Controller
        self.controller = Controller


    def test_generateTargets(self):
        self.fail()
