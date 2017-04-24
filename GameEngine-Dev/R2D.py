# R2D.py 
# Contains methods relating to 2D scenes in RikedyGame Engine

# ------------------------ TO DO -----------------------------------

# 2D pathfinding
# Collisions, walls, level map implementation and interactable objects an NPCs
# Double check pygame.sprite is being used to its full usefulness
# Is sprite killing convenient and clean?
# Easy creating and deleting items and furniture
# maybe do it in layers so different layers don't interact - makes 2D platformers possible
# learn when i really need to use object class type
# pygame display flip or refresh?
# Make dude movement more flexible?

# -------------------------Program ---------------------------------
import math, sys, pygame, pyganim
from itertools import cycle
from RikedyGame import * # hmmmmmmmmmmmm?????

class Point2D:
    def __init__(self, x=0, y=0):
        self.x, self.y = float(x), float(y)

    def addX(self,newpos):
        x = self.x + newpos
        return Point2D(x, self.y)

    def addY(self,newpos):
        y = self.y + newpos
        return Point2D(self.x, y)
 
    def rotate(self, angle):
        """ Rotates the point around the point (0,0) by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point2D(x, y)

class Scene2D(object):

    def __init__(self, game, name='Untitled Scene2D'):
        #self.number = scenenumber
        self.WindowWidth, self.WindowHeight = game.WindowWidth, game.WindowHeight
        self._dudes = pygame.sprite.Group()
        self.dudelist = cycle(self._dudes)
        self.name = name
        self._layers = dict()
        self.addLayer()
        self.playscene = False

    def transferScene(self, newscene):
        self.playscene = False
        newscene.playscene = True
        # newscene.play()
        pass

    def getInput(self, maindude):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == ord('w'):
                    maindude.moveUp = True
                    maindude.moveDown = False
                if event.key == ord('a'):
                    maindude.moveLeft = True
                    maindude.moveRight = False
                if event.key == ord('s'):
                    maindude.moveDown = True
                    maindude.moveUp = False
                if event.key == ord('d'):
                    maindude.moveRight = True
                    maindude.moveLeft = False
            if event.type == KEYUP:
                if event.key == ord('b'):
                    self.maindude = next(self.dudelist)
                if event.key == ord('w'):
                    maindude.moveUp = False
                if event.key == ord('a'):
                    maindude.moveLeft = False
                if event.key == ord('s'):
                    maindude.moveDown = False
                if event.key == ord('d'):
                    maindude.moveRight = False
                if event.key == ord('p'):
                    playscene = False
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit() 
                if event.key == ord('f'):
                        if self.game.windowSurface.get_flags() & FULLSCREEN:
                            self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
                        else:
                            self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight),pygame.FULLSCREEN)
                if event.key == ord('p'):
                        self.playscene = False
                        

    def addThing(self, thing):
        pass

    def addLayer(self):
        i = len(self._layers)
        layername = 'layer_%i' % (i)
        newlayer = layer(i)
        self._layers[layername] = newlayer

    def addDude(self, dude, layer='layer_0', location=[0,0]):
        # Add dude to scene
        #xpos = random.randint(-self.WindowWidth/2,self.WindowWidth/2)
        #ypos = random.randint(-self.WindowHeight/2,self.WindowHeight/2)
        self._dudes.add(dude)
        self._layers[layer].add(dude)
        self.dudelist = cycle(self._dudes)

    def addSceneTransferer(self, sceneTransferer, layer='layer_0'):
        self._layers[layer].add(sceneTransferer)

    def play(self, Surface):
        self.playscene = True
        while self.playscene:
            self.getInput(self.maindude)
            for l in self._layers:
                self._layers[l].draw([255,0,0],Surface,self)
            pygame.display.flip()

class SceneTransferer(pygame.Rect):
    # method: collide, collide_and_key, click
    def __init__(self, name, newscene, location, width=50, height=100, method='collide'):
        self.name = name
        self.location = Point2D(location[0],location[1])
        self.center = (600,100)
        self.width = width
        self.height = height
        self.method = method
        self.newscene = newscene

        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False
        self.idleframes = None
        self.animation = self
        self.colour = [0,100,200]

class layer(pygame.sprite.Group):

    def __init__(self,number):
        self.number = number
        self.things = dict()
        self.BG = None

    def add(self,thing):
        self.things[thing.name] = thing

    def remove(self,thing):
        del self.things[thing.name]

    def draw(self,colour,Surface,scene):
        if self.number == 0:
            # Draw background
            Surface.fill([0,0,0])
            # Movement and animation
        for t in self.things:
            if self.things[t].moveUp or self.things[t].moveDown or self.things[t].moveLeft or self.things[t].moveRight:
                self.things[t].animation = self.things[t].walkanim
                self.things[t].move(self.things[t].Dir,self.things[t].moveUp,self.things[t].moveDown,self.things[t].moveLeft,self.things[t].moveRight,self.things[t].moveSpeed)
            else:
                if type(self.things[t].animation) == pyganim.PygAnimation:
                    self.things[t].animation = self.things[t].idleanim
                else:
                    pass
                   # print('other thing')
            # Test for collisions
            if type(self.things[t]) == SceneTransferer:
                if self.things[t].colliderect(scene.maindude.rect):
                    print('Scene Transferer collision')
                    self.things[t].newscene.play(Surface)

            # Draw stuff
            cx = scene.WindowWidth/2
            cy = scene.WindowHeight/2
            windowpos = (int(cx+self.things[t].location.x),int(cy-self.things[t].location.y))
            pygame.draw.circle(Surface,[0,0,0],windowpos,6)
            if self.things[t].idleframes != None:
                #print('drawing')
                #print(self.things[t])
                self.things[t].animation.play()
                #s = t.image.get_size()
                s = self.things[t].size
                spritepos = (windowpos[0]-s.x/2,windowpos[1]-s.y/2)
                #print(spritepos)
                self.things[t].animation.blit(Surface, spritepos)
                pygame.draw.rect(Surface, [180,0,0], self.things[t].rect)#.move(cx, cy))
            if type(self.things[t]) == SceneTransferer:
                pygame.draw.rect(Surface, self.things[t].colour,self.things[t])
        


class dude(pygame.sprite.Sprite):
    # define classwide attributes
    # The group of alive dudes
    _dudes = pygame.sprite.Group()

    def __init__(self,name,location=[0,0], idleframes=None, walkframes=None):
        # define per-instance attributes
        super().__init__() #adding super call to make dude a pygame Sprite
        #pygame.sprite.Sprite.__init__(self, dude._dudes) # super call adding dude to _dudes 
        self.name = name
        self.moveUp = False
        self.moveDown = False
        self.moveLeft = False
        self.moveRight = False
        self.moveSpeed = 8
        if idleframes == None:
            self.size = Point2D(float(1),float(1))
        else:
            size = pygame.image.load(idleframes[0][0]).get_size()
        self.size = Point2D(float(size[0]),float(size[1]))
        self.location =  Point2D(float(location[0]),float(location[1]))
        dude._dudes.add(self) # IS THIS NEEDED?
        # Do sprite image stuff - Gonna use Ninjas to start
        self.idleframes = idleframes
        self.walkframes = walkframes
        if idleframes != None:
            self.idleanim = pyganim.PygAnimation(self.idleframes)
            self.walkanim = pyganim.PygAnimation(self.walkframes)
        #else:
        self.image = self.idleframes[0]
        print(self.size)
        self.framecounter = 0
        self.animation = self.idleanim
        self.rect = pygame.Rect(self.location.x, self.location.y, self.size.x/5, self.size.y/5)
        self.Dir = 'Right'

    def __del__(self):
        #del layer._layers[]
        dude._dudes.remove(self)

    def dudewalk(self):
        self.animation = self.walkanim

    def dudestand(self):
  	    self.animation = self.idleanim

    def makedude(self):
  	    pass

    def __str__(self):
  	    return "%s is a dude" % (self.name)

    def move(self, Prev, Up, Down, Left, Right, speed):
        if Up:
            self.location.y += speed
            self.rect = self.rect.move(0,-speed)
        if Down:
            self.location.y -= speed
            self.rect = self.rect.move(0,speed)
        if Left:
            self.location.x -= speed
            self.rect = self.rect.move(-speed,0)
            if Prev == 'Right':
                self.Dir = 'Left'
                #self.animation.flip(True,False)   
                self.idleanim.flip(True,False)
                self.walkanim.flip(True,False) 
        if Right:
            self.location.x += speed
            self.rect = self.rect.move(speed,0)
            if Prev == 'Left':
                self.Dir = 'Right'
                #self.animation.flip(True,False)
                self.idleanim.flip(True,False)
                self.walkanim.flip(True,False) 
        


      	
  	

