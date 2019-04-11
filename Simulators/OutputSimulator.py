from Controller import Controller
import pygame
import math

class OutputSimulator:
    def __init__(self, controller):
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
        self.titleFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.generalFont = pygame.font.SysFont('Comic Sans MS', 14)

        self.screenHeight = self.commandsDisplayHeight + 2*self.padding
        self.screenWidth = 2 * self.padding + 3 * (self.padding + self.width) + self.commandsDisplayWidth

        if isinstance(controller, Controller):
            self.controller = controller


    def update(self):
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

        pygame.display.update()


    def getEndeffactorLocations(self, cutMachines):
        endeffactorLocations = []
        controller = self.controller
        for cutMachine in cutMachines:
            endeffactorLocations.append([int(controller.handler.railMotor.currentDisplacement),
                                         int(cutMachine.vertMotor.currentDisplacement)])
        return endeffactorLocations

    def getMotorAngles(self, cutMachines):
        motorAngles = []
        for cutMachine in cutMachines:
            motorAngles.append([cutMachine.spinMotor.currentAngle(),
                                cutMachine.vertMotor.currentAngle(),
                                cutMachine.penMotor.currentAngle()])
        return motorAngles

    def updateHandlerDisplay(self, cutMachines):
        win = self.win
        height = self.handlerDisplayHeight
        width = self.handlerDisplayWidth
        titleFont = self.titleFont
        y = self.handlerDisplayTop
        x = self.padding
        motorRadius = self.motorDisplayRadius
        handler = self.controller.handler

        # Draw the border around where handler can move around
        pygame.draw.rect(win, (0, 0, 0), (x, y + self.padding, width, height), 1)
        handlerMotors = [handler.railMotor, handler.flipMotor, handler.spinMotor]
        motorY = int(self.handlerMotorDisplayTop + motorRadius + self.padding/2)

        for j in range(3):
            # Handler motors
            motorX = int(x + j * ((width - 2 * motorRadius) / 2) + motorRadius)
            pygame.draw.circle(win, (0, 0, 0), (motorX, motorY), motorRadius, 1)
            angle = math.radians(handlerMotors[j].currentAngle())
            deltaX = motorRadius * math.cos(angle)
            deltaY = motorRadius * math.sin(angle)
            pygame.draw.line(win, (0, 0, 0), (motorX, motorY),
                             (motorX + deltaX, motorY + deltaY))
            motorNames = {0: 'Rail', 1: 'Flip', 2: 'Spin'}
            textsurface = self.generalFont.render(motorNames[j], False, (0, 0, 0))
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

        # CutMachines display to show their location relative to Handler
        for cutMachine in cutMachines:
            machineX = cutMachine.homeX + x - self.controller.currentFaceWidth/2
            machineY = y + self.padding
            machineHeight = 10
            machineWidth = self.controller.currentFaceWidth
            pygame.draw.rect(win, (0, 1, 1),
                             (machineX, machineY, machineWidth, machineHeight))


    def updateMotorDisplay(self, cutMachines, i, motorDisplayTop, x):
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
        endeffactorLocations = self.getEndeffactorLocations(cutMachines)
        win = self.win
        height = self.height
        width = self.width
        pygame.draw.rect(win, (0, 0, 0), (x, displayTop, width, height), 1)
        faceWidth = int(self.controller.currentFaceWidth)
        faceHeight = int(self.controller.currentFaceHeight)
        faceX = int(x + width / 2 - faceWidth / 2)
        faceY = int(displayTop + height / 2 - faceHeight / 2)
        pygame.draw.rect(win, (31, 142, 33), (faceX, faceY, faceWidth, faceHeight))
        handlerX = self.controller.handler.railMotor.currentDisplacement

        endeffactorLocationX = int(handlerX - cutMachines[i].homeX + self.controller.currentFaceWidth/2)

        shade = 250 - cutMachines[i].penMotor.currentDisplacement
        shade = 20 if shade < 20 else shade
        shade = 255 if shade >= 255 else shade

        circleColour = (shade, shade, shade)

        if endeffactorLocationX <= 0:
            endeffactorLocationX = 0
            circleColour = (200, 200, 200)
        elif endeffactorLocationX >= faceWidth:
            endeffactorLocationX = faceWidth
            circleColour = (200, 200, 200)

        endeffactorLocationX += faceX

        endeffactorLocationY = endeffactorLocations[i][1] + int(faceY)
        pointRadius = 5
        angle = math.radians(cutMachines[i].spinMotor.currentDisplacement)
        deltaX = pointRadius * math.cos(angle)
        deltaY = pointRadius * math.sin(angle)
        pygame.draw.circle(win, circleColour, (endeffactorLocationX, endeffactorLocationY), pointRadius)
        pygame.draw.line(win, (0, 0, 0), (endeffactorLocationX, endeffactorLocationY),
                         (endeffactorLocationX + deltaX, endeffactorLocationY + deltaY))

    def updateCommandsDisplay(self):
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
        for commandNum in range(12):
            commandName = commandQueue[commandNum].name
            textsurface = generalFont.render(commandName, False, (0, 0, 0))
            win.blit(textsurface, (x+3, y + (commandNum + 1) * self.commandHeight))

    def simulate(self):
        pygame.init()

        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Machinetron Outputs")


