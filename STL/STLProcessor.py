from STL.Drill6mmCircleDetection import detectDrill

from STL.stl2png import generateSlices
from scipy import ndimage, misc
import numpy as np
import os
import cv2

class STLProcessor:
    def generateCommands(self, filename, controller):
        self.controller = controller
        # generateSlices(filename)
        outPath = "STL\output"
        path = "STL\output"

        # iterate through the names of contents of the folder
        for image_path in os.listdir(path):
            # create the full input path and read the file
            input_path = os.path.join(path, image_path)
            img = cv2.imread(input_path, 0)
            detectDrill(img)



