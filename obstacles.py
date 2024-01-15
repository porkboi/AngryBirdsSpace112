from cmu_graphics import *
import math
import random

def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

class SpaceBrick:
    def __init__(self, x, y, z, w, h, pivot, doublePivot, hasDoublePivot, structID, blockID, level, typing, hit=False):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.retention = 0.4
        self.hit = hit
        self.arg = 0
        self.pivot = pivot #list of Pivot Points, ie. [200, 400]...
        self.structID = structID
        self.blockID = blockID
        self.dAngle = 1
        self.aAngle = 0.25
        self.doublePivot = doublePivot
        self.hasDoublePivot = hasDoublePivot
        self.level = level
        if typing == "woodV":
            self.image = "src/woodPlank.png"
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y ==  other.y)

    def fall_gravity(self):
        hit = False
        ind = -1
        for i in range(len(app.planetList)):
            planet = app.planetList[i]
            if planet.r1 < distance(self.x, planet.x, self.y, planet.y) < planet.r2:
                ind = i
                break
        boundaryLst = boundaryCalculator(app.obsList)
        for i in range(len(boundaryLst)):
            if not self == app.obsList[i]:
                x1, x2, y1, y2 = boundaryLst[i]
                if min(x1, x2) < self.x + self.vx < max(x1, x2) and min(y1, y2) < self.y + self.vy < max(y1, y2):
                    hit = True
        if ind != -1 and not hit:
            planet = app.planetList[ind]
            if distance(self.x + self.vx, planet.x, self.y + self.vy, planet.y) > planet.r1 + self.w/2 - 10:
                self.x += self.vx
                self.y += self.vy
                arg = math.tanh((self.y - planet.y)/(self.x - planet.x))
                if self.x > planet.x:
                    arg += math.pi
                self.arg = math.degrees(arg)
                self.initArg = math.degrees(arg)
                self.vx += math.cos(arg)*planet.deltaF
                self.vy += math.sin(arg)*planet.deltaF
    
    def pivot_gravity(self):
        ind = -1
        for i in range(len(app.planetList)):
            planet = app.planetList[i]
            if planet.r1 < distance(self.x, planet.x, self.y, planet.y) < planet.r2:
                ind = i
                break
        bird = app.thrown[-1]
        planet = app.planetList[ind]
        if self.arg + self.dAngle <= self.initArg + 90:
            self.arg += self.dAngle
            self.dAngle += self.aAngle
            if planet.r1 + 10 < distance(self.x, planet.x, self.y, planet.y) < planet.r2:
                self.vx -= math.cos(math.radians(self.arg))*bird.vx/4
                self.vy -= math.sin(math.radians(self.arg))*bird.vy/4
                self.x += self.vx
                self.y += self.vy
        else:
            self.arg = self.initArg + 90
        for i in range(len(boundaryCalculator(app.obsList))):
            if app.obsList[i].hit:
                x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                for j in range(len(boundaryCalculator(app.obsList))):
                    #print(boundaryCalculator(app.obsList)[i], boundaryCalculator(app.obsList)[j])
                    if i != j:
                        x3, x4, y3, y4 = boundaryCalculator(app.obsList)[j]
                        if (x1 > x4 and x3 > x2) and (y4 < y2):
                            app.obsList[j].hit = True
                            #app.points += 100
            else:
                continue


def generateSpaceObstaclesL1(app, n, groundLine):
    app.collisionDict = CollisonHandler()
    spaceBrick1 = SpaceBrick(525, 330, 0, 20, 40, False, False, False, 0, 1, 0, "woodH")
    spaceBrick2 = SpaceBrick(500, 300, 0, 40, 20, True, False, False, 0, 1, 0, "woodH")
    spaceBrick3 = SpaceBrick(525, 138, 0, 20, 40, False, False, False, 0, 1, 0, "woodH")
    spaceBrick4 = SpaceBrick(500, 150, 0, 40, 20, True, False, False, 0, 1, 0, "woodH")
    return [spaceBrick1, spaceBrick2, spaceBrick3, spaceBrick4]

