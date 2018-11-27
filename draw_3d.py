import pygame
import math
import random

class vData:
    def __init__(self, x, y, z):
        self.pos = (x,y,z)
        self.posP = (0,0)
        self.force = (0,0,0)
        self.g = (0,0,0)
        self.over = False
        self.grab = False

class graph:
    def __init__(self,V,E):
        self.V = V
        self.E = E
        self.taken = ""
        self.data = {}

    def tup(self):
        return (self.V,self.E,self.data)

    def update(self,V,E,data):
            self.V = V
            self.E = E
            self.data = data

def gManta(n):
    V = [i for i in range(1,n*n + 1)]
    E = []
    for v in V:
        if (v%n)!=0:
            E.append((v,v+1))
        if v<=(n*n - n):
            E.append((v,v+n))
    return (V,E)

def graphK(n):
    V = [i for i in range(1,n+1)]
    E = []
    for i,v0 in enumerate(V):
        for v1 in V[0:i]+V[i+1:]:
            E.append((v0,v1))
    return (V,E)

def randomPos(G):
    V,E = G
    G = graph(V,E)

    for v in V:
        G.data[v] = vData(random.randrange(400,600),random.randrange(300,500),random.randrange(300,500))
    return G

def toPersp(G):
    V,E,data = G.tup()
    xFocus,yFocus = (500,400)
    depthScale = 400
    for v in V:
        x0,y0,z0 = data[v].pos
        x = ((x0 - xFocus) / float(float(z0) / float(depthScale))) + xFocus
        y = ((y0 - yFocus) / float(float(z0) / float(depthScale))) + yFocus
        data[v].posP = (x,y)
    G.update(V,E,data)

def plotGraphPers(G, show_more):
    toPersp(G)
    V,E,data = G.tup()
    for e in E:
        v0,v1 = e
        x0,y0 = data[v0].posP
        x1,y1 = data[v1].posP
        pygame.draw.line(screen, BLACK, [int(round(x0)), int(round(y0))], [int(round(x1)), int(round(y1))], 2)
    for v in V:
        x,y = data[v].posP
        if data[v].over:
            pygame.draw.circle(screen, GREEN, [int(round(x)), int(round(y))], 15, 2)
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        if data[v].grab:
            pygame.draw.circle(screen, YELLOW, [int(round(x)), int(round(y))], 15, 2)
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        else:
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        text = myfont.render(str(v), False, BLUE)
        screen.blit(text,(int(round(x))+5, int(round(y))+5))
    pass

def plotGraph(G, show_more):
    V,E,data = G.tup()
    for e in E:
        v0,v1 = e
        x0,y0,z0 = data[v0].pos
        x1,y1,z1 = data[v1].pos
        pygame.draw.line(screen, BLACK, [int(round(x0)), int(round(y0))], [int(round(x1)), int(round(y1))], 2)
    
    ma,mi = (0,0)

    for i,v in enumerate(V):
        _,_,z = data[v].pos
        if i == 1:
            ma = z
            mi = z
        else:
            if z < mi:
                mi = z
            if z > ma:
                ma = z

    for v in V:
        x,y,z = data[v].pos
        t = (z - mi)*(254-1)/(ma-mi) + 1
        col = (t, 0, 255-t)
        if data[v].over:
            pygame.draw.circle(screen, GREEN, [int(round(x)), int(round(y))], 15+int(t/100), 2)
            pygame.draw.circle(screen, col, [int(round(x)), int(round(y))], 5+int(t/100))
        if data[v].grab:
            pygame.draw.circle(screen, YELLOW, [int(round(x)), int(round(y))], 15+int(t/100), 2)
            pygame.draw.circle(screen, col, [int(round(x)), int(round(y))], 5+int(t/100))
        else:
            pygame.draw.circle(screen, col, [int(round(x)), int(round(y))], 5+int(t/100))
        if show_more:
            fx,fy,fz = data[v].force
            pygame.draw.line(screen, GREEN, [int(round(x)), int(round(y))], [int(round(x+(fx*20))), int(round(y+(fy*20)))], 2)
            text = myfont2.render(str(math.sqrt(fx**2 + fy**2)), False, GREEN)
            screen.blit(text,[int(round(x+(fx*20)))+5, int(round(y+(fy*20)))-5])
        text = myfont.render(str(v), False, col)
        screen.blit(text,(int(round(x))+5, int(round(y))+5))
    pygame.draw.line(screen, BLACK, [495, 400], [505, 400], 1)
    pygame.draw.line(screen, BLACK, [500, 395], [500, 405], 1)
    pass

