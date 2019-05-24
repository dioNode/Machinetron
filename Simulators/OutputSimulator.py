from Controller import Controller
from config import configurationMap
import pygame
import math


class OutputSimulator:
    """This is the GUI that simulates how all the motors and outputs are being displayed.

    Args:
        controller (Controller): The main controller being used to get information on the motor settings.

    """
    def __init__(self, controller):
        # Window variables
        self.carryOn = True
        self.clock = pygame.time.Clock()

        # Dimension parameters
        self.width = 150
        self.height = 150
        self.padding = 50
        self.commandsDisplayWidth = 160
        self.commandsDisplayHeight = 500
        self.commandHeight = 40
        self.motorDisplayRadius = 20
        self.handlerDisplaySize = 30
        self.handlerDisplayWidth = self.width*3 + self.padding*2
        self.handlerDisplayHeight = 100

        # Top starting points for each section
        self.endeffactorDisplayTop = self.padding
        self.motorDisplayTop = int(self.padding * 1.5 + self.height)
        self.handlerDisplayTop = self.motorDisplayTop + self.motorDisplayRadius + self.padding
        self.handlerMotorDisplayTop = self.handlerDisplayTop + self.handlerDisplayHeight + self.padding

        pygame.font.init()
        self.titleFont = pygame.font.SysFont('Arial', 30)
        self.generalFont = pygame.font.SysFont('Arial', 14)

        self.screenHeight = self.commandsDisplayHeight + 2*self.padding
        self.screenWidth = 2 * self.padding + 3 * (self.padding + self.width) + self.commandsDisplayWidth

        self.screenClicked = False
        self.screenRightClicked = False
        self.status = 0

        if isinstance(controller, Controller):
            self.controller = controller

    def update(self):
        """Update the display of the GUI.

        Looks through and checks on the outputs returned from the controller. Note this does not directly look into the
        MicrocontrollerSimulator class because the system should only be able to discern the end location from the
        information relayed back to the main control unit.

        """
        if self.carryOn:
            # Check events
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.carryOn = False  # Flag that we are done so we exit this loop

            # Clear canvas
            win = self.win
            win.fill((255, 255, 255))

            # Variables
            motorDisplayTop = self.motorDisplayTop
            displayTop = self.endeffactorDisplayTop
            controller = self.controller
            cutMachines = [controller.drill, controller.lathe, controller.mill]

            # Display stuff
            for i in range(3):
                x = self.padding + i * (self.padding + self.width)
                # Draw border rectangle
                self.updateEndeffactorDisplays(cutMachines, displayTop, i, x)
                # Draw motor angles
                self.updateMotorDisplay(cutMachines, i, motorDisplayTop, x)

            self.updateHandlerDisplay(cutMachines)
            self.updateCommandsDisplay()
            self.updateGoButton()
            pygame.display.update()
        else:
            pygame.quit()

    def getEndeffactorLocations(self, cutMachines):
        """Gets the end locations of the cut machines.

        Args:
            cutMachines (list(CutMachine)): A list of all the cut machines.

        Returns:
            A list of the end locations of the cut machines.

        """
        endeffactorLocations = []
        controller = self.controller
        for cutMachine in cutMachines:
            endeffactorLocations.append([int(controller.handler.railMotor.currentDisplacement),
                                         int(cutMachine.vertMotor.currentDisplacement)])
        return endeffactorLocations

    def getMotorAngles(self, cutMachines):
        """Gets the motor angles for each cut machine.

        Args:
            cutMachines (list(CutMachine)): A list of all the cut machines.

        Returns:
            An 2D array of the angles for motor for each cut machine.

        """
        motorAngles = []
        for cutMachine in cutMachines:
            motorAngles.append([cutMachine.spinMotor.currentAngle(),
                                cutMachine.vertMotor.currentAngle(),
                                cutMachine.penMotor.currentAngle()])
        return motorAngles

    def updateHandlerDisplay(self, cutMachines):
        """Updates the display for the handler location.

        This includes the handler's location, shape and motors.

        Args:
            cutMachines(list(CutMachine)): A list of all the cut machines.

        """
        win = self.win
        height = self.handlerDisplayHeight
        width = self.handlerDisplayWidth
        titleFont = self.titleFont
        generalFont = self.generalFont
        y = self.handlerDisplayTop
        x = self.padding
        motorRadius = self.motorDisplayRadius
        handler = self.controller.handler

        # Draw the border around where handler can move around
        pygame.draw.rect(win, (0, 0, 0), (x, y + self.padding, width, height), 1)
        handlerMotors = [handler.railMotor, handler.flipMotor, handler.spinMotor]
        motorY = int(self.handlerMotorDisplayTop + motorRadius + self.padding/2)

        for j, motor in enumerate(handlerMotors):
            # Handler motors
            motorX = int(x + j * ((width - 2 * motorRadius) / 2) + motorRadius)
            pygame.draw.circle(win, (0, 0, 0), (motorX, motorY), motorRadius, 1)
            angle = math.radians(motor.currentAngle())
            deltaX = motorRadius * math.cos(angle)
            deltaY = motorRadius * math.sin(angle)
            pygame.draw.line(win, (0, 0, 0), (motorX, motorY),
                             (motorX + deltaX, motorY + deltaY))
            motorNames = {0: 'Rail', 1: 'Flip', 2: 'Spin'}
            textsurface = generalFont.render(motorNames[j], False, (0, 0, 0))
            win.blit(textsurface, (motorX - motorRadius, motorY + motorRadius))

        # Handler name label
        textsurface = titleFont.render(handler.name, False, (0, 0, 0))
        win.blit(textsurface, (x, y))

        # Handler location
        handlerX = handler.railMotor.currentDisplacement + self.padding
        length = self.handlerDisplaySize
        averageDim = (self.controller.xLength + self.controller.yLength + self.controller.zLength) / 2
        scale = averageDim / length
        handWidth = self.controller.xLength / scale
        handHeight = self.controller.yLength / scale
        mag = math.sqrt(math.pow(handWidth/2, 2) + math.pow(handHeight/2, 2))
        centerX = handlerX
        centerY = y + height/2 + self.padding/2 + length/2
        cornerAngle = math.atan(handHeight/handWidth)
        spinDiagAngle = math.radians(self.controller.handler.spinMotor.currentDisplacement)

        # These angles are with reference to horizontal but shouldn't matter
        xtr = mag * math.cos(cornerAngle + spinDiagAngle)
        ytr = mag * math.sin(cornerAngle + spinDiagAngle)
        xtl = -mag * math.cos(cornerAngle - spinDiagAngle)
        ytl = mag * math.sin(cornerAngle - spinDiagAngle)
        xbr = mag * math.cos(cornerAngle - spinDiagAngle)
        ybr = -mag * math.sin(cornerAngle - spinDiagAngle)
        xbl = -mag * math.cos(cornerAngle + spinDiagAngle)
        ybl = -mag * math.sin(cornerAngle + spinDiagAngle)

        pointlist = [(xtr + centerX, ytr + centerY),
                     (xbr + centerX, ybr + centerY),
                     (xbl + centerX, ybl + centerY),
                     (xtl + centerX, ytl + centerY)]

        pygame.draw.polygon(win, (0, 0, 0), pointlist)

        textsurface = generalFont.render(self.controller.facename, False, (0, 0, 0))
        win.blit(textsurface, (centerX, centerY + length/2))

        # CutMachines display to show their location relative to Handler
        for cutMachine in cutMachines:
            machineX = cutMachine.homeX + x - self.controller.currentFaceWidth/2
            machineY = y + self.padding
            machineHeight = 10
            machineWidth = self.controller.currentFaceWidth
            pygame.draw.rect(win, (0, 1, 1),
                             (machineX, machineY, machineWidth, machineHeight))

    def updateMotorDisplay(self, cutMachines, i, motorDisplayTop, x):
        """Updates the motor display for each of the cut machines.

        Args:
            cutMachines (list(CutMachine)): A list of all the cut machines.
            i (int): The index of cut machine to be focused on.
            motorDisplayTop (double): The top offset of the motor display.
            x (double): The left offset of the motor display.

        """
        width = self.width
        motorRadius = self.motorDisplayRadius
        titleFont = self.titleFont
        motorAngles = self.getMotorAngles(cutMachines)
        win = self.win
        for j in range(3):
            motorX = int(x + j * ((width - 2 * motorRadius) / 2) + motorRadius)
            motorY = motorDisplayTop + motorRadius
            pygame.draw.circle(win, (0, 0, 0), (motorX, motorY), motorRadius, 1)
            angle = math.radians(motorAngles[i][j])
            deltaX = motorRadius * math.cos(angle)
            deltaY = motorRadius * math.sin(angle)
            pygame.draw.line(win, (0, 0, 0), (motorX, motorY),
                             (motorX + deltaX, motorY + deltaY))
            motorNames = {0: 'Spin', 1: 'Vert', 2: 'Pen'}
            textsurface = self.generalFont.render(motorNames[j], False, (0, 0, 0))
            win.blit(textsurface, (motorX - motorRadius, motorY + motorRadius))
        textsurface = titleFont.render(cutMachines[i].name, False, (0, 0, 0))
        win.blit(textsurface, (x, 0))

    def updateEndeffactorDisplays(self, cutMachines, displayTop, i, x):
        """Updates the cutting tool display for each of the cut machines.

        Args:
            cutMachines (list(CutMachine)): A list of all the cut machines.
            i (int): The index of cut machine to be focused on.
            displayTop (double): The top offset of the cutting tool display.
            x (double): The left offset of the cutting tool display.

        """
        endeffactorLocations = self.getEndeffactorLocations(cutMachines)
        cutmachineName = cutMachines[i].name.lower()
        # Draw the outer boundary box
        win = self.win
        height = self.height
        width = self.width
        pygame.draw.rect(win, (0, 0, 0), (x, displayTop, width, height), 1)
        faceWidth = int(self.controller.currentFaceWidth)
        faceHeight = int(self.controller.currentFaceHeight)
        # Draw the green foam box
        faceX = int(x + width / 2 - faceWidth / 2)
        faceY = int(displayTop + height / 2 - faceHeight / 2)
        pygame.draw.rect(win, (31, 142, 33), (faceX, faceY, faceWidth, faceHeight))
        # Draw the depth indicator
        currentDepth = round(cutMachines[i].penMotor.currentDisplacement, 1)
        faceThickness = self.controller.currentFaceDepth
        if self.controller.facename == 'top':
            distance2face = configurationMap[cutmachineName]['offsets']['cuttingBit2HandlerFlipBase'] - faceThickness
            cuttingBitHeightOffset = configurationMap[cutmachineName]['offsets']['cuttingBitHeightOffsetFlipped']
        else:
            distance2face = configurationMap[cutmachineName]['offsets']['cuttingBit2HandlerCenter'] - faceThickness/2
            cuttingBitHeightOffset = configurationMap[cutmachineName]['offsets']['cuttingBitHeightOffset']
        textsurface = self.generalFont.render(str(currentDepth) + ' | ' + str(distance2face), False, (0, 0, 0))
        win.blit(textsurface, (faceX + faceWidth/2, faceY + faceHeight/2))

        handlerX = self.controller.handler.railMotor.currentDisplacement

        endeffactorLocationX = int(handlerX - cutMachines[i].homeX + self.controller.currentFaceWidth/2)

        shade = 250 - cutMachines[i].penMotor.currentDisplacement
        shade = 20 if shade < 20 else shade
        shade = 255 if shade >= 255 else shade

        circleColour = (shade, shade, shade)

        offset = 10

        if endeffactorLocationX <= -offset:
            endeffactorLocationX = -offset
            circleColour = (200, 200, 200)
        elif endeffactorLocationX >= faceWidth + offset:
            endeffactorLocationX = faceWidth + offset
            circleColour = (200, 200, 200)

        endeffactorLocationX += faceX

        endeffactorLocationY = -endeffactorLocations[i][1] + self.controller.currentFaceHeight + int(faceY) + cuttingBitHeightOffset
        machineName = cutMachines[i].name.lower()
        # Draw the little end effactor location
        if machineName != 'lathe':
            pointRadius = round(configurationMap[machineName]['diameter'] / 2)
            angle = math.radians(cutMachines[i].spinMotor.currentDisplacement)
            deltaX = pointRadius * math.cos(angle)
            deltaY = pointRadius * math.sin(angle)
            pygame.draw.circle(win, circleColour, (endeffactorLocationX, endeffactorLocationY), pointRadius)
            pygame.draw.line(win, (0, 0, 0), (endeffactorLocationX, endeffactorLocationY),
                             (endeffactorLocationX + deltaX, endeffactorLocationY + deltaY))
        else:
            cutHeight = configurationMap[machineName]['length']
            cutWidth = 2
            pygame.draw.rect(win, circleColour, (endeffactorLocationX - cutWidth/2, endeffactorLocationY - cutHeight,
                                                 cutWidth, cutHeight))

    def updateCommandsDisplay(self):
        """Displays the list of commands in the queue."""
        currentCommand = self.controller.currentCommand
        commandQueue = self.controller.commandQueue
        win = self.win
        height = self.commandsDisplayHeight
        width = self.commandsDisplayWidth
        titleFont = self.titleFont
        generalFont = self.generalFont
        x = self.screenWidth - width - self.padding
        y = self.padding
        pygame.draw.rect(win, (0, 0, 0), (x, y, width, height), 1)
        textsurface = titleFont.render('Commands', False, (0, 0, 0))
        win.blit(textsurface, (x, 0))
        # Draw the commands inside
        if not currentCommand == None:
            pygame.draw.rect(win, (220, 220, 250), (x+1, y+1, width-2, self.commandHeight-2))
            textsurface = generalFont.render(currentCommand.name, False, (0, 0, 0))
            win.blit(textsurface, (x+3, y))
        for commandNum in range(min(12, len(commandQueue))):
            commandName = commandQueue[commandNum].name
            textsurface = generalFont.render(commandName, False, (0, 0, 0))
            win.blit(textsurface, (x+3, y + (commandNum + 1) * self.commandHeight))

    def simulate(self):
        """Initialises the settings necessary to start the GUI."""
        pygame.init()

        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Machinetron Outputs")

    def updateGoButton(self):
        """Display Go Button"""
        radius = 15
        status = self.controller.state
        if status == 1:
            colour = (0, 128, 0)
        elif status == 0:
            colour = (255, 0, 0)
        else:
            colour = (255, 165, 0)
        pygame.draw.circle(self.win, colour, (200, self.handlerDisplayTop + radius), radius)
        click = pygame.mouse.get_pressed()[0]
        if click == 1:
            self.screenClicked = True
        else:
            if self.screenClicked:
                self.controller.goButtonClicked()
            self.screenClicked = False

        rightClick = pygame.mouse.get_pressed()[2]
        if rightClick == 1:
            self.screenRightClicked = True
        else:
            if self.screenRightClicked:
                self.controller.resetCurrentCommand()
            self.screenRightClicked = False


