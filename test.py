#!/usr/bin/env python3
from tkinter import *


class Vue:
    def __init__(self, parent):
        self.parent = parent
        
        self.root = Tk()

        self.can = Canvas(self.root, height = 500, width = 500, bg = "white")
        self.can.bind("<Button-1>", self.setDepart)
        self.can.bind("<Button-2>", self.setArrivee)
        self.can.bind("<Button-3>", self.addWayPoint)
        
        self.panmenu = PanedWindow(orient=VERTICAL)
        self.panmenu.add(Button(self.root, text='Quitter',command=self.quitter))
        self.panmenu.add(Button(self.root, text='Affiche', command=self.affiche))
        self.panmenu.add(Button(self.root, text='Deplace', command=self.deplacement))
        self.panmenu.pack()

    def affiche(self):
        print(self.parent.modele.joueur.depart.x)
        print('case: ', int(self.parent.modele.joueur.depart.x / 20))

    def quitter(self):
        self.root.destroy()
        exit(0)

    def addWayPoint(self, event):
        print('Ok: ', event.x, event.y)
        self.parent.modele.joueur.chemin.append(Case(event.x, event.y))

    def deplacement(self):
        self.parent.modele.joueur.deplacement()
        self.root.after(100,self.deplacement)

    def setDepart(self, event):
        self.parent.modele.joueur.depart = Case(event.x, event.y)

    def setArrivee(self, event):
        self.parent.modele.joueur.arrivee = Case(event.x, event.y)

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
        self.can.create_text(self.parent.modele.joueur.depart.x, self.parent.modele.joueur.depart.y, text= "@", tags="piece")
        self.can.create_text(self.parent.modele.joueur.arrivee.x, self.parent.modele.joueur.arrivee.y, text= "X", tags="but")
    def jouer(self):
        self.dessinerGrille()
        self.updateBoard()
        self.can.pack()
        self.root.after(200,self.jouer)


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Pion:
    def __init__(self, parent, depart):
        self.depart = depart
        self.arrivee = Case(0,0)
        self.parent = parent
        self.vitesse = 20
        self.chemin = []
        # self.map = [500][500]

    def deplacement(self):
        self.chemin.append(self.arrivee)
        self.arrivee = self.chemin[0]
        self.go()

    def go(self):
        if self.heuristic(self.depart, self.arrivee) == 0:
            # print(self.chemin)
            if len(self.chemin) > 1:
                self.arrivee = self.chemin[0]
                del self.chemin[0]
            else:
                print("DONE")
                return

        if self.depart.x < self.arrivee.x:
            self.depart.x += 1
        if self.depart.y < self.arrivee.y:
            self.depart.y += 1
        if self.depart.x > self.arrivee.x:
            self.depart.x -= 1
        if self.depart.y > self.arrivee.y:
            self.depart.y -= 1

    def heuristic(self, a, b):
        """ Retourne la distance entre 2 points """
        (x1, y1) = a.x, a.y
        (x2, y2) = b.x, b.y
        return abs(x1 - x2) + abs(y1 - y2)
        

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.joueur = Pion(self, Case(0,0))

class Controleur:
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        self.vue.jouer()
        self.vue.root.mainloop()

jeu = Controleur()
