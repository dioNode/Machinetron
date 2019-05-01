from Drill6mmCircleDetection import detectDrill
import cv2
import numpy as np

def _containsHole(img, pos, radius):
    x, y = pos
    #img[y+10:y+100,x+50:x+100] = (0,0,0)
    threshold_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
    cv2.imshow('test1', threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # x and y input swapped for this argument for some reason
    if np.any(threshold_image[y, x] == 0):
        print('true')
        return True
    else:
        print('false')
        return False

def _fillHole(img, pos, radius, state): # state is 1 for white, 0 for black

    threshold_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('test1', cv2.WINDOW_NORMAL)
    # If state is 1 we want the hole filled white
    if state == 1:
        # the -1 signifies a filled circle (circle thickness)
        cv2.circle(threshold_image, pos, radius, (255, 255, 255), -1)
    # If the state is 0 we want the hole filled black
    else:
        cv2.circle(threshold_image, pos, radius, (0, 0, 0), -1)
    cv2.imshow('test1', threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img

im = cv2.imread('output/frontback/face2_0000.png')

height = np.size(im, 0)
print('height', height)
width = np.size(im, 1)
print('width', width)
x1 = round(width*0.261666666)
y1 = round(height*0.74825986)
print('x1', x1)
print('y1', y1)
a = detectDrill(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
print(a)

_containsHole(im, (x1, y1), 100)
_fillHole(im, (x1, y1), 100, 0)
