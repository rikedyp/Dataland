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
    factor = fov / (viewer_distance + self.z)
    x = self.x * factor + win_width / 2
    y = -self.y * factor + win_height / 2
    return Point3D(x, y, self.z)

# Define the box class - these will be containers which hold images and can move them around in a 3D space
class box(object):

  def __init__(self, name, species,width,height,depth,position):
    self.name = name
    self.species = species # e.g. sprite, goody, baddy, wall, cup, hero, frog
    self.width = width
    self.height = height
    self.depth = depth
    self.position = self.move(position,0,False,False,False,False)
    self.verts = self.updatePos(self.position)

  def __del__(self):
  	pass

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
    for v in thing.verts:
      # adjust verts for camera focus
      d = v#.addX(self.focus.x).addY(self.focus.y).addZ(self.focus.z)
      # Do camera rotations
      r = d.rotateX(self.theta).rotateY(self.phi)
      # Transform the point from 3D to 2D
      p = r.project(Surface.get_width(), Surface.get_height(), 256, self.r)
      # Put the point in the list of transformed vertices
      t.append(p)

  # Calculate the average Z values of each face.
  # avg_z = []
  # i = 0
  # for f in self.faces:
  #   z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
  #   avg_z.append([i,z])
  #   i = i + 1
#-------------------------------------------------
    pointlist = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    for i in range(len(t)):
      xx = int(t[i].x)
      yy = int(t[i].y)
      pointlist[i] = [xx,yy]
      pygame.draw.circle(Surface,color,(xx,yy),3)
    closed = True
    pygame.draw.aalines(Surface,color,closed,pointlist,1)
    for i in range(len(t)):
      pointlist[i]

#TODO functions moveup,down,left,right,zoomin,zoomout,rotleft,rotup,rotdown,rotright
class Game():
  pass