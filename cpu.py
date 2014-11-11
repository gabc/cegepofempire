import modele_client
import random
"""
1- besoin de variable de selection estSelectionner sur les units
    ainsi on peut leur donner un ordre a eux simplement par la vÃƒÂ©rification dans la liste
    en ne verifiant que CETTE variable
2- besoin de verifier mes methodes a transferer vers le fichier ModuleObject
"""
class Cpu(modele_client.Joueur):
    def __init__(self, ID, posX, posY):
        modele_client.Joueur.__init__(self, ID, posX, posY)
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
        # these will be needed at the initializing
        #//***************************************************************


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


    def balancementCaptif(self):
        # will be in a loop
        print("Balancement:")
        # Do you have enought villagers?Do you have enough houses? Create more*/
        self.calculVillageois()
        self.calculMaxUnit()
        if self.nbVillageois < self.maxUnitsCourrant:
            if self.nbVillageois <= (5*self.nbTypeDeRessources) and self.mode != self.offensive:
                print("cree 1 villagoie!") #// ( select town center / build villager unit /  add unit to queu)
                u1 = modele_client.Villageois(0,0,0,0)
                self.units.append(u1)
            elif self.nbVillageois <= 5 and self.mode == self.offensive:
                print("cree 1 villagoie!") #// ( select town center / build villager unit /  add unit to queu)
                u1 = modele_client.Villageois(0,0,0)
                self.units.append(u1)
        if len(self.units) > 0.75 * self.maxUnitsCourrant and self.maxUnitsCourrant < self.maxUnits:
            print("Cherche Villageoi non occuper -> construit maison") #(findUnoccupiedVillager().construire(?)
            m1 = modele_client.Maison(0,100,100)
            self.buildings.append(m1)
        for i in range(self.nbTypeDeRessources):
            if self.villageoisParRessources[i] < self.nbCollecteurParRessourcesAuBesoin[i] :
                print("chercher un villageois non occuper")
                print("Villageoi-> cherche cette ressource") #self.selectedVillager.Find( RessourceTypesNeeded(i))
                self.villageoisParRessources[i] += 1
                #// function Find will take an int and search the needed resource to start //harvesting this resource (in case they cant see any of it yet
                #// Function FindUnoccupiedVillager will look up the list of villagers; which will need a
                #// Bool Occupied; if find ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œselect / if villagernotfound ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ create villager

    def calculVillageois(self):
        self.nbVillageois = 0
        for i in (self.units):
            if i.type == "Villageois":
                self.nbVillageois += 1

    def positionMaison(self):
        #besoin d un spot logique- trouver emplacement in range from base-fullground
        for i in self.batiments: # pour tout batiment MAISON
        #    if i.type = "maison": #REGARDE LES POSITION SUIVANTS CELLE DEJA UTILISEE
            if verificationPosition(i.PosX + 1 , i.PosY): # a droite
                modele_client.creationBuilding(i.PosX + 1 , i.PosY)
        #        elif verificationPosition(x -1, y): # a gauche
        #            create house there xy
        #        elif verificationPosition(x, y +1): # en haut
        #            create house there xy
        #        elif verificationPosition(x, y -1): # en bas
        #            create house there xy
        # search in distance x1-x2 and y1-y2 if theres any spot free in a small range from townCenter
            # if True, create house at this spot

    def verificationPosition(self, PosX, PosY):
        pass # a transferer.. OU?
        # for all cases x,y used by the specific building sizes x,y :
            # if case.passable == True :
                # if case.type == "Ground" :
                   # return True

    # a transferer vers ModuleObject..
    def changerEre(self):
        self.changerEreVerif()
        if self.changerErePossible == True:
            if self.ageCourrante == self.ageDePierre:
                self.Ere2()
            elif self.ageCourrante == self.ageContemporain:
                self.Ere3()
            elif self.ageCourrante == self.ageModerne:
                self.Ere4()
            print(" changement d'ere reussi ")
        print("age courante est " + str(self.ageCourrante))

    # a transferer vers moduleObject...
    def changerEreVerif(self):
        for i in range(self.nbTypeDeRessources):
            if self.ressources[i] > 10:
                self.changerErePossible = True
                print("peut changer d'ere ! ")


    def changerAllies(self):
        pass
# le cpu ne va que s'allier a d'autre cpu pour detruire un autre joueur
# ou meme d'autre cpu, ceux ci ne vont se separer qu'en difficulter
# sinon , ils travail en equipe et s'entraide en defensive/offensive

    def calculDistanceRessource(self):
        pass
    #si la ressource est bien lointaine, faire une base
    #de recuperation de ressource plus pres de celles-ci.


    def Ere2(self):
        self.ageCourrante = self.ageContemporain
        self.nbTypeDeRessources = 4
        self.nbCollecteurParRessourcesAuBesoin[3] = 5

    def Ere3(self):
        self.ageCourrante = self.ageModerne
        self.nbTypeDeRessources = 5
        self.nbCollecteurParRessourcesAuBesoin[4] = 5

    def Ere4(self):
        self.ageCourrante = self.ageFutur



    def Decision(self):
        print("in decision")
        if self.valeurRandom > 0:
            self.valeurRandom -= 1
        else:
            #ajouter decision a cette endroit
            print("Decision d action prise!")
            self.balancementCaptif()
            self.valeurRandom = random.randrange(2,6)*20
        print("Prochaine decision dans " + str(self.valeurRandom) + " ping !")




class Controleur():
    def __init__(self):
        self.cpu = Cpu(0, 0, 0)

if __name__ == '__main__':
    c = Controleur()
    count = 0
    while (count < 10000):
        c.cpu.Decision()
        count += 1
    c.cpu.calculVillageois()
    print("le nombre de villageois est : " + str(c.cpu.nbVillageois))
    c.cpu.calculMaxUnit()
    print("le max unit courrant est : " + str(c.cpu.maxUnitsCourrant))
    print("fin",c.cpu)





