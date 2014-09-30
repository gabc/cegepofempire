# -*- coding: iso-8859-1 -*-
import Pyro4
import time
from tkinter import *

ip= "10.57.100.171"#input("ip: ")
ur="PYRO:foo@"+ip+":9999"
monserveur=Pyro4.Proxy(ur)


#===============================================================================
# ID:    - 0: Login Packet
#        - 1: Login response packet
#===============================================================================
class Action():
    def __init__(self, ID, playerID, playerName, playerX, playerY, playerTime, objectID, message):
        self.ID = ID
        self.playerID = playerID
        self.playerName = playerName
        self.playerX = playerX
        self.playerY = playerY
        self.playerTime = playerTime
        self.objectID = objectID
        self.message = message
       
            
class Player():
    def __init__(self, name, ID, x, y, currentTime):
        self.name = name
        self.ID = ID
        self.x = x
        self.y = y
        self.currentTime = currentTime



class  ServerListener():
    def __init__(self, parent):
        self.parent = parent
        self.beg = 0
        
 
                       
    def sendAndReceive(self, action):
        #envoi l'action (ID=0) et store la reponse dans une variable "reponse"
        reponse = monserveur.ClientToServer(action)
        #si reponse == 1, assign un ID au joueur
        if(reponse.ID == 1):
            print("received a login response - player ID: ", reponse.playerID)
            self.parent.m.myPlayer.ID = reponse.playerID
        elif(reponse.ID == 3):
            print("received a seed response - Seed: ", reponse.message)
            mapSeed = int(reponse.message)
            
        


class model():
    def __init__(self, parent):
        self.parent = parent
        self.mapSeed = 0
        #initialise un joueur, pas de nom ou de ID encore
        self.myPlayer = Player("", -1, -1, -1, 0)
        self.playerList = []
        self.actionList = []
        

class view():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.focus_set()
        print("tk init")

class Controleur():
    def __init__(self):
        #initialise les objets
        self.sl = ServerListener(self)
        self.m = model(self)
        self.v = view(self)
        
        #demande le nom du joueur
        self.nom=input("Votre nom, svp? ")
        self.m.myPlayer.name = self.nom;
        
        #crée une action avec le id=0 (login) et le nom du joueur
        self.action = Action(0, 1, self.nom, 0, 0, 0, 0, "")
        
        #envoi l'action du login
        self.sl.sendAndReceive(self.action)
        
        #request a seed from server
        self.action = Action(2, 0, "", 0, 0, 0, 0, "")
        
        #envoi l'action request seed
        self.sl.sendAndReceive(self.action)
        
        self.v.root.mainloop()
        
      


if __name__ == "__main__":
    c = Controleur()
