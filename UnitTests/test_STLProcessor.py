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
        from support.supportFunctions import posListMatches
        import cv2
        stlProcessor = STLProcessor()

        detectionSols = {
            'part0-frontback0': [(20, 25), (-20, 25)],
            'part1-frontback2': [(0, 100)],
            'part2-face2_0004': [],
            'part2-face3_0003': [],
            'part2-frontback3': [],
            'part3-frontback25': [(0, 40), (0, 100), (27.5, 40), (27.5, 100), (-27.5, 40), (-27.5, 100)],
        }

        for imname, coordList in detectionSols.items():
            img = cv2.imread('data/' + imname + '.png', 0)
            drillsDetected = stlProcessor._detectDrill(img, showFig=False)
            self.assertTrue(posListMatches(drillsDetected, coordList, 1))



    def test__detectLathe(self):
        from STL.STLProcessor import STLProcessor
        from support.supportFunctions import posListMatches
        import cv2
        stlProcessor = STLProcessor()

        detectionSols = {
            'part0-frontback0': 5
        }

        for imname, coordList in detectionSols.items():
            img = cv2.imread('data/' + imname + '.png', 0)
            lathesDetected = stlProcessor._detectLathe(img, showFig=False)
            # self.assertTrue(posListMatches(drillsDetected, coordList, 1))

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
