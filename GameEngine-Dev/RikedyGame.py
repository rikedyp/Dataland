# RikedyGame.py
# RikedyP Game Engine - hopefully a fairly light, simple to understand and easy to implement 2D and pseudo-3D game engine for pygame python3
# This document uses 2 spaces per indentation - do not use tab
import pygame, sys, random, math
from pygame.locals import *
import numpy as np

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
  _boxindex = 0
  _boxes = []
  _boxtypes = []
  def __init__(self, name = 'Mr. Default', species = 'Cube',width = 5,height = 5,depth = 5,position = Point3D(0,0,0),colour = [255,255,255]):
    self.name = name
    self.species = species # e.g. sprite, goody, baddy, wall, cup, hero, frog
    self.width = width
    self.height = height
    self.depth = depth
    self.position = self.move(position,0,False,False,False,False)
    self.verts = self.updatePos(self.position)
    self._boxes.append(self)
    self._boxtypes.append(species)
    self._boxindex += 1
    self.colour = colour

  def __del__(self):
  	n = box._boxindex -1
  	del box._boxes[n]
  	del box._boxtypes[n]

  def updatePos(self,position = Point3D(0,0,0)):
    # Turn location arguments into a vector array

    x0 = position.x-(self.width/2)
    x1 = position.x+(self.width/2)
    y0 = position.y-(self.height/2)
    y1 = position.y+(self.height/2)
    z0 = position.z-(self.depth/2)
    z1 = position.z+(self.depth/2)
    #print(position.x,position.y,position.z)
    self.verts = [
      Point3D(x0,y0,z0),
      Point3D(x0,y0,z1),
      Point3D(x0,y1,z0),
      Point3D(x0,y1,z1),
      Point3D(x1,y0,z0),
      Point3D(x1,y0,z1),
      Point3D(x1,y1,z0),
      Point3D(x1,y1,z1)
        ]
    return self.verts

  def getName(self):
    return self.name

  def getSpecies(self):
    return self.species

  def __str__(self):
    return "%s is a %s of size [%f,%f,%f]" % (self.name, self.species,self.width,self.height,self.depth)

  def move(self,position,speed,moveUp,moveDown,moveLeft,moveRight):
    if moveUp:
      position.z += speed
    if moveDown:
      position.z -= speed
    if moveLeft:
      position.x -= speed
    if moveRight:
      position.x += speed
    return position 
  
# Define the camera class which handles drawing the objects
class camera(object):

  def __init__(self, width, height, focus, r, theta, phi, zoomspeed, rotspeed):
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
    BLACK = [0,0,0]
    WHITE = [255,255,255]
    
  def __str__(self):
  	return "This is a camera"

  def update(self,SwitchFocus,rotUp,rotDown,rotLeft,rotRight,zoomIn,zoomOut):
    if rotDown:
  	  self.theta -= self.rotspeed
    if rotUp:
  	  self.theta += self.rotspeed
    if rotLeft: 
      self.phi -= self.rotspeed
    if rotRight:
      self.phi += self.rotspeed
    if zoomIn and self.r > 3:
      self.r -= self.zoomspeed
    if zoomOut and self.r < 10000:
      self.r += self.zoomspeed
    if SwitchFocus:
      pass

  def drawit(self,thing,Surface,color):
#-----------------------------------------------------
  # vector for transformed vertices
    t = []
    vd = []
    for v in thing.verts:
      # adjust verts for camera focus
      d = v.addX(-self.focus.x).addY(-self.focus.y).addZ(-self.focus.z)
      # Do camera rotations
      r = d.rotateX(self.theta).rotateY(self.phi)
      # calculate distance from camera to thing
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
      camr = np.sqrt(xd*xd+yd*yd+zd*zd)
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
      pygame.draw.circle(Surface,color,(xx,yy),3)
      
    closed = True
    #pointlist = sorted(pointlist)
    pygame.draw.aalines(Surface,color,closed,pointlist,1)
    return viewer_distance

class Game():
  pass