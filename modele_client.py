import math
import timeit
from utils import *
from helper import *
from deplacement import *
class Joueur():
    def __init__(self, parent, ID, name):
        self.parent = parent
        self.name = name
        self.ID = ID
        self.currentTime = 0
        self.ere = 1
        self.maxUnits = 200
        self.maxUnitsCourrant = 0
        # Index des ressources:
        # Nourriture : 0
        # Bois: 1
        # Pierre : 2
        # Or : 3
        # Energie : 4
        self.ressources = {0 : 10,
                           1 : 20,
                           2 : 30,
                           3 : 40,
                           4 : 50}
        self.playerColor = None
        self.nbTypeDeRessources = 3
        self.ageDePierre = 1
        self.ageContemporain = 2
        self.ageModerne = 3
        self.ageFutur = 4
        self.ageCourrante = self.ageDePierre
        self.changerErePossible = False
        self.allies = []
        self.units =[]
        self.buildings =[]
        self.objectsSelectionne =[]
        self.actions={"envoieRess":self.envoyerRessources}

    def metToiAJour(self):
        for u in self.units:
            u.faitAction()
        for b in self.buildings:
            b.faitAction()

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
        self.changerErePossible = False


    def changerEreVerif(self):
        if self.ageCourrante != self.ageFutur:
            for i in range(self.nbTypeDeRessources):
                if self.ressources[i] > 10:
                    self.changerErePossible = True
                    print("peut changer d'ere ! ")

    def Ere2(self):
        self.ageCourrante = self.ageContemporain
        self.nbTypeDeRessources = 4
        for i in range(self.nbTypeDeRessources):
            self.ressources[i] -= 10



    def Ere3(self):
        self.ageCourrante = self.ageModerne
        self.nbTypeDeRessources = 5
        for i in range(self.nbTypeDeRessources):
            self.ressources[i] -= 10


    def Ere4(self):
        self.ageCourrante = self.ageFutur
        for i in range(self.nbTypeDeRessources):
            self.ressources[i] -= 10

    def construireBuilding(self, idBuilding, posX ,posY ):
        pass

    def creerUnit(self, type, x, y):
        if type == "villageois":
            self.units.append(Villageois(self.ID, x, y,self))
        elif type == "guerrier":
            self.units.append(Guerrier(self.ID, x, y,self))

    def creerJoueurBuilding(self, type, x, y):
        if type == "tower":
            self.buildings.append(Tower(self.ID, x, y,self))
            self.parent.m.placeBuilding(x,y,"tower")
        if type == "barrack":
            self.buildings.append(Barrack(self.ID, x, y,self))
            self.parent.m.placeBuilding(x,y,"barrack")

    def changerAllies():
        pass

    #toute les ressources
    def envoyerRessources(self,a,b,c,d,e,f):
        print(a,b,c,d,e,f)

    def deplaceUnit(self, unit, arrive):
        idunit = unit[1]
        for u in self.units:
            if u.id == idunit:
                #print(arrive)
                u.status="deplace"
                u.deplacer(self.parent.deplaceur, arrive)
                u.target=arrive

id_objet = 0

