import cv2
import numpy as np
import matplotlib.pyplot as plt

def detectDrill(img):
    # cv2.imshow('im',img)
    # get dimensions of image
    dimensions = img.shape
    # width, height
    width = img.shape[1]
    height = img.shape[0]

    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2.2, 100,
                                param1=100, param2=30, minRadius=40, maxRadius=47)

    drillPoints = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

            drillPoints.append((i[0]/width, i[1]/height))

    return drillPoints
    # cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
    # cv2.imshow('detected circles', cimg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
