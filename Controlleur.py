from Vue import *

#WTF does the controler do:
#Pas de menus pour l'instant, on jump directement dans le jeu
#Une fois le server fini --> faire le menu "host ou join a game"
#
#Comment commence une partie???
#Obtenir une liste de joueurs (server qui repond le nb de joueurs connectes???)
#Init une carte: Creer un objet map de map.py. Utiliser le seed genere par le serveur avec map.setSeed().
#map.placeRessourcesOverworld()
#map.placeRessourcesUnderworld()
#map.placeJoueurs(listeDeJoueurs)
#La carte est maintenant generee en MEMOIRE. La il faut la dessiner.
#vue.DessineMap(map) --> Loop a travers la map. Dessine ce qui se trouve dans le canvas.
#La partie est maintenant commencee.

#Comment se deroule une partie???
#En général:
#   1.demande au server s'il y a kkchose de nouveau
#   2.calculs en memoire de: path, positions, creation de units,augmentation/baisse de ressources, attaques
#   3.dessiner sur le canvas ce qui se trouve dans ses coordonnees
#   4. message au server s'il y a action
#

class Controleur(): 
    def __init__(self):
        self.temps=0
        self.vue=Vue(self)
        self.vue.root.after(1000, self.tempsJeu())
        self.vue.root.mainloop()
        
    def tempsJeu(self):
        self.temps +=1
        self.vue.rafraichirTemps(self.temps)
        self.vue.root.after(1000,self.tempsJeu)              
            
if __name__ == "__main__":  
    c = Controleur()