class Unit():
    def __init__(self, ownerID, posX, posY,parent):
        global id_objet
        #le global fait en sorte que partout dans la page la variable id_objet
        #est garder MEME DANS LES AUTRE FONCTIONS QUI SONT ENFANT DE LEMPLACEME
        # DE LA VARIABLE: NE PAS REUTILISER
        id_objet += 1

        self.id = id_objet
        self.ownerID = ownerID

        self.type = "Unit"
        self.deplaceur = None
        #le hp d'un unit generique est -1
        self.hpMax = -1
        self.hpActuel = self.hpMax
        self.posX = posX
        self.posY = posY
        #le champs de vision est arbitraire et devrait dependre du type du Unit
        self.champDeVision = -1
        #idem pour le delai de Construction
        self.delaiDeConstruction = -1
        self.chemin = []
        self.parent=parent
        self.target=(self.posX, self.posY)
        self.status="waiting"


    def faitAction(self):
        if self.chemin:         # S'il a un chemin. Qu'il se deplace.
            self.deplacer(self.deplaceur, self.chemin)

    def isAlive(self):
        if self.hpActuel <= 0:
            return False
        else:
            return True


    def recevoirDegats(self, degatsRecus):
        if degatsRecus >= self.hpActuel:
            self.hpActuel = 0
            print("Unite mort")
        else :
            self.hpActuel -= degatsRecus

    def effectueDeplacement(self, arrive):
        ax, ay = trouvePixel(arrive.x, arrive.y)
        if self.posX > ax:
            self.posX -= self.vitesseX
        if self.posX < ax:
            self.posX += self.vitesseX

        if self.posY > ay:
            self.posY -= self.vitesseY
        if self.posY < ay:
            self.posY += self.vitesseY

class Villageois(Unit):
    def __init__(self,ownerID, posX, posY,parent):
        Unit.__init__(self,ownerID, posX, posY,parent)

        self.type = "Villageois"
        self.isMoving = False
        #j'ai decider arbitrairement de l'hp: a modifier
        #dautres variables arbitraires yee!!
        self.champDeVision = 50
        self.delaiDeConstruction =20000
        self.hpMax = 100
        self.hpActuel = self.hpMax
        self.isSelected = False ##add

        #j'imagine qu'ils veulent dire le temps en millisecondes : arbitraire
        self.collectionRate = 1
        self.collectionMax = 100
        self.collectionActuel = 0
        self.collectionType = 0
        self.currentRes=(0,0)

        self.vitesseX = 5
        self.vitesseY = 5

        #for testing purposes
        self.i=0

    def faitAction(self):
        if self.chemin:         # S'il a un chemin. Qu'il se deplace.
            self.deplacer(self.deplaceur, self.chemin)

        elif self.status is not "waiting":    #Sinon check son target si tu n'attend pas
            self.checkArrive(self.target, self.parent.parent.m)

        if self.status=="backToBase":
            self.deplacer(self.deplaceur, self.getTownCenterCoords())

        elif self.status=="atBase" and self.currentRes is not (0,0):          
            self.deplacer(self.deplaceur, self.currentRes)
            self.status="backToRes"

    def getTownCenterCoords(self):
        for b in self.parent.buildings:
            if b.type=="TownCenter":
                x=b.posX
                y=b.posY
                break
        return(x,y)

    def recolteRessource(self, case):
        if self.collectionActuel ==self.collectionMax:
            self.status="backToBase"
            print("Villager", self.id, "has a full inventory")
        elif case.nbRessource > 0:
            case.nbRessource-=self.collectionRate
            self.collectionActuel+=self.collectionRate
            self.collectionType=case.ressource
            self.currentRes=(case.posX, case.posY)
            #print("resource left: ", case.nbRessource)
            if case.nbRessource == 0:
                self.parent.parent.m.toDelete.append(case)
                case.ressource='-'
                case.passable=True;
                self.status="backToBase"
                print

        return case

    def checkArrive(self, target, game_map):
        self.i+=1
        #print(self.i)
        arrive=game_map.mat[target[0]][target[1]]

        x, y = trouveCase(self.posX, self.posY)
        townXY=self.getTownCenterCoords()

        #Si il est dans le range de 1 case de son arrivee
        if (x >= arrive.posX - 1 and x <= arrive.posX + 1) and (y >= arrive.posY - 1 and y <= arrive.posY + 1):           
        #Si t'est arrive a un town center, dump cque t'as       
            if arrive.posX==townXY[0] and arrive.posY==townXY[1]:
                self.dumpRessources()
                self.status="atBase"
            #Si la case n'a pas de ressources
            elif arrive.ressource=='-':
                print("This space has no ressources")
                self.status="waiting"
            else: 
                self.status="collecting"
                arrive=self.recolteRessource(arrive)
                game_map.mat[arrive.posX][arrive.posY]=arrive

    def deplacer(self, deplaceur, arrive):
        cx, cy = trouveCase(self.posX, self.posY)
        if self.chemin is None or self.chemin == []:
            self.deplaceur = deplaceur
            self.chemin = deplaceur.chemin(self, arrive)
        else:
            if (cx == self.chemin[0].x) and (cy == self.chemin[0].y):
                del self.chemin[0]
            if self.chemin:
                self.effectueDeplacement(self.chemin[0])

    def dumpRessources(self):
        #check s'il a vraiment des ressources a dump avant de dump
        if self.collectionActuel > 0:
            print("Villager",self.id,"dumped",int(self.collectionActuel/10),"ressources at base" )
            c = int(self.collectionType)
            self.parent.ressources[c]+=int(self.collectionActuel/10)
            self.collectionActuel = 0
            

