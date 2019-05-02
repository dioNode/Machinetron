from STL.stl2png import generateSlices
from stl import mesh
import numpy as np
import math
import os
import cv2
from support.supportFunctions import clearFolder, unique, pixelPos2mmPos, pixel2mm, mmPos2PixelPos, mm2pixel
from config import configurationMap


class STLProcessor:
    def __init__(self):
        self.controller = None
        self.path = None
        self.sliceDepth = 10
        self.filename = ''
        self.imageSlicesLeftRight = []
        self.imageSlicesTopDown = []
        self.imageSlicesFrontBack = []

    def generateCommands(self, filename, controller):
        self.controller = controller
        self.filename = filename
        self._clearFolders()
        self.path = 'STL/output'
        self._storeImageSlices()
        self.generateDrillCommands()

    def generateDrillCommands(self):
        # iterate through the names of contents of the folder
        sliceDepth = self.sliceDepth

        # Detect top down drills
        totalDrillPoints = []
        for img in self.imageSlicesTopDown:
            drillPoints = self._detectDrill(img)
            totalDrillPoints.append(drillPoints)
        # Detect holes
        totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, self.imageSlicesTopDown)
        self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, 'top')

        # Detect front drills
        totalDrillPoints = []
        for img in self.imageSlicesFrontBack:
            drillPoints = self._detectDrill(img)
            totalDrillPoints.append(drillPoints)
        # Detect holes
        totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, self.imageSlicesFrontBack)
        self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, 'front')
        # Detect back drills
        totalDrillPoints.reverse()
        # Detect holes
        imageSlicesBackFront = self.imageSlicesFrontBack
        imageSlicesBackFront.reverse()
        totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, imageSlicesBackFront)
        self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, 'back')

        # Detect left right drills
        totalDrillPoints = []
        for img in self.imageSlicesLeftRight:
            drillPoints = self._detectDrill(img)
            totalDrillPoints.append(drillPoints)
        # Detect holes
        totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, self.imageSlicesLeftRight)
        self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, 'left')
        # Detect right drills
        totalDrillPoints.reverse()
        # Detect holes
        imageSlicesRightLeft = self.imageSlicesLeftRight
        imageSlicesRightLeft.reverse()
        totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, imageSlicesRightLeft)
        self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, 'right')

    def _getTotalDrillPointsWithHoles(self, totalDrillPoints, imageSlices):
        totalDrillPointsWithHoles = []
        for img in imageSlices:
            drillPointsWithHoles = []
            for drillPoint in unique(totalDrillPoints):
                pxRadius = mm2pixel(configurationMap['drill']['diameter']/2)
                if self._containsHole(img, drillPoint, pxRadius):
                    drillPointsWithHoles.append(drillPoint)
            totalDrillPointsWithHoles.append(drillPointsWithHoles)
        return totalDrillPoints

    def _parseDrillPoints(self, totalDrillPoints, sliceDepth, face):

        trackingPoints = []
        drillHoleLengths = {}

        # Get initial holes from surface
        for drillPoint in totalDrillPoints[0]:
            drillHoleLengths[drillPoint] = 0
            trackingPoints.append(drillPoint)

        for drillPoints in totalDrillPoints:
            updatedTrackingPoints = []
            for trackedPoint in trackingPoints:
                if trackedPoint in drillPoints:
                    drillHoleLengths[trackedPoint] += sliceDepth
                    updatedTrackingPoints.append(trackedPoint)
            trackingPoints = updatedTrackingPoints

        for drillPoint, depth in drillHoleLengths.items():
            self.controller.commandGenerator.drill(
                face, drillPoint[0], drillPoint[1], depth)

    def _clearFolders(self):
        clearFolder('STL/output/frontback')
        clearFolder('STL/output/leftright')
        clearFolder('STL/output/topdown')

    def _storeImageSlices(self):
        self._clearFolders()
        self._getRotated()
        # Generate slices for topdown
        throughFace = 'topdown'
        generateSlices(self.filename, throughFace)
        facePath = self.path + '/' + throughFace
        self.imageSlicesTopDown = self._getImageSlices(facePath)
        # Generate slices for left right
        generateSlices('face3.stl', 'leftright')
        self.imageSlicesLeftRight = self._getImageSlices('STL/output/leftright')
        # Generate slices for front back
        generateSlices('face2.stl', 'frontback')
        self.imageSlicesFrontBack = self._getImageSlices('STL/output/frontback')

    def _getImageSlices(self, facePath):
        imageSlices = []
        for image_path in os.listdir(facePath):
            # create the full input path and read the file
            input_path = os.path.join(facePath, image_path)
            img = cv2.imread(input_path, 0)
            imageSlices.append(img)
        imageSlices.reverse()
        return imageSlices

    def _getRotated(self):
        rx = 90
        ry = 0
        rz = 180

        # Change this name to the required file
        # (example: for part2.stl just type in 'part2')
        stl_filename = self.filename

        for i in range(4):
            your_mesh = mesh.Mesh.from_file(stl_filename)
            your_mesh.rotate([1.0, 0.0, 0.0], math.radians(rx))
            your_mesh.rotate([0.0, 1.0, 0.0], math.radians(ry))
            your_mesh.rotate([0.0, 0.0, 1.0], math.radians(rz))
            your_mesh.save('face' + str(i + 2) + '.stl')
            i += 1
            ry += 90

    def _containsHole(self, img, pos, radius):
        x, y = pos
        return False

    def _fillHole(self, img, pos, radius, state): # state is 1 for white, 0 for black
        x, y = pos
        return img

    def _detectDrill(self, img):

        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        pxRadius = round(mm2pixel(configurationMap['drill']['diameter']/2))
        tolerance = configurationMap['drill']['detectionTolerance']

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2.2, 100,
                                    param1=100, param2=30, minRadius=pxRadius-tolerance, maxRadius=pxRadius+tolerance)
        drillPoints = []
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

                drillPoints.append((i[0], i[1]))

        # Convert from pixel to mm
        drillPointsMM = []
        for drillPoint in drillPoints:
            drillPointsMM.append(pixelPos2mmPos(drillPoint, img))

        return drillPointsMM
