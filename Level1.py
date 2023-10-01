from cmu_112_graphics import *
import time, math, random
class Projectile:
    def __init__(self,x,y,angle,speed):
        self.x=x
        self.y=y
        self.angle=angle
        self.speed=speed
    def getSpeed(self):
        return self.speed
    def getAngle(self):
        return self.angle
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setSpeed(self,speed):
        self.speed=speed
    def setAngle(self,angle):
        self.angle=angle
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
class bouncyProjectile(Projectile):
    def __init__(self,x,y,angle,speed,bounces):
        super().__init__(x,y,angle,speed)
        self.bounces=bounces
    def getBounces(self):
        return self.bounces
    def setBounces(self,bounces):
        self.bounces=bounces
class Monster:
    def __init__(self,x,y,hp):
        self.x=x
        self.y=y
        self.xv=0
        self.yv=0
        self.hp=hp
        self.path=[]
        self.angle=None
        self.stunned=0
        self.distance=None
    def getDistance(self):
        return self.distance
    def getStunned(self):
        return self.stunned
    def getAngle(self):
        return self.angle
    def getPath(self):
        return self.path
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getXV(self):
        return self.xv
    def getYV(self):
        return self.yv
    def getHp(self):
        return self.hp
    def setDistance(self,distance):
        self.distance=distance
    def setStunned(self,t):
        self.stunned=t
    def setAngle(self,a):
        self.angle=a
    def setPath(self,path):
        self.path=path
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setXV(self,xv):
        self.xv=xv
    def setYV(self,yv):
        self.yv=yv
    def setHp(self,hp):
        self.hp=hp
    def update(self):
        self.xv*=0.8
        self.yv*=0.8
class Boss(Monster):
    def __init__(self,x,y):
        super().__init__(x,y,3000)
        self.angle=0
        self.timer=30
    def setAngle(self,angle):
        self.angle=angle
    def getAngle(self):
        return self.angle
    def setTimer(self,timer):
        self.timer=timer
    def getTimer(self):
        return self.timer
class Melee(Monster):
    def __init__(self,x,y):
        super().__init__(x,y,100)
class R1(Monster):
    def __init__(self,x,y):
        super().__init__(x,y,50)
        self.projectileDelay=0
    def setProjectileDelay(self,pd):
        self.projectileDelay=pd
    def getProjectileDelay(self):
        return self.projectileDelay
        
