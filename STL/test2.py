
import numpy as np

import cv2
from support.supportFunctions import pixelPos2mmPos, pixel2mm, mmPos2PixelPos, mm2pixel, inRange
from config import configurationMap

def _containsHole(img, pos, radius, state=0):  # default hole is black
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
        cv2.circle(mask, pos, radius, (255, 255, 255), -1)



        mask = cv2.bitwise_not(mask)

        multiplied_image = cv2.multiply(img, mask)

        # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
        if sum(sum(multiplied_image)) == 0:
            return True
        else:
            return False




        # # Want mask to be opposite to hole mask since a lathe will be white not black
        # mask = np.zeros((height, width, 3), np.uint8)
        # mask[:, :] = (255, 255, 255)
        # cv2.circle(mask, pos, radius, (0, 0, 0), -1)
        # multiplied_image = cv2.multiply(img, mask)
        #
        # # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
        # if sum(sum(sum(multiplied_image))) == 0:
        #     return True
        # else:
        #     return False





img = cv2.imread('output/topdown/part0_0006.png', 0)

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

        lathePoints.append((x,y,r))

# Convert from pixel to mm
lathePointsMM = []
for lathePoint in lathePoints:
    pos = (lathePoint[0], lathePoint[1])
    radius = lathePoint[2]
    lathePointMM = pixelPos2mmPos(pos, img)
    radiusMM = pixel2mm(radius)
    mmHeight = pixel2mm(height)
    if inRange(lathePointMM, (0, mmHeight/2), configurationMap['other']['mmError']):
        lathePointsMM.append((radiusMM, lathePointMM))

print(lathePointsMM)

radius, pos = lathePointsMM[0]
pxRadius = mm2pixel(radius*1.2)
pxPos = mmPos2PixelPos(pos, img)
print(_containsHole(img, pxPos, pxRadius, 1))













