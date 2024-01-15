from cmu_graphics import *
from parabolaPlot import *
from obstacles import *
from environment import *
from birds import *
from opp import *
import math

# levelLoader: Creates Pre-determined levels

def levelLoader(level, groundLine):
    if level[-1] == "1":
        red1 = Bird("red", app.initialX, app.initialY, 3)
        app.birdList.append(red1)
        pig1 = Pig(500, 290, 0, 0)
        app.pigList.append(pig1)
        app.a = 0
        app.b = 0
        app.c = 0
        app.arg = 0
        app.argStart = 0
        app.numObs = 1
        app.obsList = generateObstaclesL1(app, app.numObs, app.groundLine[0])
    elif level[-1] == "2":
        red1 = Bird("red", app.initialX, app.initialY, 1)
        app.birdList.append(red1)
        pig1 = Pig(500, 290, 0, 0)
        app.pigList.append(pig1)
        pig2 = Pig(600, 310, 0, 0)
        app.pigList.append(pig2)
        app.a = 0
        app.b = 0
        app.c = 0
        app.arg = 0
        app.argStart = 0
        app.numObs = 1
        app.obsList = generateObstaclesL2(app, app.numObs, app.groundLine[0])
    elif level[-1] == "3":
        red1 = Bird("red", app.initialX, app.initialY, 1)
        black1 = Bird("black", app.initialX - 40, groundLine, 1)
        app.birdList.append(red1)
        app.birdList.append(black1)
        pig1 = Pig(450, 290, 0, 0)
        pig2 = Pig(625, 290, 0, 0)
        pig3 = Pig(400, 140, 0, 2)
        app.pigList.append(pig1)
        app.pigList.append(pig2)
        app.pigList.append(pig3)
        app.a = 0
        app.b = 0
        app.c = 0
        app.arg = 0
        app.argStart = 0
        app.numObs = 1
        app.obsList = generateObstaclesL3(app, app.numObs, app.groundLine[0])

def levelLoaderSpace(level):
    if level[-1] == "1":
        red1 = SpaceBird("red", app.initialX, app.initialY)
        app.birdList.append(red1)
        red2 = SpaceBird("red", app.initialX, app.initialY + 50)
        app.birdList.append(red2)
        planet1 = Planet("src/moon.png", 122, 370, 20, 0, 0)
        app.planetList.append(planet1)
        planet2 = Planet("src/moon.png", 400, 225, 50, 220, 0.5)
        app.planetList.append(planet2)
        pig1 = Pig(570, 355, 0, 0)
        pig2 = Pig(560, 105, 0, 0)
        app.pigList.append(pig1)
        app.pigList.append(pig2)
        app.arg = 0
        app.obsList = generateSpaceObstaclesL1(app, 0, 0)