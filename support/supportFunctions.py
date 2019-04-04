
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