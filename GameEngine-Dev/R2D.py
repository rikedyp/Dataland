# R2D.py writing the 2D graphics part of RikedyGame

# ------------------------ TO DO -----------------------------------

# 2D pathfinding
# sprites, animations and images/textures
# FINISH implementing pygame.sprite
# Implement pyganim for animations
# Easy creating and deleting items and furniture
# maybe do it in layers so different layers don't interact - makes 2D platformers possible
# learn when i really need to use object class type
# MAYBE use point3D so can choose to have parallax with layers instead of current layer method
# pygame display flip or refresh?
# Make levels work through .map files and level class with spawndude fct and other attributes

# -------------------------Program ---------------------------------
import math, sys, pygame, pyganim
from RikedyGame import *
class Point3D:
  def __init__(self, x = 0, y = 0):
    self.x, self.y = float(x), float(y)

  def addX(self,newpos):
    x = self.x + newpos
    return Point3D(x,self.y)

  def addY(self,newpos):
    y = self.y + newpos
    return Point3D(self.x,y)
 
  def rotateZ(self, angle):
     #  """ Rotates the point around the point (0,0) by the given angle in degrees. """
    rad = angle * math.pi / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x = self.x * cosa - self.y * sina
    y = self.x * sina + self.y * cosa
    return Point3D(x, y)

class dude(pygame.sprite.Sprite):
  # define classwide attributes
  # The group of alive dudes
  _dudes = pygame.sprite.Group()

  def __init__(self,name,alayer,position=[0,0], idleframes=None, walkframes=None):
    # define per-instance attributes
    super().__init__() #adding super call to make dude a pygame Sprite
    #pygame.sprite.Sprite.__init__(self, dude._dudes) # super call adding dude to _dudes 
    self.name = name
    self.moving = False
    if idleframes == None:
      self.size = Point3D(float(1),float(1))
    else:
      size = pygame.image.load(idleframes[0][0]).get_size()
      self.size = Point3D(float(size[0]),float(size[1]))
    self.position =  Point3D(float(position[0]),float(position[1]))
    dude._dudes.add(self)
    self.layernumber = alayer.number
    alayer.add(self)
    # Do sprite image stuff - Gonna use Ninjas to start
    self.idleframes = idleframes
    self.walkframes = walkframes
    if idleframes != None:
      self.idleanim = pyganim.PygAnimation(self.idleframes)
      self.walkanim = pyganim.PygAnimation(self.walkframes)
    #else:
    self.image = pygame.Surface([size[0],size[1]])
    self.framecounter = 0
    self.animation = self.idleanim
    self.rect = self.image.get_rect()
    self.Dir = 'Right'

  def __del__(self):
    #del layer._layers[]
    dude._dudes.remove(self)

  def dudewalk(self):
    self.animation = self.walkanim
    self.moving = True

  def dudestand(self):
  	self.animation = self.idleanim
  	self.moving = False

  def makedude(self):
  	pass

  def __str__(self):
  	return "%s is a dude" % (self.name)

  def move(self,Prev,Up,Down,Left,Right,speed):
    if Up:
      self.position.y += speed
    if Down:
      self.position.y -= speed
    if Left:
      self.position.x -= speed
      if Prev == 'Right':
        self.Dir = 'Left'
        #self.animation.flip(True,False)   
        self.idleanim.flip(True,False)
        self.walkanim.flip(True,False) 
    if Right:
      self.position.x += speed
      if Prev == 'Left':
        self.Dir = 'Right'
        #self.animation.flip(True,False)
        self.idleanim.flip(True,False)
        self.walkanim.flip(True,False) 

class layer(pygame.sprite.Group):
  _layers = []

  def __init__(self,number):
    self.number = number
    layer._layers.append(self)
    self.things = []

  def add(self,thing):
    self.things.append(thing)

  def remove(self,thing):
    thingpos = self.things.index(thing)
    del self.things[thingpos]
    

  def drawit(self,colour,Surface,g):
    if self.number == 0:
      Surface.fill([0,0,0])
      for t in self.things:
        windowpos = (int((g.WINDOWWIDTH/2)+t.position.x),int((g.WINDOWHEIGHT/2)-t.position.y))
        pygame.draw.circle(Surface,colour,windowpos,6)
        if t.idleframes != None:
          t.animation.play()
          #s = t.image.get_size()
          s = t.size
          spritepos = (windowpos[0]-s.x/2,windowpos[1]-s.y/2)
          t.animation.blit(Surface, spritepos)
      	
  	

