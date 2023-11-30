# Creates a Birds Class to store different types of birds and their special powers

from cmu_graphics import *
from parabolaPlot import *
from obstacles import *
from environment import *
from opp import *
import math

class Bird:
    def __init__(self, bird, x, y, vx):
        if bird == "red":
            self.image = "src\\angry.png"
            self.w = 30
            self.h = 30
        elif bird == "blue":
            self.image = "src\\blue.png"
        elif bird == "yellow":
            self.image = "src\\Yellow.png"
        elif bird == "black":
            self.image = "src\\Bomb.png"
            self.w = 25
            self.h = 35
        self.posX = x
        self.posY = y
        self.vx = vx
        self.dx = 0.75
        self.vy = 0
        self.retention = 0.3
        self.arg = 0
        self.hit = False
        self.block = -1

    def fall(self, app):
        #print(self.posY, self.hit)
        #print(self.vy, self.vx)
        if rounded(self.vy) != 0 or rounded(self.vx) != 0:
            self.arg += 0.05
        if self.hit:
            if self.block != -1:
                if self.posY < 352 - self.h:
                    collisionBlock = app.obsList[self.block]
                    if not (collisionBlock.x - self.w/2 < self.posX < collisionBlock.x + self.w/2):
                        self.hit = False
                    lowest = collisionBlock.y - 11
                    gravity = 0.1
                    if self.posY + self.h/2 < lowest:
                        self.vy += gravity
                    else:
                        if self.vy > 0.6:
                            self.vy = self.vy * -1 * self.retention
                            #app.points += 100
                        else:
                            if abs(self.vy) <= 0.6 or self.posY > 352+self.h:
                                self.vy = 0
                                self.vx = 0
                    self.posY += self.vy
                    self.posX += self.vx
                else:
                    self.posY = 352 - self.h/2
                    self.vx = 0
                    self.vy = 0
            else:
                if self.posY < 352 - self.h:
                    hit1 = False
                    gravity = 2
                    for i in range(len(boundaryCalculator(app.obsList))):
                        x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                        #print(y1, y2)
                        if y1 + self.h > self.posY + self.vy > y2 - self.h/2  and x2 - self.w/2 < self.posX + self.vx:
                            hit1 = True
                            self.block = i
                            app.obsList[i].hit = True
                    if not hit1:
                        self.vy += gravity
                        self.vx += 0.1
                    else:
                        if self.vy > 0.6:
                            self.vy = self.vy * -1 * self.retention
                            #app.points += 100
                        else:
                            if abs(self.vy) <= 0.6 and self.posY > 352+self.h:
                                self.vy = 0
                                self.vx = 0
                else:
                    self.vy = self.vy * -1 * self.retention
                    self.vx = self.vx * -1 * self.retention
                self.posY += self.vy
                self.posX += self.vx
        else:
            #self.vy = 2
            if self.posY < 352 - self.h/2:
                hit1 = False
                gravity = 2
                for i in range(len(boundaryCalculator(app.obsList))):
                    x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                    #print(y1, y2)
                    if y1 + self.h > self.posY + self.vy > y2 - self.h/2  and x2 - self.w/2 < self.posX + self.vx < x1 + self.w/2:
                        hit1 = True
                        app.obsList[i].hit = True
                #print(hit1)
                if not hit1:
                    print(self.posY + self.h/2, self.vy)
                    if abs(self.vy) <= 0.6 and self.posY + self.h/2 + 0.5 >= 352:
                        self.vy = 0
                        self.vx = 0
                    else:
                        self.vy += gravity
                        self.vx += 0.2
                else:
                    self.hit = True
                    if self.vy > 0.6:
                        self.vy = self.vy * -1 * self.retention
                        #app.points += 100
                    else:
                        print(self.posY + self.h/2)
                        if abs(self.vy) <= 0.6 and self.posY + self.h/2 >= 352:
                            self.vy = 0
                            self.vx = 0
            else:
                self.vy = self.vy * -1 * self.retention
                self.vx = self.vx * -1 * self.retention
            if self.posY + self.h/2 + self.vy < 352:
                self.posY += self.vy
                self.posX += self.vx
            else:
                self.posY = 352 - self.h/2
                self.posX += self.vx

    def fly(self, app):
        groundLine = app.groundLine[0]
        if self.posX <= 100:
            try:
                self.posX, self.posY = linearCorrection(app, self.posX, self.posY)
            except Exception:
                pass
        elif self.posY < groundLine - 30 and self.posX > 100 and not self.hit:
            for i in range(len(boundaryCalculator(app.obsList))):
                x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                if min(x1, x2) <= self.posX + self.vx + self.w <= max(x1, x2) and min(y1, y2) <= (app.a*((self.posX + self.vx + self.w/2)**2) + app.b*(self.posX + self.vx + self.w/2) + app.c) + 30 <= max(y1, y2):
                    app.obsList[i].hit = True
                    #app.obsList[i].vx = 25
                    self.hit = True
                    app.points += 100
                    self.block = i
                    self.vx = 1.5
                    #self.vy = -10
                else:
                    self.posX, self.posY, self.arg = birdFlyingPos(app, self.posX, self.arg, self.hit, self.vx)
            for j in range(len(pigBoundaryCalculator(app.pigList))):
                x1, x2, y1, y2 = pigBoundaryCalculator(app.pigList)[j]
                if min(x1, x2) <= self.posX + 7 <= max(x1, x2) and min(y1, y2) <= app.a*((self.posX + 7)**2) + app.b*(self.posX + 7) + app.c <= max(y1, y2):
                    app.pigList[j].hit = True
                    app.pigList[j].vx = 2
                    app.pigList[j].vy = -5
                    self.hit = True
        elif self.hit and self.posY < groundLine - 30  and self.block != -1:
            collisionBlock = app.obsList[self.block]
            '''if isinstance(app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID], list):
                self.posY = app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID][0] - 22
            else:
                self.posY = app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID] - 22'''
            app.flying = False
            #self.vy = -5
            x = app.birdList.pop(0)
            app.thrown.append(x)
            if len(app.birdList) > 0:
                app.birdList[0].posX = app.initialX
                app.birdList[0].posY = app.initialY
            app.aimdots = []
        else:
            app.flying = False
            x = app.birdList.pop(0)
            app.thrown.append(x)
            if len(app.birdList) > 0:
                app.birdList[0].posX = app.initialX
                app.birdList[0].posY = app.initialY
            app.aimdots = []

class Accelerate:
    def __init__(self):
        pass

class Triple:
    def __init__(self):
        pass

class Bomb:
    def __init__(self):
        pass
