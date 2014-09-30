# -*- coding: iso-8859-1 -*-
import Pyro4
from random import randint
import socket
import random
a = socket.gethostbyname(socket.gethostname())

#===============================================================================
# ID:    - 0: Login Packet
#        - 1: Login response packet
#        - 2: Seed packet
#        - 3: Seed response packet
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
        self.name = ""
        self.ID = 0
        self.x = 0
        self.y = 0
        self.currentTime = 0


class Server(object):
    
    
    def __init__(self):
        self.playerList = []
        self.actionList = []
        self.mapSeed = random.randint(0,100)
        print("Map seed: ", self.mapSeed)
        self.currentServerTime = 0
        
        
    def ClientToServer(self,action): #send from client to server
        #self.actionList.append(action)
        reponse = Action(-1, 0, "", 0, 0, 0, 0, "");
        #for i in range(self.actionList.__len__()):
        if action.ID == 0:
            nextPlayerID = self.playerList.__len__();
            print("received newplayer action from: ", action.playerName, ", assigning id: ", nextPlayerID)
            newPlayer = Player(action.playerName, nextPlayerID, action.playerX, action.playerY, action.playerTime)
            self.playerList.append(newPlayer)
            response = Action(1, nextPlayerID, "", 0, 0, 0, 0, "")
        elif action.ID == 2:
            response = Action(3, 0, "", 0, 0, 0, 0, str(self.mapSeed))
        return response
                

    
     
        

class Controleur():
    def __init__(self):
        self.server=Server()
        daemon=Pyro4.Daemon(host=a,port=9999)
        uri=daemon.register(self.server,"foo")
        print(uri) 

        print("Prêt!")
        daemon.requestLoop()


if __name__ == "__main__":
    c = Controleur()
