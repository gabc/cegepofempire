# -*- coding: ISO-8859-1 -*-
from tkinter import *
from tkinter.font import *
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import random
import math
from helper import *
from PIL import Image, ImageTk

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
        self.nomjoueur.insert(0,"Player_"+str(random.randrange(100)))
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
       
        
        self.placeCadre(self.cadrePartie)
        
    def afficheArtefact(self):
        #loop dans tou les unité, etc
		#for i in self.partie.civs.keys():
       
	   #afficher les changement
        self.afficheSelection()
        
    def afficheSelection(self):
        pass
		
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