# CollisionHandler saves a dictionary (O(1)) of StructureIDs and BlockIDs 
# to mark the lowest point an object can go. This helps to ensure that 
# bricks do not overlap.

class CollisonHandler:
    def __init__(self):
        self.lowests = dict()
        self.levels = dict()
    
    def add(self, structID, blockID, lowest):
        if structID in self.lowests:
            d = self.lowests[structID]
            d[blockID] = lowest
        else:
            self.lowests[structID] = dict()
            d = self.lowests[structID]
            d[blockID] = lowest
    
    def addLevel(self, level, lowest):
        self.levels[level] = lowest

# Brick Class defines bricks with 2 main methods:
#################################################
# 1. pivot_gravity: When Brick is hit by a bird
# 2. fall_gravity: When Brick is subject to gravity. Similarly uses dictionary to refrence lowest points

class Brick:
    def __init__(self, x, y, z, w, h, pivot, doublePivot, hasDoublePivot, structID, blockID, level, typing, hit=False):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.vx = 0.5
        self.vy = 0
        self.retention = 0.4
        self.hit = hit
        self.arg = 0
        self.pivot = pivot #list of Pivot Points, ie. [200, 400]...
        self.structID = structID
        self.blockID = blockID
        self.dAngle = 1
        self.aAngle = 0.25
        self.doublePivot = doublePivot
        self.hasDoublePivot = hasDoublePivot
        self.level = level
        if typing == "woodV":
            self.image = "src/woodPlank.png"
    
    def fall_gravity(self):
        #print(app.collisionDict.levels)
        if not self.doublePivot:
            #print(app.collisionDict.lowests)
            d = app.collisionDict.lowests[self.structID]
            lowest = d[self.blockID]
            #print(self.y + self.h/2, lowest)
            gravity = 1
            #print(self.y, lowest)
            if self.y + self.h/2 < lowest:
                self.vy += gravity
            else:
                if self.vy > 0.3:
                    self.vy = self.vy * -1 * self.retention
                    #app.points += 100
                else:
                    if abs(self.vy) <= 0.3 and self.y > app.collisionDict.levels[self.level]-22:
                        self.vy = 0
                        self.vx = 0
                    elif abs(self.vy) <= 0.3:
                        self.vy = 0
                        self.vx = 0
            self.y += self.vy
            self.x += self.vx
            if self.level + 1 in app.collisionDict.levels and self.blockID == 2 and len(app.collisionDict.levels) > 1:
                app.collisionDict.levels[self.level+1] = self.y - 22
            elif self.level == max(app.collisionDict.levels) and len(app.collisionDict.levels) > 1:
                app.collisionDict.lowests[self.structID][self.blockID] = app.collisionDict.levels[self.level] - 20
        else:
            d = app.collisionDict.lowests[self.structID]
            lowest = d[self.blockID]
            #print(lowest)
            x1, x2, y1, y2 = boundaryCalculator([self])[0]
            #print(x1, x2, y1, y2)
            if lowest[0] >= lowest[1]:
                self.arg = math.degrees(math.tanh((lowest[1] - lowest[0])/(x1-x2)))
            elif lowest[0] < lowest[1]:
                self.arg = math.degrees(math.tanh((lowest[0] - lowest[1])/(x1-x2)))
            higher = max(lowest)
            gravity = 1
            #print(higher, y2)
            if higher > y2 + self.h*math.cos(math.radians(self.arg)):
                self.vy += gravity
            else:
                if self.vy > 0.3:
                    self.vy = self.vy * -1 * self.retention
                    #app.points += 100
                else:
                    if abs(self.vy) <= 0.3 and self.y > app.collisionDict.levels[self.level]-22:
                        self.vy = 0
                        self.vx = 0
                    elif abs(self.vy) <= 0.3:
                        self.vy = 0
                        self.vx = 0
            self.y += self.vy
            self.x += self.vx
            if self.level + 1 in app.collisionDict.levels:
                app.collisionDict.levels[self.level+1] = higher
    
    def pivot_gravity(self):
        #print(app.collisionDict.lowests)
        d = app.collisionDict.lowests[self.structID]
        lowest = d[self.blockID]
        #print(lowest)
        if self.arg + self.dAngle < 90:
            self.arg += self.dAngle
            self.dAngle += self.aAngle
            h = (self.h/2 * math.cos(math.radians(self.arg)))*2
            self.originalX = self.x
            if h/2 + self.y < lowest:
                self.y += lowest - (h/2 + self.y)
                self.x += math.sin(math.radians(self.arg))*2.5
            if not self.hasDoublePivot:
                app.collisionDict.lowests[self.structID][self.blockID+1] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
            else:
                if self.blockID == 0:
                    app.collisionDict.lowests[self.structID][self.blockID+2][0] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
                elif self.blockID == 1:
                    app.collisionDict.lowests[self.structID][self.blockID+1][1] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
        else:
            self.arg = 90
            h = (self.h/2 * math.cos(math.radians(self.arg)))*2
            self.originalX = self.x
            if h/2 + self.y < lowest:
                self.y += lowest - (h/2 + self.y)
                self.x += math.sin(math.radians(self.arg))*2.5
            if not self.hasDoublePivot:
                app.collisionDict.lowests[self.structID][self.blockID+1] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
            else:
                if self.blockID == 0:
                    #print(app.collisionDict.lowests)
                    app.collisionDict.lowests[self.structID][self.blockID+2][0] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
                elif self.blockID == 1:
                    app.collisionDict.lowests[self.structID][self.blockID+1][1] = app.collisionDict.levels[self.level] - h - math.sin(math.radians(self.arg))*10
        for i in range(len(boundaryCalculator(app.obsList))):
            if app.obsList[i].hit:
                x1, x2, y1, y2 = boundaryCalculator(app.obsList)[i]
                for j in range(len(boundaryCalculator(app.obsList))):
                    #print(boundaryCalculator(app.obsList)[i], boundaryCalculator(app.obsList)[j])
                    if i != j:
                        x3, x4, y3, y4 = boundaryCalculator(app.obsList)[j]
                        if (x1 > x4 and x3 > x2) and (y4 < y2):
                            app.obsList[j].hit = True
                            #app.points += 100
            else:
                continue

