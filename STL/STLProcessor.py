from STL.stl2png import generateSlices
from stl import mesh
import numpy as np
import math
import os
import cv2
from support.supportFunctions import clearFolder, unique, pixelPos2mmPos, pixel2mm, mmPos2PixelPos, mm2pixel, inRange
from config import configurationMap


class STLProcessor:
    """Class for automating command generation using STL file.

    This will slice the STL file in 3 directions into images that are stored in the output folder. Rotations of the STL
    file will also be saved and image processing is used to determine toolpaths.

    Process time:
        sliceDepth = 0.5 : 1 min 44 sec
        sliceDepth = 1.0 : 1 min 06 sec

    """
    def __init__(self):
        self.controller = None
        self.path = None
        self.sliceDepth = 1
        self.filename = ''
        self.imageSlicesLeftRight = []
        self.imageSlicesTopDown = []
        self.imageSlicesFrontBack = []

    def generateCommands(self, filename, controller):
        """Generates the commands into the controller using the file.

        Args:
            filename (string): The file name and location of the stl file being used.
            controller (Controller): The main controller object.

        """
        self.controller = controller
        self.filename = filename
        self._clearFolders()
        self.path = 'STL/output'
        self._storeImageSlices()
        self._clearFaces()
        self.generateDrillCommands()
        self.generateLatheCommands()

    def generateLatheCommands(self):
        """Generates the commands to use the lathe."""
        # iterate through the names of contents of the folder

        # Detect lathes
        totalLatheRadiusList = []
        for img in self.imageSlicesTopDown:
            latheRadius = self._detectLathe(img)
            totalLatheRadiusList.append(latheRadius)

        startIdx = None
        endIdx = None
        for lathePoint in unique(totalLatheRadiusList):
            startIdx = None
            endIdx = None
            for idx, radiusList in enumerate(totalLatheRadiusList):
                if lathePoint in radiusList:
                    # Set the index
                    if startIdx is None:
                        # First instance of radius
                        startIdx = idx
                        endIdx = idx + 1
                    else:
                        endIdx = idx + 1
                else:
                    if startIdx is not None and endIdx is not None:
                        z0 = startIdx * self.sliceDepth
                        z1 = endIdx * self.sliceDepth
                        radius = pixel2mm(lathePoint)
                        self.controller.commandGenerator.lathe(z0, z1, radius)
                        startIdx = None
                        endIdx = None

        # If the lathe reaches the end, make sure it runs
        if startIdx is not None and endIdx is not None:
            z0 = startIdx * self.sliceDepth
            z1 = endIdx * self.sliceDepth
            radius = pixel2mm(lathePoint)
            self.controller.commandGenerator.lathe(z0, z1, radius)

    def generateDrillCommands(self):
        """Generates the command to use the drill."""
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
                pxRadius = 40 #mm2pixel(configurationMap['drill']['diameter']/2)
                pxDrillPoint = mmPos2PixelPos(drillPoint, img)
                if self._containsHole(img, pxDrillPoint, pxRadius):
                    drillPointsWithHoles.append(drillPoint)
            totalDrillPointsWithHoles.append(drillPointsWithHoles)
        return totalDrillPointsWithHoles

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
        clearFolder('STL/dump')

    def _clearFaces(self):
        for faceNum in range(2, 6):
            filePath = 'face' + str(faceNum) + '.stl'
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file ", filePath)

    def _storeImageSlices(self):
        self._clearFolders()
        self._getRotated()
        # Generate slices for topdown
        sliceNum = math.ceil(110/self.sliceDepth)
        throughFace = 'topdown'
        generateSlices(self.filename, throughFace, sliceNum)
        facePath = self.path + '/' + throughFace
        self.imageSlicesTopDown = self._getImageSlices(facePath, 55, 1145, 57, 1196, 76.6, 80)

        # Generate slices for left right
        sliceNum = math.ceil(int(76.6/self.sliceDepth))
        generateSlices('face3.stl', 'leftright', sliceNum)
        self.imageSlicesLeftRight = self._getImageSlices('STL/output/leftright', 55, 1145, 75, 1575, 80, 110)

        # Generate slices for front back
        sliceNum = math.ceil(80/self.sliceDepth)
        generateSlices('face2.stl', 'frontback', sliceNum+1)
        self.imageSlicesFrontBack = self._getImageSlices('STL/output/frontback', 55, 1145, 78, 1645, 76.6, 110)

    def _getImageSlices(self, facePath, x0, x1, y0, y1, width, height):
        imageSlices = []
        for image_path in os.listdir(facePath):
            # create the full input path and read the file
            input_path = os.path.join(facePath, image_path)
            img = cv2.imread(input_path, 0)
            ratio = configurationMap['other']['mmPerPixelRatio']
            croppedIm = img[y0:y1, x0:x1]
            resizedIm = cv2.resize(croppedIm, (int(width/ratio), int(height/ratio)))
            imageSlices.append(resizedIm)
            cv2.imwrite('STL/dump/'+image_path, resizedIm)
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

    def _containsHole(self, img, pos, radius, state=0): # default hole is black
        height = np.size(img, 0)
        width = np.size(img, 1)

        pos = tuple([int(round(val)) for val in pos])
        radius = int(radius)

        if state == 0:
            mask = np.zeros((height, width), np.uint8)
            cv2.circle(mask, pos, radius, (255, 255, 255), -1)
            multiplied_image = cv2.multiply(img, mask)

            # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
            if sum(sum(multiplied_image)) == 0:
                return True
            else:
                return False
        else:
            mask = np.zeros((height, width), np.uint8)
            detectRadius = int(radius*1.1)
            cv2.circle(mask, pos, detectRadius, (255, 255, 255), -1)

            mask = cv2.bitwise_not(mask)

            multiplied_image = cv2.multiply(img, mask)

            # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
            if sum(sum(multiplied_image)) == 0:
                return True
            else:
                return False

    def _fillHole(self, img, pos, radius, state): # state is 1 for white, 0 for black
        x, y = pos
        return img

    def _detectDrill(self, img):

        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        pxRadius = round(mm2pixel(configurationMap['drill']['diameter']/2))
        tolerance = configurationMap['drill']['detectionTolerance']

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2, 100,
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

    def _detectLathe(self, img):
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        height, width = img.shape

        pxRadiusMax = round(mm2pixel(configurationMap['lathe']['maxDetectionRadius']))
        pxRadiusMin = round(mm2pixel(configurationMap['lathe']['minDetectionRadius']))

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.2, 100,
                                   param1=100, param2=30, minRadius=pxRadiusMin,
                                   maxRadius=pxRadiusMax)

        image = img
        output = image.copy()

        lathePoints = []

        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                if self._containsHole(img, (x,y), r, 1):
                    lathePoints.append((x, y, r))

        # Convert from pixel to mm
        lathePointsMM = []
        for lathePoint in lathePoints:
            pos = (lathePoint[0], lathePoint[1])
            radius = lathePoint[2]
            lathePointMM = pixelPos2mmPos(pos, img)
            mmHeight = pixel2mm(height)
            if inRange(lathePointMM, (0, mmHeight / 2), configurationMap['other']['mmError']):
                lathePointsMM.append(radius)

        return lathePointsMM