class Guerrier(Unit):
    def __init__(self, ownerID, posX, posY, parent):
        Unit.__init__(self, ownerID,posX,posY, parent)
        self.type = "Guerrier"


        #Arbitraire
        self.champDeVision = 50
        self.delaiDeConstruction = 20000
        self.hpMax =100
        self.hpActuel = self.hpMax
        self.range = 1 #melee
        self.atkSpeed = 50 #en millisecondes
        self.cooldown= 20
        self.maxCooldown = 20
        self.defense = 1
        self.vitesseX = 5
        self.vitesseY = 5
        self.champDaggro = 5
        self.degat = 10
        self.actionEnCours = None
        self.targetedBy = None
        self.unitCible = None
        self.unitCibleType = None
        self.unitCiblePosCase = None


    def faitAction(self):
        if len(self.chemin) != 0:
            self.deplacer(self.deplaceur, self.chemin)
        if self.actionEnCours == None:
            self.actionEnCours = "scanEnemy"
            print(self.actionEnCours)
        elif self.actionEnCours == "scanEnemy":
            self.scanEnemy()
            print(self.actionEnCours)
        elif self.actionEnCours == "marcheVersEnemy":
            self.marcheVersEnemy()
            print(self.actionEnCours)
        elif self.actionEnCours == "attaqueCible":
            self.attaqueCible()
            print(self.actionEnCours)

        if self.cooldown != self.maxCooldown:
            self.cooldown += 1
        if self.hpActuel  ==0:
            del self


    def scanEnemy(self):
            if len(self.chemin) ==0:
                for i in self.parent.parent.modele.joueurs.values():# il faut reussir a avoir la liste des unite
                  for n in i.units:
                        if n.ownerID is not self.ownerID:
                            caseGx, caseGy = trouveCase(self.posX,self.posY)
                            caseNx, caseNy =trouveCase(n.posX, n.posY)
                            if Helper.calcDistance(caseGx, caseGy , caseNx, caseNy) <= self.champDaggro:
                                self.unitCible = n
                                self.actionEnCours = "marcheVersEnemy"
                                self.unitCibleType = "Unit"
                                self.unitCiblePosCase = (caseNx, caseNy)
                                self.unitCible.targetedBy = self
                                break

    def attaqueCible(self):
        if self.unitCible.isAlive() == True:
            caseGx, caseGy = trouveCase(self.posX,self.posY)
            caseNx, caseNy =trouveCase(self.unitCible.posX, self.unitCible.posY)

            if Helper.calcDistance(caseNx, caseNy, caseGx, caseGy) <= self.range:
                if self.cooldown == self.maxCooldown:
                    self.unitCible.recevoirDegats(self.degat)
                    self.cooldown = 0
            elif Helper.calcDistance(caseGx, caseGy, caseNx, caseNy) <= self.champDaggro and Helper.calcDistance(caseGx, caseGy, caseNx, caseNy) >= self.range:
                self.actionEnCours = "marcheVersEnemy"
            else:
                self.actionEnCours ="scanEnemy"
                self.unitCibleType = None
        else:
            self.actionEnCours="scanEnemy"
            self.unitCibleType = None

    def marcheVersEnemy(self):
        if self.unitCibleType == "Unit":
            caseGx, caseGy = trouveCase(self.posX,self.posY)
            caseNx, caseNy =trouveCase(self.unitCible.posX, self.unitCible.posY)

        if Helper.calcDistance(caseGx, caseGy, caseNx, caseNy) <= self.champDaggro and Helper.calcDistance(caseGx, caseGy, caseNx, caseNy) >= self.range:         # S'il a un chemin. Qu'il se deplace.
            print("il a un chemin")
            #self.deplaceUnit(self, (caseNx, caseNy))
            self.deplacer(self.parent.parent.deplaceur, (caseNx, caseNy))
        elif Helper.calcDistance(caseNx, caseNy, caseGx, caseGy) <= self.range and self.unitCibleType == "Unit":
            print("il n'a pas un chemin")
            self.actionEnCours = "attaqueCible"




    def recevoirDegats(self, degatsRecus):
        if degatsRecus -self.defense > self.hpActuel:
            self.hpActuel = 0
        else :
            self.hpActuel -= degatsRecus -self.defense

    def deplacer(self, deplaceur, arrive):
        cx, cy = trouveCase(self.posX, self.posY)
        if self.chemin is None or self.chemin == []:
            self.deplaceur = deplaceur
            self.chemin = deplaceur.chemin(self, arrive)
        else:
            if (cx == self.chemin[0].x) and (cy == self.chemin[0].y):
                del self.chemin[0]
            if self.chemin:
                self.effectueDeplacement(self.chemin[0])



