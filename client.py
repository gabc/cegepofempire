#!/usr/bin/env python3
import Pyro4
import random
from subprocess import Popen
import os
import socket
import platform
import atexit

from deplacement import *
from modele_client import *
from vue import *
from helper import Helper


class Controleur(object):
    def __init__(self):
        self.l=100
        self.h=100
        self.nom=""
        self.cadre=0
        self.actions=[]
        self.serveurLocal=0
        self.serveur=0
        self.myPlayer = None
        self.attend = False
        
        self.m=Map(self.l,self.h)
		
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.monip=s.getsockname()[0]
        s.close()
        
        self.deplaceur = Deplacement(self, self.m.mat)
        self.modele=Modele(self)
        self.vue=Vue(self)
        
    def creerServeur(self):
        cwd=os.getcwd()
        #print("AVANT SERVEUR")
        if platform.system() == "Linux":
            pythonExe = "/usr/bin/python3"
        else:
            #IL EST IMPORTANT DE CHECKER LA VERSION DE PYTHON!!!
            #pythonExe = "C:\\Python33\\Python.exe"
            pythonExe = "C:\\Python34\\Python.exe"
        pid = Popen([pythonExe, "serveur.py"]).pid
        
        print("APRES SERVEUR")
        self.serveurLocal=1
        return pid
        
    def jeQuitte(self):
        if self.serveur:
            self.serveur.jeQuitte(self.nom)
        
    def stopServeur(self):
        rep=self.serveur.quitter()   
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
            self.modele.rdseed = rep[2]
            #mb.showerror(title="Seed!",message="Got seed from server.")
            #random.seed(frozenset(self.modele.rdseed))
            #self.m.setSeed(frozenset(self.modele.rdseed))
            self.m.setSeed(self.modele.rdseed)
            self.m.placeRessourcesOverworld()
            self.m.placeRessourcesUnderworld()

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
            rep=self.serveur.faitAction([self.nom,0,[]])
            if rep[0]: #demarre partie
                self.modele.initPartie(rep[2][1][0][1])
                self.modele.joueurs=self.m.placeJoueurs(self.modele.joueurs, rep[2][1][0][1])
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
                #print("executer action a faire")
            self.modele.prochaineAction(self.cadre)
            self.vue.rafraichir()
            if self.actions: ##actions a envoyer au server
                #print("Envoi d'une action au server")
                rep=self.serveur.faitAction([self.nom,self.cadre,self.actions])
            else:
                rep=self.serveur.faitAction([self.nom,self.cadre,0])
                #print("Pas d'action au server")
            # print(self.actions)
            self.actions=[]
            if rep[0]:
                for i in rep[2]:
                    if i not in self.modele.actionsAFaire.keys():
                        self.modele.actionsAFaire[i]=[]
                    for k in rep[2][i]:
                        self.modele.actionsAFaire[i].append(k)
            if rep[1]=="attend":
                self.cadre=self.cadre-1  
                #print("Received attend: ", self.cadre)
            #print("Cadre",self.cadre)     
            self.vue.root.after(50,self.timerJeu)
        else:
            print("Aucun serveur connu")
        
if __name__ == '__main__':
    c=Controleur()
    c.vue.root.mainloop()
    #print("FIN")
