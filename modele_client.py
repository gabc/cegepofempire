import deplacement
import math

def roundtenth(x):
    """arrondi a la dizaine vers le bas 9 -> 0, 15 -> 10"""
    return x if x % 10 == 0 else x - x % 10

class Joueur():
    def __init__(self, parent, ID, name):
        self.parent = parent
        self.name = name
        self.ID = ID
        self.currentTime = 0
        self.ere = 1
        self.maxUnits = 200
        self.ressources = [0,0,0,0,0]
        # Index des ressources:
        # Nourriture : 0
        # BOis: 1
        # Pierre : 2
        # Or : 3
        # Energie : 4

        self.allies = []
        self.units =[]
        self.buildings =[]
        self.unitsSelectionne =[]
        self.actions={"envoieRess":self.envoyerRessources}

    def metToiAJour(self):
        for u in self.units:
            u.faitAction()

    def changerEre():
        pass

    def construireBuilding(self, idBuilding, posX ,posY ):
        pass

    def creerUnit(self, type, x, y):
        if type == "villageois":
            self.units.append(Villageois(self.ID, x, y,self))

    def changerAllies():
        pass

    #toute les ressources
    def envoyerRessources(self,a,b,c,d,e,f):
        print(a,b,c,d,e,f)        

    def deplaceUnit(self, unit, arrive):
        idunit = unit[1]

        for u in self.units:
            if u.id == idunit:
                u.deplacer(self.parent.deplaceur, arrive)

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

        self.actionEnCours = {}

    def faitAction(self):
        if self.chemin:         # S'il a un chemin. Qu'il se deplace.
            self.deplacer(self.deplaceur, self.chemin)
    
    def isAlive(self):
        if self.hpActuel <= 0:
            return False
        else:
            return True


    def recevoirDegats(self, degatsRecus):
        if degatsRecus > self.hpActuel:
            self.hpActuel = 0
        else :
            self.hpActuel -= degatsRecus

    def effectueDeplacement(self, arrive):
        if self.posX > int(arrive.x*20):
            self.posX -= self.vitesseX
        elif self.posX < int(arrive.x*20):
            self.posX += self.vitesseX
        if self.posY > int(arrive.y*20):
            self.posY -= self.vitesseY
        elif self.posY < int(arrive.y*20):
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

        self.vitesseX = 5
        self.vitesseY = 5

        self.posX = posX #add
        self.posY = posY #add
            

    def recolteRessource(self,x,y,game_map):
        if game_map.mat[y][x].nbRessource > 0:
            game_map.mat[y][x].nbRessource-0.01
            if game_map.mat[y][x].nbRessource == 0:
                game_map.mat[y][x].ressource=game_map.EMPTY_CHAR
            
    def checkArrive(self, x, y):
        if self.posX == x and self.posY == y:
            if game_map.mat[y][x].ressource is not game_map.EMPTY_CHAR:
               self.recolteRessource(arrive, self.parent.parent.m)

    def deplacer(self, deplaceur, arrive):
        if self.chemin is None or self.chemin == []:
            self.deplaceur = deplaceur
            self.chemin = deplaceur.chemin(self, arrive)            
        else:
            if (math.trunc(self.posX / 20) == math.trunc(self.chemin[0].x)) and (math.trunc(self.posY / 20) == math.trunc(self.chemin[0].y)):      
                del self.chemin[0]
            if self.chemin:
                self.effectueDeplacement(self.chemin[0])
        #self.checkArrive(arrive[0].x,arrive[0].y)
        
            

class Guerrier(Unit):
    def __init__(self, ownerID, posX, posY):
        Unit.__init__(self, ownerID,posX,posY)
        self.type = "Guerrier"


        #Arbitraire
        self.champDeVision = 50
        self.delaiDeConstruction = 20000
        self.hpMax =100
        self.hpActuel = self.hpMax
        self.range = 0 #melee
        self.atkSpeed = 600 #en millisecondes
        self.defense = 1

    def attaque(self):
        pass

    def recevoirDegats(self, degatsRecus):
        if degatsRecus -self.defense > self.hpActuel:
            self.hpActuel = 0
        else :
            self.hpActuel -= degatsRecus -self.defense



class Building():

    def __init__(self, ownerID, posX, posY):
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

    def isAlive(self):
        if self.hpActuel <= 0:
            return False
        else:
            return True


    def recevoirDegats(self, degatsRecus):
        if degatsRecus > self.hpActuel:
            self.hpActuel = 0
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
        Building.__init__(self, ownerID, posX, posY)
        self.type ="TownCenter"
        #valeurs arbitraires
        self.hpActuel = 1000
        self.hpMax = self.hpActuel
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

class Barrack(Building):
    def __init__(self, ownerID, posX, posY):
        Building.__init__(ownerID,posX,posY)
        self.type="Barrack"

        self.hpActuel = 1000
        self.hpMax = self.hpActuel
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
                        "deplace" : self.deplaceUnite,}

    def initPartie(self,listeNomsJoueurs):
        n=0
        #init tous les joueur avec leur unite, batiments, etc...
        print("Nombre total de joueurs: ", len(listeNomsJoueurs))
        for j in listeNomsJoueurs:
            print("joueur: ", j)
            if j == self.parent.nom:
                self.parent.myPlayer = Joueur(self.parent, n, j)
                self.joueurs[j] = self.parent.myPlayer
            else:
                self.joueurs[j] = Joueur(self.parent, n, j)
            n += 1

        
    def creerUnite(self, args):
        self.joueurs[args[0]].creerUnit(args[2][0], args[2][1], args[2][2])

    def deplaceUnite(self, args):
        self.joueurs[args[0]].deplaceUnit(args[2][0],args[2][1])
        
    def prochaineAction(self,cadre):
        if cadre in self.actionsAFaire.keys():
            for action in self.actionsAFaire[cadre]:
                self.actions[action[1]](action)
            del self.actionsAFaire[cadre]
        # Mise a jour:
        for j in self.joueurs.keys():
            self.joueurs[j].metToiAJour()