class Building():

    def __init__(self, ownerID, posX, posY, parent):
        self.parent = parent
        global id_objet
        id_objet += 1
        self.id = id_objet
        self.ownerID = ownerID

        self.type = "Building"

        #le hp d'un building generique est -1
        self.hpMax = -1
        self.hpActuel = self.hpMax
        self.posX = posX
        self.posY = posY
        #le champs de vision est arbitraire et devrait dependre du type du Unit
        self.champDeVision = -1
        #idem pour le delai de Construction
        self.delaiDeConstruction = -1

    def faitAction(self):
        pass

    def isAlive(self):
        if self.hpActuel <= 0:
            return False
        else:
            return True


    def recevoirDegats(self, degatsRecus):
        if degatsRecus > self.hpActuel:
            self.hpActuel = 0
            print("je me meurs et je suis un :",self.type, ", appartenant a :", self.ownerID)
        else :
            self.hpActuel -= degatsRecus


class TownCenter(Building):
    """ bref Desc des fonctions:
        uniteCreable(self) -- retourne la liste d'unite creable en String
        ( sinon en objet Unit specifique)

        createUnit(self, Unit)-- a besoin d'un objet unit : place l'Unit dans
        la liste creationQueue et change la variable tempsRestant pour le
        delaiDeConstruction de l'Unit dans l'index 0 -
        -- retourne True si la queue est pas pleine et false si la queue est
        pleine--

        unitSortir(self) -- fait en sorte de pop la premiere Unit de la queue du
        building, retourne le unit en sois et met le tempsRestant egal au
        prochain sil y en a
        ps. ceci ne prend pas en arguments le tempsRestant mais pourrait en
        dependre

        les deux methodes font en sorte que la queue soit FIFO( first in, first out)



    """


    def __init__(self, ownerID, posX, posY):
        Building.__init__(self, ownerID, posX, posY, self)
        self.type ="TownCenter"
        #valeurs arbitraires
        self.hpMax = 1000
        self.hpActuel = self.hpMax
        self.longueur = 100
        self.largeur = 100
        self.delaiDeConstruction = 20000
        self.champDeVision = 50


        #Variables specifique au TownCenter
        self.uniteCreable = [Villageois]
        self.creationQueue = []
        self.tempsRestant = 0

    def uniteCreable(self):
        return self.uniteCreable

    def createUnit(self, Unit):

        if len(self.creationQueue) < 5:
            self.creationQueue.insert(1,Unit)
        else:
            print("la queue est pleine")
            return False

        if self.creationQueue[0] == Unit:
            self.tempsRestant = Unit.delaiDeConstruction

        return True

    def unitSortir(self):
        # a appeler quand le temps Restant atteint 0
        UnitCree = None
        if len(self.creationQueue) != 0:
            UnitCree = self.creationQueue[0]
            self.creationQueue.pop(0)
            self.tempsRestant =0
            # creer l'objet dans le canvas I guess
        else:
            return false

        if len(self.creationQueue) !=0:
            self.tempsRestant = self.creationQueue[0].delaiDeConstruction


        return UnitCree

    def annulationUnit(self):
        if len(self.creationQueue != 0):
            self.creationQueue.pop()
            return True
        else :
            return False

