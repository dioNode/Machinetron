import sys, getopt
import numpy
from stl import mesh
import math

rx = 90
ry = 0
rz = 0

# Change this name to the required file
# (example: for part2.stl just type in 'part2')
stl_filename = 'part2'

for i in range(4):
    your_mesh = mesh.Mesh.from_file(stl_filename+'.stl')
    your_mesh.rotate([1.0, 0.0, 0.0], math.radians(rx))
    your_mesh.rotate([0.0, 1.0, 0.0], math.radians(ry))
    your_mesh.rotate([0.0, 0.0, 1.0], math.radians(rz))
    your_mesh.save(stl_filename+'face'+str(i+2)+'.stl')
    i += 1
    ry += 90

