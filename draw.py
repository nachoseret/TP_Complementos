import pygame
import math
import random
import argparse
import sys
import time

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW = (255, 225, 0)

# Esta clase almacena los datos extra que necesitamos de un vertice. Estos datos son
# - posicion: una tupla "pos" de flotantes x,y
# - fuerza: una tupla "force" de flotantes x,y
# - un booleano "over" que es True sii el mouse esta pasando por encima del vertice sin hacer click
# - un booleano "grab" que es True sii el vertice ha sido tomado por el mouse
# Estos ultimos dos parametros son utilizados por la funcion mouseHandler y plotGraph
class vData:
    def __init__(self, x, y):
        self.pos = (x,y)
        self.force = (0,0)
        self.over = False
        self.grab = False

# Esta clase representa a un grafo con datos extras. Ademas de las listas de
# vertices y aristas, cuenta con un atributo taken que es un string vacio en caso
# que ningun vertice este agarrado por el mouse o, en caso contrario, un string
# con el nombre del vertice agarrado por el mouse. Por otro lado, esta clase tambien
# tiene un atributo de tipo diccionario de objetos vData, que almacena datos sobre
# los vertices.
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

# Toma un objeto tipo archivo, lee el grafo que este contiene y lo devuelve en
# formato tupla de vertices y aristas.
def leer_grafo(nombre):
    G = [[],[]]
    grafo = nombre.read()
    grafo = grafo.split()
    n = int(grafo[0])
    for i in range(1,n+1):
        G[0].append(grafo[i])
    for i in range(n+1,len(grafo),2):
        G[1].append([grafo[i],grafo[i+1]])
    return G

# Toma un entero n y devuelve un grafo grilla n x n en formato tupla de vertices
# y aristas.
def gManta(n):
    V = [i for i in range(1,n*n + 1)]
    E = []
    for v in V:
        if (v%n)!=0:
            E.append((v,v+1))
        if v<=(n*n - n):
            E.append((v,v+n))
    return (V,E)

# Toma un entero n y devuelve un grafo completo Kn en formato tupla de vertices
# y aristas.
def graphK(n):
    V = [i for i in range(1,n+1)]
    E = []
    for i,v0 in enumerate(V):
        for v1 in V[0:i]+V[i+1:]:
            E.append((v0,v1))
    return (V,E)

# randomPos
# Toma un grafo en formato de tupla de vertices y aristas. Devuelve un grafo
# en formato de objeto graph, definido anteriormente, con posiciones aleatorias
# en todos los vertices. El rango de las posiciones aleatorias es 400<=x<=600,
# 300<=y<=500.
def randomPos(G):
    V,E = G
    G = graph(V,E)

    for v in V:
        G.data[v] = vData(random.randrange(400,600),random.randrange(300,500))
    return G

# plotGraph(graph,bool) -> void
# Toma el grafo y un booleano "show_more". Imprime el grafo en la ventana grafica.
# Si el atributo "over" de un vertice es True, dibuja un circulo verde alrededor
# del mismo. Si el atributo "grab" es True, dibuja un circulo amarillo alrededor
# de tal vertice. Si el argumento booleano "show_more" es True, imprime tambien los
# vectores de las fuerzas sobre cada vertice.
def plotGraph(G, show_more):
    V,E,data = G.tup()
    for e in E:
        v0,v1 = e
        x0,y0 = data[v0].pos
        x1,y1 = data[v1].pos
        pygame.draw.line(screen, BLACK, [int(round(x0)), int(round(y0))], [int(round(x1)), int(round(y1))], 2)
    for v in V:
        x,y = data[v].pos
        if data[v].over:
            pygame.draw.circle(screen, GREEN, [int(round(x)), int(round(y))], 15, 2)
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        if data[v].grab:
            pygame.draw.circle(screen, YELLOW, [int(round(x)), int(round(y))], 15, 2)
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        else:
            pygame.draw.circle(screen, RED, [int(round(x)), int(round(y))], 5)
        if show_more:
            fx,fy = data[v].force
            pygame.draw.line(screen, GREEN, [int(round(x)), int(round(y))], [int(round(x+(fx*20))), int(round(y+(fy*20)))], 2)
        text = myfont.render(str(v), False, BLUE)
        screen.blit(text,(int(round(x))+5, int(round(y))+5))
    pass

