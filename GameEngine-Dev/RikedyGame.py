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

import os, pprint

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""
    # Code by Clay Mcleod on github
    controller = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.axis_data = {0:0, 1:0, 2:0, 5:0}
        self.button_data = dict()
        for i in range(self.controller.get_numbuttons()):
            self.button_data[i] = False
        self.hat_data = dict()

    def listen(self):
        """Listen for events to happen"""
        
        #print(self.button_data)

        # if not self.hat_data:
        #     self.hat_data = {}
        #     for i in range(self.controller.get_numhats()):
        #     self.hat_data[i] = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value,2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                #print('HAT')
                self.hat_data[event.hat] = event.value

            # Insert your code on what you would like to happen for each event here!
            # In the current setup, I have the state simply printing out to the screen.
            
            #os.system('clear')
            #pprint.pprint(self.button_data)
            # print(self.axis_data)
            # print('-------------')
        return self.axis_data, self.button_data, self.hat_data
            #pprint.pprint(self.hat_data)

        #return self.button_data, self.axis_data



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
        self.windowSurface = pygame.display.set_mode((WindowWidth, WindowHeight), pygame.RESIZABLE)#,pygame.FULLSCREEN)
        pygame.display.set_caption(caption)
        self.scenes = dict()
        # Check for ps4 controller
        try:
            self.ps4 = PS4Controller()
            self.ps4.init()
        except:
            print('No Controller Found')
            self.ps4 = None
    def addScene(self, scene):
        self.scenes[scene.name] = scene

    def play(self):
        scenelist = cycle(self.scenes)
        while True:
            scene = next(scenelist)
            self.scenes[scene].play(self.ps4)



        # for scene in self.scenes:
        #     self.scenes[scene].play(self.windowSurface)
        # Do a next_scene variable
        # Make scenes easily switchable - can trigger new scene from old scene and return to old scene in prior state



