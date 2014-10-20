from tkinter import *
from tkinter.font import *
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import random
import math
from helper import *
from PIL import Image, ImageTk
from moduleObjets import *
from Map import *

class Buttonjm(Button):
    def __init__(self,parent,**kw):
        f=Font(size=7,slant="italic",weight="bold")
        kw["font"]=f
        kw["fg"]="orange"
        kw["bg"]="grey25"
        kw["relief"]="groove"
        Button.__init__(self,parent,**kw)
class Labeljm(Label):
    def __init__(self,parent,**kw):
        f=Font(size=7)
        kw["font"]=f
        kw["fg"]="orange"
        kw["bg"]="grey25"
        Label.__init__(self,parent,**kw)
  
class Vue(object):
    
    def __init__(self,parent):
        self.parent=parent
        self.modele=self.parent.modele
        self.root=Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.intercepteFermeture)
        self.cadreActif=0
        self.creeCadres()
        self.placeCadre(self.cadreConnection)

    def creeCadres(self):
        self.creeCadreConnection()
        self.creeCadreAttente()
        self.creeCadrePartie()
        
    def creeCadrePartie(self):
        self.cadrePartie=Frame(self.root)
        self.cadrePartie.rowconfigure(1,weight=1)
        self.cadrePartie.columnconfigure(0,weight=1)
        
        self.creeCadreMenuPartie()

    def creeCadreMenuPartie(self):
        self.cadreMenuPartie=Frame(self.cadrePartie,height=40,bg="grey25")
        self.cadreMenuPartie.grid_propagate(0)
        
        trouveL=Frame(self.cadreMenuPartie,height=10,bg="grey25")
        trouveL.grid(row=5,column=10,sticky=N)
        trouveB=Buttonjm(self.cadreMenuPartie,text="LOL",command=self.actionButton)
        trouveB.grid(row=10,column=10,sticky=N)
        
        
 
    def intercepteFermeture(self):
        print("Je me ferme")
        self.parent.jeQuitte()
        self.root.destroy()
        
    def afficheAttente(self):
        self.placeCadre(self.cadreAttente)
        
    def placeCadre(self,c):
        if self.cadreActif:
            self.cadreActif.pack_forget()
        self.cadreActif=c
        self.cadreActif.pack(expand=1,fill=BOTH)
 
    def creeCadreConnection(self):
        self.cadreConnection=Frame(self.root)
        cadreMenu=Frame(self.cadreConnection)

        Nom=Labeljm(cadreMenu,text="Nom: ")
        self.nomjoueur=Entry(cadreMenu)
        #print("un chiffre au hasard : " + str(random.randint(0,100)))
        self.nomjoueur.insert(0,"Player_" + str(random.randrange(100)))
        Nom.grid(column=0,row=0)
        self.nomjoueur.grid(column=1,row=0)
        

        lcree=Labeljm(cadreMenu,text="Pour créer un serveur à l'adresse inscrite  | ")
        lconnect=Labeljm(cadreMenu,text="Pour vous connecter à un serveur")
        lcree.grid(column=0,row=1)
        lconnect.grid(column=1,row=1)
        
        lip=Labeljm(cadreMenu,text=self.parent.monip)
        self.autreip=Entry(cadreMenu)
        self.autreip.insert(0,self.parent.monip)
        lip.grid(column=0,row=2)
        self.autreip.grid(column=1,row=2)
        
        creerB=Buttonjm(cadreMenu,text="Creer un serveur",command=self.creerServeur)
        connecterB=Buttonjm(cadreMenu,text="Connecter a un serveur",command=self.connecterServeur)
        creerB.grid(column=0,row=3)
        connecterB.grid(column=1,row=3)

        #self.galax=PhotoImage(file="galaxie.gif")
        #galaxl=Labeljm(self.cadreConnection,image=self.galax)
        #galaxl.pack()
        cadreMenu.pack()
        
    def creeCadreAttente(self):
        self.cadreAttente=Frame(self.root)
        cadreMenu=Frame(self.cadreAttente)
        self.listeJoueurs=Listbox(cadreMenu)
        self.demarreB=Buttonjm(cadreMenu,text="Demarre partie",state=DISABLED,command=self.parent.demarrePartie)
        self.demarreB.grid(column=0,row=1)
        self.listeJoueurs.grid(column=0,row=0)
        cadreMenu.pack(side=LEFT)
        #self.galax2=PhotoImage(file="galaxie.gif")
        #galax=Labeljm(self.cadreAttente,image=self.galax2)
        #galax.pack(side=RIGHT)
        
    def afficheListeJoueurs(self,liste):
        self.listeJoueurs.delete(0,END)
        for i in liste:
            self.listeJoueurs.insert(END,i)
        
    def initPartie(self,modele):
        self.partie=modele
        self.moi=modele.parent.nom
        
        self.cadreMenuPartie.grid(column=0,row=0,sticky=W+E)
       
        
        self.initJeu()
        
        self.placeCadre(self.cadrePartie)
    
    
    def initJeu(self):
        self.cadrePartie=Frame(self.root)
        
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
        self.canevasMilieu=Canvas(self.cadrePartie,width=800,height=600,bg="#006633")
       
        
        self.canevasMilieu.grid(column=0,row=1,columnspan=3)
        
        self.canevasMilieu.bind("<Button-1>", self.spawnUnit)
        self.canevasMilieu.bind("<Button-3>", self.setArrive)
        
        self.cadrePartie.pack()
        #self.cadreMenu.pack_forget()
        self.rafraichirCanevas()
        self.creerLigne()
        self.placeRessource()
        
    
    def spawnUnit(self,event):
        vil = Villageois(0, event.x,event.y)
        self.modele.creerUnite(vil)
        # self.parent.j.units.append(vil)
    
        
    def initCadre(self):
        
        #Haut
        self.cadreRessource=Frame(self.cadrePartie)
        self.cadreRessource.grid(column=0,row=0)
        
        self.cadrePopulation=Frame(self.cadrePartie)
        self.cadrePopulation.grid(column=1,row=0)
        
        self.cadreDiplomatie=Frame(self.cadrePartie)
        self.cadreDiplomatie.grid(column=2,row=0)
        #Bas
        self.cadreOptionUnite=Frame(self.cadrePartie)
        self.cadreOptionUnite.grid(column=0,row=2)
        
        self.cadreInfoSelection=Frame(self.cadrePartie)
        self.cadreInfoSelection.grid(column=1,row=2)
        
        self.cadreMiniMap=Frame(self.cadrePartie)
        self.cadreMiniMap.grid(column=2,row=2)
        
    #def initLabelHaut(self):
        
    #Pour le cadre de Ressource
        
    
    ####Pour les images    
       
    
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
    
        
    def afficheArtefact(self):
        #loop dans tou les unite, etc
		#for i in self.partie.civs.keys():
       
	   #afficher les changement
        self.afficheSelection()
        
    def afficheSelection(self):
        pass
	
    
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
        self.canevasMilieu.delete("unit")
        for j in self.parent.joueurs.values():
            for u in j.units:
                self.canevasMilieu.create_rectangle(u.posX,u.posY,u.posX+5,u.posY+5,fill="grey", tags="unit")
        self.root.after(100, self.rafraichirCanevas)
    
    
    def creerLigne(self):
        self.longeurLigne=20
        for i in range (self.parent.l):
            self.canevasMilieu.create_line(i*self.longeurLigne,0,i*self.longeurLigne,self.parent.h*self.longeurLigne,fill="white")
            
        for j in range (self.parent.h):
            self.canevasMilieu.create_line(0,j*self.longeurLigne,self.parent.l*self.longeurLigne,j*self.longeurLigne,fill="white")
        
    def placeRessource(self):
        for i in range(self.parent.l):
            for j in range(self.parent.h):
                print(self.parent.m.mat[j][i].ressource)
                if self.parent.m.mat[j][i].ressource == FOOD_CHAR:#nourriture
                    print("nourr")
                    self.canevasMilieu.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="red",tags="food")
                elif self.parent.m.mat[j][i].ressource == MATE_CHAR:#bois
                    print("bois")
                    self.canevasMilieu.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="brown",tags="food")
                elif self.parent.m.mat[j][i].ressource == RARE_CHAR:#or
                    print("or")
                    self.canevasMilieu.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="yellow",tags="food")
                #elif self.parent.m.mat[j][i].ressource == EMPTY_CHAR:#vide
                #    print("vide")
                #    self.canevas.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="grey",tags="food")
                elif self.parent.m.mat[j][i].ressource == ARTE_CHAR:#energie
                    print("energie")
                    self.canevasMilieu.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="blue",tags="food")
                
                

            
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
    
    
    	
    def creerServeur(self):
        nom=self.nomjoueur.get()
        leip=self.parent.monip
        if nom:
            pid=self.parent.creerServeur()
            if pid:
                self.demarreB.config(state=NORMAL)
                self.root.after(500,self.inscritClient)
        else:
            mb.showerror(title="Besoin d'un nom",message="Vous devez inscrire un nom pour vous connecter.")
            
                
    def inscritClient(self):
        nom=self.nomjoueur.get()
        leip=self.parent.monip
        self.parent.inscritClient(nom,leip)
        
    def connecterServeur(self):
        nom=self.nomjoueur.get()
        leip=self.autreip.get()
        if nom:
            self.parent.inscritClient(nom,leip)
    
    def actionButton(self):
        pass
