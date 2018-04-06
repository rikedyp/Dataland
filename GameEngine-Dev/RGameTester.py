# RGameTester.py
# chalkboard program to test the RikedyGame Engine
from RikedyGame import *

iframes = []
nframes = []
sframes = []

# Import ninja animation
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


g = Game(800, 600)
mapfile = 'Maps/map1.tmx'
s1 = Scene2D(g, mapfile)
Alice = Dude('Alice',iframes,nframes, position=[200, 500], velocity=[0, 0])
#Bob = dude('Bob',[200,-100],iframes,sframes)
s1.addDude(Alice, True)
#s1.addDude(Bob,'layer_0')
g.addScene(s1)

s2 = Scene3D(g)
Green = box('Green', [0,255,0])
# #self, name='Mr. Default', colour=[255,255,255], position=Point3D(0,0,0), speed=1, width=5, height=5, depth=5, species='Cube'
Purple = box('Purple',[100,20,200],Point3D(10,0,60), 2, 8, 8, 8)
Red = box('Red', [255,50,50], Point3D(30,0,50), 1, 5, 10, 5, 'Cuboid')
White = box('White', [240,240,240], Point3D(-100,0,0), 5, 10, 10, 10)
Pink = box('Pink', [255,100,255], Point3D(10,0,0), 3)
Blue = box('Blue', [0,100,255], Point3D(50,0,50), 3, 50, 50, 50)
Figure8 = box('Figure8', [100,220,50], Point3D(50,50,50), 3, 50, 60, 70, 'Vortex')
s2.addBox(Green)
s2.addBox(Purple)
s2.addBox(Red)
s2.addBox(White)
s2.addBox(Pink)
s2.addBox(Blue)
s2.addBox(Figure8)

# for i in range(100):
# 	limename = 'Lime%i' % (i)
# 	Lime = box(limename, [132,226,10], Point3D(i*30*math.cos(i*math.pi/7),i*30*math.sin(i*math.pi/4),i*70), 15, 65, 65, 65)
# 	s2.addBox(Lime)
s2.movebox = Green
s2.focusbox = Green
g.addScene(s2)

# ST = SceneTransferer('ST', s2, [400,100], )
# s1.addSceneTransferer(ST)
# if __name__ == "__main__":

#     try:
#         g.play
#     except:
#         pygame.quit()
#         raise
g.play()
