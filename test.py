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

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.passable = True

    def togglepassable(self):
        self.passable = self.passable != True

class Case:
    def __init__(self, p, passable, parent, poid):
        self.x = p.x
        self.y = p.y
        self.p = p              # Point
        self.passable = True
        self.parent = parent
        self.poid = poid

    def togglepassable(self):
        self.passable = not self.passable

        
class Pion:
    def __init__(self, parent, depart):
        self.depart = depart
        self.arrivee = Point(0,0)
        self.parent = parent
        self.vitesse = 20
        self.chemin = []
        
    def deplacement(self):
        if self.distance(self.depart, self.arrivee) == 0:
            if self.chemin:
                del self.chemin[0]
                self.arrivee = self.chemin[0]
            else:
                print("DONE")
                return

        self.calculechemin()
        self.moveto(self.depart, self.arrivee)

    def calculechemin(self):
        frontier = []
        frontier.append(self.depart)
        visited = {}
        visited[self.depart] = True

        while frontier:
            current = frontier.pop()
            for next in self.voisins(current):
                if next not in visited:
                    frontier.put(next)
                    visited[next] = True

    def voisins(self, case):
        """Methode sale qui retourne les voisins d'une case.
        Doit etre refaite parce que, merde."""
        voisin = []
        if case.x == 0 and case.y == 0:
            voisin.append(self.parent.map[case.x+1])
            voisin.append(self.parent.map[case.y+1])
            return voisin
        if case.x == 0:
            voisin.append(self.parent.map[case.x][case.y+1])
            voisin.append(self.parent.map[case.x][case.y-1])
            voisin.append(self.parent.map[case.x+1][case.y])
            return voisin
        if case.y == 0:
            voisin.append(self.parent.map[case.x][case.y+1])
            voisin.append(self.parent.map[case.x-1][case.y])
            voisin.append(self.parent.map[case.x+1][case.y])
            return voisin
        if case.x == 25 and case.y == 25:
            voisin.append(self.parent.map[case.x-1])
            voisin.append(self.parent.map[case.y-1])
            return voisin
        if case.x == 25:
            voisin.append(self.parent.map[case.x][case.y+1])
            voisin.append(self.parent.map[case.x][case.y-1])
            voisin.append(self.parent.map[case.x-1][case.y])
            return voisin
        if case.y == 25:
            voisin.append(self.parent.map[case.x][case.y-1])
            voisin.append(self.parent.map[case.x-1][case.y])
            voisin.append(self.parent.map[case.x+1][case.y])
            return voisin

        voisin.append(self.parent.map[case.x][case.y-1])
        voisin.append(self.parent.map[case.x][case.y+1])
        voisin.append(self.parent.map[case.x-1][case.y])
        voisin.append(self.parent.map[case.x+1][case.y])
        return voisin
        
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

    def distance(self, a, b):
        """ Retourne la distance entre 2 points """
        (x1, y1) = a.x, a.y
        (x2, y2) = b.x, b.y
        return abs(x1 - x2) + abs(y1 - y2)
        

class Modele:
    def __init__(self, parent):
        self.parent = parent
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
