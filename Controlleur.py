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


#Comment se deroule une partie???
#On attend PAS l'input du joueur. Le jeu peu se derouler sans lui. Tant mieux s'il click sur kkchose.
#
#
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
