from tkinter import *
from tkinter.font import *
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import random
import math
from helper import *
from PIL import Image, ImageTk
from utils import *
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
        self.root.title("Cegep of empire")
        self.root.protocol('WM_DELETE_WINDOW', self.intercepteFermeture)
        self.cadreActif = 0
        self.creeCadres()
        self.placeCadre(self.cadreConnection)
        self.currentX = 0
        self.currentY = 0
        self.actionSelectionnee=0#1=SpawnUnit, 2=tour##
        self.longeurLigne = 20

        self.initImgs()

    def initImgs(self):
        """Initialise les images"""
        self.imgs = {"food": ImageTk.PhotoImage(Image.open("img/food_ress.png")),
                     "wood": ImageTk.PhotoImage(Image.open("img/wood_ress.png")),
                     "gold": ImageTk.PhotoImage(Image.open("img/gold_ress.png")),
                     "energy": ImageTk.PhotoImage(Image.open("img/energy_ress.png")),
                     "art": ImageTk.PhotoImage(Image.open("img/art_ress.png")),
                     "rock": ImageTk.PhotoImage(Image.open("img/rock_ress.png")),
                     "tower": ImageTk.PhotoImage(Image.open("img/tower_build.png")),
                     "barrack": ImageTk.PhotoImage(Image.open("img/barrack_build.png")),
                     "maison": ImageTk.PhotoImage(Image.open("img/maison_build.png"))}

    def initLabel(self):
        self.labelNourriture = Label(self.cadreRessource, text="Nourriture: ", bg="red", relief=SOLID, width=15)
        self.labelNourriture.grid(column=0, row=0)
        self.labelBois = Label(self.cadreRessource, text="Bois: ", bg="brown", relief=SOLID, width=15)
        self.labelBois.grid(column=1, row=0)
        self.labelPierre = Label(self.cadreRessource, text="Pierre: ", bg="gray", relief=SOLID, width=15)
        self.labelPierre.grid(column=0, row=1)
        self.labelOr = Label(self.cadreRessource, text="Or: ", bg="gold", relief=SOLID, width=15)
        self.labelOr.grid(column=1, row=1)
        self.labelEnergie = Label(self.cadreRessource, text="Energie: ", bg="green2", relief=SOLID, width=15)
        self.labelEnergie.grid(column=0, row=2,columnspan=2)#columnspan=2
        self.labelPopulationMax= Label(self.cadrePopulation, text="" +" / " + str(self.parent.myPlayer.maxUnitsDepart))
        self.labelPopulationMax.grid(column=1, row=0)
        #boutonCentrer=Button(self.cadreRessource,text="Centrer",command=self.centrer)
        #boutonCentrer.grid(column=1,row=2)
        
    def canx(self, x):
        """Retourne le x par rapport au canevas"""
        return self.canevasMilieu.canvasx(x)

    def cany(self, y):
        """Retourne le y par rapport au canevas"""
        return self.canevasMilieu.canvasy(y)

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

        Labeljm(cadreMenu, text="Pour creer un serveur a l'adresse inscrite  | ").grid(column=0, row=1)
        Labeljm(cadreMenu, text="Pour vous connecter a un serveur").grid(column=1, row=1)
        
        Labeljm(cadreMenu, text=self.parent.monip).grid(column=0, row=2)
        self.autreip = Entry(cadreMenu)
        self.autreip.insert(0, self.parent.monip)
        self.autreip.grid(column=1, row=2)

        Buttonjm(cadreMenu, text="Creer un serveur", command=self.creerServeur).grid(column=0, row=3)
        Buttonjm(cadreMenu, text="Connecter a un serveur", command=self.connecterServeur).grid(column=1, row=3)

        cadreMenu.pack()

    def creeCadreAttente(self):
        self.cadreAttente = Frame(self.root)
        cadreMenu = Frame(self.cadreAttente)
        self.listeJoueurs = Listbox(cadreMenu)
        self.demarreB = Buttonjm(cadreMenu, text="Demarre partie", state=DISABLED, command=self.parent.demarrePartie)
        self.demarreB.grid(column=0, row=1)
        self.listeJoueurs.grid(column=0, row=0)
        cadreMenu.pack(side=LEFT)

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
        self.initLabel()
        
        self.diplomatieClic()
        self.imgLabelPopulation()
        self.initLabelBas()

        hbar=Scrollbar(self.cadrePartie)
        vbar=Scrollbar(self.cadrePartie)
        # Milieu
        self.hauteur = 600
        self.largeur = 800
        self.rHauteur = self.parent.h*20
        self.rLargeur = self.parent.l*20
        self.canevasMilieu = Canvas(self.cadrePartie, width=self.largeur, height=self.hauteur, bg="#006633",
                                    scrollregion=(0,0,self.rHauteur, self.rLargeur),
                                    xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        #self.canevasMilieu.pack(side=LEFT,expand=True,fill=BOTH)

        self.canevasMilieu.grid(column=0, row=1, columnspan=3)

        self.canevasMilieu.bind("<Button-1>", self.selectObject)  # add
        self.canevasMilieu.bind("<Motion>", self.motion)
        self.canevasMilieu.bind("u", self.spawnUnit)
        self.canevasMilieu.bind("<Button-3>", self.setArrive)

        self.canevasMilieu.bind("a", self.bougeVersGauche)
        self.canevasMilieu.bind("w", self.bougeVersHaut)
        self.canevasMilieu.bind("s", self.bougeVersBas)
        self.canevasMilieu.bind("d", self.bougeVersDroite)

        self.cadrePartie.pack()
        # self.cadreMenu.pack_forget()
        #self.rafraichirCanevas()
        self.rafraichir()
        self.creerLigne()
        self.placeRessource()
        self.placeBuilding()
        self.centrer()

    def rafraichir(self):
        """ Rafraichi la vue au complet """
        self.rafraichirInfo()
        self.rafraichirCanevas()

    def rafraichirInfo(self):
        """ Rafraichi les informations (labels, ressources, populations)"""
        self.changeLabelBois(self.parent.myPlayer.ressources[1])
        self.changeLabelEnergie(self.parent.myPlayer.ressources[4])
        self.changeLabelNourriture(self.parent.myPlayer.ressources[0])
        self.changeLabelPierre(self.parent.myPlayer.ressources[2])
        self.changeLabelOr(self.parent.myPlayer.ressources[3])
        self.changeLabelPopulation(self.parent.myPlayer.maxUnitsCourrant)


    def bougeVersGauche(self, event):
        self.canevasMilieu.xview(SCROLL, -1, "units")

    def bougeVersHaut(self, event):
        self.canevasMilieu.yview(SCROLL, -1, "units")

    def bougeVersBas(self, event):
        self.canevasMilieu.yview(SCROLL, 1, "units")

    def bougeVersDroite(self, event):
        self.canevasMilieu.xview(SCROLL, 1, "units")

    def selectObject(self, event):  # add
        if self.actionSelectionnee==0 :##
            print("-------------------------")
            print("click X: ", self.canx(self.currentX), " - Y: ", self.cany(self.currentY))
            if len(self.parent.myPlayer.objectsSelectionne) > 0:
                self.parent.myPlayer.objectsSelectionne.pop()
            for u in self.parent.myPlayer.units:
                if self.canx(self.currentX) >= u.posX and self.canx(self.currentX) <= (u.posX + 5) and self.cany(self.currentY) >= u.posY and self.cany(self.currentY) <= (u.posY + 5):
                    self.parent.myPlayer.objectsSelectionne.append(u)
                    print("selected object: ", u.type)
                    break


            if len(self.parent.myPlayer.objectsSelectionne) == 0: #si pas d'unite selectionnes
                for b in self.parent.myPlayer.buildings:
                    if b.type == "TownCenter" or b.type == "Barrack" or b.type == "Maison":
                        if self.canx(self.currentX) >= (b.posX * self.longeurLigne + self.longeurLigne / 2 - 9) and self.canx(self.currentX) <= (b.posX * self.longeurLigne + self.longeurLigne / 2 + 9) and self.cany(self.currentY) >= (b.posY * self.longeurLigne + self.longeurLigne / 2 - 9) and self.cany(self.currentY) <= ((b.posY * self.longeurLigne + self.longeurLigne / 2 + 9)):
                            self.parent.myPlayer.objectsSelectionne.append(b)
                            print("selected object: ", b.type)
                            break
                    else:
                        if self.canx(self.currentX) >= (b.posX) and self.canx(self.currentX) <= (b.posX + 18) and self.cany(self.currentY) >= (b.posY) and self.cany(self.currentY) <= ((b.posY + 18)):
                            self.parent.myPlayer.objectsSelectionne.append(b)
                            print("selected object: ", b.type)
                            break
            #print (self.parent.myPlayer.objectsSelectionne[0])
            self.optionUnite()
        elif self.actionSelectionnee==1:##
            self.actionSelectionnee=0##
            print("creating vil with owner id: ", self.parent.myPlayer.ID)##
            self.parent.actions.append([self.parent.nom, "creerUnite", ["villageois", self.canx(self.currentX), self.cany(self.currentY)]])##
        elif self.actionSelectionnee == 2:
            self.actionSelectionnee = 0
            print("creating tower with owner id: ", self.parent.myPlayer.ID)##
            caseX, caseY = trouveCase(self.canx(self.currentX), self.cany(self.currentY))
            self.parent.actions.append([self.parent.nom, "creerBuilding", ["tower", caseX, caseY]])##
        elif self.actionSelectionnee == 3: #barrack
            self.actionSelectionnee = 0
            print("creating barrack with owner id: ", self.parent.myPlayer.ID)##
            caseX, caseY = trouveCase(self.canx(self.currentX), self.cany(self.currentY))
            self.parent.actions.append([self.parent.nom, "creerBuilding", ["barrack", caseX, caseY]])##
        elif self.actionSelectionnee==4:# guerrier
            self.actionSelectionnee=0##
            print("creating vil with owner id: ", self.parent.myPlayer.ID)##
            self.parent.actions.append([self.parent.nom, "creerUnite", ["guerrier", self.canx(self.currentX), self.cany(self.currentY)]])##
        elif self.actionSelectionnee==5:# maison
            self.actionSelectionnee = 0
            print("creating house with owner id: ", self.parent.myPlayer.ID)##
            caseX, caseY = trouveCase(self.canx(self.currentX), self.cany(self.currentY))
            self.parent.actions.append([self.parent.nom, "creerBuilding", ["maison", caseX, caseY]])
            self.parent.myPlayer.maxUnitsDepart+=10

    def motion(self, event):
        self.canevasMilieu.delete("test")
        self.canevasMilieu.focus_set()
        self.currentX = event.x
        self.currentY = event.y
        xcan = self.canx(event.x)
        ycan = self.cany(event.y)
        if self.actionSelectionnee == 1:
            self.canevasMilieu.create_rectangle(xcan, ycan, xcan + 5, ycan + 5, fill=self.parent.myPlayer.playerColor, tags="test")
        elif self.actionSelectionnee == 2:
            self.canevasMilieu.create_image(xcan, ycan, image=self.imgs["tower"], anchor='nw', tags="test")
        elif self.actionSelectionnee == 3:
            self.canevasMilieu.create_image(xcan, ycan, image=self.imgs["barrack"], anchor='nw', tags="test")
        elif self.actionSelectionnee == 4:
            self.canevasMilieu.create_oval(xcan, ycan, xcan + 5, ycan + 5, fill=self.parent.myPlayer.playerColor, tags="test")
        elif self.actionSelectionnee == 5:
            self.canevasMilieu.create_image(xcan, ycan, image=self.imgs["maison"], anchor='nw', tags="test")##MAISON

    def spawnUnit(self, event):
        print("creating vil with owner id: ", self.parent.myPlayer.ID)
        self.parent.actions.append([self.parent.nom, "creerUnite", ["villageois", self.canx(self.currentX), self.cany(self.currentY)]])
        print("units "+ str(self.parent.myPlayer.maxUnitsCourrant))

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
        self.buttonCreeVillageois = Button(self.cadreOptionTownCenter, text="Creer", command=self.creeUnite, width=8)  # text="Cree",command=,
        self.buttonCreeVillageois.grid(column=0, row=1)
        buttonUpgrade = Button(self.cadreOptionTownCenter, text="Upgrade1", width=8)##
        buttonUpgrade.grid(column=1,row=1)##
        buttonUpgrade2 = Button(self.cadreOptionTownCenter, text="Upgrade2", width=8)##
        buttonUpgrade2.grid(column=2,row=1)##
        #mettre anchor
        self.cadreOptionConstruire = Frame(self.cadrePartie)##
        buttonBatiment1 = Button(self.cadreOptionConstruire,text="Tour", command=self.creeTour, width=8)##
        buttonBatiment1.grid(column=0,row=1)##
        buttonBatiment2 = Button(self.cadreOptionConstruire,text="Barrack", command=self.creeBarrack, width=8)##
        buttonBatiment2.grid(column=1,row=1)##
        buttonBatiment3 = Button(self.cadreOptionConstruire,text="Maison", command=self.creeMaison, width=8)##
        buttonBatiment3.grid(column=2,row=1)##
        buttonBatiment4 = Button(self.cadreOptionConstruire,text="Batiment4", width=8)##
        buttonBatiment4.grid(column=0,row=2)##
        buttonBatiment5 = Button(self.cadreOptionConstruire,text="Batiment5", width=8)##
        buttonBatiment5.grid(column=1,row=2)##
        buttonRetour = Button(self.cadreOptionConstruire,text="Retour",command=self.optionRetour, width=8)##
        buttonRetour.grid(column=2,row=2)##

        self.cadreOptionBarrack = Frame(self.cadrePartie)
        buttonCreeGuerrier = Button(self.cadreOptionBarrack, text="Cree", command=self.creeGuerrier, width=8)  # text="Cree",command=,
        buttonCreeGuerrier.grid(column=0, row=1)

        self.cadreOptionGuerrier = Frame(self.cadrePartie)
        buttonAttaquer = Button(self.cadreOptionGuerrier, text="Attaquer", width=8)
        buttonAttaquer.grid(column=0, row=1)
        buttonArreter = Button(self.cadreOptionGuerrier, text="Arreter", width=8)
        buttonArreter.grid(column=1, row=1)

        self.cadreInfoVillageois = Frame(self.cadrePartie)##
        self.labelVillageoisHp= Label(self.cadreInfoVillageois)##
        self.labelVillageoisProprio = Label (self.cadreInfoVillageois)##
        self.labelVillageoisNom = Label(self.cadreInfoVillageois)##
        self.labelVillageoisTransport = Label(self.cadreInfoVillageois)##

        self.cadreInfoAttaquant = Frame(self.cadrePartie)##
        self.labelAttaquantHp = Label(self.cadreInfoAttaquant,text="Points de vie : 0/0",width=10)##
        self.labelAttaquantProprio = Label(self.cadreInfoAttaquant,text="Proprietaire : ",width=10)##
        self.labelAttaquantNom = Label(self.cadreInfoAttaquant,text="Type : ",width=10)##
        self.labelAttaquantAttaque = Label(self.cadreInfoAttaquant,text="Attaque : ",width=10)##
        self.labelAttaquantDefense = Label(self.cadreInfoAttaquant,text="Defense : ",width=10)##

        self.cadreInfoTownCenter = Frame(self.cadrePartie)
        self.labelTownCenterHp = Label(self.cadreInfoTownCenter)
        self.labelTownCenterProprio = Label(self.cadreInfoTownCenter)
        self.labelTownCenterNom = Label(self.cadreInfoTownCenter)

        self.cadreInfoBarrack = Frame(self.cadrePartie)
        self.labelBarrackHp = Label(self.cadreInfoBarrack)
        self.labelBarrackProprio = Label(self.cadreInfoBarrack)
        self.labelBarrackNom = Label(self.cadreInfoBarrack)
        
        self.cadreInfoMaison = Frame(self.cadrePartie)
        self.labelMaisonHp = Label(self.cadreInfoMaison)
        self.labelMaisonProprio = Label(self.cadreInfoMaison)
        self.labelMaisonNom = Label(self.cadreInfoMaison)


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

    def creeGuerrier(self):
    	self.actionSelectionnee=4

    def creeTour(self):
        self.actionSelectionnee=2

    def creeBarrack(self):
    	self.actionSelectionnee=3
        
    def creeMaison(self):
        self.actionSelectionnee=5

    ####Pour les images

    def changeLabelNourriture(self, n):
        self.labelNourriture.config(text="Nourriture: " + str(n))

    def changeLabelBois(self, n):
        self.labelBois.config(text="Bois: " + str(n))

    def changeLabelPierre(self, n):
        self.labelPierre.config(text="Pierre: " + str(n))

    def changeLabelOr(self, n):
        self.labelOr.config(text="Or: " + str(n))

    def changeLabelEnergie(self, n):
        self.labelEnergie.config(text="Energie: " + str(n))

        # Pour le cadre de population

    def changeLabelPopulation(self, n):  # population et population max
        self.labelPopulationMax.config(text=str(n) +" / " + str(self.parent.myPlayer.maxUnitsDepart))

        # Pour le cadre Diplomatie/echange


    def afficheArtefact(self):
        # loop dans tou les unite, etc
        # for i in self.partie.civs.keys():

        # afficher les changement
        self.afficheSelection()

    def afficheSelection(self):
        pass

    def centrer(self):#Pour centrer la fenetre sur le town center
        for j in self.parent.modele.joueurs.values():
            if j.name == self.parent.nom:
                #print("mon nom: "+ j.name)
                for i in j.buildings:
                    if i.type == "TownCenter":
                        x=i.posX*self.longeurLigne
                        y=i.posY*self.longeurLigne
                        sx = float(self.rLargeur)
                        ecranx=float(self.canevasMilieu.winfo_width())/2.0
                        positionX = (x-ecranx)/sx
                        self.canevasMilieu.xview("moveto",positionX)
                        
                        sy = float(self.rHauteur)
                        ecrany=float(self.canevasMilieu.winfo_height())/2.0
                        positionY = (y-ecrany)/sy
                        self.canevasMilieu.yview("moveto",positionY)

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

        if len(self.autreJoueur) > 0:
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

    def forgetAllCadre(self):
        self.cadreOptionVillageois.grid_forget()
        self.cadreOptionTownCenter.grid_forget()
        self.cadreOptionConstruire.grid_forget()##
        self.cadreOptionBarrack.grid_forget()
        self.cadreOptionGuerrier.grid_forget()
        self.cadreInfoTownCenter.grid_forget()
        self.cadreInfoVillageois.grid_forget()##
        self.cadreInfoAttaquant.grid_forget()##
        self.cadreInfoBarrack.grid_forget()
        self.cadreInfoMaison.grid_forget()


    def optionUnite(self):
        if len(self.parent.myPlayer.objectsSelectionne) == 0:
            print("No object selected: grid forget")
            self.forgetAllCadre()

        # TownCenter
        elif self.parent.myPlayer.objectsSelectionne[0].type == "TownCenter":
            self.forgetAllCadre()
            if self.parent.myPlayer.maxUnitsCourrant >= self.parent.myPlayer.maxUnitsDepart:
                self.buttonCreeVillageois.config(state='disabled')
            else:
                self.buttonCreeVillageois.config(state='normal')
            self.labelTownCenterHp = Label(self.cadreInfoTownCenter, text="Points de vie : "+str(self.parent.myPlayer.objectsSelectionne[0].hpActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].hpMax),width=19)##,width=10)
            for j in self.parent.modele.joueurs.values():
                if j.ID == self.parent.myPlayer.objectsSelectionne[0].ownerID:
                    self.labelTownCenterProprio = Label(self.cadreInfoTownCenter,text="Proprietaire : "+j.name,width=19)
            self.labelTownCenterNom = Label(self.cadreInfoTownCenter,text="Type : "+self.parent.myPlayer.objectsSelectionne[0].type,width=19)##

            self.cadreOptionTownCenter.grid(column=0, row=2)
            self.cadreInfoTownCenter.grid(column=1, row=2)##
            self.labelTownCenterHp.grid(column=0,row=1)##
            self.labelTownCenterProprio.grid(column=0,row=2)##
            self.labelTownCenterNom.grid(column=0,row=3)##

        # Barracks
        elif self.parent.myPlayer.objectsSelectionne[0].type == "Barrack":
            self.forgetAllCadre()
            self.labelBarrackHp = Label(self.cadreInfoBarrack, text="Points de vie : "+str(self.parent.myPlayer.objectsSelectionne[0].hpActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].hpMax),width=19)##,width=10)
            for j in self.parent.modele.joueurs.values():
                if j.ID == self.parent.myPlayer.objectsSelectionne[0].ownerID:
                    self.labelBarrackProprio = Label(self.cadreInfoBarrack,text="Proprietaire : "+j.name,width=19)
            self.labelBarrackNom = Label(self.cadreInfoBarrack,text="Type : "+self.parent.myPlayer.objectsSelectionne[0].type,width=19)##

            self.cadreOptionBarrack.grid(column=0, row=2)
            self.cadreInfoBarrack.grid(column=1, row=2)##
            self.labelBarrackHp.grid(column=0,row=1)##
            self.labelBarrackProprio.grid(column=0,row=2)##
            self.labelBarrackNom.grid(column=0,row=3)##
            
        # Maison
        elif self.parent.myPlayer.objectsSelectionne[0].type == "Maison":
            self.forgetAllCadre()
            self.labelMaisonHp = Label(self.cadreInfoMaison, text="Points de vie : "+str(self.parent.myPlayer.objectsSelectionne[0].hpActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].hpMax),width=19)##,width=10)
            for j in self.parent.modele.joueurs.values():
                if j.ID == self.parent.myPlayer.objectsSelectionne[0].ownerID:
                    self.labelMaisonProprio = Label(self.cadreInfoMaison,text="Proprietaire : "+j.name,width=19)
            self.labelMaisonNom = Label(self.cadreInfoMaison,text="Type : "+self.parent.myPlayer.objectsSelectionne[0].type,width=19)##

            self.cadreInfoMaison.grid(column=1, row=2)##
            self.labelMaisonHp.grid(column=0,row=1)##
            self.labelMaisonProprio.grid(column=0,row=2)##
            self.labelMaisonNom.grid(column=0,row=3)##



        # Villageois
        elif self.parent.myPlayer.objectsSelectionne[0].type == "Villageois":
            self.forgetAllCadre()
            self.labelVillageoisHp= Label(self.cadreInfoVillageois, text="Points de vie : "+str(self.parent.myPlayer.objectsSelectionne[0].hpActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].hpMax),width=19)##
            for j in self.parent.modele.joueurs.values():
                if j.ID == self.parent.myPlayer.objectsSelectionne[0].ownerID:
                    self.labelVillageoisProprio = Label (self.cadreInfoVillageois, text="Proprietaire : "+j.name,width=19)##
            self.labelVillageoisNom = Label(self.cadreInfoVillageois, text="Type: "+self.parent.myPlayer.objectsSelectionne[0].type,width=19)##
            self.labelVillageoisTransport = Label(self.cadreInfoVillageois,text="Transport : "+str(self.parent.myPlayer.objectsSelectionne[0].collectionActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].collectionMax),width=19)##

            self.cadreOptionVillageois.grid(column=0, row=2)
            self.cadreInfoVillageois.grid(column=1, row=2)##
            self.labelVillageoisHp.grid(column=0,row=1)##
            self.labelVillageoisProprio.grid(column=0,row=2)##
            self.labelVillageoisNom.grid(column=0,row=3)##
            self.labelVillageoisTransport.grid(column=0,row=4)##

        # Attaquant
        elif self.parent.myPlayer.objectsSelectionne[0].type == "Guerrier":
            self.forgetAllCadre()
            self.labelAttaquantHp= Label(self.cadreInfoAttaquant, text="Points de vie : "+str(self.parent.myPlayer.objectsSelectionne[0].hpActuel)+"/"+str(self.parent.myPlayer.objectsSelectionne[0].hpMax),width=19)##
            for j in self.parent.modele.joueurs.values():
                if j.ID == self.parent.myPlayer.objectsSelectionne[0].ownerID:
                    self.labelAttaquantProprio = Label (self.cadreInfoAttaquant, text="Proprietaire : "+j.name,width=19)##
            self.labelAttaquantNom = Label(self.cadreInfoAttaquant, text="Type: "+self.parent.myPlayer.objectsSelectionne[0].type,width=19)##
            self.labelAttaquantAttaque = Label(self.cadreInfoAttaquant,text="Attaque : "+str(self.parent.myPlayer.objectsSelectionne[0].degat),width=10)##
            self.labelAttaquantDefense = Label(self.cadreInfoAttaquant,text="Defense : "+str(self.parent.myPlayer.objectsSelectionne[0].defense),width=10)##

            self.cadreOptionGuerrier.grid(column=0,row=2)
            self.cadreInfoAttaquant.grid(column=1,row=2)##
            self.labelAttaquantHp.grid(column=0,row=1)##
            self.labelAttaquantProprio.grid(column=0,row=2)##
            self.labelAttaquantNom.grid(column=0,row=3)##
            self.labelAttaquantAttaque.grid(column=0,row=4)##
            self.labelAttaquantDefense.grid(column=0,row=5)##

    # #
    def initLabelBas(self):
        # Pour le cadre Mini-Map
        labelMiniMap = Label(self.cadreMiniMap)
        labelMiniMap.grid(column=0, row=0)



    #===========================================================================
    # def rafraichirTemps(self,temps):
    #      labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
    #      labelTemps.grid(column=0,row=1)
    #
    #===========================================================================

    def setArrive(self, event):
        if self.actionSelectionnee > 0:
            self.actionSelectionnee = 0
            return
        if len(self.parent.myPlayer.objectsSelectionne) > 0:
            u = self.parent.myPlayer.objectsSelectionne[0]
            self.parent.actions.append([self.parent.nom, "deplace", [(0, u.id), (int(self.canx(event.x) / self.longeurLigne), int(self.cany(event.y) / self.longeurLigne))]])

    def rafraichirCanevas(self):
        self.canevasMilieu.delete("unit")
        for j in self.parent.modele.joueurs.values():
            uniteMorts=[]
            buildingMorts=[]
            for u in j.units: # Retire les units
                if u.isAlive() == False:
                    uniteMorts.append(u)
            for i in uniteMorts:
                j.units.remove(i)

            for u in j.buildings: # Retire les batiments... ish.
                if u.isAlive() == False:
                    buildingMorts.append(u)
            for i in buildingMorts:
                j.buildings.remove(i)

            for u in j.units:
                if u.type == "Guerrier":
                    self.canevasMilieu.create_oval(u.posX, u.posY, u.posX + 5, u.posY + 5, fill=j.playerColor, tags="unit")
                    if len(self.parent.myPlayer.objectsSelectionne) > 0:
                        if u == self.parent.myPlayer.objectsSelectionne[0]:
                            self.canevasMilieu.create_oval(u.posX, u.posY, u.posX + 5, u.posY + 5, fill="red", tags="unit")
                elif u.type == "Villageois":
                    self.canevasMilieu.create_rectangle(u.posX, u.posY, u.posX + 5, u.posY + 5, fill=j.playerColor, tags="unit")
                    if len(self.parent.myPlayer.objectsSelectionne) > 0:
                        if u == self.parent.myPlayer.objectsSelectionne[0]:
                            self.canevasMilieu.create_rectangle(u.posX, u.posY, u.posX + 5, u.posY + 5, fill="red", tags="unit")
            for i in j.buildings:
                caseX = i.posX * self.longeurLigne + self.longeurLigne / 2
                caseY = i.posY * self.longeurLigne + self.longeurLigne / 2
                if i.type == "Barrack":
                    self.canevasMilieu.create_rectangle(caseX-11, caseY-11, caseX + 10, caseY + 10, fill=j.playerColor, tags="unit")
                    #self.canevasMilieu.create_rectangle(i.posX * self.longeurLigne + self.longeurLigne / 2 - 9, i.posY * self.longeurLigne + self.longeurLigne / 2 - 9, i.posX * self.longeurLigne + self.longeurLigne / 2 + 9, i.posY * self.longeurLigne + self.longeurLigne / 2 + 9, fill=j.playerColor, tags="unit")

                    if len(self.parent.myPlayer.objectsSelectionne) > 0:
                        if i == self.parent.myPlayer.objectsSelectionne[0]:
                            self.canevasMilieu.create_rectangle(caseX-13, caseY-13, caseX + 12, caseY + 12, fill="red", tags="unit")
                    self.canevasMilieu.create_image(caseX-9, caseY-9, image=self.imgs["barrack"], anchor='nw', tags="unit")
                elif i.type == "Maison":
                    self.canevasMilieu.create_rectangle(caseX-11, caseY-11, caseX + 10, caseY + 10, fill=j.playerColor, tags="unit")
                    #self.canevasMilieu.create_rectangle(i.posX * self.longeurLigne + self.longeurLigne / 2 - 9, i.posY * self.longeurLigne + self.longeurLigne / 2 - 9, i.posX * self.longeurLigne + self.longeurLigne / 2 + 9, i.posY * self.longeurLigne + self.longeurLigne / 2 + 9, fill=j.playerColor, tags="unit")

                    if len(self.parent.myPlayer.objectsSelectionne) > 0:
                        if i == self.parent.myPlayer.objectsSelectionne[0]:
                            self.canevasMilieu.create_rectangle(caseX-13, caseY-13, caseX + 12, caseY + 12, fill="red", tags="unit")
                    self.canevasMilieu.create_image(caseX-9, caseY-9, image=self.imgs["maison"], anchor='nw', tags="unit")#MAISON
                elif i.type == "Tower":
                    self.canevasMilieu.create_image(caseX-9, caseY-9, image=self.imgs["tower"], anchor='nw', tags="unit")
                else: ##town center
                    self.canevasMilieu.create_rectangle(caseX - 9, caseY - 9, caseX + 9, caseY + 9, fill=j.playerColor, tags="unit")
                    if len(self.parent.myPlayer.objectsSelectionne) > 0:
                        if i == self.parent.myPlayer.objectsSelectionne[0]:
                            self.canevasMilieu.create_rectangle(caseX - 9, caseY - 9, caseX + 9, caseY + 9, fill="red", tags="unit")

    def creerLigne(self):
        for i in range (self.parent.l):
            self.canevasMilieu.create_line(i * self.longeurLigne, 0, i * self.longeurLigne, self.parent.h * self.longeurLigne, fill="white")

        for j in range (self.parent.h):
            self.canevasMilieu.create_line(0, j * self.longeurLigne, self.parent.l * self.longeurLigne, j * self.longeurLigne, fill="white")

    def placeBuilding(self):
        for j in self.parent.modele.joueurs.values():
            for i in j.buildings:
                print("building for player: ", j.name, " - x: ", i.posX, " - y: ", i.posY)
                self.canevasMilieu.create_rectangle(i.posX * self.longeurLigne + self.longeurLigne / 2 - 9, i.posY * self.longeurLigne + self.longeurLigne / 2 - 9, i.posX * self.longeurLigne + self.longeurLigne / 2 + 9, i.posY * self.longeurLigne + self.longeurLigne / 2 + 9, fill=j.playerColor, tags="food")

    def placeRessource(self):
        self.canevasMilieu.delete("img")
        for i in range(self.parent.l):
            for j in range(self.parent.h):
                if self.parent.m.mat[i][j].ressource == FOOD_CHAR :
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["food"], anchor='nw', tags='img')
                elif self.parent.m.mat[i][j].ressource == WOOD_CHAR:
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["wood"], anchor='nw', tags='img')
                elif self.parent.m.mat[i][j].ressource == ROCK_CHAR:
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["rock"], anchor='nw', tags='img')
                elif self.parent.m.mat[i][j].ressource == ARTE_CHAR:
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["art"], anchor='nw', tags='img')
                elif self.parent.m.mat[i][j].ressource == ENERGY_CHAR:
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["energy"], anchor='nw', tags='img')
                elif self.parent.m.mat[i][j].ressource == GOLD_CHAR:
                    self.canevasMilieu.create_image(i * self.longeurLigne + self.longeurLigne / 2 - 9, j * self.longeurLigne + self.longeurLigne / 2 - 9, image=self.imgs["gold"], anchor='nw', tags='img')

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
