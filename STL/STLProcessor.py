from STL.Drill6mmCircleDetection import detectDrill

from STL.stl2png import generateSlices
from scipy import ndimage, misc
import numpy as np
import os
import cv2

class STLProcessor:
    def generateCommands(self, filename, controller):
        self.controller = controller
        # generateSlices(filename)
        outPath = "STL\output"
        path = "STL\output"
        commands = []

        # iterate through the names of contents of the folder
        totalDrillPoints = []
        for image_path in os.listdir(path):
            # create the full input path and read the file
            input_path = os.path.join(path, image_path)
            img = cv2.imread(input_path, 0)
            drillPoints = detectDrill(img)
            totalDrillPoints.append(drillPoints)

        sliceDepth = 10
        totalDrillPoints.reverse()

        trackingPoints = []

        print(totalDrillPoints)

        backwardsDrillHoleLengths = {}

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
            foamWidth = controller.xLength
            foamHeight = controller.zLength
            print('test', drillPoint, depth)
            controller.commandGenerator.drill('front', drillPoint[0]*foamWidth - foamWidth/2, drillPoint[1]*foamHeight, depth)
