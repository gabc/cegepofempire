# -*- coding: ISO-8859-1 -*-
#été
import Pyro4
import random
from subprocess import Popen
import os
import socket
import platform

from serveur_2014_modele import *
from serveur_2014_vue import *
from helper import Helper

print(platform.platform())
print(platform.system())
print(platform.python_version_tuple())
print(os.getcwd())
print(os.environ)


class Controleur(object):
    def __init__(self):
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

    def creerServeur(self):
        if platform.python_version_tuple()[0]=='3':
            p="python3"
        else:
            p="python"
        p="python"
        cwd=os.getcwd()
        testJMServeur=cwd+"\\"+"serveur_2014_serveur.py"
        print("AVANT SERVEUR")
        pid = Popen(["C:\\Python33\\Python.exe", "serveur_2014_serveur.py"]).pid
        
        print("APRES SERVEUR")
        self.serveurLocal=1
        return pid
        
    def jeQuitte(self):
        if self.serveur:
            self.serveur.jeQuitte(self.nom)
        
    def stopServeur(self):
        rep=self.serveur.quitter()
        print(rep)    
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
            self.modele.rdseed=rep[2]
            mb.showerror(title="Seed!",message="Got seed from server.")
            random.seed(self.modele.rdseed)
            self.vue.afficheAttente()
            self.timerAttend()
        else:
            mb.showerror(title="Erreur!",message=rep[1])
        
    def demarrePartie(self):
        rep=self.serveur.demarrePartie()
        print("rep from server: ", rep)
    
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
            self.actions=[]
            if rep[0]:
                for i in rep[2]:
                    if i not in self.modele.actionsAFaire.keys():
                        self.modele.actionsAFaire[i]=[]
                    for k in rep[2][i]:
                        self.modele.actionsAFaire[i].append(k)
                #print("ACTIONS",self.cadre,"\nREP",rep,"\nACTIONAFAIRE",self.modele.actionsAFaire)  
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
