from cmu_graphics import *
from parabolaPlot import *
from obstacles import *
from environment import *
from birds import *
from opp import *
import math

#Distance Formula
def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

#Initialise Variables - Obstacles
def onAppStart(app):
    drawTerrain("flat")
    app.gravity = 0.5
    app.testMode = False
    app.screen = "home"
    app.stepsPerSecond = 60
    app.width = 800
    app.height = 450
    app.initialX = 100
    app.initialY = 310
    app.flying = False
    app.drag = False
    app.aimdots = []
    #app.hit = False
    app.birdList = []
    app.thrown = []
    app.pigList = []
    app.points = 0

# Mouse Press Actions:
# On home screen: Initialises Birds
# On earth screen: Initialises Dragging system
def onMousePress(app, mouseX, mouseY):
    groundLine = app.groundLine[0]
    print(mouseX, mouseY)
    if app.screen == "home":
        if distance(mouseX, 300, mouseY, 300) < 50:
            app.screen = 'space'
        elif distance(mouseX, 500, mouseY, 300) < 50:
            app.screen = 'emenu'
    elif app.screen == "emenu":
        if 30 <= mouseX <= 280 and 30 <= mouseY <= 180:
            app.screen = "earthL1"
            red1 = Bird("red", app.initialX, app.initialY, 5)
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
        elif 535 <= mouseX <= 785 and 30 <= mouseY <= 180:
            app.screen = "earth"
            red1 = Bird("red", app.initialX, app.initialY, 1.5)
            black1 = Bird("black", app.initialX - 40, groundLine, 1.5)
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
            app.obsList = generateObstacles(app, app.numObs, app.groundLine[0])
        elif distance(mouseX, 100, mouseY, 400) < 25:
            app.screen = 'home'
    elif "earth" in app.screen:
        if distance(mouseX, 100, mouseY, 400) < 25:
            app.screen = 'emenu'
            app.birdList = []
            app.pigList = []
            app.obsList = []
            app.thrown = []
            app.points = 0
        elif not app.flying:
            bird = app.birdList[0]
            if distance(bird.posX, mouseX, bird.posY, mouseY) < 50:
                app.drag = True

# On Mouse Drag: 
# On Earth Screen : Calls Parabola Plotting for Earth
# TBC On Space Screen : Calls Linear Plotting

def onMouseDrag(app, mouseX, mouseY):
    if "earth" in app.screen:
        app.aimdots = []
        if app.drag:
            if distance(app.initialX, mouseX, app.initialY, mouseY) < 70:
                d = distance(app.initialX, mouseX, app.initialY, mouseY)
                changeDistance(app, mouseX, mouseY, d)
            else:
                if mouseX - app.initialX != 0:
                    changeDistance(app, mouseX, mouseY)
                else:
                    app.birdList[0].posX = app.initialX
                    app.birdList[0].posY = mouseY

# On Mouse Release:
# On Earth Screen: End Dragging Instance, Start FLying Instance

def onMouseRelease(app, mouseX, mouseY):
    if "earth" in app.screen:
        if app.drag:
            app.dragX = app.birdList[0].posX
            app.dragY = app.birdList[0].posY
            app.drag = False
            app.flying = True

# On Step: Calculates Gravity and Flying for Bird and Bricks
############################################################
# Bird Gravity: Calculated by Parabola Motion until it hits 
# an object, then it follows an object's lowest point.

# Brick Gravity: Calculated by saving lowest points in a 
# dictionary, indexed by BrickID and StructID. 
# Refer to CollisionHandler Class

def onStep(app):
    if "earth" in app.screen and len(app.groundLine) == 1:
        #groundLine = app.groundLine[0]
        if app.flying:
            app.birdList[0].fly(app)
        for brick in app.obsList:
            if brick.hit:
                if brick.pivot:
                    brick.pivot_gravity()
            brick.fall_gravity()
        for bird in app.thrown:
            bird.fall(app)
        for pig in app.pigList:
            if pig.hit:
                pig.fly(app)
            else:
                pig.fall(app)
                
# Draws all images

def redrawAll(app):
    if app.screen == "home":
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space\\src\\normalbackground.jpg", 400, 225, align='center', width=800, height=450)
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\logo.png", 400, 100, align='center')
        #drawLabel("Angry Birds", 400, 100, size=30)
        drawCircle(300, 300, 50, fill='blue')
        #drawCircle(500, 300, 50, fill='red')
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\earth.png", 500, 300, align='center', width=100, height=100)
    elif app.screen == "emenu":
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space\\src\\normalbackground.jpg", 400, 225, align='center', width=800, height=450)
        drawRect(25, 25, 260, 160, fill="white")
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\level0.png", 30, 30, width=250, height=150)
        drawRect(530, 25, 260, 160, fill="white")
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\level1.png", 535, 30, width=250, height=150)
        drawCircle(100, 400, 25, fill='blue')
    elif "earth" in app.screen:
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space - Copy\\src\\normalbackground.jpg", 400, 225, align='center', width=800, height=450)
        #drawRect(0, 0, app.width, app.height, fill="lightBlue")
        #drawRect(0, 352, app.width, app.height, fill="green")
        #drawRect(750, 0, 50, 450, fill="black")
        for i in app.aimdots:
            x, y = i
            try:
                drawCircle(x, y, 5, fill="grey")
            except Exception:
                pass
        for j in app.obsList:
            drawObstacle(j.x, j.y, j.w, j.h, j.arg)
            #drawImage(j.image, j.x, j.y, align="center", width=j.w, height = j.h, rotateAngle=j.arg)
        for j in app.birdList:
            drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
        for j in app.thrown:
            drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
        for j in app.pigList:
            if not j.dead:
                drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h)
        drawImage("C:\\Users\\chris\\Desktop\\Python Projects\\Angry Birds Space\\src\\catapault.png", 120, 325, align='center', width=30, height=60)
        drawLabel("POINTS", 80, 40, size=30)
        drawLabel(str(app.points), 200, 40, size=30)
        drawCircle(100, 400, 25, fill='blue')

def main():
    runApp()

main()