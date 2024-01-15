from cmu_graphics import *
from parabolaPlot import *
from obstacles import *
from environment import *
from birds import *
from opp import *
from levelLoader import *
from timer import Timer
import time
import math

#Distance Formula
def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

#Initialise Variables
def onAppStart(app):
    drawTerrain("flat")
    app.story = 3
    app.gravity = 0.5
    app.testMode = False
    app.screen = "home"
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
    app.planetList= []
    app.startTime = 0
    app.timer = False

# Mouse Press Actions:
# On home screen: Initialises Birds
# On earthMenu screen: Initialises Dragging system
# On any screen with the string 'earth' in it
# Loading next level

def onMousePress(app, mouseX, mouseY):
    allDead = 0
    for i in app.pigList:
        if i.dead == True:
            allDead += 1
    if allDead == len(app.pigList):
        allDead = True
    else:
        allDead = False
    groundLine = app.groundLine[0]
    #print(mouseX, mouseY)
    if app.screen == "home":
        if app.story >= 0:
            app.story -= 1
        else:
            if distance(mouseX, 300, mouseY, 300) < 50:
                app.screen = 'smenu'
            elif distance(mouseX, 500, mouseY, 300) < 50:
                app.screen = 'emenu'
    elif app.screen == "emenu":
        app.stepsPerSecond = 60
        if 30 <= mouseX <= 280 and 30 <= mouseY <= 180:
            app.screen = "earthL1"
            levelLoader(app.screen, groundLine)
        elif 270 <= mouseX <= 520 and 210 <= mouseY <= 360:
            app.screen = "earthL2"
            levelLoader(app.screen, groundLine)
        elif 535 <= mouseX <= 785 and 30 <= mouseY <= 180:
            app.screen = "earthL3"
            levelLoader(app.screen, groundLine)
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
            app.timer = False
        elif not app.flying:
            try:
                bird = app.birdList[0]
                if distance(bird.posX, mouseX, bird.posY, mouseY) < 50:
                    app.drag = True
            except Exception:
                pass
        if allDead:
            if distance(mouseX, app.width-100, mouseY, 400) < 25:
                lastChr = chr(ord(app.screen[-1]) + 1)
                app.screen = app.screen[:-1] + lastChr
                app.birdList = []
                app.pigList = []
                app.obsList = []
                app.thrown = []
                app.points = 0
                app.timer = False
                levelLoader(app.screen, groundLine)
    elif app.screen == "smenu":
        app.stepsPerSecond = 120
        if 30 <= mouseX <= 280 and 30 <= mouseY <= 180:
            app.screen = "spaceL1"
            levelLoaderSpace(app.screen)
        elif distance(mouseX, 100, mouseY, 400) < 25:
            app.screen = 'home'
    elif "space" in app.screen:
        if distance(mouseX, 100, mouseY, 400) < 25:
            app.screen = 'smenu'
            app.birdList = []
            app.pigList = []
            app.obsList = []
            app.thrown = []
            app.points = 0
            app.timer = False
        elif not app.flying:
            try:
                bird = app.birdList[0]
                if distance(bird.posX, mouseX, bird.posY, mouseY) < 50:
                    app.drag = True
            except Exception:
                pass
                

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
    elif "space" in app.screen:
        app.aimdots = []
        if app.drag:
            if distance(app.initialX, mouseX, app.initialY, mouseY) < 70:
                d = distance(app.initialX, mouseX, app.initialY, mouseY)
                spaceChangeDistance(app, mouseX, mouseY, d)
            else:
                if mouseX - app.initialX != 0:
                    spaceChangeDistance(app, mouseX, mouseY)
                else:
                    app.birdList[0].posX = app.initialX
                    app.birdList[0].posY = mouseY
            spacePlotter(app, app.birdList[0])

# On Mouse Release:
# On Earth Screen: End Dragging Instance, Start FLying Instance

def onMouseRelease(app, mouseX, mouseY):
    if "earth" in app.screen:
        if app.drag:
            app.dragX = app.birdList[0].posX
            app.dragY = app.birdList[0].posY
            app.drag = False
            app.flying = True
    elif "space" in app.screen:
        if app.drag:
            app.dragX = app.birdList[0].posX
            app.dragY = app.birdList[0].posY
            app.drag = False
            app.flying = True
            app.birdList[0].vx = (app.initialX - app.birdList[0].posX) //6
            app.birdList[0].vy = (app.initialY - app.birdList[0].posY) //6
    

# On Step: Calculates Gravity and Flying for Bird and Bricks
############################################################
# Bird Gravity: Calculated by Parabola Motion until it hits 
# an object, then it follows an object's lowest point.

# Brick Gravity: Calculated by saving lowest points in a 
# dictionary, indexed by BrickID and StructID. 
# Refer to CollisionHandler Class

# Pig Gravity: Calculated by calculating collisions with Birds/blocks

