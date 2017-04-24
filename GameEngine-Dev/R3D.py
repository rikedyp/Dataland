# R3D.py
# Contains methods relating to 3D scenes in RikedyGame Engine

# ------------------------ TO DO -------------------------

# 3D scenes are made of planes (horizons), boxes (sprites with special 3D properties)
# and a Camera (might make Camera a special box type)
# or make Camera part of Scene3D?
# 3D collision detection using pygame rects?
# Clean up input methods
# Collision detection 
# Other verifiers for puzzles and shit
# Consider reset method
# Box collision causes scene transfer

# ---------------------- - METHOD -------------------------

# scene = Scene3D()

# ---------------------------------------------------------

import pygame, sys, random, math
from pygame.locals import * 
from itertools import cycle

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def addX(self,newpos):
        x = self.x + newpos
        return Point3D(x,self.y,self.z)

    def addY(self,newpos):
        y = self.y + newpos
        return Point3D(self.x,y,self.z)

    def addZ(self,newpos):
        z = self.z + newpos
        return Point3D(self.x,self.y,z)

    def rotateX(self, angle):
        #  """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        #""" Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        #  """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        #    """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

# Define the box class - these will be containers which hold images and can move them around in a 3D space
class box(object):

    def __init__(self, name='Mr. Default', colour=[255,255,255], position=Point3D(0,0,0), speed=5, width=5, height=5, depth=5, species='Cube'):
        self.name = name
        self.species = species # e.g. sprite, goody, baddy, wall, cup, hero, frog
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position
        self.speed = speed
        self.verts = self.updateVerts(self.position)
        self.colour = colour
        self.moveUp = False
        self.moveDown = False
        self.moveRight = False
        self.moveLeft = False

    def __del__(self):
        pass

    def updateVerts(self,position = Point3D(0,0,0)):
        # Turn location arguments into a vector array

        x0 = position.x-(self.width/2)
        x1 = position.x+(self.width/2)
        y0 = position.y-(self.height/2)
        y1 = position.y+(self.height/2)
        z0 = position.z-(self.depth/2)
        z1 = position.z+(self.depth/2)

        self.verts = [
        Point3D(x0,y0,z0),
        Point3D(x1,y0,z0),
        Point3D(x0,y1,z0),
        Point3D(x1,y1,z0),
        Point3D(x0,y0,z1),
        Point3D(x1,y0,z1),
        Point3D(x0,y1,z1),        
        Point3D(x1,y1,z1)
            ]
        return self.verts

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def __str__(self):
        return "%s is a %s of size [%f,%f,%f]" % (self.name, self.species,self.width,self.height,self.depth)

    def move(self, speed=None, moveUp=None, moveDown=None, moveLeft=None, moveRight=None):
        position = self.position
        if speed == None:
            speed = self.speed
        if moveUp == None:
            moveUp = self.moveUp
            moveDown = self.moveDown
            moveLeft = self.moveLeft
            moveRight = self.moveRight
        if moveUp:
            if moveRight:
                position.z += speed/math.sqrt(2)
                position.x += speed/math.sqrt(2)
            elif moveLeft:
                position.z += speed/math.sqrt(2)
                position.x -= speed/math.sqrt(2)
            else:
                position.z += speed
        elif moveDown:
            if moveRight:
                position.z -= speed/math.sqrt(2)
                position.x += speed/math.sqrt(2)
            elif moveLeft:
                position.z -= speed/math.sqrt(2)
                position.x -= speed/math.sqrt(2)
            else:
                position.z -= speed
        elif moveLeft:
            position.x -= speed
        elif moveRight:
            position.x += speed
        else:
            pass
        self.position = position
  