class Heap:
    #https://en.wikipedia.org/wiki/Heap_(data_structure)
    def __init__(self):
        self.heap=[]
    def add(self,n):
        i=len(self.heap)
        self.heap+=[n]
        while((i-1)//2>=0):
            j=(i-1)//2
            if(self.heap[i][1]<self.heap[j][1]):
                self.heap[i],self.heap[j]=self.heap[j],self.heap[i]
                i=j
            else:
                break
    def __repr__(self):
        s=""
        for i in self.heap:
            s+=str(i)+","
        return s
    def remove(self):
        i=len(self.heap)
        n=self.heap[0]
        temp=self.heap.pop(i-1)
        if(len(self.heap)!=0):
            self.heap[0]=temp
        index=0
        l=2*index+1
        r=2*index+2
        while((l<i-1 and self.heap[l][1]<self.heap[index][1]) or (r<i-1 and self.heap[r][1]<self.heap[index][1])):
            if(r>=i-1 or self.heap[l][1]<self.heap[r][1]):
                self.heap[index],self.heap[l]=self.heap[l],self.heap[index]
                index=l
            else:
                self.heap[index],self.heap[r]=self.heap[r],self.heap[index]
                index=r
            l=2*index+1
            r=2*index+2
        return n
    def getHeap(self):
        return self.heap
        

class Player:
    def __init__(self):
        self.x=0
        self.y=0
        self.xv=0
        self.yv=0
        self.fx=0
        self.fy=0
        self.dcTimer=181
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getXV(self):
        return self.xv
    def getYV(self):
        return self.yv
    def getFX(self):
        return self.fx
    def getFY(self):
        return self.fy
    def getDCTimer(self):
        return self.dcTimer
    def setX(self,x):
        self.x=x
        if(self.dcTimer>60):
            self.fx=x
    def setY(self,y):
        self.y=y
        if(self.dcTimer>60):
            self.fy=y
    def setXV(self,xv):
        self.xv=xv
    def setYV(self,yv):
        self.yv=yv
    def setFX(self,fx):
        self.fx=fx
    def setFY(self,fy):
        self.fy=fy
    def setDCTimer(self,timer):
        self.dcTimer=timer
    def update(self):
        self.xv*=0.8
        self.yv*=0.8

class Room():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.corridors=[]
        self.spikes=[]
        self.points={}
        self.partitions=set()
        self.monsters=set()
        self.projectiles=set()
        self.completed=False
    def getCompleted(self):
        return self.completed
    def setCompleted(self,completed):
        self.completed=completed
    def removeProjectile(self,projectile):
        self.projectiles.remove(projectile)
    def addProjectile(self,projectile):
        self.projectiles.add(projectile)
    def getProjectiles(self):
        return self.projectiles
    def removeMonster(self,monster):
        self.monsters.remove(monster)
    def addMonster(self,monster):
        self.monsters.add(monster)
    def getMonsters(self,):
        return self.monsters
    def setMonsters(self,monsters):
        self.monsters=monsters
    def addPartition(self,p):
        self.partitions.add(p)
    def getPartitions(self):
        return self.partitions
    def createPoint(self,point):
        if(point not in self.points):
            self.points[point]={}
    def addConnection(self,p1,p2,dist):
        self.points[p1][p2]=dist
        self.points[p2][p1]=dist
    def getPoints(self):
        return self.points
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setWidth(self,width):
        self.width=width
    def setHeight(self,height):
        self.height=height
    def setCorridors(self,corridors):
        self.corridors=corridors
    def getCorridors(self):
        return self.corridors
    def setSpikes(self,spikes):
        self.spikes=spikes
    def getSpikes(self):
        return self.spikes

class Corridor():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.corridors=[]
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setWidth(self,width):
        self.width=width
    def setHeight(self,height):
        self.height=height
    def setCorridors(self,corridors):
        self.corridors=corridors
    def getCorridors(self):
        return self.corridors

class Partition():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.c1=None
        self.c2=None
        self.room=None
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def setWidth(self,width):
        self.width=width
    def setHeight(self,height):
        self.height=height
    def getC1(self):
        return self.c1
    def getC2(self):
        return self.c2
    def setC1(self,c1):
        self.c1=c1
    def setC2(self,c2):
        self.c2=c2
    def getRoom(self):
        return self.room
    def setRoom(self,room):
        self.room=room

def createChildren(p,depth):
    # ALGORITHM IDEA FROM http://www.roguebasin.com/index.php/Basic_BSP_Dungeon_generation
    # EVERYTHING IMPLEMENTED AND THOUGHT OUT MYSELF FROM THE PICTURES THERE
    # Cuts the given partition into two pieces.
    # if those two pieces are big enough, sets the two as its children
    #0 for vertical cut, 1 for horizontal cut
    direction=random.randint(0,1)
    x0=p.getX()
    x1=x0+p.getWidth()
    y0=p.getY()
    y1=y0+p.getHeight()
    if(direction==0 and x1-x0<1500*2):
        if y1-y0>5000:
            direction=1
    elif(direction==1 and y1-y0<1500*2):
        if x1-x0>5000:
            direction=0
    if(direction==0):
        if(x1-x0)<1500*2:
            return None
        margins=int(0.2*p.getWidth())
        while 1:
            cut=random.randint(x0+margins,x1-margins)
            if(cut-x0>1200 and x1-cut>1200):
                c1=Partition(x0,y0,cut-x0,y1-y0)
                c2=Partition(cut,y0,x1-cut,y1-y0)
                p.setC1(c1)
                p.setC2(c2)
                createChildren(c1,depth+1)
                createChildren(c2,depth+1)
                break
    else:
        if(y1-y0)<1500*2:
            return None
        margins=int(0.2*p.getHeight())
        while 1:
            cut=random.randint(y0+margins,y1-margins)
            if(cut-y0>1200 and y1-cut>1200):
                c1=Partition(x0,y0,x1-x0,cut-y0)
                c2=Partition(x0,cut,x1-x0,y1-cut)
                p.setC1(c1)
                p.setC2(c2)
                createChildren(c1,depth+1)
                createChildren(c2,depth+1)
                break

def mousePressed(app,event):
    if(app.currentMode=="Menu" and event.x>app.width//6 and event.x<5*app.width//6 and event.y>5*app.height//20 and event.y<9*app.height//20):
        app.currentMode="Game"

    #Used for debugging
    """x,y=getAbsoluteCoords(app,event.x,event.y)
    print("MOUSE")
    print(x,y)
    aStar(app,x,y,app.player.getX(),app.player.getY())"""
    """i=isInBounds(app,event.x*10,event.y*10)
    print(i)
    if(i!=None):
        print(app.bounds[i].getCorridors())
        for c in app.bounds[i].getCorridors():
            print(app.bounds.index(c))"""

def getAbsoluteCoords(app,x,y):
    #Gets absolute coords given canvas coords
    px,py=app.player.getX(),app.player.getY()
    return x-app.width//2+px,y-app.height//2+py

def createRooms(app,p):
    # Randomly creates a room with some bounds within the given partition if
    # p has no children, otherwise, goes lower in the tree
    if(p.getC1()==None):
        x0=p.getX()
        width=p.getWidth()
        y0=p.getY()
        height=p.getHeight()
        lbound=int(0.3*width)
        rbound=int(0.8*width)
        tbound=int(0.3*height)
        bbound=int(0.8*height)
        rw=random.randint(lbound,rbound)
        rh=random.randint(tbound,bbound)
        xmargin=int(0.1*width)
        ymargin=int(0.1*height)
        rx=x0+random.randint(xmargin,width-xmargin-rw+1)
        ry=y0+random.randint(ymargin,height-ymargin-rh+1)
        r=Room(rx,ry,rw,rh)
        p.setRoom(r)
        app.bounds+=[r]
        app.incompleteRooms+=1
    else:
        createRooms(app,p.getC1())
        createRooms(app,p.getC2())

def createCorridors(app,p):
    # Makes corridors between every two partitions, starting from the bottom
    # of the tree
    if(p.getC1()!=None):
        p1=p.getC1()
        p2=p.getC2()
        createCorridors(app,p1)
        createCorridors(app,p2)
        r1=p1.getRoom()
        r2=p2.getRoom()
        if(p1.getY()==p2.getY()):
            # Vertical cut
            x0=p1.getX()
            cut=p2.getX()
            x2=p2.getX()+p2.getWidth()
            y0=p1.getY()
            y1=p1.getY()+p1.getHeight()
            counter=0
            success=False
            # Shoots 10 lines out from random y coord in both x directions, 
            # if they both intersect fully (Enough for a corridor to spawn 
            # with some room on both sides) then creates a corridor
            while counter<10:
                starty=random.randint(y0,y1)
                negDist=100
                lReached=False
                room1=None
                while negDist<cut-x0:
                    # i and j will be the actual bounds of the corridor
                    # k and l are to make sure there is sufficient space on both sides of the corridor for better-looking connections
                    # i and k need to hit the same room, j and l need to hit the same room, or else you very rarely get
                    # a funky edge-case that connects a corridor to a very close room and allows you to jump the wall
                    i=isInBounds(app,cut-negDist,starty)
                    j=isInBounds(app,cut-negDist,starty+200)
                    k=isInBounds(app,cut-negDist,starty-50)
                    l=isInBounds(app,cut-negDist,starty+200+50)
                    if(i!=None and j!=None and i==k and j==l):
                        lReached=True
                        room1=[app.bounds[i]]
                        if(i!=j):
                            room1+=[app.bounds[j]]
                        break
                    elif(i==None and j==None and k==None and l==None):
                        negDist+=100
                    else:
                        break
                rReached=False
                if(lReached):
                    posDist=100
                    rReached=False
                    while posDist<x2-cut:
                        i=isInBounds(app,cut+posDist,starty)
                        j=isInBounds(app,cut+posDist,starty+200)
                        k=isInBounds(app,cut+posDist,starty-50)
                        l=isInBounds(app,cut+posDist,starty+200+50)
                        if(i!=None and j!=None and i==k and j==l):
                            c=Corridor(cut-negDist,starty,posDist+negDist,200)
                            app.corridors+=[c]
                            app.bounds+=[c]
                            for r in room1:
                                r.setCorridors(r.getCorridors()+[c])
                                c.setCorridors(c.getCorridors()+[r])
                            app.bounds[i].setCorridors(app.bounds[i].getCorridors()+[c])
                            c.setCorridors(c.getCorridors()+[app.bounds[i]])
                            if(i!=j):
                                app.bounds[j].setCorridors(app.bounds[j].getCorridors()+[c])
                                c.setCorridors(c.getCorridors()+[app.bounds[j]])
                            rReached=True
                            break
                        elif(i==None and j==None and k==None and l==None):
                            posDist+=100
                        else:
                            break
                if(lReached and rReached):
                    success=True
                    break
                counter+=1
            # If it fails, shoots rays from random starty one x direction at a time,
            # then creates a z/s-tetrimino shaped corridor connecting the two points
            if not success:
                c1=(0,0)
                c2=(0,0)
                room1=None
                room2=None
                while 1:
                    starty=random.randint(y0,y1)
                    negDist=100
                    lReached=False
                    while negDist<cut-x0:
                        i=isInBounds(app,cut-negDist,starty)
                        j=isInBounds(app,cut-negDist,starty+200)
                        k=isInBounds(app,cut-negDist,starty-50)
                        l=isInBounds(app,cut-negDist,starty+200+50)
                        if(i!=None and j!=None and i==k and j==l):
                            lReached=True
                            room1=[app.bounds[i]]
                            if(i!=j):
                                room1+=[app.bounds[j]]
                            break
                        elif(i==None and j==None and k==None and l==None):
                            negDist+=100
                        else:
                            break
                    if(lReached):
                        c1=(cut-negDist,starty)
                        break
                while 1:
                    starty=random.randint(y0,y1)
                    posDist=100
                    rReached=False
                    while posDist<x2-cut:
                        i=isInBounds(app,cut+posDist,starty)
                        j=isInBounds(app,cut+posDist,starty+200)
                        k=isInBounds(app,cut+posDist,starty-50)
                        l=isInBounds(app,cut+posDist,starty+200+50)
                        if(i!=None and j!=None and i==k and j==l):
                            room2=[app.bounds[i]]
                            if(i!=j):
                                room2+=[app.bounds[j]]
                            rReached=True
                            break
                        elif(i==None and j==None and k==None and l==None):
                            posDist+=100
                        else:
                            break
                    if(rReached):
                        c2=(cut+posDist,starty)
                        break
                x0,y0=c1
                x1,y1=c2
                corridor1=Corridor(x0,y0,(x1-x0)//2-100,200)
                if(y0<y1):
                    corridor2=Corridor((x1+x0)//2-100,y0,200,y1-y0+200)
                else:
                    corridor2=Corridor((x1+x0)//2-100,y1,200,y0-y1+200)
                corridor3=Corridor((x1+x0)//2+100,y1,(x1-x0)//2-100,200)
                corridor1.setCorridors(corridor1.getCorridors()+[corridor2])
                corridor1.setCorridors(corridor1.getCorridors()+[corridor3])
                corridor2.setCorridors(corridor2.getCorridors()+[corridor1])
                corridor2.setCorridors(corridor2.getCorridors()+[corridor3])
                corridor3.setCorridors(corridor3.getCorridors()+[corridor1])
                corridor3.setCorridors(corridor3.getCorridors()+[corridor2])
                for r in room1:
                    r.setCorridors(r.getCorridors()+[corridor1,corridor2,corridor3])
                    corridor1.setCorridors(corridor1.getCorridors()+[r])
                    corridor2.setCorridors(corridor2.getCorridors()+[r])
                    corridor3.setCorridors(corridor3.getCorridors()+[r])
                for r in room2:
                    r.setCorridors(r.getCorridors()+[corridor1,corridor2,corridor3])
                    corridor1.setCorridors(corridor1.getCorridors()+[r])
                    corridor2.setCorridors(corridor2.getCorridors()+[r])
                    corridor3.setCorridors(corridor3.getCorridors()+[r])
                app.corridors+=[corridor1]
                app.bounds+=[corridor1]
                app.corridors+=[corridor2]
                app.bounds+=[corridor2]
                app.corridors+=[corridor3]
                app.bounds+=[corridor3]

        else:
            # Horizontal cut, just vertical cut but 90 degrees to the side
            y0=p1.getY()
            cut=p2.getY()
            y2=p2.getY()+p2.getHeight()
            x0=p1.getX()
            x1=p1.getX()+p1.getWidth()
            counter=0
            success=False
            room1=None
            while counter<100:
                startx=random.randint(x0,x1)
                negDist=100
                tReached=False
                while negDist<cut-y0:
                    i=isInBounds(app,startx,cut-negDist)
                    j=isInBounds(app,startx+200,cut-negDist)
                    k=isInBounds(app,startx-50,cut-negDist)
                    l=isInBounds(app,startx+200+50,cut-negDist)
                    if(i!=None and j!=None and i==k and j==l):
                        room1=[app.bounds[i]]
                        if(i!=j):
                            room1+=[app.bounds[j]]
                        tReached=True
                        break
                    elif(i==None and j==None and k==None and l==None):
                        negDist+=100
                    else:
                        break
                if(tReached):
                    posDist=100
                    bReached=False
                    while posDist<y2-cut:
                        i=isInBounds(app,startx,cut+posDist)
                        j=isInBounds(app,startx+200,cut+posDist)
                        k=isInBounds(app,startx-50,cut+posDist)
                        l=isInBounds(app,startx+200+50,cut+posDist)
                        if(i!=None and j!=None and i==k and j==l):
                            c=Corridor(startx,cut-negDist,200,posDist+negDist)
                            app.corridors+=[c]
                            app.bounds+=[c]
                            for r in room1:
                                r.setCorridors(r.getCorridors()+[c])
                                c.setCorridors(c.getCorridors()+[r])
                            app.bounds[i].setCorridors(app.bounds[i].getCorridors()+[c])
                            c.setCorridors(c.getCorridors()+[app.bounds[i]])
                            if(i!=j):
                                app.bounds[j].setCorridors(app.bounds[j].getCorridors()+[c])
                                c.setCorridors(c.getCorridors()+[app.bounds[j]])
                            bReached=True
                            break
                        elif(i==None and j==None and k==None and l==None):
                            posDist+=100
                        else:
                            break
                if(tReached and bReached):
                    success=True
                    break
                counter+=1
            if(not success):
                c1=(0,0)
                c2=(0,0)
                room1=None
                room2=None
                while 1:
                    startx=random.randint(x0,x1)
                    negDist=100
                    tReached=False
                    while negDist<cut-y0:
                        i=isInBounds(app,startx,cut-negDist)
                        j=isInBounds(app,startx+200,cut-negDist)
                        k=isInBounds(app,startx-50,cut-negDist)
                        l=isInBounds(app,startx+200+50,cut-negDist)
                        if(i!=None and j!=None and i==k and j==l):
                            room1=[app.bounds[i]]
                            if(i!=j):
                                room1+=[app.bounds[j]]
                            tReached=True
                            break
                        elif(i==None and j==None and k==None and l==None):
                            negDist+=100
                        else:
                            break
                    if(tReached):
                        c1=(startx,cut-negDist)
                        break
                while 1:
                    startx=random.randint(x0,x1)
                    posDist=100
                    bReached=False
                    while posDist<y2-cut:
                        i=isInBounds(app,startx,cut+posDist)
                        j=isInBounds(app,startx+200,cut+posDist)
                        k=isInBounds(app,startx-50,cut+posDist)
                        l=isInBounds(app,startx+200+50,cut+posDist)
                        if(i!=None and j!=None and i==k and j==l):
                            room2=[app.bounds[i]]
                            if(i!=j):
                                room2+=[app.bounds[j]]
                            bReached=True
                            break
                        elif(i==None and j==None and k==None and l==None):
                            posDist+=100
                        else:
                            break
                    if(bReached):
                        c2=(startx,cut+posDist)
                        break
                x0,y0=c1
                x1,y1=c2
                corridor1=Corridor(x0,y0,200,(y1-y0)//2-100)
                if(x0<x1):
                    corridor2=Corridor(x0,(y1+y0)//2-100,x1-x0+200,200)
                else:
                    corridor2=Corridor(x1,(y1+y0)//2-100,x0-x1+200,200)
                corridor3=Corridor(x1,(y1+y0)//2+100,200,(y1-y0)//2-100)
                corridor1.setCorridors(corridor1.getCorridors()+[corridor2])
                corridor1.setCorridors(corridor1.getCorridors()+[corridor3])
                corridor2.setCorridors(corridor2.getCorridors()+[corridor1])
                corridor2.setCorridors(corridor2.getCorridors()+[corridor3])
                corridor3.setCorridors(corridor3.getCorridors()+[corridor1])
                corridor3.setCorridors(corridor3.getCorridors()+[corridor2])
                for r in room1:
                    r.setCorridors(r.getCorridors()+[corridor1,corridor2,corridor3])
                    corridor1.setCorridors(corridor1.getCorridors()+[r])
                    corridor2.setCorridors(corridor2.getCorridors()+[r])
                    corridor3.setCorridors(corridor3.getCorridors()+[r])
                for r in room2:
                    r.setCorridors(r.getCorridors()+[corridor1,corridor2,corridor3])
                    corridor1.setCorridors(corridor1.getCorridors()+[r])
                    corridor2.setCorridors(corridor2.getCorridors()+[r])
                    corridor3.setCorridors(corridor3.getCorridors()+[r])
                app.corridors+=[corridor1]
                app.bounds+=[corridor1]
                app.corridors+=[corridor2]
                app.bounds+=[corridor2]
                app.corridors+=[corridor3]
                app.bounds+=[corridor3]
    return
    
def createSpikes(app,r):
    # Pick random number of spikes to generate in the room, pick place to start generating spikes, something like x coord between x0+20 and x1-40, same with y
    # Then, get x and y distance between that spike coord and every other already generated spike coord if both are positive, add it to a list or smthing
    # Then get the smallest x diff and smallest y diff from the lists and that//20 is the range where it can be generated. Maybe add a slight skew towards smaller numbers
    x0=r.getX()
    x1=x0+r.getWidth()
    y0=r.getY()
    y1=y0+r.getHeight()
    numSpikes=random.randint(0,1)+random.randint(0,1)
    for i in range(numSpikes):
        while 1:
            randx=random.randint(x0+40,x1-80)
            randy=random.randint(y0+40,y1-80)
            out=False
            xdists=[]
            ydists=[]
            for spike in r.getSpikes():
                x,y,width,height=spike
                if((randx<x and x-randx<60)or(randx>x and randx<x+width)or(randy<y and y-randy<60)or(randy>y and randy<y+height)):
                    out=True
                    break
                else:
                    if(randx<x and randy<y):
                        xdists+=[x-randx]
                        ydists+=[y-randy]
            if(out):
                continue
            maxCols=(x1-40-randx)//20
            if(len(xdists)!=0):
                maxCols=sorted(xdists)[0]//20-1
            """if(maxCols>10):
                maxCols=10"""
            maxRows=(y1-40-randy)//20
            if(len(ydists)!=0):
                maxRows=sorted(ydists)[0]//20-1
            """if(maxRows>10):
                maxRows=10"""
            cols=random.randint(2,maxCols)
            rows=random.randint(2,maxRows)
            r.setSpikes(r.getSpikes()+[(randx,randy,cols*20,rows*20)])
            break

def createMonsters(app,r):
    # Creates monsters at random inside the room but outside of any spike fields.
    x0=r.getX()
    x1=x0+r.getWidth()
    y0=r.getY()
    y1=y0+r.getHeight()
    numMonsters=random.randint(1,6)+random.randint(1,6)
    for i in range(numMonsters):
        while 1:
            randx=random.randint(x0+30,x1-30)
            randy=random.randint(y0+30,y1-30)
            failed=False
            for spike in r.getSpikes():
                x,y,w,h=spike
                if(randx+30>=x and randx-30<=x+w and randy+30>=y and randy-30<=y+h):
                    failed=True
            if(failed):
                continue
            if(random.randint(0,1)==0):
                r.addMonster(R1(randx,randy))
            else:
                r.addMonster(Melee(randx,randy))
            break


def roomGen(app):
    for r in app.bounds:
        if(isinstance(r,Room)):
            createSpikes(app,r)
            createPartitions(app,r)
            createMonsters(app,r)

def getDistance(x0,y0,x1,y1):
    # Returns the distance between the two points x0,y0 and x1,y1
    return ((x1-x0)**2+(y1-y0)**2)**0.5

def findPartition(x,y,r):
    # Returns which partition of the room the player is in (Used for a*)
    for partition in r.getPartitions():
        x0,y0,x1,y1=partition
        if(x>=x0 and x<=x1 and y>=y0 and y<=y1):
            return partition

def aStar(app,x,y,tx,ty):
    # https://en.wikipedia.org/wiki/A*_search_algorithm pseudocode referenced
    # Pathfinding algorithm
    points=findPoints(app,x,y)
    tpoints=findPoints(app,tx,ty)
    if(points==None or tpoints==None):
        return []
    pointToBegin=None
    shortest=100000
    for point in points:
        if(point not in app.currentRoom.getPoints()):
            continue
        px,py=point
        d=getDistance(px,py,tx,ty)
        if(d<shortest):
            shortest=d
            pointToBegin=(px,py)
    edge=Heap()
    edge.add((pointToBegin,getDistance(x,y,px,py)))
    cameFrom={}
    cameFrom[pointToBegin]=(x,y)
    scoreMap={}
    scoreMap[pointToBegin]=shortest
    while len(edge.getHeap())!=0:
        point,score=edge.remove()
        x,y=point
        if point in tpoints:
            path=makePath(point,cameFrom)+[(tx,ty)]
            smoothPath(app,path,app.currentRoom)
            app.path=path
            return path
        for neighbor in app.currentRoom.getPoints()[point]:
            nx,ny=neighbor
            temp=scoreMap[point]+app.currentRoom.getPoints()[point][neighbor]
            if(temp<scoreMap.get(neighbor,100000)):
                cameFrom[neighbor]=point
                scoreMap[neighbor]=temp
                edge.add((neighbor,scoreMap[point]+getDistance(nx,ny,tx,ty)))

def smoothPath(app,path,r):
    # Given a path, if any two points two apart have vision of each other, delete the point between them
    i=0
    while(i<len(path)-2):
        if(hasVision(path[i],path[i+2],r)):
            path.pop(i+1)
        else:
            i+=1
    return path

def makePath(point,cameFrom):
    # Creates a path by retracing steps in cameFrom
    path=[point]
    while(point in cameFrom):
        point=cameFrom[point]
        path=[point]+path
    return path

def findPoints(app,x,y):
    # Finds the points surrounding the partition x,y is in
    temp=findPartition(x,y,app.currentRoom)
    if(temp==None):
        return None
    x0,y0,x1,y1=temp
    points=set()
    points.add((x0,(y0+y1)/2))
    points.add(((x0+x1)/2,y0))
    points.add((x1,(y0+y1)/2))
    points.add(((x0+x1)/2,y1))
    return points

def createPartitions(app,r):
    # Partitions the room into the navigation mesh, avoiding spikes, and creates
    # points at the center of each edge that doesn't border spikes in every partition
    # http://theory.stanford.edu/~amitp/GameProgramming/MapRepresentations.html 
    xSlices=[r.getX(),r.getX()+r.getWidth()]
    ySlices=[r.getY(),r.getY()+r.getHeight()]
    for spike in r.getSpikes():
        x,y,width,height=spike
        xSlices+=[x,x+width]
        ySlices+=[y,y+height]
    xSlices.sort()
    ySlices.sort()
    for i in range(len(xSlices)-1):
        for j in range(len(ySlices)-1):
            x0=xSlices[i]
            y0=ySlices[j]
            x1=xSlices[i+1]
            y1=ySlices[j+1]
            failure=False
            left=True
            right=True
            top=True
            bottom=True
            for spike in r.getSpikes():
                x,y,width,height=spike
                if (x0>=x and x0<x+width and y0>=y and y0<y+height):
                    failure=True
                    break
                if(x0==x+width and y0>=y and y0<y+height):
                    left=False
                if(y0==y+height and x0>=x and x0<x+width):
                    top=False
                if(x1==x and y0>=y and y0<y+height):
                    right=False
                if(y1==y and x0>=x and x0<x+width):
                    bottom=False
            if(failure):
                continue
            r.addPartition((x0,y0,x1,y1))
            points=set()
            if(left):
                r.createPoint((x0,(y0+y1)/2))
                points.add((x0,(y0+y1)/2))
            if(top):
                r.createPoint(((x0+x1)/2,y0))
                points.add(((x0+x1)/2,y0))
            if(right):
                r.createPoint((x1,(y0+y1)/2))
                points.add((x1,(y0+y1)/2))
            if(bottom):
                r.createPoint(((x0+x1)/2,y1))
                points.add(((x0+x1)/2,y1))
            for p1 in points:
                for p2 in points:
                    if(p1!=p2):
                        x0,y0=p1
                        x1,y1=p2
                        d=getDistance(x0,y0,x1,y1)
                        r.addConnection(p1,p2,d)

def hasVision(p1,p2,r):
    # Each spike(rectangle) consists of four line segment edges, 
    # if a line segment drawn from p1 to p2 intersects any of these edges,
    # it intersects the spike, blocking "Vision". Vision here is not true
    # vision, it is just used so ranged monsters are incentivized to move
    # and for the purpose of path smoothing
    if(p1==p2):
        return True
    vision=True
    x0,y0=p1
    x1,y1=p2
    if(x1==x0):
        for spike in r.getSpikes():
            x,y,w,h=spike
            if(x0>=x and x0<=x+w):
                vision=False
                break
    elif(y1==y0):
        for spike in r.getSpikes():
            x,y,w,h=spike
            if(y0>=y and y0<=y+h):
                vision=False
                break
    else:
        slope=(y1-y0)/(x1-x0)
        #point slope form is y=y0+slope*(x-x0) and x=(y-y0)/slope+x0
        for spike in r.getSpikes():
            x,y,w,h=spike
            if((y0+slope*(x-x0)>=y and y0+slope*(x-x0)<=y+h and isBetween(x,x0,x1)) or (y0+slope*(x+w-x0)>=y and y0+slope*(x+w-x0)<=y+h and isBetween(x,x0,x1)) 
            or ((y-y0)/slope+x0>=x and (y-y0)/slope+x0<=x+w and isBetween(y,y0,y1)) or ((y+h-y0)/slope+x0>=x and (y+h-y0)/slope+x0<=x+w and isBetween(y,y0,y1))):
                vision=False
                break
    return vision

def isBetween(n,n0,n1):
    # If n is between n0 and n1, return True, otherwise return False
    if(n0>=n and n>=n1) or (n1>=n and n>=n0):
        return True
    return False

def drawPartition(app,canvas,p):
    x0=p.getX()
    x1=x0+p.getWidth()
    y0=p.getY()
    y1=y0+p.getHeight()
    canvas.create_rectangle(x0//10,y0//10,x1//10,y1//10,outline="Black")
    if(p.getC1()!=None):
        drawPartition(app,canvas,p.getC1())
    if(p.getC2()!=None):
        drawPartition(app,canvas,p.getC2())

def drawCorridors(app,canvas):
    for corridor in app.corridors:
        x0=corridor.getX()
        x1=x0+corridor.getWidth()
        y0=corridor.getY()
        y1=y0+corridor.getHeight()
        canvas.create_rectangle(x0/10,y0/10,x1/10,y1/10,fill="Black")

def drawRoom(app,canvas,p,depth):
    # Draws the layout of the dungeon
    r=p.getRoom()
    if(r==None):
        drawRoom(app,canvas,p.getC1(),depth+1)
        drawRoom(app,canvas,p.getC2(),depth+1)
    else:
        colors=["Red", "Orange", "Yellow", "lightGreen", "Green", "Teal", "Blue", "mediumPurple1"]
        color="Black"
        if(depth<8):
            color=colors[depth]
        x0=r.getX()
        x1=x0+r.getWidth()
        y0=r.getY()
        y1=y0+r.getHeight()
        canvas.create_rectangle(x0/10,y0/10,x1/10,y1/10,fill=color)

def startingPos(app):
    # Creates random starting position until the position is in a room
    while 1:
        randx=random.randint(0,10000)
        randy=random.randint(0,10000)
        i=isInBounds(app,randx,randy)
        if(i!=None and isinstance(app.bounds[i],Room)):
            failed=False
            for spike in app.bounds[i].getSpikes():
                x,y,w,h=spike
                if not(randx+5<=x and randx-5>=x+w and randy+5<=y and randy-5>=y+h):
                    failed=True
                    break
            if(failed):
                continue
            return randx,randy,i

def drawFound(app,canvas):
    # Draws rooms that have been found by the player
    c=copy.deepcopy(app.found)
    i=0
    while i < (len(c)):
        if(isinstance(c[i],Corridor)):
            x0=c[i].getX()
            x1=x0+c[i].getWidth()
            y0=c[i].getY()
            y1=y0+c[i].getHeight()
            canvas.create_rectangle(x0/10,y0/10,x1/10,y1/10,fill="Gray",outline="Gray")
            c.pop(i)
        else:
            i+=1
    for f in c:
        x0=f.getX()
        x1=x0+f.getWidth()
        y0=f.getY()
        y1=y0+f.getHeight()
        canvas.create_rectangle(x0/10,y0/10,x1/10,y1/10,fill="Gray",outline="Gray")

def dash(app):
    # Changes xv and yv to vector, adds 30 to the vector, changes it back
    if(app.ticks-app.lastDashed<30):
        return False
    xv=app.player.getXV()
    yv=app.player.getYV()
    v=(xv**2+yv**2)**0.5
    if(v<2):
        return False
    if(xv==0):
        xv=0.0000001
    angle=math.atan(yv/xv)
    if(xv<0):
        angle=(angle+math.pi)%(2*math.pi)
    nx,ny=polarToCartesian(angle,v+30)
    app.player.setXV(nx)
    app.player.setYV(ny)
    app.lastDashed=app.ticks
    return True

def deepcopy(app):
    # Idea and name from Amalia :>
    # Calling setX and setY on player also changes fx and fy if the player's
    # deepcopy timer (dcTimer) is greater than 60, meaning for 60 ticks 
    # (dcTimer<60) after deepcopy is used, fx and fy don't get updated.
    if(app.player.getDCTimer()<180):
        return False
    app.player.setDCTimer(0)
    return True

def shockwave(app):
    # Idea from spacetime by littlegreenland on scratch lol
    # https://scratch.mit.edu/projects/22573757/
    if(app.ticks-app.lastShockwaved<120):
        return False
    r=app.currentRoom
    if(isinstance(r,Corridor)):
        return False
    for projectile in r.getProjectiles():
        if(getDistance(app.player.getX(),app.player.getY(),projectile.getX(),projectile.getY())<250):
            pAngle=projectile.getAngle()
            pSpeed=projectile.getSpeed()
            pVector=angledMove(0,0,pAngle,pSpeed)
            sAngle=angleBetween(app.player.getX(),app.player.getY(),projectile.getX(),projectile.getY())
            sVector=angledMove(0,0,sAngle,40)
            px,py=pVector
            sx,sy=sVector
            nAngle=angleBetween(0,0,px+sx,py+sy)
            nSpeed=getDistance(0,0,px+sx,py+sy)
            projectile.setAngle(nAngle)
            projectile.setSpeed(nSpeed)
            if(isinstance(projectile,bouncyProjectile)):
                projectile.setBounces(0)
    for monster in r.getMonsters():
        if(getDistance(app.player.getX(),app.player.getY(),monster.getX(),monster.getY())<250):
            sAngle=angleBetween(app.player.getX(),app.player.getY(),monster.getX(),monster.getY())
            if(isinstance(monster,Boss)):
                sx,sy=angledMove(0,0,sAngle,10)
            else:
                sx,sy=angledMove(0,0,sAngle,20)
            monster.setXV(sx)
            monster.setYV(sy)
    app.lastShockwaved=app.ticks
    return True

def polarToCartesian(angle,dist):
    return dist*math.cos(angle),dist*math.sin(angle)

def kill(app):
    xv=app.player.getXV()
    yv=app.player.getYV()
    v2=(xv**2+yv**2)
    if(v2>=625 or app.amalia or app.ticks<30):
        return
    else:
        app.currentMode="Dead"

def timerFired(app):
    if(app.currentMode=="Game"):
        app.ticks+=1
        app.player.setDCTimer(app.player.getDCTimer()+1)
        """if(time.time()-app.lastTime)>1:
            app.lastTime=time.time()
            print(app.ticks-app.lastTick)
            app.lastTick=app.ticks"""
        if app.moveRight:
            app.player.setXV(app.player.getXV()+3)
        if app.moveLeft:
            app.player.setXV(app.player.getXV()-3)
        if app.moveUp:
            app.player.setYV(app.player.getYV()-3)
        if app.moveDown:
            app.player.setYV(app.player.getYV()+3)
        coords=isInRoom(app.player.getX()+app.player.getXV(),app.player.getY(),app.currentRoom,5)
        if(coords!=-1):
            isInCorridor=False
            newRoom=None
            if((isinstance(app.currentRoom,Room) and app.currentRoom.getCompleted()) or isinstance(app.currentRoom,Corridor)):
                for c in app.currentRoom.getCorridors():
                    if(isInRoom(app.player.getX()+app.player.getXV(),app.player.getY(),c,5)==-1):
                        isInCorridor=True
                        newRoom=c
                if(isInCorridor):
                    app.player.setX(app.player.getX()+app.player.getXV())
                    app.currentRoom=newRoom
                    if(newRoom not in app.found):
                        app.found+=[newRoom]
                    for c in newRoom.getCorridors():
                        if(c not in app.found):
                            app.found+=[c]
                else:
                    app.player.setX(coords)
            else:
                app.player.setX(coords)
        else:
            app.player.setX(app.player.getX()+app.player.getXV())
        coords=isInRoom(app.player.getX(),app.player.getY()+app.player.getYV(),app.currentRoom,5)
        if(coords!=-1):
            isInCorridor=False
            newRoom=None
            if((isinstance(app.currentRoom,Room) and app.currentRoom.getCompleted()) or isinstance(app.currentRoom,Corridor)):
                for c in app.currentRoom.getCorridors():
                    if(isInRoom(app.player.getX(),app.player.getY()+app.player.getYV(),c,5)==-1):
                        isInCorridor=True
                        newRoom=c
                if(isInCorridor):
                    app.player.setY(app.player.getY()+app.player.getYV())
                    app.currentRoom=newRoom
                    if(newRoom not in app.found):
                        app.found+=[newRoom]
                    for c in newRoom.getCorridors():
                        if(c not in app.found):
                            app.found+=[c]
                else:
                    app.player.setY(coords)
            else:
                app.player.setY(coords)
        else:
            app.player.setY(app.player.getY()+app.player.getYV())
        if(isinstance(app.currentRoom,Room)):
            x0,y0,x1,y1=app.currentPartition
            x,y=app.player.getX(),app.player.getY()
            if(x<x0 or x>x1 or y<y0 or y>y1):
                p=(findPartition(x,y,app.currentRoom))
                if(p!=None):
                    app.currentPartition=p
                    aStarMonsters(app,app.currentRoom)
            moveMonsters(app,app.currentRoom)
            moveProjectiles(app,app.currentRoom)
        app.player.update()

def boss(app):
    app.player.setX(21000)
    app.player.setY(21500)
    app.currentRoom=app.bounds[0]
    app.boss=True

def moveProjectiles(app,r):
    projectilesToDelete=set()
    for projectile in r.getProjectiles():
        monstersToDelete=set()
        for monster in r.getMonsters():
            temp=getDistance(monster.getX(),monster.getY(),projectile.getX(),projectile.getY())
            if(temp<=35):
                monster.setHp(monster.getHp()-40)
                projectilesToDelete.add(projectile)
                if(monster.getHp()<=0):
                    monstersToDelete.add(monster)
                break
        for monster in monstersToDelete:
            r.removeMonster(monster)
            if(isinstance(monster,Boss)):
                app.currentMode="Win"
            if(len(r.getMonsters())==0):
                if(not r.getCompleted()):
                    app.incompleteRooms-=1
                r.setCompleted(True)
                if(app.incompleteRooms==0):
                    boss(app)
        x,y,angle,speed=projectile.getX(),projectile.getY(),projectile.getAngle(),projectile.getSpeed()
        prevx,prevy=x,y
        i=0
        while(i<speed):
            x,y=angledMove(x,y,angle,10)
            if((app.player.getX()-x)**2+(app.player.getY()-y)**2<100):
                kill(app)
            i+=10
        dx,dy=angledMove(0,0,angle,speed)
        if(x<r.getX() or x>r.getX()+r.getWidth() or y<r.getY() or y>r.getY()+r.getHeight()):
            if(isinstance(projectile,bouncyProjectile)):
                if(projectile.getBounces()!=0):
                    if(x<r.getX()):
                        xTra=x-r.getX()
                        yTra=dy*xTra/dx
                        x=(r.getX())
                        y=(y-yTra)
                        projectile.setAngle((math.pi-projectile.getAngle())%(math.pi*2))
                    if(x>r.getX()+r.getWidth()):
                        xTra=x-r.getX()-r.getWidth()
                        yTra=dy*xTra/dx
                        x=(r.getX()+r.getWidth())
                        y=(y-yTra)
                        projectile.setAngle((math.pi-projectile.getAngle())%(math.pi*2))
                    if(y<r.getY()):
                        yTra=y-r.getY()
                        xTra=dx*yTra/dy
                        x=(x-xTra)
                        y=(r.getY())
                        projectile.setAngle((0-projectile.getAngle())%(math.pi*2))
                    if(y>r.getY()+r.getHeight()):
                        yTra=y-r.getY()-r.getHeight()
                        xTra=dx*yTra/dy
                        x=(x-xTra)
                        y=(r.getY()+r.getHeight())
                        projectile.setAngle((0-projectile.getAngle())%(math.pi*2))
                    projectile.setBounces(projectile.getBounces()-1)
                    x,y=angledMove(x,y,projectile.getAngle(),speed)
                    projectile.setX(x)
                    projectile.setY(y)
                else:
                    projectilesToDelete.add(projectile)
            else:
                projectilesToDelete.add(projectile)
        else:
            projectile.setX(x)
            projectile.setY(y)
    for projectile in projectilesToDelete:
        r.removeProjectile(projectile)


def moveMonsters(app,r):
    removed=set()
    for monster in r.getMonsters():
        x,y=monster.getX()+monster.getXV(),monster.getY()+monster.getYV()
        if(isInRoom(x,y,r,30)==-1):
            monster.setX(x)
            monster.setY(y)
        monster.update()
        x,y=monster.getX(),monster.getY()
        ms=10
        path=monster.getPath()
        m=(x,y)
        player=(app.player.getFX(),app.player.getFY())
        if(monster.getXV()>0.5 or monster.getYV()>0.5):
            for spike in r.getSpikes():
                sx,sy,sw,sh=spike
                if(x>=sx and x<=sx+sw and y>=sy and y<=sy+sh):
                    monster.setHp(monster.getHp()-20)
                    if(monster.getHp()<=0):
                        removed.add(monster)
                        continue
        if(isinstance(monster,Boss)):
            angle=monster.getAngle()
            monster.setAngle(monster.getAngle()+2*math.pi/60)
            projx,projy=angledMove(x,y,angle,58)
            r.addProjectile(bouncyProjectile(projx,projy,angle,20,1))
            angle=random.randint(0,359)/360*2*math.pi
            projx,projy=angledMove(x,y,angle,58)
            r.addProjectile(Projectile(projx,projy,angle,20))
            monster.setTimer(monster.getTimer()-1)
            if(monster.getTimer()==0):
                monster.setTimer(random.randint(45,55))
                angleToPlayer=angleBetween(x,y,app.player.getX(),app.player.getY())
                for i in range(-10,11):
                    r.addProjectile(bouncyProjectile(projx,projy,angle,20,2))
                    angle=angleToPlayer+i/360*2*math.pi
                    projx,projy=angledMove(x,y,angle,58)
        if(isinstance(monster,R1)):
            if(hasVision(m,player,r)):
                if(monster.getProjectileDelay()==0):
                    angle=angleBetween(x,y,app.player.getFX(),app.player.getFY())
                    projx,projy=angledMove(x,y,angle,37)
                    r.addProjectile(Projectile(projx,projy,angle,20))
                    monster.setProjectileDelay(random.randint(30,50))
                else:
                    monster.setProjectileDelay(monster.getProjectileDelay()-1)
                continue
        if(isinstance(monster,Melee)):
            if(monster.getStunned()>0):
                for spike in r.getSpikes():
                    sx,sy,sw,sh=spike
                    if(x>=sx and x<=sx+sw and y>=sy and y<=sy+sh):
                        monster.setHp(monster.getHp()-10)
                        if(monster.getHp()<=0):
                            removed.add(monster)
                            continue
                monster.setStunned(monster.getStunned()-1)
                continue
            if(monster.getAngle()!=None):
                dx,dy=angledMove(0,0,monster.getAngle(),40)
                if(getDistance(app.player.getX(),app.player.getY(),x,y)<40):
                    kill(app)
                x,y=x+dx,y+dy
                for otherMonster in r.getMonsters():
                    if(isinstance(otherMonster,Melee)):
                        continue
                    mx,my=otherMonster.getX(),otherMonster.getY()
                    if(getDistance(x,y,mx,my)<60):
                        removed.add(otherMonster)
                        monster.setAngle(None)
                        monster.setPath(aStar(app,x,y,app.player.getFX(),app.player.getFY()))
                        monster.setStunned(20)
                        monster.setHp(monster.getHp()-35)
                if(x<r.getX() or x>r.getX()+r.getWidth() or y<r.getY() or y>r.getY()+r.getHeight()):
                    monster.setAngle(None)
                    monster.setPath(aStar(app,x,y,app.player.getFX(),app.player.getFY()))
                    monster.setStunned(20)
                    monster.setHp(monster.getHp()-20)
                    if(monster.getHp()<=0):
                        removed.add(monster)
                        continue
                    if(x<r.getX()):
                        xTra=x-r.getX()
                        yTra=dy*xTra/dx
                        x=(r.getX())
                        y=(y-yTra)
                    if(x>r.getX()+r.getWidth()):
                        xTra=x-r.getX()-r.getWidth()
                        yTra=dy*xTra/dx
                        x=(r.getX()+r.getWidth())
                        y=(y-yTra)
                    if(y<r.getY()):
                        yTra=y-r.getY()
                        xTra=dx*yTra/dy
                        x=(x-xTra)
                        y=(r.getY())
                    if(y>r.getY()+r.getHeight()):
                        yTra=y-r.getY()-r.getHeight()
                        xTra=dx*yTra/dy
                        x=(x-xTra)
                        y=(r.getY()+r.getHeight())
                monster.setDistance(monster.getDistance()-1)
                if(monster.getDistance()==0):
                    monster.setAngle(None)
                    monster.setPath(aStar(app,x,y,app.player.getFX(),app.player.getFY()))
                    monster.setStunned(20)
                monster.setX(x)
                monster.setY(y)
                continue
            if(getDistance(x,y,app.player.getFX(),app.player.getFY())<200 and hasVision(m, player, r)):
                dist=getDistance(x,y,app.player.getFX(),app.player.getFY())*3/2//50+2
                monster.setDistance(dist)
                monster.setAngle(angleBetween(x,y,app.player.getFX(),app.player.getFY()))
                continue
        while(ms>0):
            if(len(path)==0):
                dist=getDistance(x,y,app.player.getFX(),app.player.getFY())
                if(ms>dist):
                    break
                angle=angleBetween(x,y,app.player.getFX(),app.player.getFY())
                x,y=angledMove(x,y,angle,ms)
                break
            tx,ty=path[0]
            dist=getDistance(x,y,tx,ty)
            if(ms>dist):
                ms-=dist
                x,y=tx,ty
                path.pop(0)
                monster.setPath(path)
            else:
                angle=angleBetween(x,y,tx,ty)
                x,y=angledMove(x,y,angle,ms)
                ms=0
        monster.setX(x)
        monster.setY(y)
    for toRemove in removed:
        r.removeMonster(toRemove)
    if(len(r.getMonsters())==0):
        if(not r.getCompleted()):
            app.incompleteRooms-=1
        r.setCompleted(True)
        if(app.incompleteRooms==0):
            boss(app)

def angleBetween(x0,y0,x1,y1):
    if(x1-x0)==0:
        if(y1>y0):
            return math.pi/2
        else:
            return -math.pi/2
    angle=math.atan((y1-y0)/(x1-x0))
    if(x1-x0)<0:
        angle=(angle+math.pi)%(2*math.pi)
    return angle

def angledMove(x,y,angle,dist):
    return x+math.cos(angle)*dist,y+math.sin(angle)*dist

def aStarMonsters(app,r):
    for monster in r.getMonsters():
        monster.setPath(aStar(app,monster.getX(),monster.getY(),app.player.getFX(),app.player.getFY()))

def appStarted(app):
    #app.currentMode="Room"
    #app.currentMode="Partition"
    app.currentMode="Menu"
    restart(app)
def restart(app):
    if(app.currentMode=="Dead"):
        app.currentMode="Game"
    app.boss=False
    app.amalia=False
    app.amaliaUsed=False
    app.incompleteRooms=0
    app.ticks=0
    app.lastTick=0
    app.lastTime=0
    app.p=Partition(0,0,10000,10000)
    bossRoom=Room(20000,20000,2000,2000)
    bossRoom.addMonster(Boss(21000,21000))
    app.bounds=[]
    createChildren(app.p,0)
    createRooms(app,app.p)
    app.corridors=[]
    createCorridors(app,app.p)
    roomGen(app)
    app.player=Player()
    app.currentPartition=(0,0,0,0)
    x,y,i=startingPos(app)
    app.player.setX(x)
    app.player.setY(y)
    app.timerDelay=1000//60
    app.found=[]
    app.currentRoom=app.bounds[i]
    app.found+=[app.currentRoom]
    for c in app.currentRoom.getCorridors():
        app.found+=[c]
    app.moveLeft=False
    app.moveRight=False
    app.moveUp=False
    app.moveDown=False
    app.lastDashed=-30
    app.lastShockwaved=-120
    app.path=[]
    app.bounds=[bossRoom]+app.bounds

def isInRoom(x,y,r,s):
    if(x-s<r.getX()):
        return r.getX()+s
    elif(x+s>r.getX()+r.getWidth()):
        return r.getX()+r.getWidth()-s
    elif(y-s<r.getY()):
        return r.getY()+s
    elif(y+s>r.getY()+r.getHeight()):
        return r.getY()+r.getHeight()-s
    else:
        return -1

def isInBounds(app,x,y):
    for i in range(len(app.bounds)):
        r=app.bounds[i]
        if(r.getX()<=x and x<=r.getX()+r.getWidth() and r.getY()<=y and y<=r.getY()+r.getHeight()):
            return i

def drawPlayer(app,canvas):
    xv=app.player.getXV()
    yv=app.player.getYV()
    v2=(xv**2+yv**2)
    if(app.amalia):
        color="mediumPurple1"
    else:
        color="#A94064"
    if(v2>=625):
        color="Red"
    canvas.create_oval(app.width//2-5,app.height//2-5,app.width//2+5,app.height//2+5,fill=color)
    if(app.player.getX()!=app.player.getFX() and app.player.getY()!=app.player.getFY()):
        x,y=getCanvasCoords(app,app.player.getFX(),app.player.getFY())
        canvas.create_oval(x-5,y-5,x+5,y+5,fill="lightGreen")

def drawMenu(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="#A94064",outline="")
    canvas.create_rectangle(app.width//6,5*app.height//20,5*app.width//6,9*app.height//20)
    canvas.create_text(app.width//2,7*app.height//20,text="P  L  A  Y", font = "Gothic 60")
    canvas.create_text(app.width//2,3*app.height//20,text="LEVEL 1", font = "Gothic 110")
    canvas.create_text(app.width//2,10*app.height//20,text="""Objective: Beat the dungeon and kill the boss
    Keybinds: WASD to move your character
    Spacebar to dash: gives a short burst of invincibility
    O to shockwave: reflects projectiles and pushes enemies
    P to deepcopy: place down a copy of yourself and go invisible
    M to open up a map that shows what you've explored so far
    R to restart
    Good luck! You'll need it.
    """,font = "Gothic 20", anchor="n", justify="center")
    
def drawDead(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="#A94064",outline="")
    canvas.create_text(app.width//2,app.height//2,text="Y O U  D I E D", font = "Mincho 100")
    canvas.create_text(app.width//2,6*app.height//10+10,text="Press R to restart", font = "Gothic 50")
    canvas.create_text(app.width//2,7*app.height//10,
    text="Hint: Having trouble? Turn on Amalia mode by clicking   ~\nand deeply contemplate why you aren't good enough to beat this game yourself."
    , font = "Mincho 15",justify="center")

def drawWin(app,canvas):
    if(app.amaliaUsed):
        canvas.create_text(app.width//2,app.height//2,text="C H E A T E R", font = "Mincho 100")
    else:
        canvas.create_text(app.width//2,app.height//2,text="Y O U  W I N", font = "Mincho 100")

def drawBossHp(app,canvas):
    for monster in app.currentRoom.getMonsters():
        percent=monster.getHp()/3000
        hp=monster.getHp()
    canvas.create_rectangle(app.width/6,50,5*app.width/6,100,fill="White",outline="Black")
    canvas.create_rectangle(app.width/6,50,app.width/6+2/3*app.width*percent,100,fill="Red",outline="")
    canvas.create_rectangle(app.width/6,50,5*app.width/6,100,fill="",outline="Black")
    canvas.create_text(app.width/2,75,text=f"Boss Hp: {hp}/3000",font="Mincho 20")

def redrawAll(app,canvas):
    if(app.currentMode=="Win"):
        drawWin(app,canvas)
    if(app.currentMode=="Dead"):
        drawDead(app,canvas)
    if(app.currentMode=="Menu"):
        drawMenu(app,canvas)
    if(app.currentMode=="Room"):
        drawCorridors(app,canvas)
        drawRoom(app,canvas,app.p,0)
    if(app.currentMode=="Map"):
        canvas.create_rectangle(0,0,app.width,app.height,fill="Black")
        drawFound(app,canvas)
    if(app.currentMode=="Partition"):
        drawCorridors(app,canvas)
        drawRoom(app,canvas,app.p,0)
        drawPartition(app,canvas,app.p)
    if(app.currentMode=="Game"):
        canvas.create_rectangle(0,0,app.width,app.height,fill="Black")
        drawRooms(app,canvas)
        drawPlayer(app,canvas)
        drawUI(app,canvas)
        if(app.boss):
            drawBossHp(app,canvas)
    #drawPath(app,canvas)

def drawPath(app,canvas):
    for i in range(len(app.path)-1):
        x0,y0=app.path[i]
        x1,y1=app.path[i+1]
        x0,y0=getCanvasCoords(app,x0,y0)
        x1,y1=getCanvasCoords(app,x1,y1)
        canvas.create_line(x0,y0,x1,y1,width=3,fill="Green")

def drawUI(app,canvas):
    drawDCCD(app,canvas)
    drawShockwaveCD(app,canvas)
    drawDashCD(app,canvas)
    drawMinimap(app,canvas)
    drawShockwave(app,canvas)

def drawDCCD(app,canvas):
    canvas.create_rectangle(app.width-255,app.height-105,app.width-195,app.height-45,fill="#778899")
    canvas.create_oval(app.width-250,app.height-100,app.width-200,app.height-50,fill="lightGreen")
    canvas.create_text(app.width-225,app.height-75,text=" DEEP\nCOPY")
    cooldown=(app.player.getDCTimer())/180
    if(cooldown>=1):
        canvas.create_oval(app.width-250,app.height-100,app.width-200,app.height-50,fill="")
        return
    cooldown=1-cooldown
    canvas.create_arc(app.width-251,app.height-101,app.width-199,app.height-49,start=90,extent=cooldown*360,fill="#778899",outline="#778899")

def drawShockwave(app,canvas):
    timeSince=app.ticks-app.lastShockwaved
    if(timeSince)<5:
        canvas.create_oval(app.width//2-timeSince*50,app.height//2-timeSince*50,app.width//2+timeSince*50,app.height//2+timeSince*50,outline="Cyan",width=10)

def drawShockwaveCD(app,canvas):
    canvas.create_rectangle(app.width-180,app.height-105,app.width-120,app.height-45,fill="#778899")
    canvas.create_oval(app.width-175,app.height-100,app.width-125,app.height-50,fill="Cyan")
    canvas.create_text(app.width-150,app.height-75,text="SHOCK\n WAVE")
    cooldown=(app.ticks-app.lastShockwaved)/120
    if(cooldown>=1):
        canvas.create_oval(app.width-175,app.height-100,app.width-125,app.height-50,fill="")
        return
    cooldown=1-cooldown
    canvas.create_arc(app.width-176,app.height-101,app.width-124,app.height-49,start=90,extent=cooldown*360,fill="#778899",outline="#778899")

def drawDashCD(app,canvas):
    canvas.create_rectangle(app.width-105,app.height-105,app.width-45,app.height-45,fill="#778899")
    canvas.create_oval(app.width-100,app.height-100,app.width-50,app.height-50,fill="Red")
    canvas.create_text(app.width-75,app.height-75,text="DASH")
    cooldown=(app.ticks-app.lastDashed)/30
    if(cooldown>=1):
        canvas.create_oval(app.width-100,app.height-100,app.width-50,app.height-50,fill="")
        return
    cooldown=1-cooldown
    canvas.create_arc(app.width-101,app.height-101,app.width-49,app.height-49,start=90,extent=cooldown*360,fill="#778899",outline="#778899")

def drawMinimap(app,canvas):
    canvas.create_rectangle(app.width-app.width//10-app.width//20,app.height//10-app.height//20,app.width-app.width//10+app.width//20,app.height//10+app.height//20,fill="#778899",outline="White")
    c=copy.deepcopy(app.found)
    i=0
    r=app.currentRoom
    if(isinstance(r,Corridor)):
        x0,y0=getCanvasCoords(app,r.getX(),r.getY())
        x1=x0+r.getWidth()
        y1=y0+r.getHeight()
        drawTrimmedMinimap(app,canvas,x0,y0,x1,y1)
    while i < (len(c)):
        if(isinstance(c[i],Corridor) and cornerOnCanvas(app,c[i].getX(),c[i].getY(),c[i].getWidth(),c[i].getHeight(),True)):
            x0,y0=getCanvasCoords(app,c[i].getX(),c[i].getY())
            x1=x0+c[i].getWidth()
            y1=y0+c[i].getHeight()
            drawTrimmedMinimap(app,canvas,x0,y0,x1,y1)
            c.pop(i)
        elif(not((isinstance(c[i],Room) and cornerOnCanvas(app,c[i].getX(),c[i].getY(),c[i].getWidth(),c[i].getHeight(),True)))):
            c.pop(i)
        else:
            i+=1
    for f in c:
        x0,y0=getCanvasCoords(app,f.getX(),f.getY())
        x1=x0+f.getWidth()
        y1=y0+f.getHeight()
        drawTrimmedMinimap(app,canvas,x0,y0,x1,y1)
    if(isinstance(r,Room)):
        x0,y0=getCanvasCoords(app,r.getX(),r.getY())
        x1=x0+r.getWidth()
        y1=y0+r.getHeight()
        drawTrimmedMinimap(app,canvas,x0,y0,x1,y1)
    canvas.create_rectangle(app.width-app.width//10-app.width//20,app.height//10-app.height//20,app.width-app.width//10+app.width//20,app.height//10+app.height//20,outline="White")

def drawTrimmedMinimap(app,canvas,x0,y0,x1,y1):
    if(x1<app.width/-2 or x0>app.width*3/2 or y1<app.height/-2 or y0>app.height*3/2):
        return
    if(x0<app.width/-2):
        x0=app.width/-2
    if(y0<app.height/-2):
        y0=app.height/-2
    if(x1>app.width*3/2):
        x1=app.width*3/2
    if(y1>app.height*3/2):
        y1=app.height*3/2
    canvas.create_rectangle(app.width-app.width//10-app.width//20+app.width//40+x0//20,app.height//10-app.height//20+app.height//40+y0//20,app.width-app.width//10-app.width//20+app.width//40+x1//20,app.height//10-app.height//20+app.height//40+y1//20,fill="Gray",outline="Gray")

def drawRooms(app,canvas):
    currentRooms=[app.currentRoom]+app.currentRoom.getCorridors()
    c=copy.deepcopy(app.found)
    i=0
    while i < (len(c)):
        if(isinstance(c[i],Corridor) and cornerOnCanvas(app,c[i].getX(),c[i].getY(),c[i].getWidth(),c[i].getHeight(),False)):
            x0,y0=getCanvasCoords(app,c[i].getX(),c[i].getY())
            x1=x0+c[i].getWidth()
            y1=y0+c[i].getHeight()
            canvas.create_rectangle(x0,y0,x1,y1,fill="Gray",outline="Gray")
            c.pop(i)
        elif(not((isinstance(c[i],Room) and cornerOnCanvas(app,c[i].getX(),c[i].getY(),c[i].getWidth(),c[i].getHeight(),False)))):
            c.pop(i)
        else:
            i+=1
    i=0
    while i<len(currentRooms):
        if(isinstance(currentRooms[i],Corridor)):
            x0,y0=getCanvasCoords(app,currentRooms[i].getX(),currentRooms[i].getY())
            x1=x0+currentRooms[i].getWidth()
            y1=y0+currentRooms[i].getHeight()
            canvas.create_rectangle(x0,y0,x1,y1,fill="Gray",outline="Gray")
            currentRooms.pop(i)
        else:
            i+=1
    c+=currentRooms
    for f in c:
        x0,y0=getCanvasCoords(app,f.getX(),f.getY())
        x1=x0+f.getWidth()
        y1=y0+f.getHeight()
        canvas.create_rectangle(x0,y0,x1,y1,fill="Gray",outline="Gray")
        drawSpikes(app,canvas,f)
        #drawPoints(app,canvas,f)
        drawMonsters(app,canvas,f)
        drawProjectiles(app,canvas,f)

def drawProjectiles(app,canvas,f):
    for projectile in f.getProjectiles():
        x,y=projectile.getX(),projectile.getY()
        x,y=getCanvasCoords(app,x,y)
        canvas.create_oval(x-5,y-5,x+5,y+5,fill="Blue")

def drawMonsters(app,canvas,f):
    for monster in f.getMonsters():
        if(isinstance(monster,Melee)):
            color="#4B0082"
        else:
            color="#9932CC"
        x0,y0=monster.getX(),monster.getY()
        x0,y0=getCanvasCoords(app,x0,y0)
        canvas.create_oval(x0-30,y0-30,x0+30,y0+30,fill=color)

def drawSpikes(app,canvas,f):
    for spike in f.getSpikes():
        x0,y0,width,height=spike
        x0,y0=getCanvasCoords(app,x0,y0)
        x1=x0+width
        y1=y0+height
        canvas.create_rectangle(x0,y0,x1,y1,fill="Red")


def drawPoints(app,canvas,f):
    for key in f.getPoints():
        x0,y0=key
        x0,y0=getCanvasCoords(app,x0,y0)
        canvas.create_oval(x0-5,y0-5,x0+5,y0+5,fill="Blue")
        for p in f.getPoints()[key]:
            x1,y1=p
            x1,y1=getCanvasCoords(app,x1,y1)
            canvas.create_line(x0,y0,x1,y1,width=3)

def getCanvasCoords(app,x,y):
    return(app.width//2+x-app.player.getX(),app.height//2+y-app.player.getY())

def cornerOnCanvas(app,ax,ay,width,height,minimap):
    l=[]
    l+=[getCanvasCoords(app,ax,ay)]
    l+=[getCanvasCoords(app,ax+width/4,ay)]
    l+=[getCanvasCoords(app,2*ax+width/4,ay)]
    l+=[getCanvasCoords(app,3*ax+width/4,ay)]
    l+=[getCanvasCoords(app,ax+width,ay)]
    l+=[getCanvasCoords(app,ax+width,ay+height/4)]
    l+=[getCanvasCoords(app,ax+width,ay+2*height/4)]
    l+=[getCanvasCoords(app,ax+width,ay+3*height/4)]
    l+=[getCanvasCoords(app,ax+width,ay+height)]
    l+=[getCanvasCoords(app,ax+width/4,ay+height)]
    l+=[getCanvasCoords(app,2*ax+width/4,ay+height)]
    l+=[getCanvasCoords(app,3*ax+width/4,ay+height)]
    l+=[getCanvasCoords(app,ax,ay+height)]
    l+=[getCanvasCoords(app,ax,ay+height/4)]
    l+=[getCanvasCoords(app,ax,ay+2*height/4)]
    l+=[getCanvasCoords(app,ax,ay+3*height/4)]
    success=False
    for t in l:
        x,y=t
        if(minimap==False and isOnCanvas(app,x,y)):
            success=True
            break
        elif(minimap and isOnMinimap(app,x,y)):
            success=True
            break
    return success

def isOnCanvas(app,x,y):
    if(x>=0 and y>=0 and x<=app.width and y<=app.height):
        return True
    else:
        return False

def isOnMinimap(app,x,y):
    if(x>app.width/-2 and y>app.height/-2 and x<3*app.width/2 and y<3*app.height/2):
        return True
    else:
        return False

def keyPressed(app,event):
    if(app.currentMode=="Game"):
        if(event.key=="~"):
            app.amaliaUsed=True
            app.amalia=not app.amalia
        if(event.key=="`"):
            boss(app)
        if(event.key=="w"):
            app.moveUp=True
        if(event.key=="s"):
            app.moveDown=True
        if(event.key=="d"):
            app.moveRight=True
        if(event.key=="a"):
            app.moveLeft=True
        if(event.key=="Space"):
            dash(app)
        if(event.key=="o"):
            shockwave(app)
        if(event.key=="p"):
            deepcopy(app)
    if(event.key=="m"):
        if(app.currentMode=="Game"):
            app.currentMode="Map"
        elif(app.currentMode=="Map"):
            app.currentMode="Game"
    if(event.key=="n"):
        if(app.currentMode=="Room"):
            app.currentMode="Partition"
        elif(app.currentMode=="Partition"):
            app.currentMode="Room"
    if(event.key=="b"):
        if(app.currentMode=="Menu"):
            app.currentMode="Room"
        elif(app.currentMode=="Room" or app.currentMode=="Partition"):
            app.currentMode="Menu"
    if(event.key=="r"):
        restart(app)
        

def keyReleased(app,event):
    if(event.key=="w"):
        app.moveUp=False
    if(event.key=="a"):
        app.moveLeft=False
    if(event.key=="s"):
        app.moveDown=False
    if(event.key=="d"):
        app.moveRight=False

def main():
    runApp(width=1000, height=1000, mvcCheck=False)



if __name__ == '__main__':
    main()