########################################################################################################
# LEVEL OBSTACLE GENERATION
########################################################################################################

def drawObstacle(x, y, w, h, arg):
    drawRect(x, y, w, h, fill='brown', align='center', rotateAngle=arg)

def generateObstaclesL3(app, n, groundLine):
    app.collisionDict = CollisonHandler()
    brick1 = Brick(450, 200, 0, 150, 20, False, True, True, 0, 2, 0, "woodH")
    app.collisionDict.add(brick1.structID, brick1.blockID, [352-140-22, 352-140-22])
    app.collisionDict.addLevel(brick1.level + 1, 352-140)
    app.collisionDict.addLevel(brick1.level, 352)
    #brick2 = Brick(400, 300, 0, 100, 20, False, 1, 1)
    #app.collisionDict.add(brick2.structID, brick2.blockID, 352-44)
    brick3 = Brick(400, 272, 0, 20, 140, True, False, True, 0, 0, 0, "woodV") ## 140 change to 44, 322 to 272
    app.collisionDict.add(brick3.structID, brick3.blockID, 352)
    brick4 = Brick(500, 272, 0, 20, 140, True, False, True, 0, 1, 0, "woodV")
    app.collisionDict.add(brick4.structID, brick4.blockID, 352)

    brick5 = Brick(625, 200, 0, 150, 20, False, True, True, 1, 2, 0, "woodH")
    app.collisionDict.add(brick5.structID, brick5.blockID, [352-140, 352-140])
    #brick6 = Brick(400, 300, 0, 100, 20, False, 1, 1)
    #app.collisionDict.add(brick6.structID, brick6.blockID, 352-44)
    brick7 = Brick(575, 272, 0, 20, 140, True, False, True, 1, 0, 0, "woodV") ## 140 change to 44, 322 to 272
    app.collisionDict.add(brick7.structID, brick7.blockID, 352)
    brick8 = Brick(675, 272, 0, 20, 140, True, False, True, 1, 1, 0, "woodV")
    app.collisionDict.add(brick8.structID, brick8.blockID, 352)

    brick9 = Brick(538, 30, 0, 150, 20, False, True, True, 2, 2, 1, "woodH")
    app.collisionDict.add(brick9.structID, brick9.blockID, [352-140-140-20, 352-140-140-20])
    #brick10 = Brick(400, 300, 0, 100, 20, False, 1, 1)
    #app.collisionDict.add(brick10.structID, brick10.blockID, 352-44)
    brick11 = Brick(488, 102, 0, 20, 140, True, False, True, 2, 0, 1, "woodV") ## 140 change to 44, 322 to 272
    app.collisionDict.add(brick11.structID, brick11.blockID, 352-140-20)
    brick12 = Brick(588, 102, 0, 20, 140, True, False, True, 2, 1, 1, "woodV")
    app.collisionDict.add(brick12.structID, brick12.blockID, 352-140-20)

    lst = [brick1, brick3, brick4, brick5, brick7, brick8, brick9, brick11, brick12] #
    return lst

