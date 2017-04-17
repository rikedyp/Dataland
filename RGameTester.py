# RGameTester.py
# chalkboard program to test the RikedyGame Engine
from RikedyGame import *
import numpy as np
import math
# set up pygame
pygame.init()
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

zoomfactor = 1.5
MOVESPEED = 0.5
MOVEANGLE = 3
initpos = Point3D(0,0,0)
Alice = box('Alice','Cube',2,2,2,initpos)
cam = camera(WINDOWWIDTH,WINDOWHEIGHT, Alice.position, 50, 0, 0,1,5)

# run the game loop
while True:
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

    if event.type == KEYUP:
      if event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()
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

  #if moveLeft:
  #  Alice.position[1] += MOVESPEED
  #if moveRight:
  #  Alice.position[1] -= MOVESPEED
  Alice.move(moveUp,moveDown,moveLeft,moveRight,MOVESPEED)
  verts = Alice.updatePos()
  cam.update(rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut)
  windowSurface.fill(BLACK)
  color = WHITE
    # Calculate pointlist from box, position and size
  # closed = True
  # # Draw cube
  # pointlist = np.array([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
  # i = 0
  # for i in verts:
  #   # rotate cube
  #   x,y,z = cam.rotate(x,y,z)
  #   # adjust zoom
  #   z = z+(cam.r*math.cos(cam.theta)*math.cos(cam.phi))
  #   if z != 0:
  #     f = abs(200/z) #TODO AVOID DIVIDE BY ZERO - FIND SOLUTION WHICH IGNORES ASYMPTOTE
  #     x,y = f*x,f*y
  #     pointlist[i] = [cam.cx+x,cam.cy+y]
  #     i += 1
  #     if abs(x) < cam.cx and abs(y) < cam.cy:
  #       pygame.draw.circle(windowSurface,color,(int(cam.cx)+int(x),int(cam.cy)+int(y)),3)
  # #pygame.draw.circle(windowSurface,color,(int(cam.cx),int(cam.cy)),19)
  # # for i in range(len(pointlist)):
  # pygame.draw.aalines(windowSurface, color, closed, pointlist, 3) #prolly get errors here
  # print(pointlist[0])
  cam.drawit(Alice,windowSurface,color)











  pygame.display.flip()
  mainClock.tick(40)



