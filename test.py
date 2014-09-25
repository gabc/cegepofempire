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
        
    def deplacement(self):
        self.p.m.joueur.deplace(self.p.m.joueur.depart, self.p.m.joueur.arrivee)
        self.root.after(50, self.deplacement)

    def setDepart(self, event):
        self.p.m.joueur.depart.x = event.x
        self.p.m.joueur.depart.y = event.y

    def setArrivee(self, event):
        self.p.m.joueur.arrivee = Noeud(event.x, event.y, True, 0, None)

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
        self.can.create_text(self.p.getjx(), self.p.getjy(), text= "@", tags="piece")
        self.can.create_text(self.p.getjarrx(), self.p.getjarry(), text= "X", tags="but")
        for i in range(25):
            for j in range(25):
                if self.p.m.map[i][j].passablep() == False:
                    self.can.create_text(i*20 + 10, j*20 + 10, text = "=", tags = "mur")
                    
    def jouer(self):
        self.dessinerGrille()
        self.updateBoard()
        self.can.pack()
        self.root.after(200,self.jouer)

class Noeud:
    def __init__(self, x, y, passable, poid, parent):
        self.x = x
        self.y = y
        self.passable = passable
        self.poid = poid        # Ou on le calcule a partir du parent?
        self.parent = parent    # Noeud precedent. (D'ou on vient)

    # def x (self):
    #     return self.pt.x
    # def y (self):
    #     return self.pt.y

    def passablep(self):
        return self.passable

    def togglepassable(self):
        self.passable = not self.passable
        
class Joueur:
    def __init__(self, p):
        self.p = p              # Modele
        self.depart = Noeud(0, 0, True, 0, None)
        self.arrivee = Noeud(0, 0, True, 0, None)

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
            if len(open) >= 10:
                return came_from

            for next in self.voisins(current):
                print("Dans next", next)
                f = g[nex] + h(current, next)
                if next not in g or f < g[next]:
                    g[next] = f
                    # priority = f + g(arr, next)
                    open.append(next)
                    came_from[next] = current
        return came_from

    def deplace(self, dep, arr):
        path = self.aetoile(dep,arr)
        print("After a*")
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
    
    def h(a, b):
        x1 = a.x()
        y1 = a.y()
        x2 = b.x()
        y2 = b.y()
        return abs(x1 - x2) + abs(y1 - y2)

    def voisins(self,n):
        """Retourne les voisins d'un point, ignorant tout ce qui est pas `passable'""" 
        voisin = []
        for i in [0,1,-1]:
            for j in [-1,1,0]:
                try:
                    voisin.append(self.p.map[n.x+i][n.y+j])
                    print("No fuck")
                except IndexError:
                    print("Fuck")
        print(list(voisin))
        voisin = filter(self.p.n.passablep, voisin)

        return list(voisin)
        
class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.n = Noeud(0, 0, True, 0, None)
        self.joueur = Joueur(self)
        self.map = []
        for i in range(25):
            self.map.append([])
            for j in range(25):
                self.map[i].append(Noeud(i, j, True, 0, None))
                
        
class Controleur:
    def __init__(self):
        self.m = Modele(self)
        self.vue = Vue(self)
        self.vue.jouer()
        self.vue.root.mainloop()

    def getjx(self):
        return self.m.joueur.depart.x

    def getjy(self):
        return self.m.joueur.depart.y

    def getjarrx(self):
        return self.m.joueur.arrivee.x

    def getjarry(self):
        return self.m.joueur.arrivee.y

    
jeu = Controleur()
