# RikedyGame.py
# RikedyP Game Engine - hopefully a fairly light,
# simple to understand and easy to implement 2D and
# pseudo-3D game engine for pygame python3
# This document adheres to pylint somewhat:


# ------------------------ TO DO -------------------------

# Use Point23D.addXYZ more
# Streamline functions and methods a bit
# Utilist pygame.sprite stuff
# Easy to create scenes i.e. game levels - choose 2d or 3d
# Scenes contain control parameters
# only objects in the same layer can collide
# Better variables
# Maybe use OpenGL for 3D so it can be expanded
# Set controls within game menu
# Use bluetooth controller option
# Do 3D scenes
# Put proper comments everywhere

# ---------------------- - METHOD -------------------------

# Make a game object
# Create scenes and scene progression stuff
# game.play()

# ---------------------------------------------------------

import pygame, sys, random, math
from pygame.locals import * # what does this do?
#from itertools import cycle
from R2D import *
from R3D import *

class Game(object):
    # Handles gameplay

    def __init__(self,WindowWidth,WindowHeight,caption='RikedyGame Game'):
        self.WindowHeight = WindowHeight
        self.WindowWidth = WindowWidth
        # set up pygame
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Ariel', 20)
        self.mainClock = pygame.time.Clock()
        # set up the window
        self.windowSurface = pygame.display.set_mode((WindowWidth, WindowHeight))#,pygame.FULLSCREEN)
        pygame.display.set_caption(caption)
        self.scenes = dict()

    def addScene(self, scene):
        self.scenes[scene.name] = scene

    def play(self):
        scenelist = cycle(self.scenes)
        while True:
            scene = next(scenelist)
            self.scenes[scene].play(self.windowSurface)
        # for scene in self.scenes:
        #     self.scenes[scene].play(self.windowSurface)
        # Do a next_scene variable
        # Make scenes easily switchable - can trigger new scene from old scene and return to old scene in prior state