# Suma vectorial
def sum(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0+x1,y0+y1)

# Resta vectorial
def sub(u,v):
    x0,y0 = u
    x1,y1 = v
    return (x0-x1,y0-y1)


# updatePos(graph,int) -> graph
# Calcula las fuerzas sobre todos los vertices del grafo (repulsion
# entre ellos, atraccion por las aristas y fuerza de gravedad). Luego,
# actualiza las posiciones de los vertices y retorna el grafo actualizdo.
def updatePos(G,k):
    V,E,data = G.tup()
    dist = {}

    for v in V:
        data[v].force = (0,0)

    for i,v0 in enumerate(V):
        x0,y0 = data[v0].pos
        for v1 in V[0:i]+V[i+1:]:
            x1,y1 = data[v1].pos
            dist[v0,v1] = math.sqrt((x1-x0)**2 + (y1-y0)**2)
            if dist[v0,v1] < 2E-23:
                dist[v0,v1] = 2E-23 # Epsilon de la maquina
            dist[v1,v0] = dist[v0,v1]
            f = k/dist[v0,v1]
            s = (y1-y0)/dist[v0,v1]
            c = (x1-x0)/dist[v0,v1]
            data[v0].force = sub(data[v0].force,(c*f,s*f))
            data[v1].force = sum(data[v1].force,(c*f,s*f))

    x0,y0 = (500,400)
    for v1 in V:
        x1,y1 = data[v1].pos
        dist["center",v1] = math.sqrt((x1-x0)**2 + (y1-y0)**2)
        f = 1
        if dist["center",v1] < 20:
            f = dist["center",v1]/20
        if f == 0:
            return
        s = (y1-y0)/dist["center",v1]
        c = (x1-x0)/dist["center",v1]
        data[v1].force = sub(data[v1].force,(c*f,s*f))

    for v0,v1 in E:
        x0,y0 = data[v0].pos
        x1,y1 = data[v1].pos
        f = dist[v0,v1]/k
        s = (y1-y0)/dist[v0,v1]
        c = (x1-x0)/dist[v0,v1]
        data[v0].force = sum(data[v0].force,(c*f,s*f))
        data[v1].force = sub(data[v1].force,(c*f,s*f))

    for v in V:
        data[v].pos = sum(data[v].pos,data[v].force)

    G.update(V,E,data)
    return G


# updateK(graph,int,int,int) -> int
# Toma el grafo, el coeficiente de las fuerzas, la anchura y altura
# de la ventana. Si algun vertice del grafo esta fuera de la ventana,
# achica el k a razon de 0.99 y retorna el nuevo k.
def updateK(G,k,width,height):
    V,E,data = G.tup()

    for v in V:
        x,y = data[v].pos
        if x>=width-5 or y>=height-5 or x<=5 or y<=5:
            k = k*0.99
    return k

# mouseHandler(graph) -> (graph,bool)
# Toma un objeto tipo graph, reacciona a los eventos del mouse y actualiza
# el objeto. Devuelve una tupla con el nuevo objeto graph y un booleano que
# es True sii algun vertice esta "tomado" por el mouse. Si el mouse esta
# encima de algun vertice, asigna True al atributo "over" de tal vertice. Si
# el mouse esta arrastrando un vertice, asigna True al atributo "grab" de tal
# vertice y actualiza el atributo "taken" del grafo con el nombre del vertice
# actualmente tomado.
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
        data[G.taken].pos = (x0,y0)
        inUse = True
    else:
        for v in V:
            data[v].over = False
            x1,y1 = data[v].pos
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
                data[v].pos = (x0,y0)
                inUse = True

    G.update(V,E,data)
    return G, inUse

