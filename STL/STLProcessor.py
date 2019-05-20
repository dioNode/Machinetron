from STL.stl2png import generateSlices
from stl import mesh
import numpy as np
import math
import os
import cv2
from support.supportFunctions import clearFolder, unique, pixelPos2mmPos, pixel2mm, mmPos2PixelPos, mm2pixel, \
    inRange, tupleArrayInRange
from config import configurationMap
import matplotlib.pyplot as plt


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
        self.sliceDepth = 10
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
        self.generateMillCommands()
        self._dumpImageSlices()

    def generateLatheCommands(self):
        """Generates the commands to use the lathe."""
        # iterate through the names of contents of the folder

        # Detect lathes
        totalLatheRadiusList = []
        for imNum, img in enumerate(self.imageSlicesTopDown):
            latheRadius = self._detectLathe(img)
            totalLatheRadiusList.append(latheRadius)

            for radius in latheRadius:
                # Patch up image
                height = img.shape[0]
                width = img.shape[1]
                pim = self._fillHole(img, (int(width/2), int(height/2)), radius, 0)
                # Remask over existing image
                self.imageSlicesTopDown[imNum] = pim

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
            # Trigger command
            self.controller.commandGenerator.lathe(z0, z1, radius)

    def generateDrillCommands(self):
        """Generates the command to use the drill."""
        # iterate through the names of contents of the folder
        sliceDepth = self.sliceDepth

        imageSlicesBackFront = self.imageSlicesFrontBack.copy()
        imageSlicesBackFront.reverse()
        imageSlicesRightLeft = self.imageSlicesLeftRight.copy()
        imageSlicesRightLeft.reverse()
        faceOrder = ['top', 'front', 'right', 'back', 'left']
        for facenum, imgSlices in enumerate([self.imageSlicesTopDown, self.imageSlicesFrontBack, imageSlicesRightLeft,
                                             imageSlicesBackFront, self.imageSlicesLeftRight]):
            # Detect top down drills
            totalDrillPoints = []
            for img in imgSlices:
                drillPoints = self._detectDrill(img)
                totalDrillPoints.append(drillPoints)
            # Detect holes
            totalDrillPointsWithHoles = self._getTotalDrillPointsWithHoles(totalDrillPoints, imgSlices)
            self._parseDrillPoints(totalDrillPointsWithHoles, sliceDepth, faceOrder[facenum])


    def _getTotalDrillPointsWithHoles(self, totalDrillPoints, imageSlices):
        totalDrillPointsWithHoles = []
        for img in imageSlices:
            drillPointsWithHoles = []
            for drillPoint in unique(totalDrillPoints):
                pxRadius = mm2pixel(configurationMap['drill']['diameter']/2) - \
                           configurationMap['drill']['detectionTolerance']/2
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
            # Drill command
            self.controller.commandGenerator.drill(
                face, drillPoint[0], drillPoint[1], depth)
            # Fill in hole in image
            numSlices = int(depth/self.sliceDepth)
            imageSlices = []
            if face == 'top':
                imageSlices = self.imageSlicesTopDown
            elif face == 'right':
                imageSlices = self.imageSlicesLeftRight
                imageSlices.reverse()
            elif face == 'left':
                imageSlices = self.imageSlicesLeftRight
            elif face == 'front':
                imageSlices = self.imageSlicesFrontBack
            elif face == 'back':
                imageSlices = self.imageSlicesFrontBack
                imageSlices.reverse()
            for imnum in range(numSlices):
                im = imageSlices[imnum]
                pim = self._fillHole(im, mmPos2PixelPos(drillPoint, im),
                                     mm2pixel(configurationMap['drill']['diameter']/2+1), 1) # Added 1 just in case
                imageSlices[imnum] = pim

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
        return imageSlices

    def _dumpImageSlices(self):
        names = ['frontback', 'leftright', 'topdown']
        for i,imSlices in enumerate([self.imageSlicesFrontBack, self.imageSlicesLeftRight, self.imageSlicesTopDown]):
            for j,im in enumerate(imSlices):
                cv2.imwrite('STL/dump/' + names[i] + str(j) + '.png', im)

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
        # If state is 1 we want the hole filled white
        radius = int(radius)
        if state == 1:
            # the -1 signifies a filled circle (circle thickness)
            cv2.circle(img, pos, radius, (255, 255, 255), -1)
        # If the state is 0 we want the hole filled black
        else:
            cv2.circle(img, pos, radius+400, (255, 255, 255), 800)
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

    def _detectLathe(self, img):
        cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        height, width = img.shape

        pxRadiusMax = round(mm2pixel(configurationMap['lathe']['maxDetectionRadius']))
        pxRadiusMin = round(mm2pixel(configurationMap['lathe']['minDetectionRadius']))

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.6, 100,
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





    def generateMillCommands(self):
        # img = self.imageSlicesTopDown[9]
        imageSlicesBackFront = self.imageSlicesFrontBack.copy()
        imageSlicesBackFront.reverse()
        imageSlicesRightLeft = self.imageSlicesLeftRight.copy()
        imageSlicesRightLeft.reverse()

        faceOrder = ['top', 'front', 'right', 'back', 'left']
        for facenum, imgSlices in enumerate([self.imageSlicesTopDown, self.imageSlicesFrontBack, imageSlicesRightLeft,
                          imageSlicesBackFront, self.imageSlicesLeftRight]):

            # Reverse bw of imgSlices
            for imNum, im in enumerate(imgSlices):
                pim = ~im
                imgSlices[imNum] = pim

            # Go through each image and get list of matching shapes
            imgSlices.reverse()
            surfaceIm = imgSlices[0]
            pathListWithShapes = self._detectEdge(surfaceIm)


            print('length paths', len(pathListWithShapes))
            for i,pathListPerShape in enumerate(pathListWithShapes):
                imageNum = 1
                # Loop through each shape
                print('looping through shape', i)
                currentDepth = 0
                while imageNum < len(self.imageSlicesTopDown) and self._shapeExistsInImg(
                        imgSlices[imageNum], pathListPerShape):
                    currentDepth += self.sliceDepth
                    imageNum += 1

                # Generate toolpaths
                depth = currentDepth
                borderPath = pathListPerShape
                # Shrink borderPath by mill radius


                # Mill over path

                # Keep shrinking and milling until area border path is too small

                if depth > 0:
                    # Convert to mm
                    borderPathMM = []
                    for pts in borderPath:
                        borderPathMM.append(pixelPos2mmPos(pts, imgSlices[imageNum]))

                    self.controller.commandGenerator.millPointsSequence(borderPathMM, depth, faceOrder[facenum])


        # # Convert to mm
        # pathListWithShapesMM = []
        # for pathListPerShape in pathListWithShapes:
        #     pathList = []
        #     for pts in pathListPerShape:
        #         pathList.append(pixelPos2mmPos(pts, img))
        #     pathListWithShapesMM.append(pathList)
        #
        # print('pathwith shapes', pathListWithShapesMM)
        # for pathList in pathListWithShapesMM:
        #     self.controller.commandGenerator.millPointsSequence(pathList, 40, 'top')

    def _shapeExistsInImg(self, img, pathList, mmAccuracy=1):
        pathListWithShapes = self._detectEdge(img)
        print('original', len(pathListWithShapes), len(pathList), pathList)

        for pathListPerShape in pathListWithShapes:
            print('compare', pathListPerShape)
            if tupleArrayInRange(pathListPerShape, pathList, mm2pixel(mmAccuracy)):
                print('worked')
                return True

        pathListWithShapes.reverse()
        for pathListPerShape in pathListWithShapes:
            if tupleArrayInRange(pathListPerShape, pathList, mm2pixel(mmAccuracy)):
                return True
        return False

    def _detectEdge(self, img, pixelResolution=1):# default is 1 pixel resolution
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(img, 127, 255, 0)
        # detect the edges of the mill using canny edge detector
        # edges = cv2.Canny(img, 100, 255)
        # use contours to have the coordinates in an ordered fashion to use a straight line between consecutive points
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        toolpathList = []

        for shapeList in contours:
            toolPathPerShape = []
            for ptnum, points in enumerate(shapeList):
                if ptnum % pixelResolution == 0:
                    point = points[0]
                    x = point[0]
                    y = point[1]
                    toolPathPerShape.append((x, y))
            toolpathList.append(toolPathPerShape)
        return toolpathList

    def _shrink(self, contours):
        #make the contour list more readable
        contourList = np.array([list(pt[0]) for ctr in contours for pt in ctr])
        #extract all x and y points from contours
        x = contourList[:,1]
        y = contourList[:,0]
        #max x distance of mill cutout
        xdifference = max(x) - min(x)
        #max y distance of mill cutout
        ydifference = max(y) - min(y)
        #Scaling coefficients to shrink using 10pixels = 1mm
        coef_x = (xdifference - 100) / xdifference
        coef_y = (ydifference - 100) / ydifference

        #shrink the contour
        for contour in contours:
            contour[:, :, 0] = contour[:, :, 0] * coef_x
            contour[:, :, 1] = contour[:, :,  1] * coef_y

        #make the contour list more readable
        contourList = np.array([list(pt[0]) for ctr in contours for pt in ctr])
        #extract all x and y points from contours
        x = contourList[:,1]
        y = contourList[:,0]
        #create a list of tuples (x, y) which is ordered, sequencing through them will give the toolpath
        toolpathList = list(zip(x, y))
        plt.scatter(x[:1000], y[:1000])
        plt.show()
        return contours, toolpathList






