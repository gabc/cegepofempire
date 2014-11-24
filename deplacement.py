#!/usr/bin/env python3
# C:\\Python33\python.exe
"""Module qui permet de trouver un chemin entre 2 points."""
from utils import trouveCase

class Noeud:
    """Classe representant un point (case,noeud) dans mon graphe de recherche"""
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.f = 0
        self.gc = 0
        self.parent = parent
        self.cout = 0

    def estDans(self, liste):
        """Trouve si self est dans la liste"""
        for i in liste:
            if self.x == i.x and self.y == i.y:
                return True
        return False

class Deplacement:
    """Classe encapsulant A*"""
    def __init__(self, parent, map):
        self.parent = parent
        self.map = map
        self.maxnode = 400

    def assurePassable(self, depart, arrive):
        while not self.map[arrive.x][arrive.y].isPassable():
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
        """Trouve le chemie entre la position de `unite' et
        le tuple `arrivee' (x, y)"""
        x, y = trouveCase(unite.posX, unite.posY)
        depart = Noeud(int(x), int(y), None)
        arrive = Noeud(arrivee[0], arrivee[1], None)

        arrive = self.assurePassable(depart, arrive)

        return self.astar(depart, arrive)

    def astar(self, depart, arrivee):
        open = [depart]
        closed = []

        while open:
            current = open[0]
            del open[0]
            closed.append(current)

            if self.h(current, arrivee) == 0:
                return self.path(current)

            for v in self.voisin(current):
                v.parent = current
                v.gc = self.g(v)
                f = v.gc + self.h(v, arrivee)
                v.f = f
                
                if v.estDans(open):
                    vprime = self.find(v, open) # [noeud, pos dans la liste]
                    if v.gc < vprime[0].gc or v.f < vprime[0].f:
                        del open[vprime[1]]

                if not v.estDans(open) and not v.estDans(closed):
                    open.append(v)
                    open.sort(key=lambda x: x.f)

    def find(self, noeud, liste):
        """Trouve le noeud dans la liste
        Retourne, le noeud et sa position dans la liste"""
        i = 0
        for j in liste:
            if j.x == noeud.x and j.y == noeud.y:
                return (j, i)
            i += 1

    def voisin(self, noeud):
        """Trouve les voisins (passables) du noeud `n'"""
        x = noeud.x
        y = noeud.y
        rep = []
        for i in (-1, 1, 0):
            for j in (0, 1, -1):
                try:
                    # Si c'est passable et que les deux i,j sont pas 0.
                    if self.map[y+j][x+i].isPassable() and (i != 0 or j != 0) and x+i >= 0 and y+j >= 0:
                        node = Noeud(x+i, y+j, noeud)
                        rep.append(node)
                        if i == 0 or j == 0:
                            noeud.cout = 10 # ligne droite
                        else:
                            noeud.cout = 14 # diagonale
                except IndexError:
                    pass
        return rep

    def h(self, a, b):
        """Heuristique retournant une distance entre 2 points"""
        x1, y1 = a.x, a.y
        x2, y2 = b.x, b.y
        return abs(x1 - x2) + abs(y1 - y2)

    def g(self, noeud):
        """Methode calculant la somme des couts de chaques noeuds"""
        acc = 0
        while noeud.parent is not None:
            acc += noeud.gc + noeud.cout
            noeud = noeud.parent
        return acc

    def path(self, n):
        """Retourne le chemin à partir des parents de n"""
        path = [n]              # L'arrivee est dans la liste du path
        while n.parent is not None:
            path = [n.parent] + path
            n = n.parent
        return path
