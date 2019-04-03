from Controller import Controller
import pygame
import math

class OutputSimulator:
    def __init__(self, controller):
        self.width = 150
        self.height = 150
        self.padding = 50
        self.motorDisplayRadius = 20

        pygame.font.init()
        self.titleFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.generalFont = pygame.font.SysFont('Comic Sans MS', 14)
        if isinstance(controller, Controller):
            self.controller = controller

    def update(self):
        width = self.width
        height = self.height
        padding = self.padding
        win = self.win
        motorDisplayTop = 2 * padding + height
        displayTop = padding
        controller = self.controller
        cutMachines = [controller.drill, controller.lathe, controller.mill]




        # Clear canvas
        win.fill((255, 255, 255))


        for i in range(3):
            x = padding + i * (padding + width)
            # Draw border rectangle
            self.updateEndeffactorDisplays(cutMachines, displayTop, i, win, x)
            # Draw motor angles
            self.updateMotorDisplay(cutMachines, i, motorDisplayTop, x)



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

    def updateEndeffactorDisplays(self, cutMachines, displayTop, i, win, x):
        endeffactorLocations = self.getEndeffactorLocations(cutMachines)
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
        width = self.width
        padding = self.padding
        pygame.init()
        screenWidth = padding + 3 * (padding + width)
        self.win = pygame.display.set_mode((screenWidth, 500))
        pygame.display.set_caption("Machinetron Outputs")