def sum(u,v):
    x0,y0,z0 = u
    x1,y1,z1 = v
    return (x0+x1,y0+y1,z0+z1)

def sub(u,v):
    x0,y0,z0 = u
    x1,y1,z1 = v
    return (x0-x1,y0-y1,z0-z1)

def updatePos(G,k):
    V,E,data = G.tup()
    dist = {}

    for v in V:
        data[v].force = (0,0,0)

    for i,v0 in enumerate(V):
        x0,y0,z0 = data[v0].pos
        for v1 in V[0:i]+V[i+1:]:
            x1,y1,z1 = data[v1].pos
            dist[v0,v1] = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
            if dist[v0,v1] < 2E-23:
                dist[v0,v1] = 2E-23 # Epsilon de la maquina
            dist[v1,v0] = dist[v0,v1]
            f = k/dist[v0,v1]
            s = (y1-y0)/dist[v0,v1]
            c = (x1-x0)/dist[v0,v1]
            cz = (z1-z0)/dist[v0,v1]
            data[v0].force = sub(data[v0].force,(c*f,s*f,cz*f))
            data[v1].force = sum(data[v1].force,(c*f,s*f,cz*f))

        x1,y1,z1 = (500,400,400)
        dist["center",v0] = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
        f = dist[v0,v1]*5/k
        s = (y1-y0)/dist[v0,v1]
        c = (x1-x0)/dist[v0,v1]
        cz = (z1-z0)/dist[v0,v1]
        data[v0].force = sum(data[v0].force,(c*f,s*f,cz*f))
        data[v0].g = (-c*f,-s*f,-cz*f)

    '''
    x0,y0,z0 = (500,400,400)
    for v1 in V:
        x1,y1,z1 = data[v1].pos
        dist["center",v1] = math.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
        f = 2
        if dist["center",v1] < 20:
            f = dist["center",v1]/20
        if f == 0:
            return
        s = (y1-y0)/dist["center",v1]
        c = (x1-x0)/dist["center",v1]
        cz = (z1-z0)/dist["center",v1]
        data[v1].force = sub(data[v1].force,(c*f,s*f,cz*f))
        data[v1].g = (-c*f,-s*f,-cz*f)
    '''
    for v0,v1 in E:
        x0,y0,z0 = data[v0].pos
        x1,y1,z1 = data[v1].pos
        f = dist[v0,v1]/k
        s = (y1-y0)/dist[v0,v1]
        c = (x1-x0)/dist[v0,v1]
        cz = (z1-z0)/dist[v0,v1]
        data[v0].force = sum(data[v0].force,(c*f,s*f,cz*f))
        data[v1].force = sub(data[v1].force,(c*f,s*f,cz*f))

    for v in V:
        data[v].pos = sum(data[v].pos,data[v].force)

    G.update(V,E,data)
    return G

def updateK(G,k,width,height):
    V,E,data = G.tup()

    for v in V:
        x,y,z = data[v].pos
        if x>=width-5 or y>=height-5 or x<=5 or y<=5:
            return k*0.99
    return k

