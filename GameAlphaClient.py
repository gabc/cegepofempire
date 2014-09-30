from tkinter import *
import Pyro4


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

ip= input("ip: ")
ur="PYRO:foo@"+ip+":9999"
monserveur=Pyro4.Proxy(ur)


#===============================================================================
# ID:    - 0: Login Packet
#        - 1: Login response packet
#===============================================================================
class Action():
    def __init__(self, ID, playerID, playerName, playerX, playerY, playerTime, objectID, message):
        self.ID = ID
        self.playerID = playerID
        self.playerName = playerName
        self.playerX = playerX
        self.playerY = playerY
        self.playerTime = playerTime
        self.objectID = objectID
        self.message = message

class Player():
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.currentTime = currentTime

class  ServerListener():
    def __init__(self, parent):
        self.parent = parent
        self.beg = 0

    def sendAndReceive(self, action):
        #envoi l'action (ID=0) et store la reponse dans une variable "reponse"
        reponse = monserveur.ClientToServer(action)
        #si reponse == 1, assign un ID au joueur
        if(reponse.ID == 1):
            print("received a login response - player ID: ", reponse.playerID)
            self.parent.m.myPlayer.ID = reponse.playerID
        elif(reponse.ID == 3):
            print("received a seed response - Seed: ", reponse.message)
            mapSeed = int(reponse.message)

class model():
    def __init__(self, parent):
        self.parent = parent
        self.mapSeed = 0
        #initialise un joueur, pas de nom ou de ID encore
        self.myPlayer = Player("", -1, -1, -1, 0)
        self.playerList = []
        self.actionList = []


class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root=Tk()
        self.initJeu()#Pour la classe du Frame Jeu
       
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
        self.diplomatieFenetre()
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
        
        self.cadreJeu.pack()
        
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
        
    def imgLabelNourriture(self):
        print("")
        #labelNourritureImg=Label(self.cadreRessource,text="Nourriture: 200",relief=SOLID,width=15)
        #labelNourritureImg.grid(column=0,row=0)
        
    def imgLabelBois(self):
        print("")
        #labelBoisImg=Label(self.cadreRessource,text="Bois: 150",relief=SOLID,width=15)
        #labelBoisImg.grid(column=2,row=0)
        
    def imgLabelPierre(self):
        print("")
        #labelPierreImg=Label(self.cadreRessource,text="Pierre: 100",relief=SOLID,width=15)
        #labelPierreImg.grid(column=0,row=1)
        
    def imgLabelOr(self):
        print("")
        #labelOrImg=Label(self.cadreRessource,text="Or: 150",relief=SOLID,width=15)
        #labelOrImg.grid(column=2,row=1)
        
    def imgLabelEnergie(self):
        print("")
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
        
    def diplomatieFenetre(self):
        labelDiplomatie=Label(self.cadreDiplomatie,text="Diplomatie/Echange")
        labelDiplomatie.pack()
        
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
        
    def rafraichirTemps(self,temps):
        labelTemps=Label(self.cadreMiniMap,text="Temps: "+str(temps))
        labelTemps.grid(column=0,row=1)
        
class Controleur(): 
    def __init__(self):
        self.temps=0
        self.sl = ServerListener(self)
        self.m = model(self)
        self.nom=input("Votre nom, svp? ")
        self.m.myPlayer.name = self.nom;
        #cree une action avec le id=0 (login) et le nom du joueur
        self.action = Action(0, 1, self.nom, 0, 0, 0, 0, "")
        #envoi l'action du login
        self.sl.sendAndReceive(self.action)
        #request a seed from server
        self.action = Action(2, 0, "", 0, 0, 0, 0, "")
        #envoi l'action request seed
        self.sl.sendAndReceive(self.action)

        
        
        self.vue=Vue(self)
        self.vue.root.after(1000, self.tempsJeu())
        self.vue.root.mainloop()
    
    def tempsJeu(self):
        self.temps +=1
        self.vue.rafraichirTemps(self.temps)
        self.vue.root.after(1000,self.tempsJeu)
        

        
if __name__ == "__main__":
    c = Controleur()