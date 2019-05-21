from unittest import TestCase


class TestSTLProcessor(TestCase):
    def setUp(self):
        from Controller import Controller
        self.controller = Controller(True)

    # def test_generateCommands(self):
    #     self.fail()
    #
    # def test_generateLatheCommands(self):
    #     self.fail()
    #
    # def test_generateDrillCommands(self):
    #     self.fail()
    #
    # def test__clearFolders(self):
    #     self.fail()
    #
    # def test__clearFaces(self):
    #     self.fail()
    #
    # def test__storeImageSlices(self):
    #     self.fail()
    #
    # def test__getImageSlices(self):
    #     self.fail()
    #
    # def test__dumpImageSlices(self):
    #     self.fail()
    #
    # def test__getRotated(self):
    #     self.fail()
    #
    # def test__containsHole(self):
    #     self.fail()
    #
    # def test__fillHole(self):
    #     self.fail()

    def test__detectDrill(self):
        from STL.STLProcessor import STLProcessor
        import cv2
        import numpy as np
        stlProcessor = STLProcessor()
        img0 = cv2.imread('data/part0-frontback2.png', 0)
        img1 = cv2.imread('data/part1-frontback2.png', 0)
        # img2 = cv2.imread('data/part2-topdown10.png', 0)
        # img2 = cv2.imread('data/part2-frontback3.png', 0)
        img2 = cv2.imread('data/part2-face2_0004.png', 0)
        img3 = cv2.imread('data/part3-frontback3.png', 0)
        img3 = cv2.imread('data/part3-face2_0003.png', 0)
        img = img3
        drillsDetected = stlProcessor._detectDrill(img)
        print(drillsDetected)
        cv2.imshow('Erosion', img)

        cv2.waitKey(0)


    # def test__detectLathe(self):
    #     self.fail()
    #
    # def test_generateMillCommands(self):
    #     self.fail()
    #
    # def test_millPixelPath(self):
    #     self.fail()
    #
    # def test__shapeExistsInImg(self):
    #     self.fail()
    #
    # def test__detectEdge(self):
    #     self.fail()
    #
    # def test__shrink(self):
    #     self.fail()
    #
    # def test__getShrunkenPath(self):
    #     self.fail()
