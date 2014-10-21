import random
import math
from modele_client import *

#NOTE: pour l'instant, ceci n'est seulement que pour des hauteurs et largeurs impaires pour les spawns des joueurs
#Ressources: Matériaux, nourriture, énergie, or. + artefacts



#TODO:
#Precise ressources (bois, pierre, etc)

#Ratio des ressources ( sur 100)

WOOD_RATIO=1
FOOD_RATIO=1
ROCK_RATIO=1
ARTE_RATIO=1
ENERGY_RATIO=1
GOLD_RATIO=1
UNDER_RATIO=25

#Caracteres qui representent les ressources, incluant les ressources souterraines
        
WOOD_CHAR='1'
FOOD_CHAR='2'
ROCK_CHAR='3'
ARTE_CHAR='4'
ENERGY_CHAR='5'
GOLD_CHAR='6'
EMPTY_CHAR='-'

WOOD_UNDER_CHAR='a'
FOOD_UNDER_CHAR='b'
ROCK_UNDER_CHAR='c'
ARTE_UNDER_CHAR='d'
ENERGY_UNDER_CHAR='e'
GOLD_UNDER_CHAR='f'

PLAYER_CHAR='#'

class Case:
    def __init__(self,posX,posY,ressource, ratio, passable):
        self.posX=posX
        self.posY=posY
        self.ressource=ressource
        self.ratio=ratio
        self.passable=passable

    def isPassable(self):
        return self.passable
        

