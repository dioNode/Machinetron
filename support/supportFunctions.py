from config import configurationMap
import numpy as np


def real2PlotDim(axValues):
    """Converts real coordinates to values to be plotted.
    
    Args:
        axValues (tuple): (x,y,z) values in tuple format.
        
    Returns:
        tuple: (x,y,z) values for real world.
    
    """
    return ((axValues[0], axValues[2], axValues[1]))

def plotDim2Real(realValues):
    return ((realValues[0], realValues[2], realValues[1]))


# Recursive dictionary merge
# Copyright (C) 2016 Paul Durivage <pauldurivage+github@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import collections

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def getLinearVelocityTime(u, v, s):
    t = (s - 0.5*(v-u))/u
    return t


def clearFolder(folder):
    import os
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def unique(myArray): # Used for 2d array
    output = []
    for myList in myArray:
        for ele in myList:
            if ele not in output:
                output.append(ele)
    return output


def mm2pixel(val, ratio=None):
    if ratio is None:
        ratio = configurationMap['other']['mmPerPixelRatio']
    return int(round(val / ratio))


def pixel2mm(val, ratio=None): # Ratio is mm/pixel
    if ratio is None:
        ratio = configurationMap['other']['mmPerPixelRatio']
    return val * ratio


def mmPos2PixelPos(pos, im, ratio=None):
    if ratio is None:
        ratio = configurationMap['other']['mmPerPixelRatio']
    pxheight, pxwidth = im.shape
    posX = int(round(mm2pixel(pos[0], ratio) + pxwidth/2))
    posY = int(round(pxheight - mm2pixel(pos[1], ratio)))
    return posX, posY


def pixelPos2mmPos(pos, im, ratio=None):
    if ratio is None:
        ratio = configurationMap['other']['mmPerPixelRatio']
    pxheight, pxwidth = im.shape
    posX = pixel2mm(pos[0] - pxwidth/2, ratio)
    posY = pixel2mm(pxheight - pos[1], ratio)
    return round(posX,1), round(posY,1)


def inRange(currentPos, desiredPos, errorRange):
    differenceX, differenceY = tuple(np.subtract(desiredPos, currentPos))
    return abs(differenceX) <= errorRange and abs(differenceY) <= errorRange

def tupleArrayInRange(currentTupleArray, desiredTupleArray, errorRange):
    if len(currentTupleArray) != len(desiredTupleArray):
        return False

    isInRange = True
    for i, currentTuple in enumerate(currentTupleArray):
        desiredTuple = desiredTupleArray[i]
        isInRange &= inRange(currentTuple, desiredTuple, errorRange)

    return isInRange


def cropImage(img):
    h, w = img.shape
    offset = 10
    crop_img = img[offset: h-offset, offset: w-offset]
    return crop_img

def splitNumberHex(val):
    hexval = int(round(val))
    mshalf = (hexval & 0xFF00) >> 8
    lshalf = hexval & 0xFF
    return mshalf, lshalf


def getCenterPoint(pointsList):
    # Sum up points
    centerPoint = (0, 0)
    for (x, y) in pointsList:
        cx,cy = centerPoint
        centerPoint = (x + cx, y + cy)
    # Average out points
    numpoints = len(pointsList)
    cx, cy = centerPoint
    return cx/numpoints, cy/numpoints


def posListMatches(ptsListOrg, ptsListCmp, errorThresh=0):
    # Check size equals
    if len(ptsListOrg) != len(ptsListCmp):
        return False
    # Go through original list
    for ptsOrg in ptsListOrg:
        # Go through compare list
        for ptsCmp in ptsListCmp:
            # Remove points when they match
            if inRange(ptsOrg, ptsCmp, errorThresh):
                ptsListCmp.remove(ptsCmp)
                break
    return len(ptsListCmp) == 0



