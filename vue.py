from tkinter import *
from tkinter.font import *
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import random
import math
from helper import *
from PIL import Image, ImageTk 
# from modele_client import *
from Map import *

class Buttonjm(Button):
    def __init__(self, parent, **kw):
        f = Font(size=7, slant="italic", weight="bold")
        kw["font"] = f
        kw["fg"] = "orange"
        kw["bg"] = "grey25"
        kw["relief"] = "groove"
        Button.__init__(self, parent, **kw)
class Labeljm(Label):
    def __init__(self, parent, **kw):
        f = Font(size=7)
        kw["font"] = f
        kw["fg"] = "orange"
        kw["bg"] = "grey25"
        Label.__init__(self, parent, **kw)

class Vue(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.modele = self.parent.modele
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.intercepteFermeture)
        self.cadreActif = 0
        self.creeCadres()
        self.placeCadre(self.cadreConnection)
        self.currentX = 0
        self.currentY = 0
        self.actionSelectionnee=0#1=SpawnUnit##
        
        
        self.food_ress = Image.open("./img/food_ress.png")
        self.photo_food_ress = ImageTk.PhotoImage(self.food_ress)
        self.wood_ress = Image.open("./img/wood_ress.png")
        self.photo_wood_ress = ImageTk.PhotoImage(self.wood_ress)
        self.gold_ress = Image.open("./img/gold_ress.png")
        self.photo_gold_ress = ImageTk.PhotoImage(self.gold_ress)
        self.energy_ress = Image.open("./img/energy_ress.png")
        self.photo_energy_ress = ImageTk.PhotoImage(self.energy_ress)
        self.art_ress = Image.open("./img/art_ress.png")
        self.photo_art_ress = ImageTk.PhotoImage(self.art_ress)
        self.rock_ress = Image.open("./img/rock_ress.png")
        self.photo_rock_ress = ImageTk.PhotoImage(self.rock_ress)
        
        self.tower_build = Image.open("./img/tower_build.png")##
        self.photo_tower_build = ImageTk.PhotoImage(self.tower_build)##

    def creeCadres(self):
        self.creeCadreConnection()
        self.creeCadreAttente()
        self.creeCadrePartie()
        
    def creeCadrePartie(self):
        self.cadrePartie = Frame(self.root)
        self.cadrePartie.rowconfigure(1, weight=1)
        self.cadrePartie.columnconfigure(0, weight=1)
        
        self.creeCadreMenuPartie()

    def creeCadreMenuPartie(self):
        self.cadreMenuPartie = Frame(self.cadrePartie, height=40, bg="grey25")
        self.cadreMenuPartie.grid_propagate(0)
        
        trouveL = Frame(self.cadreMenuPartie, height=10, bg="grey25")
        trouveL.grid(row=5, column=10, sticky=N)
        trouveB = Buttonjm(self.cadreMenuPartie, text="LOL", command=self.actionButton)
        trouveB.grid(row=10, column=10, sticky=N)
        
        

    def intercepteFermeture(self):
        print("Je me ferme")
        self.parent.jeQuitte()
        self.root.destroy()
        
    def afficheAttente(self):
        self.placeCadre(self.cadreAttente)
        
    def placeCadre(self, c):
        if self.cadreActif:
            self.cadreActif.pack_forget()
        self.cadreActif = c
        self.cadreActif.pack(expand=1, fill=BOTH)

    def creeCadreConnection(self):
        self.cadreConnection = Frame(self.root)
        cadreMenu = Frame(self.cadreConnection)

        Nom = Labeljm(cadreMenu, text="Nom: ")
        self.nomjoueur = Entry(cadreMenu)
        # print("un chiffre au hasard : " + str(random.randint(0,100)))
        self.nomjoueur.insert(0, "Player_" + str(random.randrange(100)))
        Nom.grid(column=0, row=0)
        self.nomjoueur.grid(column=1, row=0)
        

        lcree = Labeljm(cadreMenu, text="Pour créer un serveur à l'adresse inscrite  | ")
        lconnect = Labeljm(cadreMenu, text="Pour vous connecter à un serveur")
        lcree.grid(column=0, row=1)
        lconnect.grid(column=1, row=1)
        
        lip = Labeljm(cadreMenu, text=self.parent.monip)
        self.autreip = Entry(cadreMenu)
        self.autreip.insert(0, self.parent.monip)
        lip.grid(column=0, row=2)
        self.autreip.grid(column=1, row=2)
        
        creerB = Buttonjm(cadreMenu, text="Creer un serveur", command=self.creerServeur)
        connecterB = Buttonjm(cadreMenu, text="Connecter a un serveur", command=self.connecterServeur)
        creerB.grid(column=0, row=3)
        connecterB.grid(column=1, row=3)

        # self.galax=PhotoImage(file="galaxie.gif")
        # galaxl=Labeljm(self.cadreConnection,image=self.galax)
        # galaxl.pack()
        cadreMenu.pack()
        
    def creeCadreAttente(self):
        self.cadreAttente = Frame(self.root)
        cadreMenu = Frame(self.cadreAttente)
        self.listeJoueurs = Listbox(cadreMenu)
        self.demarreB = Buttonjm(cadreMenu, text="Demarre partie", state=DISABLED, command=self.parent.demarrePartie)
        self.demarreB.grid(column=0, row=1)
        self.listeJoueurs.grid(column=0, row=0)
        cadreMenu.pack(side=LEFT)
        # self.galax2=PhotoImage(file="galaxie.gif")
        # galax=Labeljm(self.cadreAttente,image=self.galax2)
        # galax.pack(side=RIGHT)
        
    def afficheListeJoueurs(self, liste):
        self.listeJoueurs.delete(0, END)
        for i in liste:
            self.listeJoueurs.insert(END, i)
        
    def initPartie(self, modele):
        self.partie = modele
        self.moi = modele.parent.nom
        
        self.cadreMenuPartie.grid(column=0, row=0, sticky=W + E)
        
        
        self.initJeu()
        
        self.placeCadre(self.cadrePartie)
    
    
    def initJeu(self):
        self.cadrePartie = Frame(self.root)
        
        # Call des cadre
        self.initCadre()
        # Variable bidon
        n = "100"
        self.changeLabelBois(n)
        self.changeLabelEnergie(n)
        self.changeLabelNourriture(n)
        self.changeLabelPierre(n)
        self.changeLabelOr(n)
        self.changeLabelPopulation(n)
        self.diplomatieClic()
        self.imgLabelPopulation()
        self.initLabelBas()
        
        # Milieu
        self.canevasMilieu = Canvas(self.cadrePartie, width=800, height=600, bg="#006633")
        
        
        self.canevasMilieu.grid(column=0, row=1, columnspan=3)
        
        self.canevasMilieu.bind("<Button-1>", self.selectUnit)  # add
        self.canevasMilieu.bind("<Motion>", self.motion)
        self.canevasMilieu.bind("<Key>", self.spawnUnit)
        self.canevasMilieu.bind("<Button-3>", self.setArrive)
        
        self.cadrePartie.pack()
        # self.cadreMenu.pack_forget()
        self.rafraichirCanevas()
        self.creerLigne()
        self.placeRessource()
        self.placeBuilding()
    

    def selectUnit(self, event):  # add
        if self.actionSelectionnee==0 :##
            print("-------------------------")
            print("click X: ", self.currentX, " - Y: ", self.currentY)
            if len(self.parent.myPlayer.unitsSelectionne) > 0:
                self.parent.myPlayer.unitsSelectionne.pop()
            for u in self.parent.myPlayer.units:
                u.isSelected = False
            for u in self.parent.myPlayer.units:
                print("units X: ", u.posX, " - Y: ", u.posY)
                if self.currentX >= u.posX and self.currentX <= (u.posX + 5) and self.currentY >= u.posY and self.currentY <= (u.posY + 5):
                    u.isSelected = True
                    self.parent.myPlayer.unitsSelectionne.append(u)
                    
                    print("selected: ", u.posX)
                    break
            #print (self.parent.myPlayer.unitsSelectionne[0])    
            self.optionUnite()
        elif self.actionSelectionnee==1:##
            self.actionSelectionnee=0##
            print("creating vil with owner id: ", self.parent.myPlayer.ID)##
            self.parent.actions.append([self.parent.nom, "creerUnite", ["villageois", self.currentX, self.currentY]])##

    def motion(self, event):
        self.canevasMilieu.focus_set()
        self.currentX = event.x
        self.currentY = event.y

    def spawnUnit(self, event):
        print("creating vil with owner id: ", self.parent.myPlayer.ID)
        self.parent.actions.append([self.parent.nom, "creerUnite", ["villageois", self.currentX, self.currentY]])
        
    def initCadre(self):
        
        # Haut
        self.cadreRessource = Frame(self.cadrePartie)
        self.cadreRessource.grid(column=0, row=0)
        
        self.cadrePopulation = Frame(self.cadrePartie)
        self.cadrePopulation.grid(column=1, row=0)
        
        self.cadreDiplomatie = Frame(self.cadrePartie)
        self.cadreDiplomatie.grid(column=2, row=0)
        # Bas

        self.cadreOptionVillageois = Frame(self.cadrePartie)
        buttonConstruire = Button(self.cadreOptionVillageois, text="Construire",command=self.optionConstruire, width=8)#alloa
        buttonConstruire.grid(column=0, row=1)
            
        self.cadreOptionTownCenter = Frame(self.cadrePartie)
        buttonCree = Button(self.cadreOptionTownCenter, text="Cree", width=8)  # text="Cree",command=,
        buttonCree.grid(column=0, row=1)
        buttonUpgrade = Button(self.cadreOptionTownCenter, text="Upgrade1", width=8)##
        buttonUpgrade.grid(column=1,row=1)##
        buttonUpgrade2 = Button(self.cadreOptionTownCenter, text="Upgrade2", width=8)##
        buttonUpgrade2.grid(column=1,row=1)##
        #mettre anchor
        self.cadreOptionConstruire = Frame(self.cadrePartie)##
        buttonBatiment1 = Button(self.cadreOptionConstruire,text="Tour", width=8)##
        buttonBatiment1.grid(column=0,row=1)##
        buttonBatiment2 = Button(self.cadreOptionConstruire,text="Batiment2", width=8)##
        buttonBatiment2.grid(column=1,row=1)##
        buttonBatiment3 = Button(self.cadreOptionConstruire,text="Batiment3", width=8)##
        buttonBatiment3.grid(column=2,row=1)##
        buttonBatiment4 = Button(self.cadreOptionConstruire,text="Batiment4", width=8)##
        buttonBatiment4.grid(column=0,row=2)##
        buttonBatiment5 = Button(self.cadreOptionConstruire,text="Batiment5", width=8)##
        buttonBatiment5.grid(column=1,row=2)##
        buttonRetour = Button(self.cadreOptionConstruire,text="Retour",command=self.optionRetour, width=8)##
        buttonRetour.grid(column=2,row=2)##
           
        self.cadreInfoVillageois = Frame(self.cadrePartie)##
        self.labelVillageoisHp= Label(self.cadreInfoVillageois, text="Points de vie : ",width=10)##
        self.labelVillageoisProprio = Label (self.cadreInfoVillageois, text="Proprietaire : ",width=10)##
        self.labelVillageoisNom = Label(self.cadreInfoVillageois, text="Nom : ",width=10)##
        self.labelVillageoisTransport = Label(self.cadreInfoVillageois,text="Transport : ",width=10)##
        
        self.cadreInfoAttaquant = Frame(self.cadrePartie)##
        self.labelAttaquantHp = Label(self.cadreInfoAttaquant,text="Points de vie : ",width=10)##
        self.labelAttaquantProprio = Label(self.cadreInfoAttaquant,text="Proprietaire : ",width=10)##
        self.labelAttaquantNom = Label(self.cadreInfoAttaquant,text="Nom : ",width=10)##
        self.labelAttaquantAttaque = Label(self.cadreInfoAttaquant,text="Attaque : ",width=10)##
        self.labelAttaquantDefense = Label(self.cadreInfoAttaquant,text="Defense : ",width=10)##
        
        
        self.cadreMiniMap = Frame(self.cadrePartie)
        self.cadreMiniMap.grid(column=2, row=2)
        
    # def initLabelHaut(self):
        
    # Pour le cadre de Ressource
    def optionConstruire(self):##
        self.cadreOptionVillageois.grid_forget()##
        self.cadreOptionConstruire.grid(column=0, row=2)##
        
    def optionRetour(self):##
        self.cadreOptionConstruire.grid_forget()##
        self.cadreOptionVillageois.grid(column=0, row=2)##
    
    def creeUnite(self):
        self.actionSelectionnee=1
    
    ####Pour les images    
        
    def changeLabelNourriture(self, n):
        labelNourriture = Label(self.cadreRessource, text="Nourriture: " + n, bg="red", relief=SOLID, width=15)
        labelNourriture.grid(column=0, row=0)  # (column=1,row=0)
        
    def changeLabelBois(self, n):
        labelBois = Label(self.cadreRessource, text="Bois: " + n, bg="brown", relief=SOLID, width=15)
        labelBois.grid(column=1, row=0)  # (column=3,row=0)
        
    def changeLabelPierre(self, n):
        labelPierre = Label(self.cadreRessource, text="Pierre: " + n, bg="gray", relief=SOLID, width=15)
        labelPierre.grid(column=0, row=1)  # (column=1,row=1)
        
    def changeLabelOr(self, n):
        labelOr = Label(self.cadreRessource, text="Or: " + n, bg="gold", relief=SOLID, width=15)
        labelOr.grid(column=1, row=1)  # (column=3,row=1)
        
    def changeLabelEnergie(self, n):
        labelEnergie = Label(self.cadreRessource, text="Energie: " + n, bg="green2", relief=SOLID, width=15)
        labelEnergie.grid(column=0, row=2, columnspan=2)  # (column=1,row=2,columnspan=2)
        
        # Pour le cadre de population
    
    def changeLabelPopulation(self, n):  # population et population max
        labelPopulationMax = Label(self.cadrePopulation, text=n + "/200")
        labelPopulationMax.grid(column=1, row=0)
        
        # Pour le cadre Diplomatie/echange
    
        
    def afficheArtefact(self):
        # loop dans tou les unite, etc
        # for i in self.partie.civs.keys():
        
        # afficher les changement
        self.afficheSelection()
        
    def afficheSelection(self):
        pass
    
    
    def diplomatieFenetre(self, event):
        self.toplevel = Toplevel()
        # frame pour echange et alliance
        self.cadreAlliance = Frame(self.toplevel)
        self.cadreAlliance.grid(column=0, row=0)
        
        self.cadreEchange = Frame(self.toplevel)
        self.cadreEchange.grid(column=1, row=0)
        
        self.toplevel.focus_set()  # il y a un focus sur le canvas clear focus
        
        # liste pour tout les joueurs sauf nous dans le dropdown menu
        self.autreJoueur = []
        for j in self.parent.modele.joueurs.values():
            print(j)
            if j.name != self.parent.nom:
                self.autreJoueur.append(j.name)
        
        self.var = StringVar(self.toplevel)
        self.var.set(self.autreJoueur[0])
        # titres
        labelAllie = Label(self.cadreAlliance, text="Alliance", width=15)
        labelAllie.grid(column=0, row=0, columnspan=2)
        
        labelEchange = Label(self.cadreEchange, text="Echange", width=15)
        labelEchange.grid(column=0, row=0, columnspan=2)
        
        # dropdown menu
        self.listeEchange = OptionMenu(self.cadreEchange, self.var, self.autreJoueur)  # tranfere a modele_client
        self.listeEchange.grid(column=0, row=1, columnspan=2)
        
        # labels
        
        labelDiplomatieNourriture = Label(self.cadreEchange, text="Nourriture", relief=SOLID, width=15)
        labelDiplomatieNourriture.grid(column=0, row=2)
        
        labelDiplomatieBois = Label(self.cadreEchange, text="Bois", relief=SOLID, width=15)
        labelDiplomatieBois.grid(column=0, row=3)
        
        labelDiplomatieOr = Label(self.cadreEchange, text="Or", relief=SOLID, width=15)
        labelDiplomatieOr.grid(column=0, row=4)
        
        labelDiplomatiePierre = Label(self.cadreEchange, text="Pierre", relief=SOLID, width=15)
        labelDiplomatiePierre.grid(column=0, row=5)
        
        labelDiplomatieEnergie = Label(self.cadreEchange, text="Energie", relief=SOLID, width=15)
        labelDiplomatieEnergie.grid(column=0, row=6)
        
        # Sliders
        
        self.sliderNourriture = Scale(self.cadreEchange, orient=HORIZONTAL, length=200, width=20, sliderlength=10, from_=0, to=500)
        self.sliderNourriture.grid(column=1, row=2)
        
        self.sliderBois = Scale(self.cadreEchange, orient=HORIZONTAL, length=200, width=20, sliderlength=10, from_=0, to=500)
        self.sliderBois.grid(column=1, row=3)
        
        self.sliderOr = Scale(self.cadreEchange, orient=HORIZONTAL, length=200, width=20, sliderlength=10, from_=0, to=500)
        self.sliderOr.grid(column=1, row=4)
        
        self.sliderPierre = Scale(self.cadreEchange, orient=HORIZONTAL, length=200, width=20, sliderlength=10, from_=0, to=500)
        self.sliderPierre.grid(column=1, row=5)
        
        self.sliderEnergie = Scale(self.cadreEchange, orient=HORIZONTAL, length=200, width=20, sliderlength=10, from_=0, to=500)
        self.sliderEnergie.grid(column=1, row=6)

        buttonEnvoyer = Button(self.cadreEchange, text="Envoyer", command=self.envoyerRessource)
        buttonEnvoyer.grid(column=0, row=7, columnspan=2)
        
    def envoyerRessource(self):
        # Nom,Nourriture,Bois,Or,Pierre,Energie
        varEnvoie = [self.parent.nom, "envoieRess", [self.var.get(),
                                                        self.sliderNourriture.get(),
                                                        self.sliderBois.get(),
                                                        self.sliderOr.get(),
                                                        self.sliderPierre.get(),
                                                        self.sliderEnergie.get()]]
        print("action envoyer :", varEnvoie)
        # self.parent.actions.append(varEnvoie)
        
        
    def diplomatieClic(self):
        labelDiplomatie = Label(self.cadreDiplomatie, text="Diplomatie/Echange", relief=SOLID, height=5, width=25)  # anchor:E
        labelDiplomatie.pack()
        labelDiplomatie.bind("<Button-1>", self.diplomatieFenetre)
        
    def optionUnite(self):
        #labelOptionUnite = Label(self.cadreOptionUnite, text="Option d'unite")
        #labelOptionUnite.grid(column=0, row=0, columnspan=2)
        #alloa
        if len(self.parent.myPlayer.unitsSelectionne) > 0:
            print("type: ", self.parent.myPlayer.unitsSelectionne[0].type)
        
        if len(self.parent.myPlayer.unitsSelectionne) < 1:
            print("grid forget")
            self.cadreOptionVillageois.grid_forget()
            self.cadreOptionTownCenter.grid_forget()
            self.cadreOptionConstruire.grid_forget()##
            self.cadreInfoVillageois.grid_forget()##
            self.cadreInfoAttaquant.grid_forget()##
        
        # TownCenter
        elif self.parent.myPlayer.unitsSelectionne[0].type == "TownCenter":
            self.cadreOptionTownCenter.grid(column=0, row=2)
        
        # Barracks
        elif self.parent.myPlayer.unitsSelectionne[0].type == "Building":
            buttonCree = Button(self.cadreOptionUnite, text="Cree", width=8)  # text="Cree",command=,
            buttonCree.grid(column=0, row=1)
        
        # Villageois
        elif self.parent.myPlayer.unitsSelectionne[0].type == "Villageois":
            print("ici")
            self.cadreOptionVillageois.grid(column=0, row=2)
            self.cadreInfoVillageois.grid(column=1, row=2)##
            self.labelVillageoisHp.grid(column=0,row=1)##
            self.labelVillageoisProprio.grid(column=0,row=2)##
            self.labelVillageoisNom.grid(column=0,row=3)##
            self.labelVillageoisTransport.grid(column=0,row=4)##
            
        
        # Attaquant
        elif self.parent.myPlayer.unitsSelectionne[0].type == "Guerrier":
            self.cadreInfoAttaquant.grid(column=1,row=2)##
            self.labelAttaquantHp.grid(column=0,row=1)##
            self.labelAttaquantProprio.grid(column=0,row=2)##
            self.labelAttaquantNom.grid(column=0,row=3)##
            self.labelAttaquantAttaque.grid(column=0,row=4)##
            self.labelAttaquantDefense.grid(column=0,row=5)##
            
            ##A changer
            buttonAttaquer = Button(self.cadreOptionUnite, text="Attaquer", width=8)
            buttonAttaquer.grid(column=0, row=1)
        
            buttonArreter = Button(self.cadreOptionUnite, text="Arreter", width=8)
            buttonArreter.grid(column=1, row=1)


    # #    
    def initLabelBas(self):
        # Pour le cadre Info Selection
        
        #labelInfoSelection = Label(self.cadreInfoSelection, text="Info sur Selection")##
        #labelInfoSelection.pack()##
        
        # Pour le cadre Mini-Map
        
        labelMiniMap = Label(self.cadreMiniMap, text="Mini-Map")
        labelMiniMap.grid(column=0, row=0)
    
    
    
    #===========================================================================
    # def rafraichirTemps(self,temps):
    #      labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
    #      labelTemps.grid(column=0,row=1)
    #     
    #===========================================================================
    
    def setArrive(self, event):
        print("setarr", event.x, event.x / self.longeurLigne)
        for u in self.parent.myPlayer.units:
            if u.isSelected == True:
                self.parent.actions.append([self.parent.nom, "deplace", [(0, u.id), (int(event.x / self.longeurLigne), int(event.y / self.longeurLigne))]])
				#self.modele.deplaceUnite((0, u.id), (int(event.x / self.longeurLigne), int(event.y / self.longeurLigne)))
        
    def rafraichirCanevas(self):
        self.canevasMilieu.delete("unit")
        for j in self.parent.modele.joueurs.values():
            for u in j.units:
                if u.isSelected == True:
                    self.canevasMilieu.create_rectangle(u.posX, u.posY, u.posX + 5, u.posY + 5, fill="red", tags="unit")
                else:
                    self.canevasMilieu.create_rectangle(u.posX, u.posY, u.posX + 5, u.posY + 5, fill=j.playerColor, tags="unit")
    
    def creerLigne(self):
        self.longeurLigne = 20
        for i in range (self.parent.l):
            self.canevasMilieu.create_line(i * self.longeurLigne, 0, i * self.longeurLigne, self.parent.h * self.longeurLigne, fill="white")
                
        for j in range (self.parent.h):
            self.canevasMilieu.create_line(0, j * self.longeurLigne, self.parent.l * self.longeurLigne, j * self.longeurLigne, fill="white")
    
    def placeBuilding(self):
        print("placeBuilding")
        for j in self.parent.modele.joueurs.values():
            for i in j.buildings:
                print("building for player: ", j.name, " - x: ", i.posX, " - y: ", i.posY)
                self.canevasMilieu.create_rectangle(i.posX * self.longeurLigne + self.longeurLigne / 2 - 9, i.posY * self.longeurLigne + self.longeurLigne / 2 - 9, i.posX * self.longeurLigne + self.longeurLigne / 2 + 9, i.posY * self.longeurLigne + self.longeurLigne / 2 + 9, fill=j.playerColor, tags="food")
    
    
    def placeRessource(self):
        for i in range(self.parent.h):
            for j in range(self.parent.l):
                # print(self.parent.m.mat[j][i].ressource)
                if self.parent.m.mat[i][j].ressource == FOOD_CHAR:  # nourriture
                    # print("nourr")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_food_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="red", tags="food")
                elif self.parent.m.mat[i][j].ressource == WOOD_CHAR:  # bois
                    # print("bois")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_wood_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="brown", tags="wood")
                elif self.parent.m.mat[i][j].ressource == ROCK_CHAR:  # pierre
                    # print("pierre")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_rock_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="gray", tags="rock")
                # elif self.parent.m.mat[j][i].ressource == EMPTY_CHAR:#vide
                #      print("vide")
                #      self.canevasMilieu.create_rectangle(i*self.longeurLigne+self.longeurLigne/2-9,j*self.longeurLigne+self.longeurLigne/2-9,i*self.longeurLigne+self.longeurLigne/2+9,j*self.longeurLigne+self.longeurLigne/2+9,fill="grey",tags="food")
                elif self.parent.m.mat[i][j].ressource == ARTE_CHAR:  # energie
                    # print("energie")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_art_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="blue", tags="artefact")

                elif self.parent.m.mat[i][j].ressource == ENERGY_CHAR:  # energie
                    # print("energie")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_energy_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="green2", tags="energie")
                    
                elif self.parent.m.mat[i][j].ressource == GOLD_CHAR:  # energie
                    # print("energie")
                    self.canevasMilieu.create_image(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.photo_gold_ress, anchor='nw', tags='img')
                    # self.canevasMilieu.create_rectangle(j * self.longeurLigne + self.longeurLigne / 2 - 9, i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 + 9, i * self.longeurLigne + self.longeurLigne / 2 + 9, fill="gold", tags="or")

        
    def imgLabelPopulation(self):
        labelPopulation = Label(self.cadrePopulation, text="Population:", width=15)
        labelPopulation.grid(column=0, row=0)
    
    # ##Pour les changements de labels
    
    
        
    def creerServeur(self):
        nom = self.nomjoueur.get()
        leip = self.parent.monip
        if nom:
            pid = self.parent.creerServeur()
            if pid:
                self.demarreB.config(state=NORMAL)
                self.root.after(500, self.inscritClient)
        else:
            mb.showerror(title="Besoin d'un nom", message="Vous devez inscrire un nom pour vous connecter.")
                    
    def inscritClient(self):
        nom = self.nomjoueur.get()
        leip = self.parent.monip
        self.parent.inscritClient(nom, leip)
        
    def connecterServeur(self):
        nom = self.nomjoueur.get()
        leip = self.autreip.get()
        if nom:
            self.parent.inscritClient(nom, leip)
    
    def actionButton(self):
        pass
