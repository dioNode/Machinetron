import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

# Create a new plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('part2.STL')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
test = np.meshgrid(your_mesh)
print(len(test[0]))

# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
plt.show()


plt.plot(your_mesh.points[0][0:3])
plt.show()