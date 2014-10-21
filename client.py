#!/usr/bin/env python3
import Pyro4
import random
from subprocess import Popen
import os
import socket
import platform
import atexit

from deplacement import *
from modele_serveur import *
from vue import *
from helper import Helper


class Controleur(object):
    def __init__(self):
        self.l=40
        self.h=30
        #liste=[Joueur(1,"a"), Joueur(2,"b")]
        
        self.m=Map(self.l,self.h)
        self.m.setSeed(10)
        self.m.placeRessourcesOverworld()
        self.m.placeRessourcesUnderworld()

        self.deplaceur = Deplacement(self, self.m.mat)
        
        self.temps=0
        self.joueurs = {} # = Joueur(0, "test")
        self.nom=""
        self.cadre=0
        self.actions=[]
        self.serveurLocal=0
        self.serveur=0
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.monip=s.getsockname()[0]
        s.close()
        
        self.modele=Modele(self)
        self.vue=Vue(self)
        # self.timerJeu()
        
    def creerServeur(self):
        cwd=os.getcwd()
        print("AVANT SERVEUR")
        if platform.system() == "Linux":
            pythonExe = "/usr/bin/python3"
        else:
            pythonExe = "C:\\Python33\\Python.exe"
        pid = Popen([pythonExe, "serveur.py"]).pid
        
        print("APRES SERVEUR")
        self.serveurLocal=1
        return pid
        
    def jeQuitte(self):
        if self.serveur:
            self.serveur.jeQuitte(self.nom)
        
    def stopServeur(self):
        rep=self.serveur.quitter()
        # print(rep)    
        self.serveur=0
        input("FERMER")
        
    def inscritClient(self,nom,leip):
        ad="PYRO:controleurServeur@"+leip+":47099"
        self.serveur=Pyro4.core.Proxy(ad)
        Pyro4.socketutil.setReuseAddr(self.serveur)
        
        rep=self.serveur.inscritClient(nom)
        if rep[0]:
            self.nom=nom
            self.rnd=random.Random()
            self.modele.rdseed=10 #rep[2]
            mb.showerror(title="Seed!",message="Got seed from server.")
            random.seed(self.modele.rdseed)#frozenset(self.modele.rdseed))
            # self.m.setSeed(frozenset(self.modele.rdseed))
            # self.m.placeRessourcesOverworld()
            # self.m.placeRessourcesUnderworld()

            self.vue.afficheAttente()
            self.timerAttend()
        else:
            mb.showerror(title="Erreur!",message=rep[1])
        
    def demarrePartie(self):
        rep=self.serveur.demarrePartie()
        # print("rep from server: ", rep)
                
    # ******  SECTION d'appels automatique        
    def timerAttend(self):
        if self.serveur:
            rep=self.serveur.faitAction([self.nom,self.cadre,[]])
            if rep[0]: #demarre partie
                self.modele.initPartie(rep[2][1][0][1])
                self.vue.initPartie(self.modele)
                self.vue.root.after(10,self.timerJeu)
            elif rep[0]==0: #waiting room
                self.vue.afficheListeJoueurs(rep[2])
                self.vue.root.after(10,self.timerAttend)
        else:
            print("Aucun serveur attache")
               
    def timerJeu(self):
        if self.serveur:
            self.cadre=self.cadre+1
            self.modele.prochaineAction(self.cadre)
            self.vue.afficheArtefact()
            if self.actions:
                rep=self.serveur.faitAction([self.nom,self.cadre,self.actions])
            else:
                rep=self.serveur.faitAction([self.nom,self.cadre,0])
            # print(self.actions)
            self.actions=[]
            if rep[0]:
                for i in rep[2]:
                    if i not in self.modele.actionsAFaire.keys():
                        self.modele.actionsAFaire[i]=[]
                    for k in rep[2][i]:
                        self.modele.actionsAFaire[i].append(k)
                # print("ACTIONS",self.cadre,"\nREP",rep,"\nACTIONAFAIRE",self.modele.actionsAFaire)  
            if rep[1]=="attend":
                self.cadre=self.cadre-1  
            #print("Cadre",self.cadre)     
            self.vue.root.after(50,self.timerJeu)
        else:
            print("Aucun serveur connu")
        
if __name__ == '__main__':
    c=Controleur()
    c.vue.root.mainloop()
    print("FIN")
