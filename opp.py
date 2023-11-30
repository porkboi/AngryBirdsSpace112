from cmu_graphics import *
from parabolaPlot import *
from obstacles import *
from environment import *
from birds import *
import math

class Pig:
    def __init__(self, x, y, structID, blockID, dead=False):
        self.image = "src\\normalPig.png"
        self.posX = x
        self.posY = y
        self.w = 40
        self.h = 40
        self.dead = dead
        self.hp = 100
        self.structID = structID
        self.blockID = blockID
        self.vx = 0
        self.dx = 0.75
        self.vy = 1
        self.retention = 0.4
        self.hit = False
    
    def fall(self, app):
        if isinstance(app.collisionDict.lowests[self.structID][self.blockID], list):
            #print(app.collisionDict.lowests[self.structID][self.blockID])
            lowest = max(app.collisionDict.lowests[self.structID][self.blockID])
        else:
            lowest = app.collisionDict.lowests[self.structID][self.blockID]
        gravity = 1
        if self.posY + self.h/2 < lowest:
            self.vy += gravity
        else:
            if self.vy > 0.3:
                self.hp -= 1
                if self.hp == 0:
                    self.dead = True
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
        for i in range(len(boundaryCalculator(app.obsList))):
            x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
            arg = app.obsList[i].arg
            if arg != 0 and min(x1, x2) <= self.posX + 7 <= max(x1, x2) and min(y1, y2) <= self.posY <= max(y1, y2) and not self.dead:
                self.dead = True
                app.points += 50
    
    def fly(self, app):
        if isinstance(app.collisionDict.lowests[self.structID][self.blockID], list):
            #print(app.collisionDict.lowests[self.structID][self.blockID])
            lowest = max(app.collisionDict.lowests[self.structID][self.blockID])
        else:
            lowest = app.collisionDict.lowests[self.structID][self.blockID]
        gravity = 0.45
        #up = 0.75
        ax = 0.5
        hit = False
        for i in range(len(boundaryCalculator(app.obsList))):
            x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
            if y1 + self.h/2 > self.posY + self.vy > y2 - self.h/2  and x2 - self.w/2 < self.posX + self.vx:
                hit = True
        if not hit:
            self.vy += gravity
            self.vx += ax
        elif abs(self.vy) <= 0.3:
            self.vy = 0
            self.vx = 0
            self.hit=False
        else:
            self.hp -= 33
            if self.hp <= 0:
                self.dead = True
                app.points += 500
            self.vy = self.vy * -1 * self.retention
            self.vx = self.vx * -1 * self.retention
        self.posY += self.vy
        self.posX += self.vx

def pigBoundaryCalculator(lst):
    newLst = []
    for pig in lst:
        x1 = pig.posX + pig.w/2
        x2 = pig.posX - pig.w/2
        y1 = pig.posY + pig.h/2
        y2 = pig.posY - pig.h/2
        newLst.append((x1, x2, y1, y2))
    return newLst