# -*- encoding: ISO-8859-1 -*-
import Pyro4
import os
from threading import Timer
import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
monip=s.getsockname()[0]
#s.close()

daemon = Pyro4.core.Daemon(host=monip,port=47099) 
#Pyro4.socketutil.setReuseAddr(daemon)

class Client(object):
    def __init__(self,nom):
        self.nom=nom
        self.cadreCourant=0
        self.cadreEnAttenteMax=0
        self.actionsEnAttentes={}
        
class ModeleService(object):
    def __init__(self,parent,rdseed):
        self.parent=parent
        self.etatJeu=0
        self.rdseed=rdseed
        self.cadreCourant=0
        self.cadreFutur=5
        self.clients={}
        self.cadreDelta={}
        
    def creeClient(self,nom):
        if self.etatJeu==0:
            if nom in self.clients.keys():
                return [0,"Erreur de nom, recommencer avec un autre nom"]
            c=Client(nom)
            self.cadreDelta[nom]=0
            self.clients[nom]=c
            return [1,"Bienvenue",self.rdseed]
        else:
            return [0,"Partie deja en cours"]
    
    
    def demarrePartie(self):
        if self.etatJeu==0:
            self.etatJeu=1
            for i in self.clients:
                self.clients[i].actionsEnAttentes[1]=[["demarrePartie",list(self.clients.keys())]]
            return 1
        else:
            return 0
    
    def faitAction(self,p):
        nom=p[0]
        cadre=p[1]
        if cadre>self.cadreCourant:
            self.cadreCourant=cadre
        if p[2]:
            cadreVise=self.cadreCourant+self.cadreFutur
            for i in self.clients:
                self.clients[i].cadreEnAttentesMax=cadreVise
                if cadreVise in self.clients[i].actionsEnAttentes.keys():
                    #erreur de multiples entrees
                    #self.clients[i].actionsEnAttentes[cadreVise].append(p[2])
                    for j in p[2]:
                        self.clients[i].actionsEnAttentes[cadreVise].append(j)
                        
                else:
                    self.clients[i].actionsEnAttentes[cadreVise]=p[2]
                print("ACTION ",self.clients[i].nom,self.clients[i].actionsEnAttentes)

        rep=[]
        
        self.cadreDelta[nom]=cadre
        mini=min(list(self.cadreDelta.values()))
        if cadre-3>mini:
            message="attend"
        else:
            message=""
            
        if self.clients[nom].actionsEnAttentes:
            print(nom,self.clients[nom].actionsEnAttentes)
            if cadre<min(self.clients[nom].actionsEnAttentes.keys()):
                rep= self.clients[nom].actionsEnAttentes
                self.clients[nom].actionsEnAttentes={}
                rep= [1,message,rep]
            else:
                print("AYOYE") # ici on a un probleme car une action doit se produire dans le passé
        else:
            rep= [0,message,list(self.clients.keys())]
        return rep
                
class ControleurServeur(object):
    def __init__(self):
        rand=os.urandom(8)
        self.modele=ModeleService(self,rand)
        
    def inscritClient(self,nom):
        rep=self.modele.creeClient(nom)
        return rep
    
    def demarrePartie(self):
        rep=self.modele.demarrePartie()
        return rep
    
    def faitAction(self,p):
        rep=self.modele.faitAction(p)
        return rep
    
    def quitter(self):
        t=Timer(1,self.fermer)
        t.start()
        return "ferme"
    
    def jeQuitte(self,nom):
        del self.modele.clients[nom]
        del self.modele.cadreDelta[nom]
        if not self.modele.clients:
            self.quitter()
        return 1
    
    def fermer(self):
        daemon.shutdown()
    


controleurServeur=ControleurServeur()
daemon.register(controleurServeur, "controleurServeur")  
 
print("Serveur Pyro actif sous le nom \'controleurServeur\'")
daemon.requestLoop()
