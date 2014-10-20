from tkinter import *
<<<<<<< HEAD

=======
from moduleObjets import *
from map import *
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0

#===============================================================================
# #A Faire
# -Changer les width
<<<<<<< HEAD
# -Changer les labels pour les images ainsi que les variables
=======
# -Changer les labels pour les images ainsi que les variables/Done
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0
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
<<<<<<< HEAD
        self.initJeu()#Pour la classe du Frame Jeu
       
    def initJeu(self): 
        
        self.cadreJeu=Frame(self.root)
=======
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
        
    def spawnUnit(self,event):
        vil = Villageois(0, event.x,event.y)
        self.parent.j.units.append(vil)

       
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
       
        
        self.canevas.grid(column=0,row=1,columnspan=3)
        
        self.canevas.bind("<Button-1>", self.spawnUnit)
        self.canevas.bind("<Button-3>", self.setArrive)
        
        self.cadreJeu.pack()
        self.cadreMenu.pack_forget()
        self.rafraichirCanevas()
        self.creerLigne()
        self.placeRessource()
        
    def initCadre(self):
        
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0
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
<<<<<<< HEAD
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
=======
        
    #def initLabelHaut(self):
        
    #Pour le cadre de Ressource
        
    
    ####Pour les images    
       
        
    def creerLigne(self):
        self.longeurLigne=20
        for i in range (self.parent.l):
            self.canevas.create_line(i*self.longeurLigne,0,i*self.longeurLigne,self.parent.h*self.longeurLigne,fill="white")
            
        for j in range (self.parent.h):
            self.canevas.create_line(0,j*self.longeurLigne,self.parent.l*self.longeurLigne,j*self.longeurLigne,fill="white")
        
    def placeRessource(self):
        for i in range(self.parent.h):
            for j in range(self.parent.l):
                #print(self.parent.m.mat[j][i].ressource)
                if self.parent.m.mat[i][j].ressource == FOOD_CHAR:#nourriture
                    #print("nourr")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="red",tags="food")
                elif self.parent.m.mat[i][j].ressource == WOOD_CHAR:#bois
                    #print("bois")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="brown",tags="wood")
                elif self.parent.m.mat[i][j].ressource == ROCK_CHAR:#pierre
                    #print("pierre")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="gray",tags="rock")
                #elif self.parent.m.mat[j][i].ressource == EMPTY_CHAR:#vide
                #    print("vide")
                #    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="grey",tags="food")
                elif self.parent.m.mat[i][j].ressource == ARTE_CHAR:#energie
                    #print("energie")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="blue",tags="artefact")

                elif self.parent.m.mat[i][j].ressource == ENERGY_CHAR:#energie
                    #print("energie")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="green2",tags="energie")
                
                elif self.parent.m.mat[i][j].ressource == GOLD_CHAR:#energie
                    #print("energie")
                    self.canevas.create_rectangle(j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2+9,i*self.longeurLigne+self.longeurLigne/2+9,fill="gold",tags="or")
                
                

            
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
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0
        labelPopulationMax.grid(column=1,row=0)
        
        #Pour le cadre Diplomatie/echange
        
<<<<<<< HEAD
        labelDiplomatie=Label(self.cadreDiplomatie,text="Diplomatie/Echange")
        labelDiplomatie.pack()
        
=======
    def diplomatieFenetre(self,event):
        self.toplevel = Toplevel()
        
        
    def diplomatieClic(self):
        labelDiplomatie=Label(self.cadreDiplomatie,text="Diplomatie/Echange",relief=SOLID,height=5,width=25)#anchor:E
        labelDiplomatie.pack()
        labelDiplomatie.bind("<Button-1>", self.diplomatieFenetre)
        
    def initLabelBas(self):
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0
        #Pour le cadre Option Unite
        
        labelOptionUnite=Label(self.cadreOptionUnite,text="Option d'unite")
        labelOptionUnite.pack()
        
        #Pour le cadre Info Selection
        
        labelInfoSelection=Label(self.cadreInfoSelection,text="Info sur Selection")
        labelInfoSelection.pack()
        
        #Pour le cadre Mini-Map
        
        labelMiniMap=Label(self.cadreMiniMap,text="Mini-Map")
<<<<<<< HEAD
        labelMiniMap.pack()
        
        
        self.cadreJeu.pack()
     
class Controleur(): 
    def __init__(self):
        self.vue=Vue(self)
        self.vue.root.mainloop()

        
if __name__ == "__main__":
    c = Controleur()
        
=======
        labelMiniMap.grid(column=0,row=0)
        
    #===========================================================================
    #def rafraichirTemps(self,temps):
    #    labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
    #    labelTemps.grid(column=0,row=1)
    #   
    #===========================================================================
      
    def setArrive(self,event):
        print("asdf")
          
    def rafraichirCanevas(self):
        self.canevas.delete("unit")
        for u in self.parent.j.units:
            self.canevas.create_rectangle(u.posX,u.posY,u.posX+5,u.posY+5,fill="grey", tags="unit")
        self.root.after(100, self.rafraichirCanevas)
        
"""if __name__ == "__main__":  
    from moduleObjets import *
    from map import *
    

    
    class Controleur(): 
        def __init__(self):
            self.l=45
            self.h=35
            liste=[Joueur(1), Joueur(2)]
            self.m=Map(self.l,self.h)
            #self.m.setSeed(10)
            self.m.placeRessourcesOverworld()
            self.m.placeRessourcesUnderworld()
            
            self.temps=0
            self.j = Joueur(0)
            self.vue=Vue(self)
            #self.vue.root.after(100, self.vue.rafraichirCanevas)
            self.vue.root.mainloop()
        
        #=======================================================================
        def tempsJeu(self):
             self.temps +=1
             self.vue.rafraichirTemps(self.temps)
             self.vue.root.after(1000,self.tempsJeu)
        #=======================================================================
            
    
            

    c = Controleur()"""
>>>>>>> b080f01bd50405f894e1b11f1c8618b21d3c42f0
