""" Quest - An epic journey.

Contains methods relating to 2D scenes in RikedyGame Engine

------------------------ TO DO -----------------------------------

2D pathfinding
Learn to use loggings
Collisions, walls, level map implementation and interactable objects an NPCs
Double check pygame.sprite is being used to its full usefulness
Is sprite killing convenient and clean?
learn when i really need to use object class type
pygame display flip or refresh?
Make dude movement more flexible?
Use load image convert thing
End of scene reset option
Compare methods with pyscroll quest.py
Try to make more efficient
Change text depending on input type

-------------------------Program ---------------------------------
"""
import os.path
import sys

import pygame, pyganim
from pygame.locals import *
from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

# define configuration variables here
RESOURCES_DIR = 'data'

DUDE_MOVE_SPEED = 200  # pixels per second
MAP_FILENAME = 'Maps/untitled.tmx'


# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)


# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))


class Dude(pygame.sprite.Sprite):
    """ Our Dude

    The Dude has three collision rects, one for the whole sprite "rect" and
    "old_rect", and another to check collisions with walls, called "feet".

    The position list is used because pygame rects are inaccurate for
    positioning sprites; because the values they get are 'rounded down'
    as integers, the sprite would move faster moving left or up.

    Feet is 1/2 as wide as the normal rect, and 8 pixels tall.  This size size
    allows the top of the sprite to overlap walls.  The feet rect is used for
    collisions, while the 'rect' rect is used for drawing.

    There is also an old_rect that is used to reposition the sprite if it
    collides with level walls.
    """

    def __init__(self, name, idleframes=None, walkframes=None, position=[0, 0], velocity=[0, 0]):
        self.name = name
        pygame.sprite.Sprite.__init__(self)
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        # Do sprite image stuff - Gonna use Ninjas to start
        if idleframes != None:
            self.idleanim = pyganim.PygAnimation(idleframes)
            self.walkanim = pyganim.PygAnimation(walkframes)
        #else:
        self.current_animation = self.idleanim
        self.idleanim.play()
        self.walkanim.play()
        #self.image = self.idleanim._images[0]
        #self.rect = self.image.get_rect()
        #self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
        self.dir = 'right'

    @property
    def image(self):
        return self.current_animation.getCurrentFrame()

    @property
    def rect(self):
        self._update_rect()
        return self._rect

    def _update_rect(self):
        self._rect = self.current_animation.getRect()
        self._rect.topleft = self.position

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt):

        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        if abs(self.velocity[0]) > 0 or abs(self.velocity[1]) > 0:
            self.current_animation = self.walkanim
        else:
            self.current_animation = self.idleanim
        if self.velocity[0] < 0 and self.dir == 'right':
            self.walkanim.flip(True, False)
            self.idleanim.flip(True, False) # Consolidate into function or property method thing
            self.dir = 'left'
        if self.velocity[0] > 0 and self.dir == 'left':
            self.walkanim.flip(True, False)
            self.idleanim.flip(True, False)
            self.dir = 'right'
        self.image
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
        #print('moving maindude')
    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom


