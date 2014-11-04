#!/usr/bin/env python3
# C:\\Python33\python.exe
import time

class Noeud:
    def __init__(self, x, y, f, gc, parent):
        self.x = x
        self.y = y
        self.f = f
        self.gc = gc
        self.parent = parent
        self.cout = 0

    def estDans(self, liste):
        for i in liste:
            if self.x == i.x and self.y == i.y:
                return True
        return False

class Deplacement:
    def __init__(self, parent, map):
        self.parent = parent
        self.map = map
        self.maxnode = 400

    def assurePassable(self, depart, arrive):
        while not self.map[arrive.y][arrive.x].isPassable():
            if arrive.x > depart.x:
                arrive.x -= 1
            elif arrive.x < depart.x:
                arrive.x += 1
            if arrive.y > depart.y:
                arrive.y -= 1
            elif arrive.y < depart.y:
                arrive.y += 1

        return arrive

    def chemin(self, unite, arrivee):
        depart = Noeud(int(unite.posX/20), int(unite.posY/20), 0, 0, None)
        arrive = Noeud(arrivee[0], arrivee[1], 0, 0, None)

        arrive = self.assurePassable(depart, arrive)

        return self.astar(depart, arrive)

    def astar(self, depart, arrivee):
        open = [depart]
        closed = []
        temps = time.time()
        
        while open:
            current = open[0]
            del open[0]
            closed.append(current)
                
            if self.h(current, arrivee) == 0:
                return self.path(current)

            for v in self.voisin(current):
                v.parent = current
                v.gc = self.g(v)
                f = v.gc + self.h(v,arrivee)
                v.f = f         
                
                if v.estDans(open):
                    vprime = self.find(v, open) # [noeud, pos dans la liste]
                    if v.gc < vprime[0].gc or v.f < vprime[0].f:
                        del open[vprime[1]]

                if not v.estDans(open) and not v.estDans(closed):
                    open.append(v)
                    open.sort(key = lambda x: x.f)

    def find(self, n, liste):
        i = 0
        for o in liste:
            if o.x == n.x and o.y == n.y:
                return (o, i)
            i += 1

    def voisin(self, n):
        x = n.x
        y = n.y
        rep = []
        for i in (-1,1,0):
            for j in (0,1,-1):
                try:
                    # Si c'est passable et que les deux i,j sont pas 0.
                    if self.map[y+i][x+j].isPassable() and (i != 0 or j != 0) : # Voir si le test est bon
                        np = Noeud(x+i, y+j, 0, 0, n)
                        rep.append(np)
                        if i == 0 or j == 0:
                            n.cout = 10 # ligne droite
                        else:
                            n.cout = 14 # diagonale
                except IndexError:
                    pass
        return rep

    def h(self, a, b):
        x1, y1 = a.x, a.y
        x2, y2 = b.x, b.y
        return abs(x1 - x2) + abs(y1 - y2)
        
    def g(self, n):
        acc = 0
        while n.parent is not None:
            acc += n.gc + n.cout
            n = n.parent
        return acc
        
    def path(self, n):
        path = [n]              # L'arrivee est dans la liste du path
        while n.parent is not None:
            path = [n.parent] + path
            n = n.parent
        return path
