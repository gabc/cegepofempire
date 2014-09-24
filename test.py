#!/usr/bin/env python3
from tkinter import *

class Vue:
    def __init__(self, p):
        self.p = p
        
        self.root = Tk()

        self.can = Canvas(self.root, height = 500, width = 500, bg = "white")
        self.can.bind("<Button-1>", self.setDepart)
        self.can.bind("<Button-2>", self.setArrivee)
        self.can.bind("<Button-3>", self.toggleMur)
        
        self.panmenu = PanedWindow(orient=VERTICAL)
        self.panmenu.add(Button(self.root, text='Quitter',command=self.quitter))
        self.panmenu.add(Button(self.root, text='Deplace', command=self.deplacement))
        self.panmenu.pack()

    def quitter(self):
        self.root.destroy()
        exit(0)

    def toggleMur(self, event):
        self.p.m.map[int(event.x/20)][int(event.y/20)].togglepassable()
        
    def addWayPoint(self, event):
        print('Ok: ', event.x, event.y)
        self.p.m.joueur.chemin.append(Case(event.x, event.y))

    def deplacement(self):
        self.p.m.joueur.deplacement()
        self.root.after(50, self.deplacement)

    def setDepart(self, event):
        self.p.m.joueur.depart = Case(event.x, event.y)

    def setArrivee(self, event):
        self.p.m.joueur.arrivee = Case(event.x, event.y)

    def addMur(self,event):
        print(event.x)

    def dessinerGrille(self):
        for i in range(501):
            self.can.create_line(i*20,0,i*20, 500 * 20)
        for i in range(501):
            self.can.create_line(0, i*20, 500 * 20, i*20)
            
    def updateBoard(self):
        self.can.delete("piece")
        self.can.delete("but")
        self.can.delete("mur")
        self.can.create_text(self.p.m.joueur.depart.x, self.p.m.joueur.depart.y, text= "@", tags="piece")
        self.can.create_text(self.p.m.joueur.arrivee.x, self.p.m.joueur.arrivee.y, text= "X", tags="but")
        for i in range(25):
            for j in range(25):
                if self.p.m.map[i][j].passable == False:
                    self.can.create_text(i*20 + 10, j*20 + 10, text = "=", tags = "mur")
                    
    def jouer(self):
        self.dessinerGrille()
        self.updateBoard()
        self.can.pack()
        self.root.after(200,self.jouer)

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Noeud:
    def __init__(self, pt, passable, poid, parent):
        self.pt = pt
        self.passable = passable
        self.poid = poid        # Ou on le calcule a partir du parent?
        self.parent = parent    # Noeud precedent. (D'ou on vient)

    def x(self):
        return self.pt.x
    def y(self):
        return self.pt.y

    def passablep(self):
        return self.passable
    
class Joueur:
    def __init__(self, p):
        self.p = p              # Modele

    def deplace(self, dep, arr):
        path = aetoile(dep,arr)
        if self.h(dep, arr) == 0:
            if path:
                del path[0]
                arr = path[0]
            else:
                print("DONE")
                return
            self.moveto(dep, arr)

    def moveto(self, dep, arr):
        while self.distance(dep, arr) != 0:
            if dep.x < arr.x:
                dep.x += 1
            if dep.y < arr.y:
                dep.y += 1
            if dep.x > arr.x:
                dep.x -= 1
            if dep.y > arr.y:
                dep.y -= 1
        
    def aetoile(self, dep, arr):
        """ dep c'est un noeud de depart, et arr c'est un point d'arrivee (un noeud au pire) """
        open = [dep]
        close = []
        current = None
        g = {}                  # Cost_so_far
        g[dep] = 0
        came_from = {}
        
        while open:
            current = open[0]   # .pop()?

            # early exit

            for next in self.voisins(current):
                f = g[nex] + h(current, next)
                if next not in g or f < g[next]:
                    g[next] = f
                    # priority = f + g(arr, next)
                    open.append(next)
                    came_from[next] = current
        return came_from
    
    def h(a, b):
        x1 = a.x()
        y1 = a.y()
        x2 = b.x()
        y2 = b.y()
        return abs(x1 - x2) + abs(y1 - y2)

    def voisins(n):             # Pardon de la mochete.
        """Retourne les voisins d'un point, ignorant tout ce qui est pas `passable'""" 
        voisin = []
        try:
            voisin.append(self.p.map[n.x()][n.y()-1])
        except IndexError:
            pass
        try:
            voisin.append(self.p.map[n.x()][n.y()+1])
        except IndexError:
            pass
        try:
            voisin.append(self.p.map[n.x()+1][n.y()])
        except IndexError:
            pass
        try:
            voisin.append(self.p.map[n.x()-1][n.y()])
        except IndexError:
            pass

        voisin = filter(self.p.n.passablep, voisin) # Donner un qui est dans le voisin? ._.
        
class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.n = Noeud(None, True, 0, None)
        self.joueur = Pion(self, Case(0,0))
        self.map = []
        for i in range(25):
            self.map.append([])
            for j in range(25):
                self.map[i].append(Case(i,j))
                
        
class Controleur:
    def __init__(self):
        self.m = Modele(self)
        self.vue = Vue(self)
        self.vue.jouer()
        self.vue.root.mainloop()

jeu = Controleur()