class Scene2D(object):
    """ This class is a 2D game level

    This class will load data, create a pyscroll group, a dude object.
    It also reads input and moves the Dude around the map.
    Finally, it uses a pyscroll group to render the map and Dude.
    """
    filename = get_map(MAP_FILENAME)

    def __init__(self, game, mapfile, name='Untitled Scene2D'):
        self.game = game
        self.name = name
        self.screen = self.game.windowSurface

        # true while playscene
        self.playscene = False

        # load data from pytmx
        tmx_data = load_pygame(mapfile)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size(), clamp_camera=True)
        self.map_layer.zoom = 2

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=2)

        # # put the dude in the center of the map
        # self.dude.position = self.map_layer.map_rect.center
        # self.dude._position[0] -= 200
        # self.dude._position[1] += 400


    def addDude(self, dude, maindude=False):
        # add our dude to the scene's group
        self.group.add(dude)
        if maindude:
            self.maindude = dude

    def draw(self, surface):

        # center the map/screen on our main dude
        self.group.center(self.maindude.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)

    def getInput(self, ps4):
        """ Handle pygame input events
        """
        if ps4 != None:
            axis, button, hat = ps4.listen()
            if axis == None:
                pass#return #print('No axis')
            else:
                # Move left right (Left stick)
                if axis[0] == None:
                    pass
                elif axis[0] < 0:
                    self.maindude.velocity[0] = -DUDE_MOVE_SPEED*-axis[0]
                elif axis[0] > 0:
                    self.maindude.velocity[0] = DUDE_MOVE_SPEED*axis[0]
                elif axis[0] == 0:
                    self.maindude.velocity[0] = 0
                else:
                    pass
                # Move up down (Left stick)
                if axis[1] == None:
                    pass
                elif axis[1] < 0:
                    self.maindude.velocity[1] = -DUDE_MOVE_SPEED*-axis[1]
                elif axis[1] > 0:
                    self.maindude.velocity[1] = DUDE_MOVE_SPEED*axis[1]
                elif axis[1] == 0:
                    self.maindude.velocity[1] = 0
                else:
                    pass

            if button == None:
                #print('NONE')
                pass
            else:
                if button[1]: # Square
                    pass
                if button[3]: # Triangle
                    pass
                if button[8]: # Share
                    pygame.quit()
                    sys.exit()
                if button[9]: # Options
                    while button[9]:
                        axis, button, hat = ps4.listen()
                    self.playscene = False

                #print(button)

            for event in pygame.event.get():
                # this will be handled if the window is resized
                if event.type == VIDEORESIZE:
                    init_screen(event.w, event.h)
                    self.map_layer.set_size((event.w, event.h))




            # elif axis[0] == None:
            #     movebox.moveRight = False
            #     movebox.moveLeft = False
            # elif axis[0] < 0:
            #     movebox.moveLeft = True
            #     movebox.moveRight = False
            # elif axis[0] > 0:
            #     movebox.moveRight = True
            #     movebox.moveLeft = False
            # elif axis[0] == 0:
            #     movebox.moveRight = False
            #     movebox.moveLeft = False

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playscene = False

                if event.type == KEYDOWN:
                    if event.key == ord('w'):
                        self.maindude.velocity[1] = -DUDE_MOVE_SPEED
                    if event.key == ord('a'):
                        self.maindude.velocity[0] = -DUDE_MOVE_SPEED
                    if event.key == ord('s'):
                        self.maindude.velocity[1] = DUDE_MOVE_SPEED
                    if event.key == ord('d'):
                        self.maindude.velocity[0] = DUDE_MOVE_SPEED
                    if event.key == ord('x'):
                        self.map_layer.zoom += .25
                    if event.key == ord('z'):
                        value = self.map_layer.zoom - .25
                        if value > 0:
                            self.map_layer.zoom = value

                if event.type == KEYUP:
                    if event.key == ord('w'):
                        self.maindude.velocity[1] = 0
                    if event.key == ord('a'):
                        self.maindude.velocity[0] = 0
                    if event.key == ord('s'):
                        self.maindude.velocity[1] = 0
                    if event.key == ord('d'):
                        self.maindude.velocity[0] = 0
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit() 

                    if event.key == ord('p'):
                        self.playscene = False

                # this will be handled if the window is resized
                if event.type == VIDEORESIZE:
                    init_screen(event.w, event.h)
                    self.map_layer.set_size((event.w, event.h))

    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)

    def play(self, ps4):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        self.playscene = True
        clock.tick(1500) # wait for playscene = false signal to go (ps4 button thing)
        from collections import deque
        times = deque(maxlen=30)

        try:
            while self.playscene:
                dt = clock.tick(120) / 1000.
                times.append(clock.get_fps())
                Surface = self.screen
                self.getInput(ps4)
                self.update(dt)
                self.draw(Surface)

                # Write instruction text
                text = 'Move dude:   w a s d' 
                textsurface = self.game.myfont.render(text, True, (20, 20, 20))
                Surface.blit(textsurface,(50,50))
                text = 'Zoom in/out:    x/z'
                textsurface = self.game.myfont.render(text, True, (20, 20, 20))
                Surface.blit(textsurface,(50,80))  
                text = 'Next scene:     p' 
                textsurface = self.game.myfont.render(text, True, (20, 20, 20))
                Surface.blit(textsurface,(50,130)) 
                text = 'Quit:           Esc' 
                textsurface = self.game.myfont.render(text, True, (20, 20, 20))
                Surface.blit(textsurface,(50,145)) 

                pygame.display.flip()

        except KeyboardInterrupt:
            self.playscene = False

