# Python program to demonstrate erosion and
# dilation of images.
import cv2
import numpy as np

# Reading the input image
img = cv2.imread('dump/topdown10.png', 0)

# Taking a matrix of size 5 as the kernel
kernel = np.ones((5, 5), np.uint8)

# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img, 127, 255, 0)
img = ~img

# The first parameter is the original image,
# kernel is the matrix with which image is
# convolved and third parameter is the number
# of iterations, which will determine how much
# you want to erode/dilate a given image.
img_erosion = cv2.erode(img, kernel, iterations=50)
# img_dilation = cv2.dilate(img, kernel, iterations=20)

cv2.imshow('Input', img)
cv2.imshow('Erosion', img_erosion)
# cv2.imshow('Dilation', img_dilation)

cv2.waitKey(0)