class Map:
    """Methodes

    setSeed(seed): pour set le seed recu par le server

    placeRessourceType(ratio, char): place un type "char" de ressources sur la map, avec un ratio "ratio"

    placeRessourcesOverworld(): place toutes les ressources du jeu sur le dessus de la map

    placeRessourcesUnderworld(): place toutes les ressources sous-terre de la map

    placeJoueurs(listeJoueurs): place les spawns des joueurs inscrits selon un cercle ou une ellipse

    printMapCon(): Print la map dans la console. Attention, ca peut être long avec une grosse map

    printMapToFile(): Créé un fichier "map.txt" et y envois la map

    countRessources(): Pour avoir les statistiques de la map"""
        
    def __init__(self, largeur, hauteur):
        self.ressources=[]
        self.units=[]
        self.buildings=[]
        self.largeur=largeur
        self.hauteur=hauteur
        #print("largeur: ", self.largeur, ", hauteur: ", self.hauteur)
        self.mat=[[Case(j,i,EMPTY_CHAR, 100, True) for j in range(largeur)] for i in range(hauteur)]        

    def setSeed(self, seed):
        random.seed(seed)
        
    def placeRessourceType(self, ratio, char):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                nb = random.randrange(100)
                if nb <= ratio and self.mat[i][j].ressource==EMPTY_CHAR:
                    self.mat[i][j] = Case(j,i,char,ratio, False)
                

    def placeRessourcesOverworld(self):
        #OVERWORLD RESSOURCES
        self.placeRessourceType(WOOD_RATIO, WOOD_CHAR)
        self.placeRessourceType(ROCK_RATIO, ROCK_CHAR)
        self.placeRessourceType(FOOD_RATIO, FOOD_CHAR)
        self.placeRessourceType(GOLD_RATIO, GOLD_CHAR)
        self.placeRessourceType(ENERGY_RATIO, ENERGY_CHAR)
        self.placeRessourceType(ARTE_RATIO, ARTE_CHAR)

    def placeRessourcesUnderworld(self):
        #UNDERWORLD RESSOURCES
        for i in range(self.hauteur):
            for j in range(self.largeur):
                res = random.randrange(100)
                if res <= UNDER_RATIO:
                    if self.mat[i][j].ressource == WOOD_CHAR:
                        self.mat[i][j].ressource = WOOD_UNDER_CHAR

                    if self.mat[i][j].ressource == FOOD_CHAR:
                        self.mat[i][j].ressource = FOOD_UNDER_CHAR
                        
                    if self.mat[i][j].ressource == ROCK_CHAR:
                        self.mat[i][j].ressource = ROCK_UNDER_CHAR
                        
                    if self.mat[i][j].ressource == ARTE_CHAR:
                        self.mat[i][j].ressource = ARTE_UNDER_CHAR

                    if self.mat[i][j].ressource == ENERGY_CHAR:
                        self.mat[i][j].ressource = ENERGY_UNDER_CHAR

                    if self.mat[i][j].ressource == GOLD_CHAR:
                        self.mat[i][j].ressource = GOLD_UNDER_CHAR


    def placeJoueurs(self,listeJoueurs):

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

        #print(listeAngles)

        #selon un cercle
        #Equation pour un cercle
        #x = cx + r * cos(a)
        #y = cy + r * sin(a)
        #r = radius, cx & cy = origin, a=angle
        #aire=math.pi*(rayon*rayon)

        joueur=0

        if self.largeur == self.hauteur:

            for angle in listeAngles:
                x = math.trunc(rayon * math.cos(math.radians(angle)) + math.trunc(middleX))
                y = math.trunc(rayon * math.sin(math.radians(angle)) + math.trunc(middleY))
                print("x =", x,"y =", y,"a =",angle)
                self.mat[y][x]=Case(x,y,PLAYER_CHAR,0,False)
                listeJoueurs[joueur].buildings.append(TownCenter(joueur, x, y))

        #selon une ellipse
        #Equation pour une ellipse
        #x = (abcos * (angle)) / racine de ((b^2 * cos^2(angle)) + (a^2 * sin^2(angle))
        #y =(absin * (angle)) / racine de ((b^2 * cos^2(angle)) + (a^2 * sin^2(angle))
        #a = demie-grand axe --> largeur / 2
        #b = demie-petit axe --> hauteur / 2

        else:
            a=self.largeur/2
            b=self.hauteur/2

            for angle in listeAngles:
                x = math.trunc(middleX + (a*b*math.cos(math.radians(angle))) / math.sqrt( ((math.pow(b,2)) * math.pow(math.cos(math.radians(angle)),2)) + ((math.pow(a,2)) * math.pow(math.sin(math.radians(angle)),2))  ))
                y = math.trunc(middleY + (a*b*math.sin(math.radians(angle))) / math.sqrt( ((math.pow(b,2)) * math.pow(math.cos(math.radians(angle)),2)) + ((math.pow(a,2)) * math.pow(math.sin(math.radians(angle)),2))  ))
                if x == self.largeur:
                    x = self.largeur -1
                print("x =", x,"y =", y,"a =",angle)
                self.mat[y][x]=Case(x,y,PLAYER_CHAR,0,False)
                listeJoueurs[joueur].buildings.append(TownCenter(joueur, x, y))
    
    def printMapCon(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                print(self.mat[i][j].ressource, end="")
            print("")

    def printMapToFile(self):
        f = open('map.txt','w')
        for i in range(self.hauteur):
            for j in range(self.largeur):
                f.write(str(self.mat[i][j].ressource))
            f.write("\n")
        f.close()

    def printPassable(self):
        f = open('map.txt','w')
        for i in range(self.hauteur):
            for j in range(self.largeur):
                print(self.mat[i][j].isPassable())

    #I like stats
    def countRessources(self):
        res1=0
        res2=0
        res3=0
        res4=0
        res5=0
        art=0
        vide=0
        res1EtUnder=0
        res2EtUnder=0
        res3EtUnder=0
        res4EtUnder=0
        res5EtUnder=0
        resartEtUnder=0
        
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if self.mat[i][j].ressource == WOOD_CHAR:

                    res1 += 1

                if self.mat[i][j].ressource == FOOD_CHAR:

                    res2 += 1

                if self.mat[i][j].ressource == ROCK_CHAR:

                    res3 += 1


                if self.mat[i][j].ressource == ENERGY_CHAR:

                    res4 += 1

                if self.mat[i][j].ressource == GOLD_CHAR:

                    res5 += 1

                if self.mat[i][j].ressource == ARTE_CHAR:

                    art += 1

                if self.mat[i][j].ressource == EMPTY_CHAR:

                    vide += 1

                if self.mat[i][j].ressource == WOOD_UNDER_CHAR:

                    res1EtUnder += 1
                    
                if self.mat[i][j].ressource == FOOD_UNDER_CHAR:

                    res2EtUnder += 1
                    
                if self.mat[i][j].ressource == ROCK_UNDER_CHAR:

                    res3EtUnder += 1

                if self.mat[i][j].ressource == ENERGY_UNDER_CHAR:

                    res4EtUnder += 1

                if self.mat[i][j].ressource == ENERGY_UNDER_CHAR:

                    res5EtUnder += 1
                    
                if self.mat[i][j].ressource == ARTE_UNDER_CHAR:

                    resartEtUnder += 1

        #PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT
        print("")
        print('Bois=',res1)
        print('Food=',res2)
        print('Pierre=',res3)
        print('Energie=',res4)
        print('Or=',res5)
        print('Artefacts=',art)
        print('Vide=',vide)
        print('Materiaux + under=',res1EtUnder)
        print('Food + under=',res2EtUnder)
        print('Rare + under=',res3EtUnder)
        print('Artefact + under=',resartEtUnder)
        
  
#For testing purposes
"""l=3
h=3

j1=Joueur(1,1,1)
j2=Joueur(2,2,2)

liste=[]

liste.append(j1)
liste.append(j2)


m=Map(l,h)

#m.setSeed(10)

m.placeRessourcesOverworld()

m.placeRessourcesUnderworld()

m.placeJoueurs(liste)

#m.equilibreRessources(liste) <-- To do

#m.printMapToFile()

m.printMapCon()

m.printPassable()"""

#m.countRessources()