def generateObstaclesL1(app, n, groundLine):
    app.collisionDict = CollisonHandler()
    brick1 = Brick(450, 180, 0, 100, 20, False, False, False, 0, 1, 0, "woodH")
    app.collisionDict.add(brick1.structID, brick1.blockID, 352 - 140 - 6)
    app.collisionDict.addLevel(brick1.level, 352)
    brick2 = Brick(450, 280, 0, 20, 150, True, False, False, 0, 0, 0, "woodV")
    app.collisionDict.add(brick2.structID, brick2.blockID, 352)

    lst = [brick1, brick2]
    return lst

def generateObstaclesL2(app, n, groundLine):
    app.collisionDict = CollisonHandler()
    brick1 = Brick(450, 200, 0, 100, 20, False, False, False, 0, 1, 0, "woodH")
    app.collisionDict.add(brick1.structID, brick1.blockID, 352 - 140 - 20)
    app.collisionDict.addLevel(brick1.level, 352)
    brick2 = Brick(450, 280, 0, 20, 150, True, False, False, 0, 0, 0, "woodV")
    app.collisionDict.add(brick2.structID, brick2.blockID, 352)
    brick3 = Brick(550, 315, 0, 20, 50, True, False, True, 1, 0, 0, "woodV")
    app.collisionDict.add(brick3.structID, brick3.blockID, 352)
    brick4 = Brick(650, 315, 0, 20, 50, True, False, True, 1, 1, 0, "woodV")
    app.collisionDict.add(brick4.structID, brick4.blockID, 352)
    brick5 = Brick(600, 290, 0, 120, 20, False, True, True, 1, 2, 0, "woodH")
    app.collisionDict.add(brick5.structID, brick5.blockID, [352-40, 352-40])

    lst = [brick1, brick2, brick3, brick4, brick5]
    return lst

def boundaryCalculator(lst):
    newLst = []
    for brick in lst:
        halfH = (brick.h*math.cos(math.radians(brick.arg)) + brick.w*math.sin(math.radians(brick.arg)))/2
        halfW = (brick.h*math.sin(math.radians(brick.arg)) + brick.w*math.cos(math.radians(brick.arg)))/2
        x1 = brick.x + halfW
        x2 = brick.x - halfW
        y1 = brick.y + halfH
        y2 = brick.y - halfH
        newLst.append((x1, x2, y1, y2))
    return newLst