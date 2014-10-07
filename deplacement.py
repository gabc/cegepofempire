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

class Deplacement:
    def __init__(self, parent, map):
        self.parent = parent
        
        self.map = map

        self.maxnode = 400
        
    def chemin(self, unite, arrivee):
        depart = Noeud(unite.posX, unite.posY, 0, 0, None)
        arrive = Noeud(arrivee[0], arrivee[1], 0, 0, None)
        return self.astar(depart, arrive)

    def astar(self, depart, arrivee):
        open = [depart]
        closed = []
        temps = time.time()
        
        while open:
            current = open[0]
            del open[0]
            closed.append(current)

            if len(open) > self.maxnode:
                print("FOOOO")
                open = open[:self.maxnode] # Si la liste est trop grande.
            
            # si c'est trop long. On sort.
            if time.time() - temps >= 0.05: # 0.0sec
                return self.path(current)
            else:
                # print(time.time() - temps)
                temps = time.time()
                
            if self.h(current, arrivee) == 0:
                return self.path(current)
                
            for v in self.voisin(current):
                f = self.g(v) + self.h(v,arrivee)
                v.parent = current  # Je pense que je le fais deja dans voisin(), mais dans le doute
                v.f = f             # Meeeh
                v.gc = self.g(v)         # MEEEEH Je le met ou le +10?

                # if v in open or v in closed and v.f Si il est dans open, ou closed. Et que f est plus petit que l'autre.
                #  open.append(v) Le remetre dans open.. basically.
                if v in open:
                    vprime = self.find(v) # [noeud, pos dans la liste]
                    if v.gc < vprime[0].gc:
                        del open[vprime[1]]

                if v not in open and v not in closed: # Boule infinie?
                    open.append(v)
                    open.sort(key = lambda x: x.f)

    def find(self, n):
        i = 0
        for o in open:
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
                    if self.map[x+i][y+j].isPassable() and (i != 0 or j != 0) : # Voir si le test est bon
                        n = Noeud(x+i, y+j, 0, 0, n)
                        rep.append(n)
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
            acc += n.gc #+ n.cout
            n = n.parent
        return acc
        
    def path(self, n):
        path = [n]              # L'arrivee est dans la liste du path
        while n.parent is not None:
            path = [n.parent] + path
            n = n.parent
        return path


if __name__ == '__main__':
    class Foo:
        def __init__(self,x,y):
            self.posX = x
            self.posY = y

    from map import *
    import cProfile             # Si il est la.
    l=55
    h=25
    liste=[Joueur(1,"a"), Joueur(2,"b")]
    m=Map(l,h)
    m.setSeed(10)
    m.placeRessourcesOverworld()
    m.placeRessourcesUnderworld()
    m.placeJoueurs(liste)
    #m.equilibreRessources(liste) <-- To do
    #m.printMapToFile()
    dx = 2
    dy = 2
    ax = 1
    ay = 15
    d = Deplacement(None, m.mat)
    cProfile.run('path = d.chemin(Foo(dx,dy),(ax,ay))')
    # path = d.chemin(Foo(dx,dy),(ax,ay))

    
    str = ""
    flag = False
    for i in range(h):          # l et h dans le bon ordre?
        for j in range(l):
            if i == dx and j == dy:
                str += "D"
            elif i == ax and j == ay:
                str += "A"
            else:
                for p in path:
                    if i == p.x and j == p.y:
                        str +="."
                        flag = True
                if not flag:
                    str += m.mat[j][i].ressource
                flag = False
        print(str)
        str = ""
    for i in path:
        print(i.x, i.y)
    # print(path)
