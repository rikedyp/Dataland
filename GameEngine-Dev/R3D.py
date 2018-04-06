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

    def __init__(self, name='Mr. Default', colour=[255,255,255], position=Point3D(0,0,0), speed=1, width=5, height=5, depth=5, species='Cuboid'):
        # Defined species:
        # Cuboid - plain unmoving box
        # Movecube - moveable box 
        self.name = name
        self.species = species # e.g. sprite, goody, baddy, wall, cup, hero, frog
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position
        self.speed = speed
        self.wiggle = False
        self.figure8 = False
        self.t = 0
        self.verts = self.updateVerts(self.position)
        self.colour = colour
        self.moveUp = False
        self.moveDown = False
        self.moveRight = False
        self.moveLeft = False
        self.screenpos = []
        

    def __del__(self):
        pass

    def updateVerts(self,position = Point3D(0,0,0)):
        #print('updateVerts')
        # Turn location arguments into a vector array
        x0 = position.x-(self.width/2)
        x1 = position.x+(self.width/2)
        y0 = position.y-(self.height/2)
        y1 = position.y+(self.height/2)
        z0 = position.z-(self.depth/2)
        z1 = position.z+(self.depth/2)
        # if self.wiggle:
        #     #print('wiggle')
        #     x0 += 0.1*math.sin(self.t)#*math.cos(self.t)
        #     x1 += 0.1*math.cos(self.t)
        #     y0 += 0.1*math.sin(self.t)
        #     y1 -= 0.1*math.sin(self.t)#*math.cos(self.t)
        #     z0 -= 0.1*math.cos(self.t)
        #     z1 += 0.1*math.sin(self.t)
        #     self.t += 0.1
            #print(self.t)
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
        if self.wiggle:
            i = 0
            while i < 8:
                self.verts[i].x += 1*math.sin(self.t)
                self.verts[i+1].x += 1*math.sin(self.t)*math.cos(self.t)
                self.verts[i].y -= 1*math.sin(self.t)
                self.verts[i+1].y += 1*math.cos(self.t)
                self.verts[i].z -= 1*math.sin(self.t)
                self.verts[i+1].z -= 1*math.cos(self.t)
                self.t += 0.03
                i += 2
        if self.figure8:
            #a = 0
            #b = 0
            #((a*a))
            t = self.t
            for i in range(8):
                self.verts[i].x = position.x+self.width*math.sin(t+i)#((self.t**2)-1)/((self.t**2)+1)
                self.verts[i].y = position.y+self.height*math.sin(t+i)*math.cos(t+i)#(2*self.t*((self.t**2)-1))/(((self.t**2)+1)**2)
                self.verts[i].z = position.z+self.width*math.sin(t+i)
            self.t += 0.02

            #while i < 2:

        
        
        return self.verts

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def __str__(self):
        return "%s is a %s of size [%f,%f,%f]" % (self.name, self.species,self.width,self.height,self.depth)

    def move(self, speed=None, moveUp=None, moveDown=None, moveLeft=None, moveRight=None):
        #print('move')
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

    def __init__(self, width, height, zoomspeed=1, rotspeed=2.5, focus=Point3D(0,0,0), r=20, theta=0, phi=0):
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
        #self.screenpos = []

        BLACK = [0,0,0] #???
        WHITE = [255,255,255]
    
    def __str__(self):
        return "This is a Camera"

    def switchFocus(self, box):
        self.focus = box.position

    def update(self, cameramotion, rotspeed=None):
        if rotspeed == None:
            rotspeed = self.rotspeed
        if cameramotion[0]:
            self.theta += rotspeed
        if cameramotion[1]:
            self.theta -= rotspeed
        if cameramotion[2]: 
            self.phi -= rotspeed
        if cameramotion[3]:
            self.phi += rotspeed
        if cameramotion[4] and self.r > 3:
            self.r -= self.zoomspeed
        if cameramotion[5] and self.r < 10000:
            self.r += self.zoomspeed

    def drawit(self,thing,Surface,colour):
        # vector for transformed vertices
        t = []
        vd = []
        screenpos = []
        for v in thing.verts:
            # adjust verts for Camera focus
            d = v.addX(-self.focus.x).addY(-self.focus.y).addZ(-self.focus.z)
            # Do Camera rotations
            r = d.rotateX(self.theta).rotateY(self.phi)
            # # calculate distance from Camera to thing
            # th = self.theta*math.pi/180
            # ph = self.phi*math.pi/180
        
            # xc = self.r*math.cos(th)*math.sin(ph)
            # yc = self.r*math.sin(th)*math.sin(ph)
            # zc = self.r*math.cos(th)*math.cos(ph)
            # self.pos = Point3D(xc,yc,zc)
            # self.posrot = self.pos.rotateX(self.theta).rotateY(self.phi)
            # xd = r.x + self.posrot.x 
            # yd = r.y + self.posrot.y 
            # zd = r.z + self.posrot.z 
            # camr = math.sqrt(xd*xd+yd*yd+zd*zd)
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
            screenpos.append([xx,yy])
            pygame.draw.circle(Surface,colour,(xx,yy),3)
      
        closed = True
        #pointlist = sorted(pointlist)
        pygame.draw.aalines(Surface,colour,closed,pointlist,1)
        return screenpos

