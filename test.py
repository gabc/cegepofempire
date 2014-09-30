#!/usr/bin/env python3
class Noeud:
    def __init__(self, x, y, f, gc, parent):
        self.x = x
        self.y = y
        self.f = f
        self.gc = gc
        self.parent = parent
        
class Point:
    def __init__(self, x, y, flag):
        self.x = x
        self.y = y
        self.flag = flag

# Fuck that
# 0 = passable
# 1 = depart
# 2 = arrive
# 3 = mur
# 4 = chemin

map = []
path = []
depart = Noeud(1, 1, 0, 0, None)
arrivee = Noeud(20,18, 0, 0, None)
trouble = [(3,5), (4,6), (5,5),(7,7),(10,10),(9,8),(12,14),(20,3),(20,10), (12,15),(12,16),(13,17),(13,18),(12,18), (12,17),(13,19),(13,20)]

PASSABLE = 3

def initmap():
    for i in range(25):
        map.append([])
        for j in range(25):
            map[i].append(Point(i,j,0))
    map[depart.x][depart.y].flag = 1
    map[arrivee.x][arrivee.y].flag = 2
    for i in trouble:
        map[i[0]][i[1]].flag = 3
    
def printmap():
    for i in range(25):
        t = ""
        for j in range(25):
            if map[i][j].flag == 0:
                t+="."
            elif map[i][j].flag == 1:
                t+="D"
            elif map[i][j].flag == 2:
                t+="A"
            elif map[i][j].flag == 3:
                t+="-"
            elif map[i][j].flag == 4:
                t+="+"
        print(t)

def voisin(n):
    x = n.x
    y = n.y
    rep = []
    for i in (-1,1,0):
        for j in (0,1,-1):
            try:
                if map[x+i][y+j].flag != 3 and (i != 0 or j != 0) :  # Si c'est passable et que les deux i,j sont pas 0.
                    rep.append(Noeud(x+i, y+j, 0, 0, n))
            except IndexError:
                pass
    return rep

def h(a, b):
    x1, y1 = a.x, a.y
    x2, y2 = b.x, b.y
    return abs(x1 - x2) + abs(y1 - y2)

def g(n):
    acc = 0
    while n.parent is not None:
        acc += n.gc
        n = n.parent
    return acc
        
def path(n):
    path = []
    while n.parent is not None:
        path = [n.parent] + path
        n = n.parent
    return path
    
def chemin():
    open = [depart]
    closed = []

    while open:
        current = open[0]
        del open[0]
        closed.append(current)

        if h(current, arrivee) == 0:
            return path(current)

        for v in voisin(current):
            f = g(v) + h(v,arrivee)
            v.parent = current  # Je pense que je le fais déjà dans voisin(), mais dans le doute
            v.f = f             # Meeeh
            v.gc = g(v) + 10    # MEEEEH Je le met ou le +10?

            # if v in open or v in closed and v.f Si il est dans open, ou closed. Et que f est plus petit que l'autre.
            #  open.append(v) Le remetre dans open.. basically.

            if v not in open and v not in closed: # Boule infinie?
                open.append(v)
            open.sort(key = lambda x: x.f)
                
## Theoriquement, le `main'
initmap()
printmap()
foo = chemin()
for i in foo:
    print(i.x, i.y)
    map[i.x][i.y].flag = 4
printmap()
