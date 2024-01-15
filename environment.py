from cmu_graphics import *
import math
import random

# Draws Terrain

def drawTerrain(location="flat", **kwargs):
    if location == "flat":
        app.groundLine = [330]
    elif location == "hilly":
        if "n" in kwargs:
            n = kwargs["n"]
            app.groundLine = [random.randint(200, 330) for i in range(n)]
        else:
            app.groundLine = [330]

class Planet:
    def __init__(self, image, x, y, r1, r2, deltaF):
        self.image = image
        self.x = x
        self.y = y
        self.r1 = r1
        self.r2 = r2
        self.m = (4/3*math.pi*r1**3)//100000
        self.deltaF = deltaF
    