class Maison(Building):
    def __init__(self, ownerID, posX, posY, parent):
        Building.__init__(self, ownerID,posX,posY, parent)
        self.type="Maison"

        self.hpMax = 700
        self.hpActuel = self.hpMax
        self.longueur = 100
        self.largeur = 100
        self.delaiDeConstruction = 10000

class Barrack(Building):
    def __init__(self, ownerID, posX, posY, parent):
        Building.__init__(self, ownerID, posX, posY, parent)
        self.type="Barrack"

        self.hpMax = 1000
        self.hpActuel = self.hpMax

        self.longueur = 100
        self.largeur = 100
        self.delaiDeConstruction = 20000
        self.champDeVision = 50

        self.uniteCreable = [Guerrier]
        self.creationQueue = []
        self.tempsRestant = 0

    def uniteCreable(self):
        return self.uniteCreable

    def createUnit(self, Unit):

        if len(self.creationQueue) < 5:
            self.creationQueue.insert(1,Unit)
        else:
            print("la queue est pleine")
            return False

        if self.creationQueue[0] == Unit:
            self.tempsRestant = Unit.delaiDeConstruction

        return True

    def unitSortir(self):
        # a appeler quand le temps Restant atteint 0
        UnitCree = None
        if len(self.creationQueue) != 0:
            UnitCree = self.creationQueue[0]
            self.creationQueue.pop(0)
            self.tempsRestant =0
            # creer l'objet dans le canvas I guess
        else:
            return false

        if len(self.creationQueue) !=0:
            self.tempsRestant = self.creationQueue[0].delaiDeConstruction


        return UnitCree

    def annulationUnit(self):
        if len(self.creationQueue != 0):
            self.creationQueue.pop()
            return True
        else :
            return False

