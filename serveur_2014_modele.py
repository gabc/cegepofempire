import random
from helper import Helper
import math

   
class Unite(object):
    def __init__(self,parent,id,p,x=20,y=20):
        self.parent=parent
        self.id=id
        self.nom=parent.nom
        self.x=p.x+x
        self.y=p.y+y
   
    def bougerUnite(self):
        pass
                
    def prochaineAction(self):
        #print("DO SOMETING")
        pass
                        
                        
class Modele(object):
    id=0
    def nextId():
        Modele.id=Modele.id+1
        return Modele.id
    
    def __init__(self,parent):
        self.parent=parent
        self.unites=[]
        self.actionsAFaire=[]
        
    def initPartie(self,listeNomsJoueurs):
        n=0
		#init tous les joueur avec leur unite, batiments, etc...
        for j in listeNomsJoueurs:
            pass

        
    def creerUnite(self, unit):
        x=unit.posX
        y=unit.posY
        self.actionsAFaire.append(["creerUnite",self.parent.cadre,[unit.ownerID,x,y]])

        
    def prochaineAction(self,cadre):
        for action in self.actionsAFaire:
            print("Y'a un truc qui se passe", action)
            self.parent.serveur.faitAction(action)
