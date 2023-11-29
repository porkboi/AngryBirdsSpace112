from cmu_graphics import *
import math
import random

def drawTerrain(location="flat", **kwargs):
    if location == "flat":
        app.groundLine = [330]
    elif location == "hilly":
        if "n" in kwargs:
            n = kwargs["n"]
            app.groundLine = [random.randint(200, 330) for i in range(n)]
        else:
            app.groundLine = [330]