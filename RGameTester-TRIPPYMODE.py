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
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
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
zoomIn = False
zoomOut = False

zoomfactor = 1.5
MOVESPEED = 1
MOVEANGLE = 5

blank = np.array([[0,0,0],[0,0,0]])
Alice = box('Alice','Cube',100,100,200,[0,0,0],blank)
cam = camera(WINDOWWIDTH,WINDOWHEIGHT, Alice.position, 50, 0, 0)

# run the game loop
while True:
  # check for events
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
   
    if event.type == KEYDOWN:
      # change the keyboard variables
      if event.key == K_LEFT or event.key == ord('a'):
        moveRight = False
        moveLeft = True
      if event.key == K_RIGHT or event.key == ord('d'):
        moveLeft = False
        moveRight = True
      if event.key == K_UP or event.key == ord('w'):
        moveDown = False
        moveUp = True
      if event.key == K_DOWN or event.key == ord('s'):
        moveUp = False
        moveDown = True
      if event.key == ord('z'):
      	zoomIn = True
      	zoomOut = False
      if event.key == ord('x'):
      	zoomIn = False
      	zoomOut = True

    if event.type == KEYUP:
      if event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

  #keys = pygame.key.get_pressed()
  #if keys[K_LEFT]:
  #  cam.update()
  # if keys[K_RIGHT]:
  #   player.pos.left += 10
  # if keys[K_UP]:
  #   player.pos.top -= 10
  # if keys[K_DOWN]:
  #   player.pos.left += 10
  # if keys[K_SPACE]: 
  #  print 'firing gun'
      if event.key == K_LEFT or event.key == ord('a'):
        moveLeft = False
      if event.key == K_RIGHT or event.key == ord('d'):
        moveRight = False
      if event.key == K_UP or event.key == ord('w'):
        moveUp = False
      if event.key == K_DOWN or event.key == ord('s'):
        moveDown = False
      if event.key == ord('z'):
      	zoomIn = False
      if event.key == ord('x'):
      	zoomOut = False

  
  Alice.updatePos()
    #print(cam.r,cam.theta,cam.phi)
    #Bob = box('Bob','Cube',6,7,8,[300,200,200])
    #print (Alice,'\n',Bob)
    #print (cam)
  cam.update(moveUp,moveDown,moveLeft,moveRight,zoomIn,zoomOut)
  windowSurface.fill(BLACK)
  color = WHITE
  closed = True
    # Calculate pointlist from box, position and size
  points = Alice.points
  
  # Draw cube
  for x,y,z in points:
    # rotate points
    x,y,z = cam.rotate(x,y,z)
    # adjust zoom
    z = z+cam.r
    f = 20/z
    x,y = f*x,f*y
    if abs(x) < cam.cx and abs(y) < cam.cy:
      pygame.draw.circle(windowSurface,color,(int(cam.cx)+int(x),int(cam.cy)+int(y)),3)
  #pygame.draw.circle(windowSurface,color,(int(cam.cx),int(cam.cy)),19)
  # for i in range(len(pointlist)):
    


  # # x' = (rcos(theta)sin(phi)+x)   + zcosthetacosphi
  # # y' = (rsin(theta)sin(phi)+y)
  # # z' = rcostheta cos phi
  #   if pointlist[i,0] < 0:
  #     pointlist[i,0] = (cam.width/2)+points[i,0]
  #   pointlist[i,0] = (cam.width/2)+points[i,0]+points[i,2]*math.cos(cam.theta)
  #   pointlist[i,1] = (cam.height/2)+points[i,1]+points[i,2]*math.cos(cam.theta)
  #pygame.draw.aalines(windowSurface, color, closed, pointlist, 3) #prolly get errors here

  #print(cam.r,cam.theta,cam.phi)

  # x = r cos(theta) sin(phi)
  # y = 

  pygame.display.flip()
  mainClock.tick(40)



