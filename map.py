import random
import math

#NOTE: pour l'instant, ceci n'est seulement que pour des hauteurs et largeurs impaires pour les spawns des joueurs
#Ressources: Matériaux, nourriture, énergie, or. + artefacts



#TODO:
#Precise ressources (bois, pierre, etc)

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
        self.WATER_CHAR='-'
        self.mat=[[self.WATER_CHAR for j in range(hauteur)] for i in range(largeur)]        

        #Ratio , sur 100, des ressources
        
        self.MATE_RATIO=30
        self.FOOD_RATIO=25
        self.RARE_RATIO=15
        self.ARTE_RATIO=1
        self.UNDER_RATIO=25

        #Caracteres qui representent les ressources, incluant les ressources souterraines
        
        self.MATE_CHAR='1'
        self.FOOD_CHAR='2'
        self.RARE_CHAR='3'
        self.ARTE_CHAR='4'
        self.MATE_UNDER_CHAR='a'
        self.FOOD_UNDER_CHAR='b'
        self.RARE_UNDER_CHAR='c'
        self.ARTE_UNDER_CHAR='d'

        #Donc les lettres "abcd" signifient qu'il y a 2 ressources sur une case. Une "overworld" et une "underworld"
        #Ex: bois overworld et charbon underworld

    def setSeed(self, seed):
        random.seed(seed)
        
    def placeRessourceType(self, ratio, char):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                nb = random.randrange(100)
                if nb <= ratio and self.mat[j][i]==self.WATER_CHAR:
                    self.mat[j][i] = char
                

    def placeRessourcesOverworld(self):
        #OVERWORLD RESSOURCES
        self.placeRessourceType(self.MATE_RATIO, self.MATE_CHAR)
        self.placeRessourceType(self.FOOD_RATIO, self.FOOD_CHAR)
        self.placeRessourceType(self.RARE_RATIO, self.RARE_CHAR)
        self.placeRessourceType(self.ARTE_RATIO, self.ARTE_CHAR)

    def placeRessourcesUnderworld(self):
        #UNDERWORLD RESSOURCES
        for i in range(self.hauteur):
            for j in range(self.largeur):
                res = random.randrange(100)
                if res <= self.UNDER_RATIO:
                    if self.mat[j][i] == self.MATE_CHAR:
                        self.mat[j][i] = self.MATE_UNDER_CHAR

                    if self.mat[j][i] == self.FOOD_CHAR:
                        self.mat[j][i] = self.FOOD_UNDER_CHAR
                        
                    if self.mat[j][i] == self.RARE_CHAR:
                        self.mat[j][i] = self.RARE_UNDER_CHAR
                        
                    if self.mat[j][i] == self.ARTE_CHAR:
                        self.mat[j][i] = self.ARTE_UNDER_CHAR


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

        if self.largeur == self.hauteur:

            for angle in listeAngles:
                x = math.trunc(rayon * math.cos(math.radians(angle)) + math.trunc(middleX))
                y = math.trunc(rayon * math.sin(math.radians(angle)) + math.trunc(middleY))
                #print("x =", x,"y =", y,"a =",angle)
                self.mat[x][y]='#'
            #print("Cercle")

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
                self.mat[x][y]='#'                            
    
    def printMapCon(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                print(self.mat[j][i], end="")
            print("")

    def printMapToFile(self):
        f = open('map.txt','w')
        for i in range(self.hauteur):
            for j in range(self.largeur):
                f.write(str(self.mat[j][i]))
            f.write("\n")
        f.close()

    #I like stats
    def countRessources(self):
        res1=0
        res2=0
        res3=0
        art=0
        eau=0
        res1EtUnder=0
        res2EtUnder=0
        res3EtUnder=0
        resartEtUnder=0
        
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if self.mat[j][i] == self.MATE_CHAR:

                    res1 += 1

                if self.mat[j][i] == self.FOOD_CHAR:

                    res2 += 1

                if self.mat[j][i] == self.RARE_CHAR:

                    res3 += 1

                if self.mat[j][i] == self.ARTE_CHAR:

                    art += 1

                if self.mat[j][i] == self.WATER_CHAR:

                    eau += 1

                if self.mat[j][i] == self.MATE_UNDER_CHAR:

                    res1EtUnder += 1
                    
                if self.mat[j][i] == self.FOOD_UNDER_CHAR:

                    res2EtUnder += 1
                    
                if self.mat[j][i] == self.RARE_UNDER_CHAR:

                    res3EtUnder += 1
                    
                if self.mat[j][i] == self.ARTE_UNDER_CHAR:

                    resartEtUnder += 1

        #PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT PRINT
        print("")
        print('Materiaux=',res1)
        print('Food=',res2)
        print('Rare=',res3)
        print('Artefacts=',art)
        print('Eau=',eau)
        print('Materiaux + under=',res1EtUnder)
        print('Food + under=',res2EtUnder)
        print('Rare + under=',res3EtUnder)
        print('Artefact + under=',resartEtUnder)
        
  
"""For testing purposes
l=55
h=25
liste=[1,2,3,4]

m=Map(l,h)

m.placeRessourcesOverworld()

m.placeRessourcesUnderworld()

m.placeJoueurs(liste)

#m.equilibreRessources(liste) <-- To do

#m.printMapToFile()

m.printMapCon()

m.countRessources()"""


