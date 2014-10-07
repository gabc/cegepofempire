from tkinter import *


#===============================================================================
# #A Faire
# -Changer les width
# -Changer les labels pour les images ainsi que les variables/Done
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
        self.initMenu()#Pour la classe du Frame Jeu
       
    #Pour liste de server   
    def initMenu(self):
        self.cadreMenu=Frame(self.root)
        self.cadreAttendre=Frame(self.cadreMenu)
        self.cadreButton=Frame(self.cadreMenu)
        self.listeJoueurs=Listbox(self.cadreAttendre)
        
        buttonCreer=Button(self.cadreButton,text="Creer",width=15,command=self.initJeu)
        buttonCreer.grid(column=1,row=0)
        buttonJoindre=Button(self.cadreButton,text="Joindre",width=15)
        buttonJoindre.grid(column=1,row=1)
        buttonOption=Button(self.cadreButton,text="Options",width=15)
        buttonOption.grid(column=1,row=2)
        
        self.listeJoueurs.grid(column=0,row=0)
        self.cadreAttendre.grid(column=0,row=0)
        self.cadreButton.grid(column=1,row=0)
        self.cadreMenu.pack()
        
    def canevasClick(self,event):
        self.canevas = event.widget
        print("clic at : x:"+str( event.x)+" y:"+str(event.y))
            
       
    def initJeu(self): 
        
        self.cadreJeu=Frame(self.root)
        
        #Call des cadre
        self.initCadre()
        #Variable bidon
        n="100"
        self.changeLabelBois(n)
        self.changeLabelEnergie(n)
        self.changeLabelNourriture(n)
        self.changeLabelPierre(n)
        self.changeLabelOr(n)
        self.changeLabelPopulation(n)
        self.diplomatieClic()
        self.imgLabelPopulation()
        self.initLabelBas()
        
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
        
        self.canevas.bind("<Button-1>", self.canevasClick)
        
        self.cadreJeu.pack()
        self.cadreMenu.pack_forget()

        
    def initCadre(self):
        
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
        
    #def initLabelHaut(self):
        
    #Pour le cadre de Ressource
        
    
    ####Pour les images    
        
    def imgLabel(self):
        print("")
        #labelNourritureImg=Label(self.cadreRessource,text="Nourriture: 200",relief=SOLID,width=15)
        #labelNourritureImg.grid(column=0,row=0)
        
        #labelBoisImg=Label(self.cadreRessource,text="Bois: 150",relief=SOLID,width=15)
        #labelBoisImg.grid(column=2,row=0)
        
        #labelPierreImg=Label(self.cadreRessource,text="Pierre: 100",relief=SOLID,width=15)
        #labelPierreImg.grid(column=0,row=1)
        
        #labelOrImg=Label(self.cadreRessource,text="Or: 150",relief=SOLID,width=15)
        #labelOrImg.grid(column=2,row=1)

        #labelEnergieImg=Label(self.cadreRessource,text="Energie: 0",relief=SOLID,width=15)
        #labelEnergieImg.grid(column=0,row=2,columnspan=2)
        
    def imgLabelPopulation(self):
        labelPopulation=Label(self.cadrePopulation,text="Population:",width=15)
        labelPopulation.grid(column=0,row=0)
    
    ###Pour les changements de labels
        
    def changeLabelNourriture(self, n):
        labelNourriture=Label(self.cadreRessource,text="Nourriture: "+n,relief=SOLID,width=15)
        labelNourriture.grid(column=0,row=0)#(column=1,row=0)
        
    def changeLabelBois(self, n):
        labelBois=Label(self.cadreRessource,text="Bois: "+n,relief=SOLID,width=15)
        labelBois.grid(column=1,row=0)#(column=3,row=0)
        
    def changeLabelPierre(self, n):
        labelPierre=Label(self.cadreRessource,text="Pierre: "+n,relief=SOLID,width=15)
        labelPierre.grid(column=0,row=1)#(column=1,row=1)
        
    def changeLabelOr(self, n):
        labelOr=Label(self.cadreRessource,text="Or: "+n,relief=SOLID,width=15)
        labelOr.grid(column=1,row=1)#(column=3,row=1)
        
    def changeLabelEnergie(self, n):
        labelEnergie=Label(self.cadreRessource,text="Energie: "+n,relief=SOLID,width=15)
        labelEnergie.grid(column=0,row=2,columnspan=2)#(column=1,row=2,columnspan=2)
        
        #Pour le cadre de population
    
    def changeLabelPopulation(self, n):#population et population max
        labelPopulationMax=Label(self.cadrePopulation,text=n+"/200")
        labelPopulationMax.grid(column=1,row=0)
        
        #Pour le cadre Diplomatie/echange
        
    def diplomatieFenetre(self,event):
        self.toplevel = Toplevel()
        
        
    def diplomatieClic(self):
        labelDiplomatie=Label(self.cadreDiplomatie,text="Diplomatie/Echange",relief=SOLID,height=5,width=25)#anchor:E
        labelDiplomatie.pack()
        labelDiplomatie.bind("<Button-1>", self.diplomatieFenetre)
        
    def initLabelBas(self):
        #Pour le cadre Option Unite
        
        labelOptionUnite=Label(self.cadreOptionUnite,text="Option d'unite")
        labelOptionUnite.pack()
        
        #Pour le cadre Info Selection
        
        labelInfoSelection=Label(self.cadreInfoSelection,text="Info sur Selection")
        labelInfoSelection.pack()
        
        #Pour le cadre Mini-Map
        
        labelMiniMap=Label(self.cadreMiniMap,text="Mini-Map")
        labelMiniMap.grid(column=0,row=0)
        
<<<<<<< HEAD
    #===========================================================================
    # def rafraichirTemps(self,temps):
    #     labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
    #     labelTemps.grid(column=0,row=1)
    #   
    #===========================================================================
      
if __name__ == "__main__":  
    class Controleur(): 
        def __init__(self):
            self.temps=0
            self.vue=Vue(self)
            #self.vue.root.after(1000, self.tempsJeu())
            self.vue.root.mainloop()
        
        #=======================================================================
        # def tempsJeu(self):
        #     self.temps +=1
        #     self.vue.rafraichirTemps(self.temps)
        #     self.vue.root.after(1000,self.tempsJeu)
        #=======================================================================
            
    
            

    c = Controleur()
=======
    def rafraichirTemps(self,temps):
        labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
        labelTemps.grid(column=0,row=1)
>>>>>>> 74bd3e71191db4ceb019e49e93f1b3b1ede8893e
        
