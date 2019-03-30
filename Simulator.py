import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import operator

from Controller import Controller
from supportFunctions import real2PlotDim, plotDim2Real

class Simulator:
    """Simulates the action commands given by the user.
    
    This doesn't necessarily have to work with the controller and should
    actually be independant of it. Based on the user's commands, it should
    roughly model what the user should expect. Note it should not be 
    computationally heavy and should just give the user a very basic idea of
    what to expect.
    
    Attributes:
        controller (Controller): The controller used to control MACHINETRON.
        fig (PyPlot.Figure): A figure to display everything in the simulation.
    
    """
    def __init__(self, controller, fig):
        print("Simulator created...")
        if isinstance(controller, Controller):
            print("controller valid")
            self.controller = controller
            self.ax = Axes3D(fig)
        
        self.blockInstructions = []
            
    def simulate(self):
        
        self.addFoamBlock()
        for block in self.blockInstructions:
            lengths, offsets, face_color = block
            self.addRectangle(lengths, offsets, 'cyan', 0.3)
            
        plt.show()

    

    def addFoamBlock(self):
        ax = self.ax
        
        lengths = real2PlotDim(self.controller.getLengths())
        offsets = ((0,0,0))
        
        ax.set_xlim3d(0,lengths[0])
        ax.set_ylim3d(0,lengths[1])
        ax.set_zlim3d(0,lengths[2])
        ax.set_aspect('equal')
        
        face_color = [0.5, 0.5, 1] 
        
        self.addRectangle(lengths, offsets, face_color)

    def addRectangle(self, lengths, offsets, face_color, alpha=0.1):
        ax = self.ax
        
        xLength, yLength, zLength = lengths
        
        # Do corners
        verts = [[(0,0,0), (0,yLength,0), (0,yLength,zLength), (0,0,zLength)],
                 [(xLength,0,0), (xLength,yLength,0), (xLength,yLength,zLength), (xLength,0,zLength)],
                 [(0,0,0), (xLength,0,0), (xLength,0,zLength), (0,0,zLength)],
                 [(0,yLength,0), (xLength,yLength,0), (xLength,yLength,zLength), (0,yLength,zLength)],
                 [(0,0,0), (xLength,0,0), (xLength,yLength,0), (0,yLength,0)],
                 [(0,0,zLength), (xLength,0,zLength), (xLength,yLength,zLength), (0,yLength,zLength)],
                 ]
        
        # Add offsets
        for vertNum, vert in enumerate(verts):
            for pointNum, point in enumerate(vert):
                ele = verts[vertNum][pointNum]
                verts[vertNum][pointNum] = tuple(map(operator.add, offsets, ele))
    
    
        collection = Poly3DCollection(verts, linewidths=1, alpha=alpha, edgecolors="black")
        
        collection.set_facecolor(face_color)
        ax.add_collection3d(collection)
        ax.autoscale_view()
        
    
        
    def reshapeFrontM(self, widthHeightTuples):
        currentHeight = 0
        for widthHeightTuple in widthHeightTuples:
            zLength = widthHeightTuple[0]
            yLength = widthHeightTuple[1]
            xLength = self.controller.getLengths()[0]
            lengths = real2PlotDim((xLength, yLength, zLength))
            yOffset = currentHeight
            xOffset = 0
            zOffset = (self.controller.getLengths()[2] - zLength)/2
            offsets = real2PlotDim((xOffset, yOffset, zOffset))
            self.blockInstructions.append((lengths, offsets, 'cyan'))
            currentHeight += yLength
        
        
        
        