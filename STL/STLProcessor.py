from STL.stl2png import generateSlices

class STLProcessor:
    def generateCommands(self, filename, controller):
        self.controller = controller
        generateSlices(filename)



