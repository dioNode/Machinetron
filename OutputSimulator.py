from Controller import Controller
import pygame
import math

class OutputSimulator:
    def __init__(self, controller):
        self.width = 150
        self.height = 150
        self.padding = 50
        self.motorDisplayRadius = 20
        self.handlerDisplaySize = 30
        self.handlerDisplayWidth = self.width*3 + self.padding*2
        self.handlerDisplayHeight = 150

        # Top starting points for each section
        self.endeffactorDisplayTop = self.padding
        self.motorDisplayTop = int(self.padding * 1.5 + self.height)
        self.handlerDisplayTop = self.motorDisplayTop + self.motorDisplayRadius + self.padding
        self.handlerMotorDisplayTop = self.handlerDisplayTop + self.handlerDisplayHeight + self.padding

        pygame.font.init()
        self.titleFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.generalFont = pygame.font.SysFont('Comic Sans MS', 14)

        self.screenHeight = 600
        self.screenWidth = self.padding + 3 * (self.padding + self.width)

        if isinstance(controller, Controller):
            self.controller = controller


    def update(self):
        win = self.win
        motorDisplayTop = self.motorDisplayTop
        displayTop = self.endeffactorDisplayTop
        controller = self.controller
        cutMachines = [controller.drill, controller.lathe, controller.mill]




        # Clear canvas
        win.fill((255, 255, 255))


        for i in range(3):
            x = self.padding + i * (self.padding + self.width)
            # Draw border rectangle
            self.updateEndeffactorDisplays(cutMachines, displayTop, i, x)
            # Draw motor angles
            self.updateMotorDisplay(cutMachines, i, motorDisplayTop, x)

        self.updateHandlerDisplay()

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

    def updateHandlerDisplay(self):
        win = self.win
        height = self.handlerDisplayHeight
        width = self.handlerDisplayWidth
        titleFont = self.titleFont
        y = self.handlerDisplayTop
        x = self.padding
        motorRadius = self.motorDisplayRadius
        handler = self.controller.handler

        pygame.draw.rect(win, (0, 0, 0), (x, y + self.padding, width, height), 1)
        handlerMotors = [handler.railMotor, handler.flipMotor, handler.spinMotor]

        for j in range(3):
            motorX = int(x + j * ((width - 2 * motorRadius) / 2) + motorRadius)
            motorY = int(self.handlerMotorDisplayTop + motorRadius + self.padding/2)
            pygame.draw.circle(win, (0, 0, 0), (motorX, motorY), motorRadius, 1)
            angle = math.radians(handlerMotors[j].currentAngle())
            deltaX = motorRadius * math.cos(angle)
            deltaY = motorRadius * math.sin(angle)
            pygame.draw.line(win, (0, 0, 0), (motorX, motorY), (motorX + deltaX, motorY + deltaY))
            motorNames = {0: 'Rail', 1: 'Flip', 2: 'Spin'}
            textsurface = self.generalFont.render(motorNames[j], False, (0, 0, 0))
            win.blit(textsurface, (motorX - motorRadius, motorY + motorRadius))
        textsurface = titleFont.render(handler.name, False, (0, 0, 0))
        win.blit(textsurface, (x, y))

        handlerX = handler.railMotor.currentDisplacement + self.padding
        length = self.handlerDisplaySize
        pygame.draw.rect(win, (0, 0, 0), (handlerX, y + height/2, length, length))


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
            pygame.draw.line(win, (0, 0, 0), (motorX, motorY), (motorX + deltaX, motorY + deltaY))
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
        faceWidth = int(self.controller.xLength)
        faceHeight = int(self.controller.zLength)
        faceX = int(x + width / 2 - faceWidth / 2)
        faceY = int(displayTop + height / 2 - faceHeight / 2)
        pygame.draw.rect(win, (31, 142, 33), (faceX, faceY, faceWidth, faceHeight))
        # endeffactorLocatonX = endeffactorLocations[i][0] + int(faceX)
        handlerX = self.controller.handler.railMotor.currentDisplacement

        endeffactorLocationX = int(handlerX - cutMachines[i].homeX)

        if endeffactorLocationX < 0:
            endeffactorLocationX = 0
        elif endeffactorLocationX > faceWidth:
            endeffactorLocationX = faceWidth

        endeffactorLocationX += faceX

        endeffactorLocationY = endeffactorLocations[i][1] + int(faceY)
        pygame.draw.circle(win, (0, 1, 0), (endeffactorLocationX, endeffactorLocationY), 5)

    def simulate(self):
        pygame.init()

        self.win = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Machinetron Outputs")