# Define the Camera class which handles drawing the objects
class Camera(object):

    def __init__(self, width, height, zoomspeed=1, rotspeed=3, focus=Point3D(0,0,0), r=20, theta=0, phi=0):
        self.width = width
        self.height = height
        self.focus = focus
        self.r = r # distance from focus
        self.theta = theta # altitude angle in radians
        self.phi = phi # azimuthal angle in radians
        self.cx = width/2
        self.cy = height/2
        self.zoomspeed = zoomspeed
        self.rotspeed = rotspeed
        self.pos = Point3D(0,0,r)

        BLACK = [0,0,0] #???
        WHITE = [255,255,255]
    
    def __str__(self):
        return "This is a Camera"

    def switchFocus(self, box):
        self.focus = box.position

    def update(self, cameramotion):
        if cameramotion[0]:
            self.theta += self.rotspeed
        if cameramotion[1]:
            self.theta -= self.rotspeed
        if cameramotion[2]: 
            self.phi -= self.rotspeed
        if cameramotion[3]:
            self.phi += self.rotspeed
        if cameramotion[4] and self.r > 3:
            self.r -= self.zoomspeed
        if cameramotion[5] and self.r < 10000:
            self.r += self.zoomspeed

    def drawit(self,thing,Surface,colour):
        # vector for transformed vertices
        t = []
        vd = []
        for v in thing.verts:
            # adjust verts for Camera focus
            d = v.addX(-self.focus.x).addY(-self.focus.y).addZ(-self.focus.z)
            # Do Camera rotations
            r = d.rotateX(self.theta).rotateY(self.phi)
            # calculate distance from Camera to thing
            th = self.theta*math.pi/180
            ph = self.phi*math.pi/180
        
            xc = self.r*math.cos(th)*math.sin(ph)
            yc = self.r*math.sin(th)*math.sin(ph)
            zc = self.r*math.cos(th)*math.cos(ph)
            self.pos = Point3D(xc,yc,zc)
            self.posrot = self.pos.rotateX(self.theta).rotateY(self.phi)
            xd = r.x + self.posrot.x 
            yd = r.y + self.posrot.y 
            zd = r.z + self.posrot.z 
            camr = math.sqrt(xd*xd+yd*yd+zd*zd)
            viewer_distance = self.r+r.z 
            vd.append(float(viewer_distance))
            if viewer_distance > 0:
                p = r.project(Surface.get_width(), Surface.get_height(), 512, viewer_distance)
                #else p = null
                # Put the point in the list of transformed vertices
                t.append(p)
        vd = sorted(vd)
        if vd[0] < 0.8:
            t = 'null'

        # Calculate the average Z values of each face.
        # avg_z = []
        # i = 0
        # for f in self.faces:
        #   z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
        #   avg_z.append([i,z])
        #   i = i + 1
        #-------------------------------------------------
        pointlist = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        if t == 'null':
            return viewer_distance
        for i in range(len(t)):
            xx = int(t[i].x)
            yy = int(t[i].y)
            pointlist[i] = [xx,yy]
            pygame.draw.circle(Surface,colour,(xx,yy),3)
      
        closed = True
        #pointlist = sorted(pointlist)
        pygame.draw.aalines(Surface,colour,closed,pointlist,1)
        return viewer_distance