class game(object):
  # Handles gameplay 

  def __init__(self,WINDOWWIDTH,WINDOWHEIGHT):
    self.WINDOWHEIGHT = WINDOWHEIGHT
    self.WINDOWWIDTH = WINDOWWIDTH
	# set up pygame
    pygame.init()
    pygame.font.init()
    self.myfont = pygame.font.SysFont('Ariel', 20)
    self.mainClock = pygame.time.Clock()
    # set up the window
    self.windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#,pygame.FULLSCREEN)
    pygame.display.set_caption('Graphics1')
    FS = False # Fullscreen toggle

    WHITE = [255,255,255]
    BLACK = [0,0,0]

    

  def play(self):
    pygame.font.init()
    myfont = pygame.font.SysFont('Ariel', 20)
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    MOVESPEED = 8
    dudemoveindex = 0
    # Run the game loop
    while True:
      for event in pygame.event.get():
        if event.type == KEYDOWN:
          if event.key == ord('w'):
            moveUp = True
            moveDown = False
          if event.key == ord('a'):
            moveLeft = True
            moveRight = False
          if event.key == ord('s'):
            moveDown = True
            moveUp = False
          if event.key == ord('d'):
            moveRight = True
            moveLeft = False

        if event.type == KEYUP:
          if event.key == ord('w'):
            moveUp = False
          if event.key == ord('a'):
            moveLeft = False
          if event.key == ord('s'):
            moveDown = False
          if event.key == ord('d'):
            moveRight = False
          if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit() 
          if event.key == ord('n'):
            # Spawn randomly located new dude
            xpos = random.randint(-self.WINDOWWIDTH/2,self.WINDOWWIDTH/2)
            ypos = random.randint(-self.WINDOWHEIGHT/2,self.WINDOWHEIGHT/2)
            newname = 'newguy #%i' % (len(dude._dudes)-1)
            newguy = dude(newname,baselayer,[xpos,ypos],iframes,sframes)
            spritelist = dude._dudes.sprites()
            print(spritelist[dudemoveindex])
            print('Created')
            print(dudemoveindex)
          if event.key == ord('m') and len(dude._dudes) > 1:
            spritelist = dude._dudes.sprites()
          	# Delete moveable dude
            print(spritelist[dudemoveindex])
            print('deleted')
            # Which layer?
            layernumber = spritelist[dudemoveindex].layernumber
            # Remove dude from layer
            layer._layers[layernumber].remove(spritelist[dudemoveindex])
            # Remove dude from list of dudes
            del spritelist[dudemoveindex]
            if dudemoveindex > 0:
              dudemoveindex -= 1
            else:
              dudemoveindex = 0
            spritelist[dudemoveindex].dudestand
            print(dudemoveindex)
          if event.key == ord('b'):
            spritelist = dude._dudes.sprites()
            spritelist[dudemoveindex].dudestand()
            dudemoveindex += 1
            if dudemoveindex >= len(spritelist):
              dudemoveindex = 0
            spritelist[dudemoveindex].dudewalk()
            print(spritelist[dudemoveindex])
            print('who can now be moved')
            print(dudemoveindex)
            # TODO there is a bug when changing moveable character while character is moving

      for l in layer._layers:
        for t in l.things:
      	  if t.moving:
      	    if moveUp or moveDown or moveLeft or moveRight:
      	      t.animation = t.walkanim
      	      t.move(t.Dir,moveUp,moveDown,moveLeft,moveRight,MOVESPEED)
      	    else:
      	      t.animation = t.idleanim
      	  else:
      	  	t.animation = t.idleanim
      for l in layer._layers:
        l.drawit([0,0,0],self.windowSurface,self)
      text = 'Move dude: w,a,s,d,             New dude: n   Delete dude: m   Change moveable dude: b   '
      textsurface = myfont.render(text, True, (200, 200, 200))
      self.windowSurface.blit(textsurface,(50,50))
      pygame.display.flip()
      self.mainClock.tick(24)
      #print(layer._layers[0].number)
      #print(dude._dudes[0])
      #print(dude._dudes[0].position.x,dude._dudes[0].position.x)

g = game(800,400)
baselayer = layer(0)
iframes = []
nframes = []
sframes = []

for i in range(4):
  path = 'Ninja/4x/idle_%i.png' % (i)
  ninja = (path, 250)
  iframes.append(ninja)
for i in range(6):
  path = 'Ninja/4x/run_%i.png' % (i)
  ninja = (path, 100)
  nframes.append(ninja)
  path = 'Ninja/4x/swim_%i.png' % (i)
  ninja = (path, 100)
  sframes.append(ninja)
# ninstand = pyganim.PygAnimation(iframes)
# ninrun = pyganim.PygAnimation(nframes)
# ninswim = pyganim.PygAnimation(sframes)

guy = dude('Alice',baselayer,[0,0],iframes,nframes)
guy.moving = True
#guy.move(1,0,0,0,3)
g.play()