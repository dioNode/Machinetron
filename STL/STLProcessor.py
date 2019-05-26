from STL.stl2png import generateSlices
from stl import mesh
import numpy as np
import math
import os
import cv2
from support.supportFunctions import clearFolder, unique, pixelPos2mmPos, pixel2mm, mmPos2PixelPos, mm2pixel, \
    inRange, tupleArrayInRange, getCenterPoint, incRange
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
        self.sliceDepth = 10
        self.filename = ''
        self.imageSlicesLeftRight = []
        self.imageSlicesRightLeft = []
        self.imageSlicesTopDown = []
        self.imageSlicesFrontBack = []
        self.imageSlicesBackFront = []

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
        self.controller.writeToHistory(filename)
        self.generateDrillCommands()
        # self.generateLatheCommands()
        self._dumpImageSlices()
        self.generateMillCommands(showFig=controller.useSimulator)

    def generateLatheCommands(self):
        """Generates the commands to use the lathe.

        This should go through the image slices of each direction and look for circles that are
        centered around the middle and within a certain radius range. It will then go through and
        calculate the depths of each lathe and replace the images so the mill will not detect the
        lathes.

        """
        # iterate through the names of contents of the folder

        # Detect lathes for each image in the image slices
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
        # Go through the list of lathe shapes to calculate depths and send a command if appropriate
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
                        self.controller.commandGenerator.lathe(self.controller.zLength - z1,
                                                               self.controller.zLength - z0, radius)
                        startIdx = None
                        endIdx = None

        # If the lathe reaches the end, make sure it runs
        if startIdx is not None and endIdx is not None:
            z0 = startIdx * self.sliceDepth
            z1 = endIdx * self.sliceDepth
            # Flip because lathe goes from top down
            radius = pixel2mm(lathePoint)
            # Trigger command
            self.controller.commandGenerator.lathe(self.controller.zLength - z1, self.controller.zLength - z0, radius)

    def generateDrillCommands(self):
        """Generates the command to use the drill.

        This goes through each image slice to find drill hole circles. It then goes through the layers of
        images slices from each surface to determine where the drill could come from and patches up the
        holes in the image as it goes for the mill and lathe.

        """
        # iterate through the names of contents of the folder
        faceOrder = [('top', None), ('front', 'back'), ('left', 'right')]
        pxRadius = mm2pixel(configurationMap['drill']['diameter']/2)

        for facenum, imgSlices in enumerate([self.imageSlicesTopDown,
                                             self.imageSlicesFrontBack, self.imageSlicesLeftRight]):

            # Go through and check if drill can penetrate from surface
            for startingImgNum, imgNumDir in [(0, 1), (len(imgSlices)-1, -1)]:

                faceSide = 0 if imgNumDir == 1 else 1
                face = faceOrder[facenum][faceSide]

                # Detect throughDrillHoles as all the drill holes throughout the image slices
                throughDrillHoles = []
                totalDrillHoles = []
                for img in imgSlices:
                    drillHoles = self._detectDrill(img)
                    # print('all', drillHoles)
                    # cv2.imshow('sdf', img)
                    # cv2.waitKey(0)
                    totalDrillHoles.append(drillHoles)
                    for drillHole in drillHoles:
                        if drillHole not in throughDrillHoles:
                            throughDrillHoles.append(drillHole)

                if face is not None:
                    for surfaceHole in throughDrillHoles:
                        imgnum = startingImgNum
                        depth = 0
                        containsHoleWithin = False # This has crossed the actual drill hole and not just empty space
                        while imgnum < len(imgSlices) and depth < configurationMap['drill']['depth'] and \
                                self._containsHole(imgSlices[imgnum],
                                mmPos2PixelPos(surfaceHole, imgSlices[imgnum]),
                                pxRadius - mm2pixel(configurationMap['other']['mmError'] / 2), 0):
                            if surfaceHole in totalDrillHoles[imgnum]:
                                # There is a drill hole shape here, clear it out from images
                                pim = self._fillHole(imgSlices[imgnum], mmPos2PixelPos(surfaceHole, imgSlices[imgnum]),
                                                     pxRadius + mm2pixel(configurationMap['other']['mmError'] / 2), 1)
                                imgSlices[imgnum] = pim
                                containsHoleWithin = True

                            depth += self.sliceDepth
                            imgnum += imgNumDir
                        # Do drill
                        if depth > 0 and containsHoleWithin:
                            (x, z) = surfaceHole
                            self.controller.commandGenerator.drill(face, x, z, depth)

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
        self.imageSlicesTopDown.reverse()

        # Generate slices for left right
        sliceNum = math.ceil(int(76.6/self.sliceDepth))
        generateSlices('face3.stl', 'leftright', sliceNum)
        self.imageSlicesLeftRight = self._getImageSlices('STL/output/leftright', 55, 1145, 75, 1575, 80, 110)
        self.imageSlicesRightLeft = self.imageSlicesLeftRight.copy()
        self.imageSlicesRightLeft.reverse()

        # Generate slices for front back
        sliceNum = math.ceil(80/self.sliceDepth)
        generateSlices('face2.stl', 'frontback', sliceNum+1)
        self.imageSlicesFrontBack = self._getImageSlices('STL/output/frontback', 55, 1145, 78, 1645, 76.6, 110)
        self.imageSlicesBackFront = self.imageSlicesFrontBack.copy()
        self.imageSlicesBackFront.reverse()

    def _getImageSlices(self, facePath, x0, x1, y0, y1, width, height):
        imageSlices = []
        for image_path in os.listdir(facePath):
            # create the full input path and read the file
            input_path = os.path.join(facePath, image_path)
            img = cv2.imread(input_path, 0)
            ratio = configurationMap['other']['mmPerPixelRatio']
            croppedIm = img[y0:y1, x0:x1]
            resizedIm = cv2.resize(croppedIm, (int(width/ratio), int(height/ratio)))
            ret,pim = cv2.threshold(resizedIm, 127, 255, cv2.THRESH_BINARY)
            imageSlices.append(pim)
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

    def _detectDrill(self, img, showFig=False):

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
        if showFig:
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('image', 80*2, 110*2)
            cv2.imshow('image', cimg)
            cv2.waitKey(0)

        # Convert from pixel to mm
        drillPointsMM = []
        for drillPoint in drillPoints:
            drillPointsMM.append(pixelPos2mmPos(drillPoint, img))

        return drillPointsMM

    def _detectLathe(self, img, showFig=False):
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

        if showFig:
            cv2.imshow('img', output)

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

    def generateMillCommands(self, showFig=False):
        """Generates the mill toolpath commands.

        The mill autonomous commands should go through each face and find the contour of the
        surface image. It then goes down to detect how deep each shape goes and generates the
        inner mills by eroding the image.

        Args:
            showFig (Boolean): Whether to show a visual representation of the mill path.

        """

        faceOrder = ['top', 'front', 'right', 'back', 'left']
        for facenum, imgSlices in enumerate([self.imageSlicesTopDown, self.imageSlicesFrontBack,
                                             self.imageSlicesRightLeft, self.imageSlicesBackFront,
                                             self.imageSlicesLeftRight]):

            # Reverse bw of imgSlices
            for imNum, im in enumerate(imgSlices):
                pim = ~im
                imgSlices[imNum] = pim

            # Go through each image and get list of matching shapes
            surfaceIm = imgSlices[0]
            pathListWithShapes = self._detectEdge(surfaceIm)
            cimg = cv2.cvtColor(surfaceIm, cv2.COLOR_GRAY2BGR)
            gotShapes = False
            for i,pathListPerShape in enumerate(pathListWithShapes):
                imageNum = 1
                # Loop through each shape
                currentDepth = 0
                while imageNum < len(imgSlices)-1 and self._shapeExistsInImg(
                        imgSlices[imageNum], pathListPerShape):
                    currentDepth += self.sliceDepth
                    imageNum += 1

                # Generate toolpaths
                depth = currentDepth
                borderPath = pathListPerShape
                # Shrink borderPath by mill radius
                centerPoint = getCenterPoint(borderPath)
                if depth > 0: # This means we will be milling inside the shapes
                    cv2.circle(cimg, (int(centerPoint[0]), int(centerPoint[1])), 10, (0, 0, 255), 4)
                    self.controller.commandGenerator.retractMill()
                    # Initial shrink half a mill diameter
                    millDepth = configurationMap['mill']['pushIncrement']
                    for d in incRange(millDepth, depth, millDepth) if depth > millDepth else [depth]:
                        shrunkIm = self._shrink(surfaceIm, mm2pixel(configurationMap['mill']['diameter'] / 2), 1)
                        shrunkShapePts = self._detectEdge(shrunkIm)
                        shrunkPath = self._getShrunkenPath(shrunkShapePts, centerPoint)
                        if shrunkPath != []:
                            gotShapes = True
                            # Show path being milled
                            self.millPixelPath(shrunkPath, imgSlices[imageNum], d, faceOrder[facenum])
                            if showFig:
                                for millPoint in shrunkPath:
                                    cv2.circle(cimg, millPoint, 3, (255, 0, 0), 1)

                            while True: # Keep shrinking until your shape has disappeared
                                shrunkIm = self._shrink(shrunkIm, mm2pixel(configurationMap['mill']['diameter'] / 2))
                                shrunkShapePts = self._detectEdge(shrunkIm)
                                if shrunkShapePts == []:
                                    break
                                shrunkPath = self._getShrunkenPath(shrunkShapePts, centerPoint)
                                self.millPixelPath(shrunkPath, imgSlices[imageNum], d, faceOrder[facenum])
                                # Show path being milled
                                if showFig:
                                    for millPoint in shrunkPath:
                                        cv2.circle(cimg, millPoint, 3, (0, 255, 0), 1)

            if showFig and gotShapes:
                cv2.namedWindow('Milling paths', cv2.WINDOW_NORMAL)
                # cv2.resizeWindow('Milling paths', 80 * 2, 110 * 2)
                cv2.imshow('Milling paths', cimg)
                cv2.waitKey(0)

            self.controller.commandGenerator.retractMill()

    def millPixelPath(self, millPath, im, depth, face):
        """Convert the mill path from pixels to mm then mill it out.

        Args:
            millPath (array(tuple)): A list of points that need to be milled out in pixels.
            im (Img): A cv2 image for dimension references.
            depth (float): The depth it needs to be milled into the foam.
            face (string): The surface face of the foam being worked on.

        """
        # Convert to mm
        if len(millPath) > 0:
            borderPathMM = []
            for pts in millPath:
                borderPathMM.append(pixelPos2mmPos(pts, im))
            (x0, z0) = borderPathMM[0]
            self.controller.commandGenerator.moveTo(self.controller.mill, x0, z0, face=face, retractFirst=False)
            self.controller.commandGenerator.millPointsSequence(borderPathMM, depth, face, closedLoop=True)

    def _shapeExistsInImg(self, img, pathList, mmAccuracy=1):
        pathListWithShapes = self._detectEdge(img)

        for pathListPerShape in pathListWithShapes:
            if tupleArrayInRange(pathListPerShape, pathList, mm2pixel(mmAccuracy)):
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

    def _shrink(self, img, numPixels, iterations=2):
        # Taking a matrix of size 5 as the kernel
        # kernel = np.ones((5, 5), np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (numPixels, numPixels))

        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(img, 127, 255, 0)

        # The first parameter is the original image,
        # kernel is the matrix with which image is
        # convolved and third parameter is the number
        # of iterations, which will determine how much
        # you want to erode/dilate a given image.
        img_erosion = cv2.erode(img, kernel, iterations=iterations)

        # cv2.imshow('Erosion', img_erosion)
        # cv2.waitKey(0)

        return img_erosion

    def _getShrunkenPath(self, shrunkShapePts, centerPoint):
        for shapePts in shrunkShapePts:
            shrunkCenterPoint = getCenterPoint(shapePts)
            # Check if distance is within acceptable range
            dx = centerPoint[0] - shrunkCenterPoint[0]
            dy = centerPoint[1] - shrunkCenterPoint[1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < mm2pixel(5):
                return shapePts
        return []



