
import client
import random
from Map import *
from modele_client import *
"""
A LIRE:
    TEST POSSIBLE:
        1- VERIFICATION A CHAQUE nb X de tic A PRENDRE UNE DECISION
        2- ENGAGE UN VILLAGEOIS  J USQU A UN NOMBRE DE 5 x NOMBRE DE RESSOURCES NECESSAIRE SELON L AGE COURRANT
        3- CONSTRUCTION DE MAISON LORQUE LE NOMBRE DE VILLAGEOIS ATTEINT 75/100 DU MAX UNITS COURRANT
        4- LA CONSTRUCTION DES BATIMENTS SE FONT TOUS SUR DES CASES PASSABLE- ET METTE CES CASE IMPASSABLE

tout cela fonctionne theoriquement. je n ai pas fait de tests ultime mais tout semble fonctionnel
ps- les print sont deja present alors faite le rouler.

pour une plus ample comprehension: verifier ce que le controleur fait.
ctrl-f : balancementCaptif
ctrl-f : Decision
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

    def chercherVilagoisNonOccuper(self):
        for i in self.units:
            if i.type == "Villageois":
                if i.occuper == False:
                    i.estSelectionner = True
                    # ou peut importe la function de selection

    def calculMaxUnit(self):
        #a deplacer vers modele client
        #appel la fonction a la construction et destruction d une maison
        self.maxUnitsCourrant = 10
        for i in self.buildings:
            if i.type=="Maison":
                self.maxUnitsCourrant += 10

    def printBatimentsPositions(self):
        print("Position de tout les buildings :")
        for i in self.buildings:
            print( str(i.type) + " - : ( " + str(i.posX) + ", " + str(i.posY) + " )")

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
                villageois = Villageois(self.ID,0,0,0)
                self.units.append(villageois)
            elif self.nbVillageois <= 5 and self.mode == self.offensive:
                #changer pour que le TownCenter fait le villageois
                villageois = Villageois(self.ID,0,0)
                self.units.append(villageois)
            else:
                #changer cette ligne pour que la barrack fait le guerrier
                guerrier = Guerrier(self.ID,0,0)
                self.units.append(guerrier)
        if len(self.units) > 0.75 * self.maxUnitsCourrant and self.maxUnitsCourrant < self.maxUnits:
            #print("Cherche Villageois non occuper -> construit maison") #(findUnoccupiedVillager().construire(?)
            self.verificationPosition(self.m.mat)
            maison = Maison(self.ID, self.cherchePosX, self.cherchePosY, self.parent)
            #changer pour que le villageois non occuper construit la maison a cette position
            self.buildings.append(maison)
            self.m.mat[self.cherchePosY][self.cherchePosX].passable = False
        for i in range(self.nbTypeDeRessources):
            if self.villageoisParRessources[i] < self.nbCollecteurParRessourcesAuBesoin[i] :
                self.villageoisParRessources[i] += 1
        if self.buildings.count %5 == 0:
            self.verificationPosition(self.m.mat)
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
                    print("fait le batiment en haut de : " + i.type)
                    self.cherchePosY = i.posY + self.iteratorNumber
                    self.cherchePosX = i.posX
                    self.positionVerifBool = True

                elif matrice[i.posY - self.iteratorNumber][i.posX].isPassable() == True :
                    print("fait le batiment en bas de : " + i.type)
                    self.cherchePosY = i.posY - self.iteratorNumber
                    self.cherchePosX = i.posX
                    self.positionVerifBool = True

                elif matrice[i.posY][i.posX + self.iteratorNumber].isPassable() == True :
                    print("fait le batiment a droite de : " + i.type)
                    self.cherchePosY = i.posY
                    self.cherchePosX = i.posX + self.iteratorNumber
                    self.positionVerifBool = True

                elif matrice[i.posY][i.posX - self.iteratorNumber].isPassable() == True :
                    print("fait le batiment a gauche de : " + i.type)
                    self.cherchePosY = i.posY
                    self.cherchePosX = i.posX - self.iteratorNumber
                    self.positionVerifBool = True

            if self.positionVerifBool == True:
                break





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
        for i in range(self.nbTypeDeRessources):
            self.ressources[i] -= 10
    def Ere3(self):
        self.ageCourrante = self.ageModerne
        self.nbTypeDeRessources = 5
        self.nbCollecteurParRessourcesAuBesoin[4] = 5
        for i in range(self.nbTypeDeRessources):
            self.ressources[i] -= 10
    def Ere4(self):
        self.ageCourrante = self.ageFutur
        for i in range(self.nbTypeDeRessources):
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
            self.valeurRandom = random.randrange(2,6)*200
        #print("Prochaine decision dans " + str(self.valeurRandom) + " ping !")



class Controleur():
    def __init__(self):
        self.cpu = Cpu(0, 15, 15, 0)
        self.townCenter = TownCenter(self.cpu.ID,15,15)
        self.cpu.m.mat[15][15].passable = False
        self.cpu.buildings.append(self.townCenter)
if __name__ == '__main__':
    c = Controleur()
    count = 0
    while (count < 50000):
        c.cpu.Decision()
        count += 1
    c.cpu.calculVillageois()
    print("le nombre de villageois est : " + str(c.cpu.nbVillageois))
    c.cpu.calculMaxUnit()
    print("le max unit courrant est : " + str(c.cpu.maxUnitsCourrant))
    c.cpu.printBatimentsPositions()
    print("fin",c.cpu)





