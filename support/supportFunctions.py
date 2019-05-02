
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