class Scene3D(object):

    def __init__(self, game, name='Untitled Scene3D'):
        #self.number = scenenumber
        self.game = game
        self.screen = self.game.windowSurface
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

    def getInput(self, movebox, ps4):
        if ps4 != None:
            axis, button, hat = ps4.listen()
            print(axis)
            if axis == None:
                pass#return #print('No axis')
            else:
                # Move left right (Left stick)
                if axis[0] == None:
                    pass
                elif axis[0] < 0:
                    movebox.move(movebox.speed*-axis[0], False, False, True, False)
                elif axis[0] > 0:
                    movebox.move(movebox.speed*axis[0], False, False, False, True)
                elif axis[0] == 0:
                    movebox.moveLeft = False
                    movebox.moveRight = False
                else:
                    pass
                # Move up down (Left stick)
                if axis[1] == None:
                    pass
                elif axis[1] < -0.1:
                    movebox.move(movebox.speed*-axis[1], True, False, False, False)
                elif axis[1] > 0.1:
                    movebox.move(movebox.speed*axis[1], False, True, False, False)
                else:
                    movebox.moveUp = False
                    movebox.moveDown = False
                # Rotate camera left right (Right stick)
                if axis[2] == None:
                    pass
                elif axis[2] < -0.1:
                    cameramotion = [False, False, True, False, False, False]
                    self.camera.update(cameramotion, self.camera.rotspeed*-axis[2])
                    # self.rotLeft = False
                    # self.rotRight = False
                elif axis[2] > 0.1:
                    cameramotion = [False, False, False, True, False, False]
                    self.camera.update(cameramotion, self.camera.rotspeed*axis[2])
                    # self.rotLeft = False
                    # self.rotRight = True
                else:
                    self.rotLeft = False
                    self.rotRight = False
                # Rotate camera up and down
                if axis[5] == None:
                    pass
                elif axis[5] < -0.1:
                    cameramotion = [True, False, False, False, False, False]
                    self.camera.update(cameramotion, self.camera.rotspeed*axis[5])
                    # self.rotUp = True
                    # self.rotDown = False
                elif axis[5] > 0.1:
                    cameramotion = [False, True, False, False, False, False]
                    self.camera.update(cameramotion, self.camera.rotspeed*-axis[5])
                    # self.rotUp = False
                    # self.rotDown = True
                else:
                    self.rotUp = False
                    self.rotDown = False

            if hat != {}:
                #print(hat[0])
                if hat[0] == (0,1):
                    while hat[0] == (0,1):
                        axis, button, hat = ps4.listen()
                    if self.game.windowSurface.get_flags() & FULLSCREEN:
                        self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight))
                    else:
                        self.game.windowSurface = pygame.display.set_mode((self.WindowWidth, self.WindowHeight),pygame.FULLSCREEN)
            else:
                pass


            if button == None:
                #print('NONE')
                pass
            else:
                if button[1]: # X
                    while button[1]:
                        axis, button, hat = ps4.listen()
                    self.movebox = self._boxes[next(self._boxlist)]
                    print('Move box')
                    print(self.movebox.name)
                if button[3]: # Triangle
                    while button[3]:
                        axis, button, hat = ps4.listen()
                    self.focusbox = self._boxes[next(self._boxlist)]
                    self.camera.switchFocus(self.focusbox)
                    print('Focus box')
                    print(self.focusbox.name)
                if button[6]: # R2
                    self.zoomOut = True
                if not button[6]:
                    self.zoomOut = False
                if button[7]: # R2
                    self.zoomIn = True
                if not button[7]:
                    self.zoomIn = False
                if button[8]: # Share
                    while button[8]:
                        axis, button, hat = ps4.listen()
                    pygame.quit()
                    sys.exit()
                if button[9]: # Options
                    while button[9]:
                        axis, button, hat = ps4.listen()
                    self.playscene = False

                #print(button)




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

                    # Keyboard and mouse events

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
                        if event.key == K_LEFT: # Camera motions
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
                        if event.key == ord('w'): # Moveable box motions
                            print('w')
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
                        # Animation keys
                        if event.key == ord('v'): # Make a vortex box wiggle
                            print ('v')
                            self.movebox.wiggle = True
                        if event.key == ord('b'): # Make a vortex box wiggle
                            print ('b')
                            self.movebox.figure8 = True

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
                        # Animation keys
                        if event.key == ord('v'): # Make a vortex box wiggle
                            self.movebox.wiggle = False
                        if event.key == ord('b'): # Make a vortex box wiggle
                            self.movebox.figure8 = False
                        # Game keys --------------------------------------
                        # --- SUBROUTINE THESE --------
                        if event.key == ord('q'):
                            self.switchBox()
                        if event.key == ord('e'):
                            self.switchFocus()
                        if event.key == ord('p'):
                            self.playscene = False

    def addBox(self, box, location=[0,0]):
        # Add box to scene
        self._boxes[box.name] = box
        self._boxlist = cycle(self._boxes)

    def switchBox(self):
        newmove = self._boxes[next(self._boxlist)]
        self.movebox = newmove

    def switchFocus(self):
        if self.focusbox == self.movebox:
            newfocus = self._boxes[next(self._boxlist)]
        else:
            newfocus = self.movebox
        self.camera.switchFocus(newfocus)
        self.focusbox = newfocus

    def play(self, ps4):
        # probably self.playscene
        boxmatchsensitivity = 10 # Sort this out
        self.clock = self.game.mainClock
        self.clock.tick(1000) # wait for playscene = false signal to go (ps4 button thing)
        #self.ps4 = ps4
        self.playscene = True
        Surface = self.screen
        while self.playscene:

            Surface.fill([0,0,0])
            text = 'Move movebox:   w a s d' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,50))
            text = 'Move camera:    Up Down Left Right'
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,65))
            text = 'Zoom in/out:    x/z'
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,80))
            text = 'Switch movebox:     q'
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,95))
            text = 'Switch focusbox:    e' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,110))   
            text = 'Next scene:     p' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,130)) 
            text = 'Quit:           Esc' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,145)) 
            text = 'Fullscreen:     f' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,160)) 
            text = 'Wiggle box:     v' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,175))
            text = 'Figure 8:     b' 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(50,190))

            text = 'Current movebox:   %s' % (self.movebox.name) 
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(300,50))
            text = 'Current focus:  %s' % (self.focusbox.name)
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(300,65))
            
            

            self.getInput(self.movebox, ps4)
            self.movebox.move()
            cameramotion = [self.rotUp, self.rotDown, self.rotLeft, self.rotRight, self.zoomIn, self.zoomOut]
            self.camera.update(cameramotion)

            for box in self._boxes:
                self._boxes[box].updateVerts(self._boxes[box].position)
                self._boxes[box].screenpos = self.camera.drawit(self._boxes[box], Surface, self._boxes[box].colour)
            # check for perspective collisions with camera focus box and move box # this doesn't seem efficient?
            # get focusbox screen positions
            if type(self.focusbox.screenpos) != float:
                for i in range(len(self.focusbox.screenpos)):
                    x = self.focusbox.screenpos[i][0]
                    y = self.focusbox.screenpos[i][1]
                    self.focusbox.screenpos[i] = [int(x), int(y)]
                focusboxverts = map(tuple, self.focusbox.screenpos)
            else:
                pass#print('Focus box floater')
            # move box screen positions
            if type(self.movebox.screenpos) != float:
                for i in range(len(self.movebox.screenpos)):
                    x = self.movebox.screenpos[i][0]
                    y = self.movebox.screenpos[i][1]
                    self.movebox.screenpos[i] = [int(x), int(y)]    
                moveboxverts = map(tuple, self.movebox.screenpos)
            else:
                pass#print('Move box floater')
            # compare all the boxes
            for box in self._boxes:
                if type(self._boxes[box].screenpos) == float:
                    pass#print('Other box floater')
                elif type(self._boxes[box].screenpos) == list:
                    for i in range(len(self._boxes[box].verts)):
                        x = self._boxes[box].screenpos[i][0]
                        y = self._boxes[box].screenpos[i][1]
                        self._boxes[box].screenpos[i] = [int(x),int(y)]
                        #self._boxes[box].screenpos[i,0] = int(self._boxes[box].screenpos[i,0])
                    #boxverts = map(int, self._boxes[box].screenpos)
                    boxverts = map(tuple, self._boxes[box].screenpos)
                    sboxverts = sorted(boxverts)
                    if type(self.focusbox.screenpos) ==  float:
                        print('Focus box floater')
                    else:
                        focusboxverts = map(tuple, self.focusbox.screenpos)
                        sfocusboxverts = sorted(focusboxverts)
                    if type(self.movebox.screenpos) == float:
                        print('Move box floater')
                    else:
                        moveboxverts = map(tuple, self.movebox.screenpos)
                        smoveboxverts = sorted(moveboxverts)

                    if box != self.focusbox.name:
                        #print(sboxverts)
                        # find if projected box centers and widths and heights match (within a range)
                        # boxes have 8 verts
                        if len(sboxverts) > 1:
                            boxwidth = sboxverts[-1][0] - sboxverts[0][0]
                            boxheight = sboxverts[-1][1] - sboxverts[0][1]
                            boxcenter = [sboxverts[0][0] + boxwidth/2, sboxverts[0][1] + boxheight/2]
                        else:
                            print('Box width not defined')
                            print(sboxverts)
                        
                        #print(sfocusboxverts)
                        if len(sfocusboxverts) > 1:
                            focusboxwidth = sfocusboxverts[-1][0] - sfocusboxverts[0][0]
                            focusboxheight = sfocusboxverts[-1][1] - sfocusboxverts[0][1]
                            focusboxcenter = [sfocusboxverts[0][0] + focusboxwidth/2, sfocusboxverts[0][1] + focusboxheight/2]
                            boxdiff = [abs(focusboxcenter[0] - boxcenter[0]), abs(focusboxcenter[1] - boxcenter[1])]
                            boxsizediff = [abs(focusboxwidth - boxwidth), abs(focusboxheight - boxheight)]
                            if boxdiff[0] < boxmatchsensitivity and boxdiff[1] < boxmatchsensitivity:
                                if boxsizediff[0] < boxmatchsensitivity and boxsizediff[1] < boxmatchsensitivity:
                                    print('Focus box perspective event')
                                    print(self._boxes[box])
                                
                        else:
                            print('Focus box width not defined')
                            print(sfocusboxverts)

                    if box != self.movebox.name:
                        # Now check for movebox match
                        if len(smoveboxverts) > 1:
                            moveboxwidth = smoveboxverts[-1][0] - smoveboxverts[0][0]
                            moveboxheight = smoveboxverts[-1][1] - smoveboxverts[0][1]
                            moveboxcenter = [smoveboxverts[0][0] + moveboxwidth/2, smoveboxverts[0][1] + moveboxheight/2]
                            boxdiff = [abs(moveboxcenter[0] - boxcenter[0]), abs(moveboxcenter[1] - boxcenter[1])]
                            boxsizediff = [abs(moveboxwidth - boxwidth), abs(moveboxheight - boxheight)]
                            if boxdiff[0] < boxmatchsensitivity and boxdiff[1] < boxmatchsensitivity:
                                if boxsizediff[0] < boxmatchsensitivity and boxsizediff[1] < boxmatchsensitivity:
                                    # print(self.movebox)
                                    # print('Move box perspective event')
                                    # print(self._boxes[box])
                                    pass
                                else:
                                    pass
                            else:
                                pass
                        else:
                            print('Move box width not defined')
                            print(smoveboxverts)
            # Refresh the display   
            # FPS
            self.game.mainClock.tick()
            time = pygame.time.get_ticks()
            text = 'Time:  %3.2f' % (time)
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(300,80))
            fps = self.game.mainClock.get_fps()
            text = 'FPS:  %3.2f' % (fps)
            textsurface = self.game.myfont.render(text, True, (20, 200, 20))
            Surface.blit(textsurface,(300,95))
            pygame.display.flip()
