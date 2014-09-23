from tkinter import *


#===============================================================================
# #A Faire
# -Changer les width
# -Changer les labels pour les images ainsi que les variables
# -Accents sur lettres
# -Diplomatie
# -Option Main Menu
# -Dessin hard code des ressources
# -Verifier Main Menu
# -Reorganiser le code
#===============================================================================

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root=Tk()
        self.initJeu()#Pour la classe du Frame Jeu
       
    def initJeu(self): 
        
        self.cadreJeu=Frame(self.root)
        #Haut
        self.cadreRessource=Frame(self.cadreJeu)
        self.cadreRessource.grid(column=0,row=0)
        
        self.cadrePopulation=Frame(self.cadreJeu)
        self.cadrePopulation.grid(column=1,row=0)
        
        self.cadreDiplomatie=Frame(self.cadreJeu)
        self.cadreDiplomatie.grid(column=2,row=0)
        #Bas
        self.cadreOptionUnite=Frame(self.cadreJeu)
        self.cadreOptionUnite.grid(column=0,row=2)
        
        self.cadreInfoSelection=Frame(self.cadreJeu)
        self.cadreInfoSelection.grid(column=1,row=2)
        
        self.cadreMiniMap=Frame(self.cadreJeu)
        self.cadreMiniMap.grid(column=2,row=2)
        #Milieu
        self.canevas=Canvas(self.cadreJeu,width=800,height=600,bg="#006633")
        #Pierre
        self.canevas.create_rectangle(50,50,75,75,fill="grey")
        self.canevas.create_rectangle(50,100,75,75,fill="grey")
        #Or
        self.canevas.create_oval(500,75,550,125,fill="yellow")
        self.canevas.create_oval(525,100,550,125,fill="yellow")
        #Arbre(methode)
        self.canevas.create_polygon(50,200,75,150,100,200,fill="green")
        
        self.canevas.grid(column=0,row=1,columnspan=3)
        
        #Pour le cadre de Ressource
        
        labelNourriture=Label(self.cadreRessource,text="Nourriture: 200",relief=SOLID,width=15)
        labelNourriture.grid(column=0,row=0)
        
        labelBois=Label(self.cadreRessource,text="Bois: 150",relief=SOLID,width=15)
        labelBois.grid(column=1,row=0)
        
        labelPierre=Label(self.cadreRessource,text="Pierre: 100",relief=SOLID,width=15)
        labelPierre.grid(column=0,row=1)
        
        labelOr=Label(self.cadreRessource,text="Or: 150",relief=SOLID,width=15)
        labelOr.grid(column=1,row=1)
        
        labelEnergie=Label(self.cadreRessource,text="Energie: 0",relief=SOLID,width=15)
        labelEnergie.grid(column=0,row=2,columnspan=2)
        
        #Pour le cadre de population
        
        labelPopulation=Label(self.cadrePopulation,text="Population:",width=15)
        labelPopulation.grid(column=0,row=0)
        
        labelPopulationMax=Label(self.cadrePopulation,text="0/55")
        labelPopulationMax.grid(column=1,row=0)
        
        #Pour le cadre Diplomatie/echange
        
        labelDiplomatie=Label(self.cadreDiplomatie,text="Diplomatie/Echange")
        labelDiplomatie.pack()
        
        #Pour le cadre Option Unite
        
        labelOptionUnite=Label(self.cadreOptionUnite,text="Option d'unite")
        labelOptionUnite.pack()
        
        #Pour le cadre Info Selection
        
        labelInfoSelection=Label(self.cadreInfoSelection,text="Info sur Selection")
        labelInfoSelection.pack()
        
        #Pour le cadre Mini-Map
        
        labelMiniMap=Label(self.cadreMiniMap,text="Mini-Map")
        labelMiniMap.pack()
        
        
        self.cadreJeu.pack()
     
class Controleur(): 
    def __init__(self):
        self.vue=Vue(self)
        self.vue.root.mainloop()

        
if __name__ == "__main__":
    c = Controleur()
        
