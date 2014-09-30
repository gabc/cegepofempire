#!/usr/bin/env python3
# C:\\Python33\python.exe
class Noeud:
    def __init__(self, x, y, f, gc, parent):
        self.x = x
        self.y = y
        self.f = f
        self.gc = gc
        self.parent = parent
        self.cout = 0

class Deplacement:
    def __init__(self, parent, map):
        self.parent = parent
        self.map = map

    def chemin(self, unite, arrivee):
        depart = Noeud(unite.x, unite.y, 0, 0, None)
        arrive = Noeud(arrivee[0], arrivee[1], 0, 0, None)
        return self.astar(depart, arrive)

    def astar(self, depart, arrivee):
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
                v.parent = current  # Je pense que je le fais deja dans voisin(), mais dans le doute
                v.f = f             # Meeeh
                v.gc = g(v)         # MEEEEH Je le met ou le +10?
                    
                # if v in open or v in closed and v.f Si il est dans open, ou closed. Et que f est plus petit que l'autre.
                #  open.append(v) Le remetre dans open.. basically.
                    
                if v not in open and v not in closed: # Boule infinie?
                    open.append(v)
                    open.sort(key = lambda x: x.f)

    def voisin(n):
        x = n.x
        y = n.y
        rep = []
        for i in (-1,1,0):
            for j in (0,1,-1):
                try:
                    # Si c'est passable et que les deux i,j sont pas 0.
                    if self.map[x+i][y+j].isPassable() and (i != 0 or j != 0) :  
                        n = Noeud(x+i, y+j, 0, 0, n)
                        rep.append(n)
                        if i == 0 or j == 0:
                            n.cout = 10 # ligne droite
                        else:
                            n.cout = 14 # diagonale
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