def mouseHandler(G):
    V,E,data = G.tup()
    x0,y0 = pygame.mouse.get_pos()
    click,_,_ = pygame.mouse.get_pressed()
    inUse = False
    if not click:
        for v in V:
            data[v].grab = False
        G.taken = ""
        pygame.mouse.set_visible(True)
        pass
    if G.taken != "":
        _,_,z = data[G.taken].pos
        data[G.taken].pos = (x0,y0,z)
        inUse = True
    else:
        for v in V:
            data[v].over = False
            x1,y1,z1 = data[v].pos
            dist = (x1-x0)**2 + (y1-y0)**2
            if dist < 225 or data[v].grab:
                data[v].over = True
            if data[v].over and not data[v].grab and click:
                pygame.mouse.set_pos((x1,y1))
                pygame.mouse.set_visible(False)
                x0,y0 = (x1,y1)
                data[v].grab = True
                G.taken = v
            if data[v].grab:
                data[v].pos = (x0,y0,z1)
                inUse = True

    G.update(V,E,data)
    return G, inUse

def plotMenu(inUse, auto, k, width, height):
    pygame.draw.rect(screen, WHITE, [0, 0, 255, 30])
    if auto:
        pygame.draw.rect(screen, RED, [0, 0, 80, 30],2)
        text = myfont.render("AUTO", False, RED)
    else:
        pygame.draw.rect(screen, BLACK, [0, 0, 80, 30],2)
        text = myfont.render("AUTO", False, BLACK)
    screen.blit(text,text.get_rect(center = [40,15]))
    if k <= 255:
        col = (k,   255-k,   0)
    else:
        col = RED
    text = myfont.render("K = "+str(int(k)), False, col)
    screen.blit(text,text.get_rect(center = [170,15]))
    pygame.draw.rect(screen, BLACK, [120, 0, 100, 30],2)
    pygame.draw.rect(screen, BLACK, [85, 0, 30, 30],2) # -
    text = myfont.render("-", False, BLACK)
    screen.blit(text,text.get_rect(center = [100,15]))
    pygame.draw.rect(screen, BLACK, [225, 0, 30, 30],2) # +
    text = myfont.render("+", False, BLACK)
    screen.blit(text,text.get_rect(center = [240,15]))

    if not inUse:
        click,_,_ = pygame.mouse.get_pressed()
        x0,y0 = pygame.mouse.get_pos()
        if click and x0>=85 and x0<=115 and y0<=30:
            auto = False
            k = k-1
            if k <= 10:
                k = 10
        if click and x0>=225 and x0<=255 and y0<=30:
            auto = False
            k = k+1
        if click and x0<=80 and y0<=30:
            auto = True
    return (auto,k)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 25)
myfont2 = pygame.font.SysFont('Arial', 15)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255, 225, 0)

width = 1000
height = 800
screen = pygame.display.set_mode([width,height])

pygame.display.set_caption("FRUCHTERMAN - REINGOLD")

done = False
clock = pygame.time.Clock()

Petersen = randomPos(([1,2,3,4,5,6,7,8,9,10],
    [(1,2),(2,3),(3,4),(4,5),(5,1),(1,7),(2,8),(3,9),(4,10),(5,6),(7,10),(10,8),(8,6),(6,9),(9,7)]))

Cubo = randomPos(( [1,2,3,4,5,6,7,8] ,
    [(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5),(1,5),(2,6),(3,7),(4,8)]))

BTree = randomPos(([1,2,3,4,5,6,7],
    [(4,2),(4,6),(2,1),(2,3),(6,5),(6,7)]))

nonConnected = randomPos(( [1,2,3,4,5,6,7,8] ,
    [(1,2),(2,3),(3,4),(4,1),(5,6),(6,7),(7,8),(8,5)]))

#G = randomPos(graphK(8))
G = randomPos(gManta(5))
#G = Cubo
k = 100
auto = True

while not done:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.fill(WHITE)
    plotGraph(G, False)
    G,inUse = mouseHandler(G)
    G = updatePos(G,k)
    auto, k = plotMenu(inUse,auto,k,width,height)
    if auto:
        k = updateK(G,k,width,height)
    pygame.display.flip()

pygame.quit()
