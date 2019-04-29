from STL.Drill6mmCircleDetection import detectDrill

from STL.stl2png import generateSlices
from scipy import ndimage, misc
import numpy as np
import os
import cv2
from support.supportFunctions import clearFolder


class STLProcessor:
    def __init__(self):
        self.controller = None
        self.path = None
        self.sliceDepth = 10

    def generateCommands(self, filename, controller):
        self.controller = controller
        self._clearFolders()
        generateSlices(filename, 'leftright')
        self.path = 'STL/output'
        self.generateDrillCommands()

    def generateDrillCommands(self):
        # iterate through the names of contents of the folder
        throughFace = 'leftright'
        sliceDepth = self.sliceDepth
        totalDrillPoints = []
        facePath = self.path + '/' + throughFace
        for image_path in os.listdir(facePath):
            # create the full input path and read the file
            input_path = os.path.join(facePath, image_path)
            img = cv2.imread(input_path, 0)
            drillPoints = detectDrill(img)
            totalDrillPoints.append(drillPoints)

        totalDrillPoints.reverse()
        self._parseDrillPoints(totalDrillPoints, sliceDepth, 'top')

    def _parseDrillPoints(self, totalDrillPoints, sliceDepth, face):

        trackingPoints = []
        backwardsDrillHoleLengths = {}

        self.controller.setFace(face)
        foamWidth = self.controller.currentFaceWidth
        foamHeight = self.controller.currentFaceHeight

        # Get initial holes from surface
        for drillPoint in totalDrillPoints[0]:
            backwardsDrillHoleLengths[drillPoint] = 0
            trackingPoints.append(drillPoint)

        for drillPoints in totalDrillPoints:
            updatedTrackingPoints = []
            for trackedPoint in trackingPoints:
                if trackedPoint in drillPoints:
                    backwardsDrillHoleLengths[trackedPoint] += sliceDepth
                    updatedTrackingPoints.append(trackedPoint)
            trackingPoints = updatedTrackingPoints

        for drillPoint, depth in backwardsDrillHoleLengths.items():

            self.controller.commandGenerator.drill(
                face, drillPoint[0]*foamWidth - foamWidth/2, drillPoint[1]*foamHeight, depth)

    def _clearFolders(self):
        clearFolder('STL/output/frontback')
        clearFolder('STL/output/leftright')
        clearFolder('STL/output/topdown')

    def _storeImageSlices(self):
        pass
