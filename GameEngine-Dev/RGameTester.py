# RGameTester.py
# chalkboard program to test the RikedyGame Engine
from RikedyGame import *

baselayer = layer(0)
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

g = Game(800,600)

s1 = Scene2D(g)
s1.loadMap('Maps/untitled.tmx')
Alice = dude('Alice',[0,0],iframes,nframes)
Bob = dude('Bob',[200,-100],iframes,sframes)
s1.addDude(Alice, 'layer_0')
s1.addDude(Bob,'layer_0')
s1.maindude = Alice
s1.camdude = Alice
g.addScene(s1)

s2 = Scene3D(g)
Corey = box('Corey', [200,200,0])
Dave = box('Dave',[200,200,200],Point3D(10,0,0))
s2.addBox(Corey)
s2.addBox(Dave)
s2.movebox = Corey
s2.focusbox = Dave
g.addScene(s2)

ST = SceneTransferer('ST', s2, [200,100], )
s1.addSceneTransferer(ST)

g.play()
