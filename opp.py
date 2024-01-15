from cmu_graphics import *
from obstacles import *
from environment import *
import math

def pigsAllDead():
    allDead = 0
    for i in app.pigList:
        if i.dead == True:
            allDead += 1
    if allDead == len(app.pigList):
        allDead = True
    else:
        allDead = False
    return allDead

def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Pig Class: Generates Pigs with 2 methods:
############################################################################
# 1. Fly: When Pig is hit by a bird
# 2. Fall: When Pig is subject to gravity. Similarly uses dictionary to refrence lowest points

class Pig:
    def __init__(self, x, y, structID, blockID, dead=False):
        # Citation: https://angrybirds.fandom.com/wiki/Minion_Pigs/Small_Pig
        self.image = "src/normalPig.png"
        self.posX = x
        self.posY = y
        if "space" in app.screen:
            self.w = 30
            self.h = 30
        else:
            self.w = 40
            self.h = 40
        self.dead = dead
        self.hp = 100
        self.structID = structID
        self.blockID = blockID
        self.vx = 0
        self.dx = 0.75
        self.vy = 1
        self.vys = 0
        self.retention = 0.4
        self.hit = False
        self.drop = False
        self.arg = 0
    
    def spaceFall(self, app):
        drop = False
        ind = -1
        for i in range(len(app.planetList)):
            planet = app.planetList[i]
            #print(distance(self.posX, planet.x, self.posY, planet.y))
            if planet.r1 < distance(self.posX, planet.x, self.posY, planet.y) < planet.r2:
                ind = i
                break
        boundaryLst = boundaryCalculator(app.obsList)
        planet = app.planetList[ind]
        for i in range(len(boundaryLst)):
            x1, x2, y1, y2 = boundaryLst[i]
            #print(x1, x2, self.posX - self.h/2)
            if self.posX < planet.x and self.posY < planet.y:
                if min(x1, x2) < self.posX + self.h/2 < max(x1, x2) and min(y1, y2) < self.posY + self.w/2 < max(y1, y2):
                    drop = True
                    self.hp -= 50
            elif self.posX > planet.x and self.posY < planet.y:
                if min(x1, x2) < self.posX - self.h/2 < max(x1, x2) and min(y1, y2) < self.posY + self.w/2 < max(y1, y2):
                    drop = True
                    self.hp -= 50
            elif self.posX < planet.x and self.posY > planet.y:
                if min(x1, x2) < self.posX + self.h/2 < max(x1, x2) and min(y1, y2) < self.posY - self.w/2 < max(y1, y2):
                    drop = True
                    self.hp -= 50
            elif self.posX > planet.x and self.posY > planet.y:
                if min(x1, x2) < self.posX - self.h/4 < max(x1, x2) and min(y1, y2) < self.posY - self.w/2 < max(y1, y2):
                    drop = True
                    self.hp -= 50
            
        #print(ind, drop, self.vx, self.vys,self.hp)
        if ind != -1 and not drop and not self.dead:
            if distance(self.posX + self.vx, planet.x, self.posY + self.vys, planet.y) > planet.r1 + self.w/2 - 10:
                self.posX += self.vx
                self.posY += self.vys
                arg = math.tanh((self.posY - planet.y)/(self.posX - planet.x))
                if self.posX > planet.x:
                    arg += math.pi
                self.arg = math.degrees(arg)
                self.vx += math.cos(arg)*planet.deltaF*0.5
                self.vys += math.sin(arg)*planet.deltaF*0.5
        elif drop and not self.dead and abs(self.vx) > 3.5:
            self.vx = 0
            self.vys = 0
            if self.hp <= 0:
                self.dead = True
                app.points += 500

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

# Calculates a boundary box for pigs to measure collisions.

def pigBoundaryCalculator(lst):
    newLst = []
    for pig in lst:
        x1 = pig.posX + pig.w/2
        x2 = pig.posX - pig.w/2
        y1 = pig.posY + pig.h/2
        y2 = pig.posY - pig.h/2
        newLst.append((x1, x2, y1, y2))
    return newLst