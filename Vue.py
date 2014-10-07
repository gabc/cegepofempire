from tkinter import *
from moduleObjets import *

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
       
        
    def creerLigne(self):
        self.longeurLigne=20
        for i in range (self.parent.l):
            self.canevas.create_line(i*self.longeurLigne,0,i*self.longeurLigne,self.parent.h*self.longeurLigne,fill="white")
            
        for j in range (self.parent.h):
            self.canevas.create_line(0,j*self.longeurLigne,self.parent.l*self.longeurLigne,j*self.longeurLigne,fill="white")
        
    def placeRessource(self):
        for i in range(self.parent.l):
            for j in range(self.parent.h):
                print(self.parent.m.mat[j][i].ressource)
                if self.parent.m.mat[j][i].ressource == FOOD_CHAR:#nourriture
                    print("nourr")
                    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="red",tags="food")
                elif self.parent.m.mat[j][i].ressource == MATE_CHAR:#bois
                    print("bois")
                    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="brown",tags="food")
                elif self.parent.m.mat[j][i].ressource == RARE_CHAR:#or
                    print("or")
                    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="yellow",tags="food")
                #elif self.parent.m.mat[j][i].ressource == EMPTY_CHAR:#vide
                #    print("vide")
                #    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="grey",tags="food")
                elif self.parent.m.mat[j][i].ressource == ARTE_CHAR:#energie
                    print("energie")
                    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="blue",tags="food")
                
                

            
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
        
if __name__ == "__main__":  
    from moduleObjets import *
    from map import *
    

    
    class Controleur(): 
        def __init__(self):
            self.l=40
            self.h=30
            liste=[Joueur(1,"a"), Joueur(2,"b")]
            self.m=Map(self.l,self.h)
            self.m.setSeed(10)
            self.m.placeRessourcesOverworld()
            self.m.placeRessourcesUnderworld()
            
            self.temps=0
            self.j = Joueur(0, "test")
            self.vue=Vue(self)
            #self.vue.root.after(100, self.vue.rafraichirCanevas)
            self.vue.root.mainloop()
        
        #=======================================================================
        def tempsJeu(self):
             self.temps +=1
             self.vue.rafraichirTemps(self.temps)
             self.vue.root.after(1000,self.tempsJeu)
        #=======================================================================
            
    
            

    c = Controleur()