def onStep(app):
    #print(app.flying)
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
        if pigsAllDead() and not app.timer:
            app.timer = Timer()
            app.timer.start()
    elif "space" in app.screen:
        if app.flying:
            app.birdList[0].fly()
        for brick in app.obsList:
            if brick.hit:
                if brick.pivot:
                    brick.pivot_gravity()
            brick.fall_gravity()
        for bird in app.thrown:
            bird.fall(app)
        for pig in app.pigList:
            '''if pig.hit:
                pig.fly(app)
            else:'''
            pig.spaceFall(app)
        if pigsAllDead() and not app.timer:
            app.timer = Timer()
            app.timer.start()

                
# Draws all images

def redrawAll(app):
    if app.screen == "home":
        if app.story >= 0:
            drawImage("src/story.png", 400, 225, align='center', width=800, height=450)
            rectList = [(app.width*0.75, app.height*0.75, app.width/2, app.height/2), 
                        (app.width*0.25, app.height*0.75, app.width/2, app.height/2), 
                        (app.width*0.75, app.height*0.25, app.width/2, app.height/2)]
            for i in range(app.story):
                a, b, c, d= rectList[i]
                drawRect(a, b, c, d, fill="white", align="center")
            drawLabel("Click the screen to continue!", app.width/2, 425, font="AngryBirds")
        else:
            # Citation: https://www.deviantart.com/yoshibowserfanatic/art/Angry-Birds-Poached-Eggs-Theme-I-Background-406945305
            drawImage("src/normalbackgroundHD.jpg", 400, 225, align='center', width=800, height=450)
            drawLabel("Angry Birds", 400, 100, size=100, font="AngryBirds")
            drawLabel("Select a game mode:", 400, 200, size=30, font="AngryBirds")
            drawLabel("Space", 300, 250, font="AngryBirds")
            drawLabel("Earth", 500, 250, font="AngryBirds")
            # Citation: https://www.istockphoto.com/illustrations/moon
            drawImage("src/moon.png", 300, 300, align='center', width=100, height=100)
            # Citation: https://www.istockphoto.com/illustrations/planet-earth
            drawImage("src/earth.png", 500, 305, align='center', width=95, height=95)
    elif app.screen == "emenu":
        # Citation: https://www.deviantart.com/yoshibowserfanatic/art/Angry-Birds-Poached-Eggs-Theme-I-Background-406945305
        drawImage("src/normalbackground.jpg", 400, 225, align='center', width=800, height=450)
        drawRect(25, 25, 260, 160, fill="white")
        drawImage("src/level0.png", 30, 30, width=250, height=150)
        drawLabel("Level 1", 155, 205, font="AngryBirds", size = 30)
        drawRect(530, 25, 260, 160, fill="white")
        drawImage("src/level1.png", 535, 30, width=250, height=150)
        drawLabel("Level 3", 645, 205, font="AngryBirds", size = 30)
        drawRect(270, 205, 260, 160, fill="white")
        drawImage("src/level2.png", 275, 210, width=250, height=150)
        drawLabel("Level 2", 400, 180, font="AngryBirds", size = 30)
        drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
    elif "earth" in app.screen:
        # Citation: https://www.deviantart.com/yoshibowserfanatic/art/Angry-Birds-Poached-Eggs-Theme-I-Background-406945305
        drawImage("src/normalbackground.jpg", 400, 225, align='center', width=800, height=450)
        
        allDead = pigsAllDead()

        if isinstance(app.timer, bool):
            if len(app.birdList) > 0 or not allDead:
                for i in app.aimdots:
                    x, y = i
                    try:
                        drawCircle(x, y, 2, fill="grey")
                    except Exception:
                        pass
                for j in app.obsList:
                    drawObstacle(j.x, j.y, j.w, j.h, j.arg)
                for j in app.birdList:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.thrown:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.pigList:
                    if not j.dead:
                        drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h)
                # Citation: https://angrybirds.fandom.com/wiki/Catapault
                drawImage("src/catapault.png", 120, 325, align='center', width=30, height=60)
                drawLabel("POINTS", 80, 40, size=30, font="AngryBirds")
                drawLabel(str(app.points), 200, 40, size=30, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
            else:
                drawRect(app.width/2, app.height/2, app.width*(3/4), app.height*(3/4), fill="red", align = "center")
                drawLabel(f"Level {app.screen[-1]} Failed", app.width/2, app.height*(1/3), size=30, font="AngryBirds")
                drawLabel(f"Score: {app.points}", app.width/2, app.height*(2/3), size=20, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
                #drawCircle(app.width-100, 400, 25, fill='red')
        else:
            if not app.timer.stop(len(app.pigList)):
                for i in app.aimdots:
                    x, y = i
                    try:
                        drawCircle(x, y, 2, fill="grey")
                    except Exception:
                        pass
                for j in app.obsList:
                    drawObstacle(j.x, j.y, j.w, j.h, j.arg)
                for j in app.birdList:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.thrown:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.pigList:
                    if not j.dead:
                        drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h)
                # Citation: https://angrybirds.fandom.com/wiki/Catapault
                drawImage("src/catapault.png", 120, 325, align='center', width=30, height=60)
                drawLabel("POINTS", 80, 40, size=30, font="AngryBirds")
                drawLabel(str(app.points), 200, 40, size=30, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)  
            else:
                drawRect(app.width/2, app.height/2, app.width*(3/4), app.height*(3/4), fill="green", align = "center")
                drawLabel(f"Level {app.screen[-1]} Complete", app.width/2, app.height*(1/3), size=30, font="AngryBirds")
                drawLabel(f"Score: {app.points}", app.width/2, app.height*(2/3), size=20, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
                drawImage("src/next.png", app.width-100, 400, align='center', width=50, height=50)
    elif app.screen == "smenu":
        # Citation: https://www.reddit.com/r/onlyramens/comments/mq4ega/angry_birds_space_pig_dipper_clean_background/
        drawImage("src/space.png", 400, 225, align='center', width=800, height=450)
        drawRect(25, 25, 260, 160, fill="white")
        drawImage("src/spaceL1.png", 30, 30, width=250, height=150)
        drawLabel("Level 1", 155, 205, font="AngryBirds", size = 30, fill="white")
        drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
    elif "space" in app.screen:
        # Citation: https://www.reddit.com/r/onlyramens/comments/mq4ega/angry_birds_space_pig_dipper_clean_background/
        drawImage("src/space_lite.png", 400, 225, align='center', width=800, height=450)
        allDead = pigsAllDead()

        if isinstance(app.timer, bool):
            if len(app.birdList) > 0 or not allDead:
                for j in app.planetList:
                    if j.r2 != 0:
                        drawCircle(j.x, j.y, j.r2, align="center", fill="lightBlue")
                    drawImage(j.image, j.x, j.y, align="center", width=j.r1*2, height=j.r1*2)
                for j in app.obsList:
                    drawObstacle(j.x, j.y, j.w, j.h, j.arg)
                for j in app.birdList:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.thrown:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for i in app.aimdots:
                    x, y = i
                    try:
                        drawCircle(x, y, 2, fill="grey")
                    except Exception:
                            pass
                for j in app.pigList:
                    if not j.dead:
                        drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                # Citation: https://angrybirds.fandom.com/wiki/Catapault
                drawImage("src/catapault.png", 120, 325, align='center', width=30, height=60)
                drawLabel("POINTS", 80, 40, size=30, font="AngryBirds", fill="white")
                drawLabel(str(app.points), 200, 40, size=30, font="AngryBirds", fill="white")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
            else:
                drawRect(app.width/2, app.height/2, app.width*(3/4), app.height*(3/4), fill="red", align = "center")
                drawLabel(f"Level {app.screen[-1]} Failed", app.width/2, app.height*(1/3), size=30, font="AngryBirds")
                drawLabel(f"Score: {app.points}", app.width/2, app.height*(2/3), size=20, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
                #drawCircle(app.width-100, 400, 25, fill='red')
        else:
            if not app.timer.stop(len(app.pigList)):
                for j in app.planetList:
                    if j.r2 != 0:
                        drawCircle(j.x, j.y, j.r2, align="center", fill="lightBlue")
                    drawImage(j.image, j.x, j.y, align="center", width=j.r1*2, height=j.r1*2)
                for j in app.obsList:
                    drawObstacle(j.x, j.y, j.w, j.h, j.arg)
                for j in app.birdList:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for j in app.thrown:
                    drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                for i in app.aimdots:
                    x, y = i
                    try:
                        drawCircle(x, y, 2, fill="grey")
                    except Exception:
                            pass
                for j in app.pigList:
                    if not j.dead:
                        drawImage(j.image, j.posX, j.posY, align='center', width=j.w, height=j.h, rotateAngle = (j.arg)/math.pi*180)
                # Citation: https://angrybirds.fandom.com/wiki/Catapault
                drawImage("src/catapault.png", 120, 325, align='center', width=30, height=60)
                drawLabel("POINTS", 80, 40, size=30, font="AngryBirds", fill="white")
                drawLabel(str(app.points), 200, 40, size=30, font="AngryBirds", fill="white")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
            else:
                drawRect(app.width/2, app.height/2, app.width*(3/4), app.height*(3/4), fill="green", align = "center")
                drawLabel(f"Level {app.screen[-1]} Complete", app.width/2, app.height*(1/3), size=30, font="AngryBirds")
                drawLabel(f"Score: {app.points}", app.width/2, app.height*(2/3), size=20, font="AngryBirds")
                # Citation: https://angrybirds.fandom.com/wiki/Sprites_Resource
                drawImage("src/back.png", 100, 400, align='center', width=50, height=50)
                drawImage("src/next.png", app.width-100, 400, align='center', width=50, height=50)
            

def main():
    runApp()

main()