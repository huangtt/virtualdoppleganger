import math
import time
import csv
import GUIInterface
import random
from time import gmtime, strftime

getViewer().show()
getCamera().reset()

#scene.run("maze10.py")
scene.run("linearmaze.py")
scene.run("mazeenhancement.py")
scene.run("mines.py")
#scene.run("ground.py")
scene.run("tile.py")
scene.run("finishLine.py")
scene.run("controller.py")
scene.run("character.py")
scene.run("collision.py")
scene.run("camera.py")
scene.run("lights.py")
#scene.run("trackingcamera.py")
scene.run("tutorialcamera.py")
scene.run("menu.py")
scene.run("music.py")

