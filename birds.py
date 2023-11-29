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
            self.image = "C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\angry.png"
            self.w = 30
            self.h = 30
        elif bird == "blue":
            self.image = "C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\blue.png"
        elif bird == "yellow":
            self.image = "C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\Yellow.png"
        elif bird == "black":
            self.image = "C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\Bomb.png"
            self.w = 25
            self.h = 35
        self.posX = x
        self.posY = y
        self.vx = vx
        self.dx = 0.75
        self.vy = 0
        self.retention = 0.4
        self.arg = 0
        self.hit = False
        self.block = -1

    def fall(self, app):
        if self.block != -1:
            collisionBlock = app.obsList[self.block]
            lowest = collisionBlock.y - 11
            gravity = 1
            if self.posY + self.h/2 < lowest:
                self.vy += gravity
            else:
                if self.vy > 0.3:
                    self.vy = self.vy * -1 * self.retention
                    #app.points += 100
                else:
                    if abs(self.vy) <= 0.3 and self.posY > 352+self.h:
                        self.vy = 0
                        self.vx = 0
                    elif abs(self.vy) <= 0.3:
                        self.vy = 0
                        self.vx = 0
            self.posY += self.vy
            self.posX += self.vx
        else:
            hit1 = False
            gravity = 1
            for i in range(len(boundaryCalculator(app.obsList))):
                x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                #print(y1, y2)
                if y1 + self.h > self.posY + self.vy > y2 - self.h/2  and x2 - self.w/2 < self.posX + self.vx:
                    hit1 = True
            if not hit1:
                self.vy += gravity
            else:
                if self.vy > 0.3:
                    self.vy = self.vy * -1 * self.retention
                    #app.points += 100
                else:
                    if abs(self.vy) <= 0.3 and self.posY > 352+self.h:
                        self.vy = 0
                        self.vx = 0
                    elif abs(self.vy) <= 0.3:
                        self.vy = 0
                        self.vx = 0
            self.posY += self.vy
            self.posX += self.vx

    def fly(self, app):
        groundLine = app.groundLine[0]
        if self.posX <= 100:
            try:
                self.posX, self.posY = linearCorrection(app, self.posX, self.posY)
            except Exception:
                pass
        elif self.posY < groundLine and self.posX > 100 and not self.hit:
            for i in range(len(boundaryCalculator(app.obsList))):
                x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                if min(x1, x2) <= self.posX + self.vx + self.w/2 <= max(x1, x2) and min(y1, y2) <= app.a*((self.posX + self.vx + self.w/2)**2) + app.b*(self.posX + self.vx + self.w/2) + app.c <= max(y1, y2):
                    app.obsList[i].hit = True
                    #app.obsList[i].vx = 25
                    self.hit = True
                    app.points += 100
                    self.block = i
                else:
                    self.posX, self.posY, self.arg = birdFlyingPos(app, self.posX, self.arg, self.hit, self.vx)
            for j in range(len(pigBoundaryCalculator(app.pigList))):
                x1, x2, y1, y2 = pigBoundaryCalculator(app.pigList)[j]
                if min(x1, x2) <= self.posX + 7 <= max(x1, x2) and min(y1, y2) <= app.a*((self.posX + 7)**2) + app.b*(self.posX + 7) + app.c <= max(y1, y2):
                    app.pigList[j].hit = True
                    app.pigList[j].vx = 2
                    app.pigList[j].vy = -5
                    self.hit = True
        elif self.hit and self.posY < groundLine and self.block != -1:
            collisionBlock = app.obsList[self.block]
            if isinstance(app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID], list):
                self.posY = app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID][0] - 22
            #else:
                #self.posY = app.collisionDict.lowests[collisionBlock.structID][collisionBlock.blockID] - 22
            app.flying = False
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
