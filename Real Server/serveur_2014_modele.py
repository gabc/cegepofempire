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
        
    def initPartie(self,listeNomsJoueurs):
        n=0
		#init tous les joueur avec leur unite, batiments, etc...
        for j in listeNomsJoueurs:
            pass

        
    def creerUnite(self,):
        x=random.randrange(self.parent.largeur_espace)
        y=random.randrange(self.parent.hauteur_espace)
        random.seed(self.rdseed)
        self.actions.append(["creerUnite",[self.nom,x,y]])
        self.creerEtoiles()
        
    def prochaineAction(self,cadre):
        if cadre in self.actionsAFaire:
            for i in self.actionsAFaire[cadre]:
                #print("ACTIONENCOURS",i)
                self.civs[i[0]].actions[i[1]](i[2])
            del self.actionsAFaire[cadre]
            #print("NO1",cadre)
                
        for i in self.unites:
            self.unites[i].prochaineAction()