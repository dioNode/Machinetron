from Controller import Controller
import pygame
import math

class OutputSimulator:
    def __init__(self, controller):
        self.width = 150
        self.height = 150
        self.padding = 50
        if isinstance(controller, Controller):
            self.controller = controller

    def update(self):
        width = self.width
        height = self.height
        padding = self.padding
        win = self.win
        motorDisplayTop = 2 * padding + height
        motorRadius = 20



        railMotor = self.controller.handler.railMotor
        flipMotor = self.controller.handler.flipMotor
        spinMotor = self.controller.handler.spinMotor

        motorAngles = [[railMotor.currentAngle(), flipMotor.currentAngle(), spinMotor.currentAngle()],
                       [0, 45, 90],
                       [120, 270, 0]]

        endeffactorLocations = [[railMotor.currentDisplacement, spinMotor.currentDisplacement],
                                [0, 45],
                                [10, 50]]


        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False

        win.fill((255, 255, 255))

        for i in range(3):
            x = padding + i * (padding + width)
            pygame.draw.rect(win, (0, 0, 0), (x, padding, width, height), 1)
            endeffactorLocatonX = endeffactorLocations[i][0] + x
            endeffactorLocatonY = endeffactorLocations[i][1] + padding
            pygame.draw.circle(win, (0, 1, 0), (endeffactorLocatonX, endeffactorLocatonY), 5)

            for j in range(3):
                self.updateMotor(i, j, motorAngles, motorDisplayTop, motorRadius, width, win, x)

        pygame.display.update()

        # for i in range(3):
        #     for j in range(3):
        #         motorAngles[i][j] += 10

        # pygame.quit()

    def updateMotor(self, i, j, motorAngles, motorDisplayTop, motorRadius, width, win, x):
        motorX = int(x + j * ((width - 2 * motorRadius) / 2) + motorRadius)
        motorY = motorDisplayTop + motorRadius
        pygame.draw.circle(win, (0, 0, 0), (motorX, motorY), motorRadius, 1)
        angle = math.radians(motorAngles[i][j])
        deltaX = motorRadius * math.cos(angle)
        deltaY = motorRadius * math.sin(angle)
        pygame.draw.line(win, (0, 0, 0), (motorX, motorY), (motorX + deltaX, motorY + deltaY))

    def simulate(self):
        width = self.width
        height = self.height
        padding = self.padding
        pygame.init()
        screenWidth = padding + 3 * (padding + width)
        self.win = pygame.display.set_mode((screenWidth, 500))
        pygame.display.set_caption("First Game")

