Build 0.1.7b

Pour démarrer le jeu, double-clickez sur client.py et démarrez un server.

Pour démarrer un serveur, vous devez clicker sur le bouton Creer Serveur, on rentre ensuite dans une fenêtre d'attente.
Ensuite, un joueur dans une autre machine peut joindre pendant que l'hôte est encore en attente.
Pour démarrer la partie, l'hôte doit clicker sur démarrer partie.

À l'instant, la carte est générée aléatoirement. Vous serez probablement perdu dès le départ.
Sinon, chaque joueur est assigné à une couleur. Le Towncenter principale va être de la couleur qui vous est
assignée.

Pour vous déplacer dans la carte, il faut utiliser les touches W,A,S et D.

	W = vers le haut
	A = vers la gauche
	S = vers le bas
	D = vers la droite

Sinon, pour jouer normalement, vous pouvez toujours clicker (click gauche)sur votre Town Center, et un menu s'affichera dans le bas.
Les options de bâtiments et d'unités s'y trouvent.

Le but du jeu est de créer des unités de guerre et détruire ceux des adversaires.

Gerer les ressources et les villageois, créer des guerrier et defendre les bases sont la meilleure façon de gagner.

Il y a un tableau qui gère la diplomacie et qui permet de donner des ressources à d'autres joueurs



Bâtiments disponibles:

TownCenter:

	Le TownCenter est le bâtiment principal de votre civilisation. Les villageois sont créés à partir du TownCenter.

	Le bouton Creer met un villageois au niveau de la souris. Un click gauche va placer l'unité dans la map si on à assez de ressources(tâchez de ne pas en abuser).

	Pour faire déplacer un unité, sélectionnez le avec un click gauche, et faite un click droit sur la case où vous voulez l'envoyer.



Barrack:

	Sert à Produire des unités de guerre.


Maison:

	Sert à augmenter le maximum de population pour les unités


Tour:

	Sert à defendre les points statiques

Chateau:

	Sert à produire des unités de haut niveau (moutons)

Unités disponibles:

Villageois:
	Cout: 30 Nourriture

	Le Villageois sert à créer des bâtiments et à récolter des ressources.

	Pour récolter, il faut left-click un villageois(l'unité selectionné deviendra rouge) et ensuite right-click une ressource.
	Le villageois fera des aller-retour jusqu'à ce le node est consumé.

	Pour créer des bâtiments, il faut sélectionner un villageois et choisir Construire dans le menu.
	Plusieurs options sont disponibles mais tous nécessitent des ressources avant d'être construit

Guerrier:
	Cout:50 Nourriture ,25 Or 
	
	Unité de guerre de base, doit aller au melee pour pouvoir faire des dégâts

Chevalier:
	Cout:200 Nourriture ,200 Or 

	Plus dispendieux que le Guerrier, il est cependant très rapide. doit attaquer au melee
Archer:
	Cout:20 Nourriture, 40 Bois, 15 Or
	Unité à distance. Plus fragile que le Guerrier mais le pouvoir d'attaquer à distance en vaut la peine

Mouton:
	Cout:500 Nourriture, 500 Or, 500 Energy
	Unité ultime. Peu de choses peuvent l'affronter



Ressources disponibles:

Nourriture:
	Sert à créer les villageois et les unités de guerre
Bois:
	Sert à construire un bâtiments
Or:
	Sert à construire les unités de guerre et les bâtiments
Pierre:
	Sert à la construction des bâtiments
Énergie:
	Sert à nourrir les moutons grourmands.




L'ÉTAT DU JEU:

	
	-Toutes les ressources sont récoltables.
	-Les unités et établissements coutent des ressources.
	-Beaucoup d'information est toujours dompé dans la console.
	-Le joueur commence avec son Town Centre à l'écran(peut être situé dans le coin de l'écran)
	-Lorsqu'une ressource est vide, elle disparait.
	-Les crééables: villageois, guerriers, tours, barracks
	-Les guerriers et les tours peuvent attaquer (pas d'animation)
	-Le changement d'ère n'est pas implémenté
