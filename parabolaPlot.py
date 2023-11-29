from cmu_graphics import *
import math

def distance(x1, x2, y1, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def trajectory(app, x, y):
    vx = app.initialX - x
    vy = app.initialY - y
    while y < 352:
        drawCircle(x, y, 5)
        x += vx
        y += vy
        vy -= 9.81

# parabolaPlot: main function which creates the parabola shape of the bird's 
# flight by modelling a quadratic equation and saving the coordinates

def parabolaPlot(app, arg, step):
    app.arg = arg
    app.argStart = arg
    arg = 3*math.pi/2 - arg
    a = (app.birdList[0].posY - app.initialY - math.tan(arg)*app.birdList[0].posX - math.tan(arg)*app.initialX)/(app.birdList[0].posX - app.initialX)
    a = -(a/1000)
    c = 500
    b = -0.003*900
    app.a = a
    app.b = b
    app.c = c
    return a*(step)**2 + b*step + c

# linearCorrection: Linearly Corrects the movement of the bird from release point to the catapault

def linearCorrection(app, currentX, currentY):
    try:
        a = ((app.a*(100**2) + app.b*100 + app.c)-(app.dragY))/(100-app.dragX)
        b = (app.dragY + app.initialY-a*app.dragX - a*app.initialX)/2
        currentX += 20
        currentY = a * currentX + b
        return currentX, currentY
    except Exception:
        pass

# Calculates the Bird's Flight Path before powers

def birdFlyingPos(app, currentX, arg, hit, vx):
    if hit:
        currentX += 2
        currentY = app.a*((currentX+2)**2) + app.b*(currentX+2) + app.c
        arg += app.argStart/(((-app.b/2)-100)/5)
    else:
        currentX += vx
        currentY = app.a*(currentX**2) + app.b*currentX + app.c
        arg += app.argStart/(((-app.b/2)-100)/5)
    return currentX, currentY, arg

# Aiming the Bird

def changeDistance(app, mouseX, mouseY, d=70):
    app.birdList[0].posX = mouseX
    app.birdList[0].posY = mouseY
    if mouseX - app.initialX != 0:
        arg = math.tanh((mouseY - app.initialY)/(mouseX - app.initialX))
        app.birdList[0].posX = app.initialX - d* math.cos(arg)
        app.birdList[0].posY = app.initialY - d* math.sin(arg)
        app.birdList[0].arg = arg
        for step in range(100, 800, 20):
            coordinate = parabolaPlot(app, arg, step)
            if coordinate < 352:
                app.aimdots.append((step, coordinate))