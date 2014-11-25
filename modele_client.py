import deplacement
import math
import timeit
from utils import *
from helper import *

class Joueur():
    def __init__(self, parent, ID, name):
        self.parent = parent
        self.name = name
        self.ID = ID
        self.currentTime = 0
        self.ere = 1
        self.maxUnits = 200
        self.maxUnitsCourrant = 10
        self.ressources = [10,20,30,40,50]
        self.playerColor = None
        # Index des ressources:
        # Nourriture : 0
        # Bois: 1
        # Pierre : 2
        # Or : 3
        # Energie : 4
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
        self.status="spawned"


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
        self.collectionRate = 3000
        self.collectionMax = 25
        self.collectionActuel = 0

        self.vitesseX = 5
        self.vitesseY = 5

    def faitAction(self):
        if self.chemin:         # S'il a un chemin. Qu'il se deplace.
            self.deplacer(self.deplaceur, self.chemin)
        elif self.status is not "spawned":    #Sinon check son target si il ne viens pas juste de spawn
            self.checkArrive(self.target, self.parent.parent.m)

        if self.status=="return":
            self.deplacer(self.deplaceur, self.getTownCenterCoords())
            self.status="waiting"

    def getTownCenterCoords(self):
        for b in self.parent.buildings:
            if b.type=="TownCenter":
                x=b.posX
                y=b.posY
                break
        return(x,y)

    def recolteRessource(self, case):
        if self.collectionActuel ==self.collectionMax:
            self.status="return"
            print("retour d'un villageois")
        elif case.nbRessource > 0:
            case.nbRessource-=1
            self.collectionActuel+=1
            print(self.collectionActuel)
            print(self.id, "resource left: ", case.nbRessource)
            if case.nbRessource == 0:
                self.parent.parent.m.toDelete.append(case)
                case.ressource='-'
                case.passable=True;
                self.status="return"

        return case

    def checkArrive(self, target, game_map):
        #check si le target est en pixels ou en cases de jeu
        if target[0] > game_map.largeur and target[1] > game_map.hauteur:
            arrive=game_map.mat[math.trunc(target[0]/self.parent.parent.vue.longeurLigne)][math.trunc(target[1]/self.parent.parent.vue.longeurLigne)]
        else:
            arrive=game_map.mat[target[0]][target[1]]

        x, y = trouveCase(self.posX, self.posY)

        #Si il est dans le range de 1 case de son arrivee
        if (x >= arrive.posX - 1 and x <= arrive.posX + 1) and (y >= arrive.posY - 1 and y <= arrive.posY + 1):
            if arrive.ressource is not "-":
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

class Guerrier(Unit):
    def __init__(self, ownerID, posX, posY, parent):
        Unit.__init__(self, ownerID,posX,posY, parent)
        self.type = "Guerrier"


        #Arbitraire
        self.champDeVision = 50
        self.delaiDeConstruction = 20000
        self.hpMax =100
        self.hpActuel = self.hpMax
        self.range = 10 #melee
        self.atkSpeed = 50 #en millisecondes
        self.cooldown= 20
        self.maxCooldown = 20
        self.defense = 1
        self.vitesseX = 5
        self.vitesseY = 5
        self.champDaggro = 30
        self.degat = 10
        self.actionEnCours = None
        self.targetedBy = None
        self.unitCible = None


    def faitAction(self):
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
        elif self.chemin:
            self.deplacer(self.deplaceur, self.chemin)

        if self.cooldown != self.maxCooldown:
            self.cooldown += 1
        if self.hpActuel  ==0:
            del self
            print ("je  suis mort")

    def scanEnemy(self):
            if self.chemin:
                self.deplacer(self.deplaceur, self.chemin)
            if self.targetedBy and self.unitCible is None:
                self.unitCible = self.targetedBy
                self.attaqueCible(self.targetedBy)
            else:
                for i in self.parent.parent.modele.joueurs.values():# il faut reussir a avoir la liste des unite
                  for n in i.units:
                        if n.ownerID is not self.ownerID:
                            if Helper.calcDistance(self.posX, self.posY , n.posX, n.posY) <= self.champDaggro:
                                self.unitCible = n
                                self.actionEnCours = "marcheVersEnemy"
                                #self.chemin[0].x = n.posX a modifier asap 18/11/2014
                                #self.chemin[0].y = n.posY
                                break

    def attaqueCible(self):
        if self.unitCible.isAlive():
            if Helper.calcDistance(self.unitCible.posX, self.unitCible.posY, self.posX, self.posY) <= self.range:
                if self.cooldown == self.maxCooldown:
                    self.unitCible.recevoirDegats(self.degat)
                    self.cooldown = 0
            elif Helper.calcDistance(self.unitCible.posX, self.unitCible.posY, self.posX, self.posY) <= self.champDaggro and Helper.calcDistance(self.unitCible.posX, self.unitCible.posY, self.posX, self.posY) >= self.range:
                self.actionEnCours = "marcheVersEnemy"
            else:
                self.actionEnCours ="scanEnemy"
        else:
            self.actionEnCours="scanEnemy"

    def marcheVersEnemy(self):
        if self.chemin:         # S'il a un chemin. Qu'il se deplace.
            self.deplacer(self.deplaceur, self.chemin)
        elif self.unitCible.isAlive() and self.chemin is None:
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
#                self.chemin[0].x = self.target[0]
#                self.chemin[0].y = self.target[1]


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
    def __init__(self, ownerID, posX, posY):
        Building.__init__(self, ownerID,posX,posY)
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
        self.champDaggro = 30
        self.target=None
        self.targetedBy = None
        self.actionEnCours = None
        self.degat = 50
        self.cooldown = 30
        self.cooldownMax = self.cooldown


    def attaqueCible(self):
        if self.target.isAlive():
            if Helper.calcDistance(self.target.posX, self.target.posY, self.posX, self.posY) <= self.champDaggro:
                if self.cooldown == 30:
                    self.target.recevoirDegats(self.degat)
                    self.cooldown = 0



            else:
                self.actionEnCours ="scanEnemy"
        else:
            self.actionEnCours="scanEnemy"





    def scanEnemy(self):
        if self.targetedBy and target is None:
            self.target = self.targetedBy
            self.attaqueCible(targetedBy)
        else:
            for i in self.parent.parent.modele.joueurs.values():# il faut reussir a avoir la liste des unite
                for n in i.units:
                    if n.ownerID is not self.ownerID:
                        if Helper.calcDistance(self.posX, self.posY , n.posX, n.posY) <= self.champDaggro:
                            self.target = n
                            self.actionEnCours = "attaqueCible"
                            self.attaqueCible(n)
                            break
            for i in self.parent.parent.modele.joueurs.values():
                for n in i.buildings:
                    if n.ownerID is not self.ownerID:
                        if Helper.calcDistance(self.posX, self.posY , n.posX, n.posY) <= self.champDaggro:

                            self.target = n
                            self.actionEnCours = "attaqueCible"
                            self.attaqueCible()
                            break


    def faitAction(self):
        if self.actionEnCours == None:
            self.actionEnCours ="scanEnemy"
        if self.actionEnCours == "scanEnemy":
            self.scanEnemy()
        if self.actionEnCours == "attaqueCible":
            self.attaqueCible()

        if self.cooldown != self.cooldownMax:
            self.cooldown += 1
        if self.hpActuel  ==0:
            del self
            print ("je  suis mort")





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



