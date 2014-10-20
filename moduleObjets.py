#-------------------------------------------------------------------------------
# Name:        module objets
# Purpose:
#
# Author:      Sergio F
#
# Created:     25/09/2014
# Copyright:   (c) Sergio F 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
#Captain's Log entry : 28/09/2014:
# ajouter la fonction recevoirDegats et isAlive a l'objet Unit
#Fonctionne avec Villageaois

#Creer la class building: changer owner a ownerID, hp a hpActuel et HpMax
# dans le scrum
#
#

#Building herite de Unit

#Creer TownCenter
#TownCenter a des nouvelle variable  tempsRestant, creationQueue
#TownCenter a des nouvelles methodes unitSortir
#: voir __doc__
#-------------------------------------------------------------------------------







# Captain's Log entry 25/09/2014:

# jai ajouter la variable type aux instances de Unit et de Villageois qui sert
# a identifier le type en string, vous pouvez quand meme utiliser isinstance a la
# place,
# je suis en train de travailler sur d'autres variables qui pourrait etre utile

# jai cru que ca serait bien d'inclure le hpActuel et le hpMax pour ainsi diviser
# la variable hp qui etais pas trop significative

# chaque unite devrait avoir aussi une vitesse de deplacement cela va etre ajoute
# comme variable a Unit




# le id_objet est une variable static qui ne sert qu'a compter on est rendu au
# combien ieme objet cree
# on peut le mettre dans le module oÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Âº on cree les objets
# le global fait en sorte que partout dans la page la variable et son contenu
# est garder MEME DANS LES AUTRE FONCTIONS QUI SONT ENFANT DE LEMPLACEME
# DE LA VARIABLE: NE PAS REUTILISER



#-------------------------------------------

class Joueur():
    def __init__(self, ID, name):
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



    def changerEre():
        pass

    def construireBuilding(self, idBuilding, posX ,posY ):
        pass

    def creerUnit(self, type, x, y):
        if type == "villageois":
            self.units.append(Villageois(self.ID, x, y))

    def changerAllies():
        pass

    def envoyerRessources():
        pass





id_objet = 0

class Unit():
    def __init__(self, ownerID, posX, posY):
        global id_objet
        #le global fait en sorte que partout dans la page la variable id_objet
        #est garder MEME DANS LES AUTRE FONCTIONS QUI SONT ENFANT DE LEMPLACEME
        # DE LA VARIABLE: NE PAS REUTILISER
        id_objet += 1

        self.id = id_objet
        self.ownerID = ownerID

        self.type = "Unit"

        #le hp d'un unit generique est -1
        self.hpMax = -1
        self.hpActuel = self.hpMax
        self.posX = posX
        self.posY = posY
        #le champs de vision est arbitraire et devrait dependre du type du Unit
        self.champDeVision = -1
        #idem pour le delai de Construction
        self.delaiDeConstruction = -1


    def deplacer():
        pass

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






        print(" numero de l'id est : %s" % self.id)
        print(" numero du owner est : %s" % self.ownerID)


class Villageois(Unit):

    def __init__(self,ownerID, posX, posY):
        Unit.__init__(self,ownerID, posX, posY)
        self.type = "Villageois"

        #j'ai decider arbitrairement de l'hp: a modifier
        #dautres variables arbitraires yee!!
        self.champDeVision = 50
        self.delaiDeConstruction =20000
        self.hpMax = 100
        self.hpActuel = self.hpMax

        #j'imagine qu'ils veulent dire le temps en millisecondes : arbitraire
        self.collectionRate = 3000




        print("le type de cette unite est : %s" % self.type)

    def recolteRessource():
        pass

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














def main():
    """"
    unit1=Unit("player1", 0,0)
    print("le type de cette unite est : %s" % unit1.type)
    unit2=Villageois("player2", 100, 100)

    print("pos en xy de l'unit %s : x =%d y =%d" % (unit2.id, unit2.posX, unit2.posY))

    print("vie avant dmg de unit2 : %d" % unit2.hpActuel)

    unit2.recevoirDegats(50)

    print("vie apres dmg de unit1 : %d" % unit2.hpActuel)
    """



    building = TownCenter("Tom",0, 0)

    building.createUnit(Villageois("Tom", 0, 0))

    print(building.tempsRestant)

    building.tempsRestant -= 10000

    print(building.tempsRestant)

    print(building.creationQueue[0].id)

    Unit1 =building.unitSortir()

    print (" id de l'unit %s" % Unit1.id)

    print(Unit1.type)

    print("id du towncenter %s" % building.id)

    building2 = TownCenter("Henry", 1, 1)

    print("id du towncenter 2 :%s" % building2.id)







if __name__ == '__main__':
    main()
