
import client
import random
from Map import *
from modele_client import *
"""
POUR MODIFIER LA VALEUR DE TEMPS DE JEU AUQUEL LE CPU FAIT SES OPTIONS:
    - tout au bas de la page, au niveau du controleur:
        - changer la valeur int 7000 dans cette ligne:
               while (count < 7000):

    -plus la valeur est elever, plus le cpu aura le temps de cree des units, des maison et des tower
    -sa monnaie va monter d elle meme, pour verifier le changement d ere au bon moment
    cependant, les buildings et units ne coute rien en se moment..

"""
class Cpu(Joueur):
    def __init__(self, ID, posX, posY,parent):
        Joueur.__init__(self, ID, posX, posY)
        self.ressources = [0,0,0,0,0]
        self.villageoisParRessources = [0,0,0,0,0]
        self.nbCollecteurParRessourcesAuBesoin = [5,5,5,0,0]
        self.units = []
        self.nbVillageois = 0
        #nbTypeDeRessources = 3
        self.valeurRandom = random.randrange(2,6) * 20
        self.valeurRandomPosX = random.randrange(100,120)
        self.valeurRandomPosY = random.randrange(100,120)
        self.click = (self.valeurRandomPosX, self.valeurRandomPosY)
        # Index des ressources _Reminder
        # Nourriture          # index 0
        # bois                # index 1
        # roche               # index 3
        # or                  # index 4
        # energy              # index 5
        #//***************************************************************//
        #// integer are meant to easily switch from a state to another \ name are understood better
        self.balanced = 0
        self.offensive = 1
        self.defensive = 2
        self.mode = self.balanced
        self.cherchePosX = 0
        self.cherchePosY = 0
        self.positionVerifBool = False
        #ageDePierre = 1
        #ageContemporain = 2
        #ageModerne = 3
        #ageFutur = 4
        #ageCourrante = self.ageDePierre
        #changerErePossible = False

        self.food = 0
        self.wood = 0
        self.rock = 0
        self.gold = 0
        self.energy = 0
        self.ressourcesAuBesoin = [self.food, self.wood, self.rock, self.gold, self.energy]
        self.iteratorNumber = 1
        # these will be needed at the initializing
        #//***************************************************************
        self.m = Map(40,30)
        self.m.placeRessourcesOverworld()
        self.m.placeRessourcesUnderworld()
        self.verifVillageoisNonOccuper = False

    def chercherVillageoisNonOccuper(self):
        self.verifVillageoisNonOccuper = False
        for i in self.units:
            if i.type == "Villageois":
                if i.isMoving == False:
                    i.estSelectionner = True
                    self.verifVillageoisNonOccuper = True
                    # ou peut importe la function de selection

    def calculMaxUnit(self):
        #a deplacer vers modele client
        #appel la fonction a la construction et destruction d une maison
        self.maxUnitsCourrant = 10
        for i in self.buildings:
            if i.type=="Maison":
                self.maxUnitsCourrant += 10

    def printBatimentsPositions(self):
        NbMaison = 0
        NbTower = 0
        NbBarrack = 0
        print("Position de tout les buildings :")
        for i in self.buildings:
            print(" " + str(i.type) + " - : ( " + str(i.posX) + ", " + str(i.posY) + " )")
            if i.type == "Maison":
                 NbMaison += 1
            if i.type == "Tower":
                NbTower += 1
        print("Batiments:")
        print(" Tower: " + str(NbTower))
        print(" Maison: " + str(NbMaison))
    def balancementCaptif(self):
        # will be in a loop
        #print("Balancement:")
        # Do you have enought villagers?Do you have enough houses? Create more*/
        self.calculVillageois()
        self.calculMaxUnit()
        self.incrementationRessourcesTest()
        if self.nbVillageois < self.maxUnitsCourrant:
            if self.nbVillageois <= (10*self.nbTypeDeRessources) and self.mode != self.offensive:
                #changer pour que le towncenter fait le villageois
                self.nouveauUnit("villageois")
                """
                villageois = Villageois(self.ID,0,0,self.parent)
                self.units.append(villageois)
                """
            elif self.nbVillageois <= 5 and self.mode == self.offensive:
                #changer pour que le TownCenter fait le villageois
                self.nouveauUnit("villageois")
                """
                villageois = Villageois(self.ID,0,0,self.parent)
                self.units.append(villageois)
                """
            elif len(self.units) < self.maxUnits:
                #changer cette ligne pour que la barrack fait le guerrier
                self.nouveauUnit("guerrier")
                """
                guerrier = Guerrier(self.ID,0,0,self.parent)
                self.units.append(guerrier)
                """
        if len(self.units) > 0.75 * self.maxUnitsCourrant and self.maxUnitsCourrant < self.maxUnits:
            #print("Cherche Villageois non occuper -> construit maison") #(findUnoccupiedVillager().construire(?)
            self.verificationPosition(self.m.mat)
            self.chercherVillageoisNonOccuper()
            if self.verifVillageoisNonOccuper == True:
                maison = Maison(self.ID, self.cherchePosX, self.cherchePosY, self.parent)
                #changer pour que le villageois non occuper construit la maison a cette position
                self.buildings.append(maison)
                self.m.mat[self.cherchePosY][self.cherchePosX].passable = False
            else:
                if len(self.units) < self.maxUnitsCourrant:
                    self.nouveauUnit("villageois")
                    """
                    villageois = Villageois(self.ID,0,0,self.parent)
                    self.units.append(villageois)
                    """
        for i in range(self.nbTypeDeRessources):
            if self.villageoisParRessources[i] < self.nbCollecteurParRessourcesAuBesoin[i] :
                self.villageoisParRessources[i] += 1
        if len(self.buildings) %5 == 0:
            self.verificationPosition(self.m.mat)
            #self.creerJoueurBuilding("tower", self.cherchePosX, self.cherchePosY)

            tower = Tower(self.ID, self.cherchePosX, self.cherchePosY, self.parent)
            self.buildings.append(tower)


    def calculVillageois(self):
        self.nbVillageois = 0
        for i in (self.units):
            if i.type == "Villageois":
                self.nbVillageois += 1


    def verificationPosition(self, matrice): # m.mat
        self.iteratorNumber = 1
        self.positionVerifBool = False
        while self.iteratorNumber < 10 and self.positionVerifBool == False:
            for i in self.buildings:
                if matrice[i.posY + self.iteratorNumber][i.posX].isPassable() == True :
                    self.cherchePosY = i.posY + self.iteratorNumber
                    self.cherchePosX = i.posX
                    self.positionVerifBool = True

                elif matrice[i.posY - self.iteratorNumber][i.posX].isPassable() == True :
                    self.cherchePosY = i.posY - self.iteratorNumber
                    self.cherchePosX = i.posX
                    self.positionVerifBool = True

                elif matrice[i.posY][i.posX + self.iteratorNumber].isPassable() == True :
                    self.cherchePosY = i.posY
                    self.cherchePosX = i.posX + self.iteratorNumber
                    self.positionVerifBool = True

                elif matrice[i.posY][i.posX - self.iteratorNumber].isPassable() == True :
                    self.cherchePosY = i.posY
                    self.cherchePosX = i.posX - self.iteratorNumber
                    self.positionVerifBool = True

            if self.positionVerifBool == True:
                break

    def nouveauUnit(self, type): #"villageois" ou "guerrier"
        for i in self.buildings:
            if i.type == "TownCenter":

                self.valeurRandomPosX = random.randrange(100,120)
                self.valeurRandomPosY = random.randrange(100,120)
                self.click = (self.valeurRandomPosX + i.posX * 20 , self.valeurRandomPosY + i.posY * 20)
                self.creerUnit(type,self.valeurRandomPosX + i.posX*20, self.valeurRandomPosY + i.posY*20)



    def incrementationRessourcesTest(self):
        for i in range(self.nbTypeDeRessources):
            if self.ressources[i] < 100 :
                self.ressources[i] += 1


    def calculDistanceRessource(self):
        pass
    # cherche la ressource necessaire la plus proche dans la map
    # et envoie son villageois en ramasser avec sa fonction


    def Ere2(self):
        self.ageCourrante = self.ageContemporain
        self.nbTypeDeRessources = 4
        self.nbCollecteurParRessourcesAuBesoin[3] = 5
        for i in range(self.nbTypeDeRessources -1):
            self.ressources[i] -= 10
    def Ere3(self):
        self.ageCourrante = self.ageModerne
        self.nbTypeDeRessources = 5
        self.nbCollecteurParRessourcesAuBesoin[4] = 5
        for i in range(self.nbTypeDeRessources - 1):
            self.ressources[i] -= 10
    def Ere4(self):
        self.ageCourrante = self.ageFutur
        for i in range(self.nbTypeDeRessources - 1):
            self.ressources[i] -= 10


    def Decision(self):
        if self.valeurRandom > 0:
            self.valeurRandom -= 1
        else:
            #ajouter decision a cette endroit
            #print("Decision d action prise!")
            self.balancementCaptif()
            if self.ageCourrante != self.ageFutur:
                self.changerEre()
                print("food" + str(self.ressources[0]) + "wood" + str(self.ressources[1]) + "rock" + str(self.ressources[2]) + "gold" + str(self.ressources[3]) + "energy" + str(self.ressources[4]))
            self.valeurRandom = random.randrange(2,6)*20
        #print("Prochaine decision dans " + str(self.valeurRandom) + " ping !")

    def printUnitsQte(self):
        NbVillageois = 0
        NbGuerrier = 0
        self.calculMaxUnit()
        print("le max unit courrant est : " + str(c.cpu.maxUnitsCourrant))
        for i in self.units:
            if i.type == "Guerrier":
                NbGuerrier += 1
            if i.type == "Villageois":
                NbVillageois += 1
        print("Units:")
        print(" Guerrier: " + str(NbGuerrier))
        print(" Villageois: " + str(NbVillageois))

class Controleur():
    def __init__(self):
        self.cpu = Cpu(0, 15, 15, 0)
        self.townCenter = TownCenter(self.cpu.ID,15,15)
        self.cpu.m.mat[15][15].passable = False
        self.cpu.buildings.append(self.townCenter)
if __name__ == '__main__':
    c = Controleur()
    count = 0
    while (count < 7000):
        c.cpu.Decision()
        count += 1
    c.cpu.printBatimentsPositions()
    c.cpu.printUnitsQte()
    print("fin",c.cpu)





