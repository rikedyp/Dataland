# RGameTester.py
# chalkboard program to test the RikedyGame Engine
from RikedyGame import *
import numpy as np
import math
# set up pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)
mainClock = pygame.time.Clock()
# set up the window
WINDOWWIDTH = 800   
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#,pygame.FULLSCREEN)
pygame.display.set_caption('Graphics1')


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

zoomfactor = 1.5
MOVESPEED = 0.5
MOVEANGLE = 3
Alice = box('Alice','Cube',2,2,2,Point3D(0,0,0))
Bob = box('Bob','Cube',5,5,5,Point3D(0,0,0))
cam = camera(WINDOWWIDTH,WINDOWHEIGHT, Alice.position, 50, 0, 0,1,5)
Reset = False
# run the game loop
while True:
  if Reset:
    Alice = box('Alice','Cube',2,2,2,Point3D(0,0,0))
    Bob = box('Bob','Cube',5,5,5,Point3D(0,0,0))
    cam = camera(WINDOWWIDTH,WINDOWHEIGHT, Alice.position, 50, 0, 0,1,5)
  # check for events
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
   
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
      if event.key == ord('c'):
        SwitchFocus = True

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
      if event.key == ord('x'):
        zoomIn = False
      if event.key == ord('z'):
        zoomOut = False
      if event.key == ord('w'):
        moveUp = False
      if event.key == ord('s'):
        moveDown = False
      if event.key == ord('a'):
        moveLeft = False
      if event.key == ord('d'):
        moveRight = False
      if event.key == ord('c'):
        SwitchFocus = False

  cam.update(SwitchFocus,rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut) 
  #print(Bob.position.x)
  Alice.position = Alice.move(Alice.position,MOVESPEED,moveUp,moveDown,moveLeft,moveRight)
  Alice.name = 'AAA'
  Bob.name = 'BBB'
  #print(Alice.position.x)
  Alice.verts = Alice.updatePos(Alice.position)
  windowSurface.fill(BLACK)
  color = WHITE
  Bob.verts = Bob.updatePos(Bob.position)
  cam.drawit(Alice,windowSurface,color)
  color = GREEN
  cam.drawit(Bob,windowSurface,color)
  #print(Alice.position.x,Alice.position.z)
  #print(Bob.name,Alice.name)
# TODO make game loop part of a class?
#   Collision detection
#   Path finding
#   Make camera able to change focus to objects and maybe can use an invisible object or some moveable location to have moveable camera
#   Make objects rotatable in gamespace (not camera space)  

  # Draw on control instructions
  text = 'Move white box: w,a,s,d,         Rotate camera up,down,left,right     Zoom camera z,x'
  textsurface = myfont.render(text, True, (200, 200, 200))
  windowSurface.blit(textsurface,(50,50))
  pygame.display.flip()
  mainClock.tick(40)



