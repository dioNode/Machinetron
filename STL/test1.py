from Drill6mmCircleDetection import detectDrill
import cv2
import numpy as np


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


def _fillHole(img, pos, radius, state): # state is 1 for white, 0 for black
    cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
    # If state is 1 we want the hole filled white
    if state == 1:
        # the -1 signifies a filled circle (circle thickness)
        cv2.circle(img, pos, radius, (255, 255, 255), -1)
    # If the state is 0 we want the hole filled black
    else:
        cv2.circle(img, pos, radius, (0, 0, 0), -1)
    cv2.imshow('test1', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img

im = cv2.imread('output/frontback/face2_0000.png')

#testagain

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

_containsHole(im, (x1, y1), 40)
#_fillHole(im, (x1, y1), 100, 0)
