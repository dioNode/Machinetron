from Drill6mmCircleDetection import detectDrill
import cv2
import numpy as np
import matplotlib.pyplot as plt


def _containsHole(img, pos, radius, state=0): #default hole is black
    height = np.size(img, 0)
    print('height', height)
    width = np.size(img, 1)
    print('width', width)

    if state == 0:
        mask = np.zeros((height, width, 3), np.uint8)
        cv2.circle(mask, pos, radius, (255, 255, 255), -1)
        multiplied_image = cv2.multiply(img, mask)

        cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
        cv2.imshow('test1', multiplied_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
        if sum(sum(sum(multiplied_image))) == 0:
            print('true')
            return True
        else:
            print('false')
            return False
    else:
        # Want mask to be opposite to hole mask since a lathe will be white not black
        mask = np.zeros((height, width, 3), np.uint8)
        mask[:, :] = (255, 255, 255)
        cv2.circle(mask, pos, radius, (0, 0, 0), -1)
        multiplied_image = cv2.multiply(img, mask)

        cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
        cv2.imshow('test1', multiplied_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Count the number of white pixels in image (Change from 0 to maybe < 10 to account for error)
        if sum(sum(sum(multiplied_image))) == 0:
            print('true')
            return True
        else:
            print('false')
            return False


def _fillHole(img, pos, radius, state):#state=1(fill inside circle white for drill),state=0(fill outside white for lathe)
    cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
    # If state is 1 we want the hole filled white
    if state == 1:
        # the -1 signifies a filled circle (circle thickness)
        cv2.circle(img, pos, radius, (255, 255, 255), -1)
    # If the state is 0 we want the outside filled white for the lathe
    else:
        #Offset a circle 400 radius and draw a white circle with thickness 2*400 to fill outside of lathe circle white
        cv2.circle(img, pos, radius+400, (255, 255, 255), 800)
    cv2.imshow('test1', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


def _detectEdge(img):
    #detect the edges of the mill using canny edge detector
    edges = cv2.Canny(img, 100, 255)
    #use contours to have the coordinates in an ordered fashion to use a straight line between consecutive points
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #make the contour list more readable
    contourList = np.array([list(pt[0]) for ctr in contours for pt in ctr])
    #extract all x and y points from contours
    x = contourList[:,1]
    y = contourList[:,0]
    #create a list of tuples (x, y) which is ordered, sequencing through them will give the toolpath
    toolpathList = list(zip(x, y))
    #cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
    #cv2.imshow('test1', edges)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    plt.scatter(x[:1000], y[:1000])
    plt.show()
    return contours, toolpathList

def _shrink(contours):
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


def _expand(contours):
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
    coef_x = (xdifference + 100) / xdifference
    coef_y = (ydifference + 100) / ydifference

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







im = cv2.imread('dump/topdown5.png')

#testagain again

height = np.size(im, 0)
print('height', height)
width = np.size(im, 1)
print('width', width)
x1 = round(width*0.26166666666666666)
y1 = round(height*0.7482598607888631)
print('x1', x1)
print('y1', y1)
a = detectDrill(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
print(a)

#_containsHole(im, (x1, y1), 40)
_fillHole(im, (383, 400), 348, 0)
#contours, toolpathList = _detectEdge(im)
#contours, toolpathList = _shrink(contours)
#_expand(contours)