class Scene3D(object):

    def __init__(self, game, name='Untitled Scene3D'):
        #self.number = scenenumber
        self.WindowWidth, self.WindowHeight = game.WindowWidth, game.WindowHeight
        self.game = game
        self._boxes = dict()
        self._boxlist = cycle(self._boxes)
        self.name = name
        self._planes = dict()
        self.playscene = False
        self.camera = Camera(self.WindowWidth, self.WindowHeight)
        # Camera variables
        self.rotUp = False
        self.rotDown = False
        self.rotLeft = False
        self.rotRight = False
        self.zoomIn = False
        self.zoomOut = False
        # Mouse variables
        self.LeftClickDown = False
        self.RightClickDown = False

    def getInput(self, movebox):

        for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    zoomIn = False
                    zoomOut = False
                    xMouse = event.pos[0]
                    yMouse = event.pos[1]
                    if event.button == 1:
                        # left 
                        self.LeftClickDown = True
                    if event.button == 2:
                        # middle click
                        pass
                    if event.button == 3:
                        # right click
                        self.RightClickDown = True        
                    if event.button == 4:
                        # Scroll up

                        self.camera.update([self.rotUp, self.rotDown, self.rotLeft, self.rotRight, True, False]) 
                    if event.button == 5:
                        # Scroll down
                        self.camera.update([self.rotUp, self.rotDown, self.rotLeft, self.rotRight, False, True]) 

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # left click up
                        self.LeftClickDown = False
                    if event.button == 2:
                        # middle click up
                        pass
                    if event.button == 3:
                        # right click up
                        self.RightClickDown = False

                if event.type == pygame.MOUSEMOTION:
                    if self.RightClickDown:
                        xrel,yrel = event.rel
                        self.camera.theta -= yrel/self.camera.rotspeed
                        #if xrel > 0 and cam.phi > -math.pi/2:
                        self.camera.phi -= xrel/self.camera.rotspeed
                        #if xrel < 0 and cam.phi < math.pi/2:
                        #  cam.phi -= xrel/dragfactor

                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.rotRight = False
                        self.rotLeft = True
                    if event.key == K_RIGHT:
                        self.rotLeft = False
                        self.rotRight = True
                    if event.key == K_UP:
                        self.rotDown = False
                        self.rotUp = True
                    if event.key == K_DOWN:
                        self.rotUp = False
                        self.rotDown = True
                    if event.key == ord('x'):
                        self.zoomIn = True
                        self.zoomOut = False
                    if event.key == ord('z'):
                        self.zoomIn = False
                        self.zoomOut = True
                    if event.key == ord('w'):
                        movebox.moveUp = True
                        movebox.moveDown = False
                    if event.key == ord('a'):
                        movebox.moveLeft = True
                        movebox.moveRight = False
                    if event.key == ord('s'):
                        movebox.moveDown = True
                        movebox.moveUp = False
                    if event.key == ord('d'):
                        movebox.moveRight = True
                        movebox.moveLeft = False
                    if event.key == ord('r'):
                        Reset = True

                if event.type == KEYUP:
                    # General keys ---------------------------------------
                    if event.key == ord('w'):
                        movebox.moveUp = False
                    if event.key == ord('a'):
                        movebox.moveLeft = False
                    if event.key == ord('s'):
                        movebox.moveDown = False
                    if event.key == ord('d'):
                        movebox.moveRight = False
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit() 
                    if event.key == ord('r'):
                        Reset = False
                    if event.key == K_LEFT:
                        self.rotLeft = False
                    if event.key == K_RIGHT:
                        self.rotRight = False
                    if event.key == K_UP:
                        self.rotUp = False
                    if event.key == K_DOWN:
                        self.rotDown = False
                    if event.key == ord('x'):
                        self.zoomIn = False
                    if event.key == ord('z'):
                        self.zoomOut = False
                    if event.key == ord('f'):
                        if self.game.windowSurface.get_flags() & FULLSCREEN:
                            self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
                        else:
                            self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight),pygame.FULLSCREEN)
                    # Game keys --------------------------------------
                    if event.key == ord('q'):
                        self.movebox = self._boxes[next(self._boxlist)]
                    if event.key == ord('e'):
                        self.camera.switchFocus(self._boxes[next(self._boxlist)])
                    if event.key == ord('p'):
                        self.playscene = False

    def addBox(self, box, location=[0,0]):
        # Add box to scene
        self._boxes[box.name] = box
        self._boxlist = cycle(self._boxes)

    def play(self, Surface):
        # probably self.playscene
        self.playscene = True

        while self.playscene:
            Surface.fill([0,0,0])
            self.getInput(self.movebox)
            self.movebox.move()
            cameramotion = [self.rotUp, self.rotDown, self.rotLeft, self.rotRight, self.zoomIn, self.zoomOut]
            self.camera.update(cameramotion)
            for box in self._boxes:
                self._boxes[box].updateVerts(self._boxes[box].position)
                self.camera.drawit(self._boxes[box], Surface, self._boxes[box].colour)
            pygame.display.flip()