# plotMenu(bool,bool,int) -> (bool,int)
# Imprime el menu que permite cambiar el valor de k (coeficiente
# de las fuerzas) o encender el ajuste automatico (ver funcion updateK).
# Responde a los eventos del mouse sobre los botones del menu
# y actualiza k y auto si corresponde. Si el argumento inUse es
# True, imprime el menu pero no reacciona al mouse. Esto es usado
# para que si se arrastra un vertice sobre algun boton del menu,
# no se activen los mismos.
def plotMenu(inUse, auto, k):
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
            if k <= 30:
                k = 30
        if click and x0>=225 and x0<=255 and y0<=30:
            auto = False
            k = k+1
        if click and x0<=80 and y0<=30:
            auto = True
    return (auto,k)

# Imprime una tabla con datos en la terminal para el modo verbose
def verbose(G,k,dT,it):
    V,E,data = G.tup()
    print("ITERACION "+str(it))
    print("k = "+str(k))
    print("Tiempo CPU = "+str(dT))
    print("Vertice\t\tposX\t\tposY\t\tfX\t\tfY")
    for v in V:
        x,y = data[v].pos
        fx,fy = data[v].force
        print(v+"\t"+str(x)+"\t"+str(y)+"\t"+str(fx)+"\t"+str(fy))


# ----------------------------------------------------------

# Argumentos de la llamada al programa
ap = argparse.ArgumentParser()
ap.add_argument( '-v', '-verbose', action='store_true', help='Modo verbose')
ap.add_argument('file', type=argparse.FileType('r'), help='Especificar archivo de donde leer el grafo', default=None)
ap.add_argument('-K', nargs='?', type=int, default=100, help='Especificar coeficiente de fuerza inicial')
args = vars(ap.parse_args())

width = 1000 # Ancho de la ventana
height = 800 # Alto de la ventana
screen = pygame.display.set_mode([width,height]) # Creamos la pantalla

# Inicializamos pygame
pygame.init()
pygame.font.init()

# Creamos la fuente de texto que vamos a utilizar
myfont = pygame.font.SysFont('Arial', 25)

# Nombre de la ventana
pygame.display.set_caption("FRUCHTERMAN - REINGOLD")

done = False # done == True sii la ventana fue cerrada
clock = pygame.time.Clock() # Inicializamos el reloj de pygame

G = randomPos(leer_grafo(args["file"])) # Leemos grafo del archivo y lo transformamos en objeto con randomPos
k = args["K"] # Seteamos el coeficiente de fuerzas inicial
if k <= 30:
    k = 30
auto = True # Modo de ajuste automatico encendido por defecto
it = 1 # Contador de iteraciones

while not done: # Mientras que la ventana este abierta
    clock.tick(60) # 60 fps

    for event in pygame.event.get(): # Si se cierra la ventana, done pasa a ser True
        if event.type == pygame.QUIT:
            done=True

    screen.fill(WHITE) # Fondo blanco
    plotGraph(G, args["v"]) # Imprimimos el grafo. En modo verbose tambien imprimimos los vectores fuerza
    G,inUse = mouseHandler(G) # Reaccionamos a los eventos del mouse
    if args["v"]: # En modo verbose calculamos el tiempo en CPU que lleva realizar una iteracion
        t0 = time.clock()
    G = updatePos(G,k)
    if args["v"]: # En modo verbose calculamos el tiempo promedio que lleva hacer una iteracion y lo imprimimos
        t1 = time.clock()
        if it == 1:
            dT = (t1 - t0)
        dT = dT + (t1 - t0)
        if it%60 == 0 or it == 1: # Actualizamos el promedio una vez por segundo para que sea legible
            avg = dT/it
        text = myfont.render("Tiempo de CPU promedio por iteracion = " + str(avg), False, BLACK)
        screen.blit(text,[5,780])
        verbose(G,k,t1-t0,it) # En modo verbose, imprimimos una tabla de datos en la terminal por cada iteracion
    auto, k = plotMenu(inUse,auto,k) # Imprimimos el menu
    if auto and k > 30: # Si el ajuste automatico esta encendido, llamamos a updateK
        k = updateK(G,k,width,height)
    pygame.display.flip() # Renderizamos
    it+=1 # Sumamos uno a la cantidad de iteraciones

pygame.quit()
