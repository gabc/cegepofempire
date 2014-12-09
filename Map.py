import random
import math
from modele_client import *

#TODO:
#Precise ressources (bois, pierre, etc)

#Ratio des ressources (sur 100)

WOOD_RATIO=10
FOOD_RATIO=5
ROCK_RATIO=5
ARTE_RATIO=1
ENERGY_RATIO=2
GOLD_RATIO=2
UNDER_RATIO=25

#Caracteres qui representent les ressources, incluant les ressources souterraines

ID_CASE=0

class Case:
    def __init__(self,posX,posY,passable):
        global ID_CASE
        self.posX=posX
        self.posY=posY
        self.passable=passable
        self.ressource=EMPTY
        self.underRes=0
        self.building=0
        self.nbRessource=0

        ID_CASE+=1
        self.id=ID_CASE

    def isPassable(self):
        return self.passable


class Map:
    """Methodes

    initMap(): initialize toutes les cases vides de la map

    setSeed(seed): pour set le seed recu par le server

    placeRessourceType(ratio, char): place un type "char" de ressources sur la map, avec un ratio "ratio"

    placeRessourcesOverworld(): place toutes les ressources du jeu sur le dessus de la map

    placeRessourcesUnderworld(): place toutes les ressources sous-terre de la map

    placeJoueurs(listeJoueurs): place les spawns des joueurs inscrits selon un cercle ou une ellipse

    printMapCon(): Print la map dans la console. Attention, ca peut ÃƒÂªtre long avec une grosse map

    printMapToFile(): CrÃƒÂ©ÃƒÂ© un fichier "map.txt" et y envois la map

    countRessources(): Pour avoir les statistiques de la map

    placeBuilding(posX, posY, buildingType): place un building a la position x,y, si la case n'est pas occupee. retourne true si la case ne l'etait pas, false si oui.

    clearSpace(self, building, listeRessources): enleve les ressource pres du building passe en parametre"""

    def __init__(self, largeur, hauteur):
        self.ressources=[]
        self.units=[]
        self.buildings=[]
        self.largeur=largeur
        self.hauteur=hauteur
        #print("largeur: ", self.largeur, ", hauteur: ", self.hauteur)
        self.mat=[[Case(i,j,True) for j in range(hauteur)] for i in range(largeur)]
        self.toDelete=[]
        self.MAX_RESSOURCE=2000

    def setSeed(self, seed):
        random.seed(seed)

    def placeRessource(self, ratio, char):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                nb = random.randrange(100)
                if nb < ratio and self.mat[i][j].ressource==EMPTY:
                    self.mat[i][j].passable=False
                    self.mat[i][j].ressource = char
                    self.mat[i][j].nbRessource=self.MAX_RESSOURCE

    def placeRessourceUnder(self, ratio, char):
         for i in range(self.largeur):
            for j in range(self.hauteur):
                nb = random.randrange(100)
                if nb <= ratio:
                    self.mat[i][j].underRes=char
                    self.mat[i][j].nbRessource=self.MAX_RESSOURCE

    def placeRessourcesOverworld(self):
        #OVERWORLD RESSOURCES
        self.placeRessource(WOOD_RATIO, WOOD)
        self.placeRessource(ROCK_RATIO, ROCK)
        self.placeRessource(FOOD_RATIO, FOOD)
        self.placeRessource(GOLD_RATIO, GOLD)
        self.placeRessource(ENERGY_RATIO, ENERGY)
        #self.placeRessource(ARTE_RATIO, ARTE)

    def placeRessourcesUnderworld(self):
        #UNDERWORLD RESSOURCES
        self.placeRessourceUnder(UNDER_RATIO, ROCK_UNDER)
        self.placeRessourceUnder(UNDER_RATIO, ENERGY_UNDER)
        self.placeRessourceUnder(UNDER_RATIO, GOLD_UNDER)


    def placeJoueurs(self,listeJoueurs, listeNomsJoueurs):

        nbJoueurs=len(listeJoueurs)

        if nbJoueurs <= 2:
            divs=2
        else:
            divs=nbJoueurs

        angle=360/divs

        middleX=self.largeur/2
        middleY=self.hauteur/2

        rayon=self.largeur/2

        listeAngles=[]

        anglesPossibles=[0,40,80,120,160,200,240,280,320]

        i = 0

        while i < nbJoueurs:
            angle = anglesPossibles[random.randrange(9)]

            if listeAngles.count(angle) == 0:

                listeAngles.append(angle)

                i += 1

        else:
            a=self.largeur/2
            b=self.hauteur/2

        joueur=0

        for angle in listeAngles:
            
            #selon un cercle
            #Equation pour un cercle
            #x = cx + r * cos(a)
            #y = cy + r * sin(a)
            #r = radius, cx & cy = origin, a=angle
            #aire=math.pi*(rayon*rayon)
            
            if self.largeur == self.hauteur:
                x = math.trunc(rayon * math.cos(math.radians(angle)) + math.trunc(middleX))
                y = math.trunc(rayon * math.sin(math.radians(angle)) + math.trunc(middleY))

            else:
                
                #selon une ellipse
                #Equation pour une ellipse
                #x = (abcos * (angle)) / racine de ((b^2 * cos^2(angle)) + (a^2 * sin^2(angle))
                #y =(absin * (angle)) / racine de ((b^2 * cos^2(angle)) + (a^2 * sin^2(angle))
                #a = demie-grand axe --> largeur / 2
                #b = demie-petit axe --> hauteur / 2
                
                x = math.trunc(middleX + (a*b*math.cos(math.radians(angle))) / math.sqrt( ((math.pow(b,2)) * math.pow(math.cos(math.radians(angle)),2)) + ((math.pow(a,2)) * math.pow(math.sin(math.radians(angle)),2))  ))
                y = math.trunc(middleY + (a*b*math.sin(math.radians(angle))) / math.sqrt( ((math.pow(b,2)) * math.pow(math.cos(math.radians(angle)),2)) + ((math.pow(a,2)) * math.pow(math.sin(math.radians(angle)),2))  ))

            #Pour eviter les index out of range
            if x == self.largeur:
                x = x - 2

            if y == self.hauteur:
                y = y - 2

            self.mat[x][y].building="TownCenter"
            self.mat[x][y].ressource=EMPTY
            self.mat[x][y].nbRessource=0
            self.mat[x][y].passable=False
            listeJoueurs[listeNomsJoueurs[joueur]].buildings.append(TownCenter(joueur, x, y))

            joueur+=1

        #vide les cases trop pres des spawns
        listeRes=self.getListeRessources()

        for j in listeNomsJoueurs:
            self.clearSpace(listeJoueurs[j].buildings[0],listeRes)

        return listeJoueurs

    def clearSpace(self, building, listeRessources):
        x=building.posX
        y=building.posY

        for r in listeRessources:
            #si pos x de la ressource est dans le range de 1 case du town center
            if r.posX >= x - 1 and r.posX <= x + 1:
                #si pos y de la ressource est dans le range de 1 case du town center
                if r.posY >= y - 1 and r.posY <= y + 1:
                    r.ressource=EMPTY
                    r.nbRessource=0
                    r.passable=True
                    self.mat[r.posX][r.posY]=r

    def placeBuilding(self, posX, posY, buildingType):
        self.mat[posX][posY].building = buildingType
        self.mat[posX][posY].passable=False

    def getListeRessources(self):
        ressources=[]

        for i in range(self.largeur):
            for j in range(self.hauteur):
                if self.mat[i][j].ressource is not EMPTY:
                    ressources.append(self.mat[i][j])

        return ressources

    def printMapCon(self):
        for i in range(self.largeur):
            for j in range(self.hauteur):
                print(self.mat[i][j].ressource, end="")
            print("")

    def printMapToFile(self):
        f = open('map.txt','w')
        for i in range(self.largeur):
            for j in range(self.hauteur):
                f.write(str(self.mat[i][j].ressource))
            f.write("\n")
        f.close()

    def printPassable(self):
        f = open('map.txt','w')
        for i in range(self.largeur):
            for j in range(self.hauteur):
                print(self.mat[i][j].isPassable())
