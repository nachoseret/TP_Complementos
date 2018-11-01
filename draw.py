import pygame
import math
import random 

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
    pos = {}
    force = {}

    for v in V:
        pos[v] = (random.randrange(400,600),random.randrange(300,500))
        force[v] = (0,0)
    return (V,E,pos,force)

def plotGraph(G, show_more):
    V,E,pos,force = G
    for e in E:
        v0,v1 = e
        x0,y0 = pos[v0]
        x1,y1 = pos[v1]
        pygame.draw.line(screen, BLACK, [int(round(x0)), int(round(y0))], [int(round(x1)), int(round(y1))], 2)
    for v in V:
        x,y = pos[v]
        pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        if show_more:
            fx,fy = force[v]
            pygame.draw.line(screen, GREEN, [int(round(x)), int(round(y))], [int(round(x+(fx*20))), int(round(y+(fy*20)))], 2)
            text = myfont2.render(str(math.sqrt(fx**2 + fy**2)), False, GREEN)
            screen.blit(text,[int(round(x+(fx*20)))+5, int(round(y+(fy*20)))-5])
        text = myfont.render(str(v), False, BLUE)
        screen.blit(text,(int(round(x))+5, int(round(y))+5))
    pass

def sum(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0+x1,y0+y1)

def sub(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0-x1,y0-y1)

def updatePos(G,k):
    V,E,pos,force = G

    for v in V:
        force[v] = (0,0)

    for i,v0 in enumerate(V):
        x0,y0 = pos[v0]
        for v1 in V[0:i]+V[i+1:]:
            x1,y1 = pos[v1]
            dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            f = k/dist
            s = (y1-y0)/dist
            c = (x1-x0)/dist
            force[v0] = sub(force[v0],(c*f,s*f))
            force[v1] = sum(force[v1],(c*f,s*f))

    for v0,v1 in E:
        x0,y0 = pos[v0]
        x1,y1 = pos[v1]
        dist = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        f = dist/k
        s = (y1-y0)/dist
        c = (x1-x0)/dist
        force[v0] = sum(force[v0],(c*f,s*f))
        force[v1] = sub(force[v1],(c*f,s*f))

    for v in V:
        pos[v] = sum(pos[v],force[v])

    return (V,E,pos,force)

def updateK(G,k,width,height):
    V,E,pos,force = G

    for v in V:
        x,y = pos[v]
        if x>=width-5 or y>=height-5 or x<=5 or y<=5:
            return k*0.99
    return k

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 25)
myfont2 = pygame.font.SysFont('Arial', 15)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

width = 1000
height = 800
screen = pygame.display.set_mode([width,height])
 
pygame.display.set_caption("FRUCHTERMAN - REINGOLD")

done = False
clock = pygame.time.Clock()

Petersen = randomPos(([1,2,3,4,5,6,7,8,9,10],
    [(1,2),(2,3),(3,4),(4,5),(5,1),(1,7),(2,8),(3,9),(4,10),(5,6),(7,10),(10,8),(8,6),(6,9),(9,7)]))

BTree = ([1,2,3,4,5,6,7],
    [(4,2),(4,6),(2,1),(2,3),(6,5),(6,7)])

G = randomPos(gManta(4))
k = 100

while not done:
    clock.tick(60)
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.fill(WHITE)
    plotGraph(G, False)
    G = updatePos(G,k)
    k = updateK(G,k,width,height)
    pygame.display.flip()

pygame.quit()