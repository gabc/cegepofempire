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
        self.actionsAFaire={}
        self.actions=[]
        
    def initPartie(self,listeNomsJoueurs):
        n=0
		#init tous les joueur avec leur unite, batiments, etc...
        for j in listeNomsJoueurs:
            pass

        
    def creerUnite(self, unit):
        x=unit.posX
        y=unit.posY
        self.parent.actions.append(["creerUnite",[unit.ownerID,x,y,unit.type]])

    def deplaceUnite(self, unit, arrive):
        self.parent.actions.append(["deplace",[unit[0], unit, arrive]])
        
    def prochaineAction(self,cadre):
        # print(self.actionsAFaire)
        if cadre in self.actionsAFaire:
            for action in self.actionsAFaire[cadre]:
                # print("Fait par, ", action[0])
                # print("Fait: ", action[1])
                if action[0] == "creerUnite":
                    self.parent.joueurs[action[1][0]].creerUnit("villageois",action[1][1], action[1][2])
                elif action[0] == "deplace":
                    self.parent.joueurs[action[1][0]].deplaceUnit(action[1][1],action[1][2])

            del self.actionsAFaire[cadre]
            
