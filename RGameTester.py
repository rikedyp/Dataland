# RGameTester.py
# chalkboard program to test the RikedyGame Engine
from RikedyGame import *
import numpy as np
import math
# set up pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Ariel', 20)
mainClock = pygame.time.Clock()
# set up the window
WINDOWWIDTH = 800   
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#,pygame.FULLSCREEN)
pygame.display.set_caption('Graphics1')
FS = False # Fullscreen toggle

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
rotUp = False
rotDown = False
rotLeft = False
rotRight = False
zoomIn = False
zoomOut = False
SwitchFocus = False
RightClickDown = False
LeftClickDown = False
xdragfactor = 360/WINDOWWIDTH
ydragfactor = 360/WINDOWHEIGHT
zoomfactor = 10
MOVESPEED = 0.5
boxindex = 0
boxmoveindex = 0

# Create some stuff
Alice = box('Alice','Cuboid',2,2,2,Point3D(0,0,0),WHITE)
Bob = box('Bob','Cuboid',5,5,5,Point3D(0,0,0),GREEN)
Corey = box('Corey','Cube',5,5,5,Point3D(0,0,10),[50,100,255])
Dave = box('Dave','Cube',100,100,100,Point3D(0,0,0),[0,255,255])
cam = camera(WINDOWWIDTH,WINDOWHEIGHT, Alice.position, 20, 0, 0,1,5)

# run the game loop
Reset = False
while True:
  if Reset:
    cam.r = 20
    cam.theta = 0
    cam.phi = 0

  # check for events
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
   
    if event.type == pygame.MOUSEBUTTONDOWN:
      zoomIn = False
      zoomOut = False
      xMouse = event.pos[0]
      yMouse = event.pos[1]
      if event.button == 1:
        # left 
        LeftClickDown = True
      if event.button == 2:
        # middle click
        pass
      if event.button == 3:
        # right click
        RightClickDown = True        
      if event.button == 4:
        # scroll no more
        zoomIn = True
        zoomOut = False
        cam.update(SwitchFocus,rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut) 
        zoomIn = False
      if event.button == 5:
        zoomIn = False
        zoomOut = True
        cam.update(SwitchFocus,rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut) 
        zoomOut = False

    if event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        # left click up
        LeftClickDown = False
        pass
      if event.button == 2:
        # middle click up
        pass
      if event.button == 3:
        # right click up
        RightClickDown = False

    if event.type == pygame.MOUSEMOTION:
      if RightClickDown:
        xrel,yrel = event.rel
        if yrel > 0 and cam.theta > -90:
          cam.theta -= yrel*ydragfactor
        if yrel < 0 and cam.theta < 90:
          cam.theta -= yrel*ydragfactor
        #if xrel > 0 and cam.phi > -math.pi/2:
        cam.phi -= xrel*xdragfactor
        #if xrel < 0 and cam.phi < math.pi/2:
        #  cam.phi -= xrel/dragfactor

    if event.type == KEYDOWN:
      # change the keyboard variables
      if event.key == K_LEFT:
        rotRight = False
        rotLeft = True
      if event.key == K_RIGHT:
        rotLeft = False
        rotRight = True
      if event.key == K_UP:
        rotDown = False
        rotUp = True
      if event.key == K_DOWN:
        rotUp = False
        rotDown = True
      if event.key == ord('x'):
        zoomIn = True
        zoomOut = False
      if event.key == ord('z'):
      	zoomIn = False
      	zoomOut = True
      if event.key == ord('w'):
        moveUp = True
        moveDown = False
      if event.key == ord('s'):
        moveUp = False
        moveDown = True
      if event.key == ord('a'):
        moveLeft = True
        moveRight = False
      if event.key == ord('d'):
        moveLeft = False
        moveRight = True
      if event.key == ord('r'):
        Reset = True
      if event.key == ord('q'):
        boxindex += 1
        if boxindex >= len(box._boxes):
          boxindex = 0        
        cam.focus = box._boxes[boxindex].position
        print(box._boxes[boxindex]) 
        print('who is now in focus.')
        #cam.focus = boxes
        SwitchFocus = True
        
      if event.key == ord('e'):
        boxmoveindex += 1
        if boxmoveindex >= len(box._boxes):
          boxmoveindex = 0
        print(box._boxes[boxmoveindex])
        print('who can now be moved')

    if event.type == KEYUP:
      if event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == ord('r'):
        Reset = False
      if event.key == K_LEFT:
        rotLeft = False
      if event.key == K_RIGHT:
        rotRight = False
      if event.key == K_UP:
        rotUp = False
      if event.key == K_DOWN:
        rotDown = False
      if event.key == ord('w'):
        moveUp = False
      if event.key == ord('s'):
        moveDown = False
      if event.key == ord('a'):
        moveLeft = False
      if event.key == ord('d'):
        moveRight = False
      if event.key == ord('q'):
        SwitchFocus = False
      if event.key == ord('x'):
        zoomIn = False
      if event.key == ord('z'):
        zoomOut = False
      if event.key == ord('f') and FS == False:
        FS = True
        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.FULLSCREEN)
      elif event.key == ord('f') and FS == True:
        FS = False
        windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
      else:
        pass

  cam.update(SwitchFocus,rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut) 
  #print(Bob.position.x)
  #print(box._boxes[boxindex].position.x)
  #print(boxindex)
  #print(boxmoveindex)
  
  windowSurface.fill(BLACK)
  color = WHITE
  color = GREEN
  box._boxes[boxmoveindex].position = box._boxes[boxmoveindex].move(box._boxes[boxmoveindex].position,MOVESPEED,moveUp,moveDown,moveLeft,moveRight)
  
  # print(cam.theta,cam.phi,cam.r)
  # print('ok')
  # Corey = box('Corey','Bean',3,ss3,3,Point3D(0,0,0))

  # print(box._boxes)
  # print(' ')
  # print(box._boxtypes)

  # print('Bob is dead')
  # print(box._boxes)
  # print(' ')
  # print(box._boxtypes)
# TODO make game loop part of a class?
#   Collision detection
#   Path finding
#   Make boxes easily creatable and destroyable within game loop or whatever
#   Make objects rotatable in gamespace (not camera space)  
#   Make text a fct within camera
#   Make key and mouse press part a fct within RikedyGame

  # Draw on control instructions
  text = 'Move box: w,a,s,d,             Rotate camera: up,down,left,right, right click and drag   '
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,50))
  text = 'Reset camera: r,                     Zoom camera: z,x,scroll'
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,70))
  text = 'Switch camera focus: q,              Switch moveable box: e'
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,90))
  text = "Moveable %s: %s" % (box._boxes[boxmoveindex].species,box._boxes[boxmoveindex].name)
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,110))
  text = "%s in focus: %s" % (box._boxes[boxindex].species,box._boxes[boxindex].name)
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,130))
  text = "Toggle Fullscreen: f"
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,150))
  #print(cam.pos.z - Alice.position.z)#38
  #print(viewerdist)
  for b in range(len(box._boxes)):
    box._boxes[b].updatePos(box._boxes[b].position)
    cam.drawit(box._boxes[b],windowSurface,box._boxes[b].colour)
  pygame.display.flip()
  mainClock.tick(40)