# modifier le 11/11/2014
class Tower(Building):
    def __init__(self, ownerID, posX, posY, parent):
        Building.__init__(self, ownerID, posX, posY, parent)
        self.type = "Tower"
        self.hpMax = 400
        self.hpActuel = self.hpMax
        self.longueur = 20
        self.largeur = 20
        self.delaiDeConstruction = -1
        self.champDeVision = -1
        self.champDaggro = 5
        self.target=None
        self.typeTarget =None
        self.targetedBy = None
        self.actionEnCours = "scanEnemy" # Comme ça. Pas besoin de if :D
        self.degat = 50
        self.cooldown = 30
        self.cooldownMax = self.cooldown


    def attaqueCible(self):
        if self.target.isAlive() == True:
            if self.typeTarget == "Building":
                if Helper.calcDistance(self.target.posX, self.target.posY, self.posX, self.posY) <= self.champDaggro:
                    if self.cooldown == self.cooldownMax:
                        self.target.recevoirDegats(self.degat)
                        self.cooldown = 0
            elif self.typeTarget == "Unit":
                caseNx, caseNy =trouveCase(self.target.posX,self.target.posY)
                if Helper.calcDistance(caseNx, caseNy, self.posX, self.posY) <= self.champDaggro:
                    if self.cooldown == self.cooldownMax:
                        self.target.recevoirDegats(self.degat)
                        print("Hp de la cible: ",self.target.hpActuel)
                        print("la cible est morte ? : ", self.target.isAlive())
                        self.cooldown = 0



            else:
                self.actionEnCours ="scanEnemy"
                self.unitCibleType = None
        else:
            self.actionEnCours="scanEnemy"
            self.unitCibleType = None





    def scanEnemy(self):
        if self.targetedBy and target is None:
            self.target = self.targetedBy
            self.attaqueCible(targetedBy)
        else:
            for i in self.parent.parent.modele.joueurs.values():# il faut reussir a avoir la liste des unite
                for n in i.units:
                    if n.ownerID is not self.ownerID and n.isAlive() == True:
                        caseNx, caseNy = trouveCase(n.posX, n.posY)
                        if Helper.calcDistance(self.posX, self.posY , caseNx, caseNy) <= self.champDaggro:
                            self.target = n
                            self.typeTarget = "Unit"
                            self.actionEnCours = "attaqueCible"
                            break
            for i in self.parent.parent.modele.joueurs.values():
                for n in i.buildings:
                    if n.ownerID is not self.ownerID and n.isAlive() == True:
                        if Helper.calcDistance(self.posX, self.posY , n.posX, n.posY) <= self.champDaggro:
                            self.target = n
                            self.typeTarget = "Building"
                            self.actionEnCours = "attaqueCible"
                            break


    def faitAction(self):
        getattr(self, self.actionEnCours)()

        if self.cooldown != self.cooldownMax:
            self.cooldown += 1
        if self.hpActuel  ==0:
            del self





#





class Modele(object):
    id=0
    def nextId():
        Modele.id=Modele.id+1
        return Modele.id

    def __init__(self,parent):
        self.parent=parent
        self.unites=[]
        self.actionsAFaire={}
        self.joueurs = {} # = Joueur(0, "test")
        self.actions = {"creerUnite" : self.creerUnite,
                        "deplace" : self.deplaceUnite,
                        "creerBuilding": self.creerBuilding,}

    def initPartie(self,listeNomsJoueurs):
        n=0
        self.playerColors = ["blue", "green", "yellow", "purple", "brown", "black", "white", "orange", "pink"]
        #init tous les joueur avec leur unite, batiments, etc...
        print("Nombre total de joueurs: ", len(listeNomsJoueurs))
        for j in listeNomsJoueurs:
            self.joueurs[j] = Joueur(self.parent, n, j)
            self.joueurs[j].playerColor = self.playerColors[n]
            print("joueur: ", j, " - color", self.joueurs[j].playerColor)
            if j == self.parent.nom:
                self.parent.myPlayer = self.joueurs[j]
                print("My player color", self.joueurs[j].playerColor)
            n += 1


    def creerUnite(self, args):
        self.joueurs[args[0]].creerUnit(args[2][0], args[2][1], args[2][2])
        self.joueurs[args[0]].maxUnitsCourrant+=1


    def deplaceUnite(self, args):
        self.joueurs[args[0]].deplaceUnit(args[2][0],args[2][1])

    def creerBuilding(self, args):
        print(args)
        self.joueurs[args[0]].creerJoueurBuilding(args[2][0], args[2][1], args[2][2])

    def prochaineAction(self,cadre):
        if cadre in self.actionsAFaire.keys():
            for action in self.actionsAFaire[cadre]:
                self.actions[action[1]](action)
            del self.actionsAFaire[cadre]
        # Mise a jour:
        for j in self.joueurs.keys():
            self.joueurs[j].metToiAJour()



