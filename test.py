#!/usr/bin/env python3
# class Point:
#     def __init__(self,x,y,poid,passable, parent):
#         self.x = x
#         self.y = y
#         self.poid = poid
#         self.passable = passable
#         self.parent = parent
        
#     def togglepassable(self):
#         self.passable = not self.passable

#     def passablep(self):
#         return self.passable


# Fuck that
# 0 = passable
# 1 = depart
# 2 = arrive
# 3 = mur

map = []
path = []
depart = (2,2)
arrivee = (5,2)
PASSABLE = 3
def initmap():
    for i in range(25):
        map.append([])
        for j in range(25):
            map[i].append(0)

def printmap():
    for i in range(25):
        t = ""
        for j in range(25):
            if map[i][j] == 0:
                t+="."
            elif map[i][j] == 1:
                t+="D"
            elif map[i][j] == 2:
                t+="A"
            elif map[i][j] == 3:
                t+="-"
        print(t)

def voisin(xy):
    x = xy[0][0]
    y = xy[0][1]
    rep = [(0,0)]
    for i in (-1,1,0):
        for j in (0,1,-1):
            try:
                if map[x+i][y+j] != 3 and (i != 0 or j != 0) :  # Si c'est passable et que les deux i,j sont pas 0.
                    rep.append((x+i,y+j))
            except IndexError:
                pass
    return rep

def distance(a, b):
    (x1, y1) = a[0]
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def chemin():


# Theoriquement, le `main'
initmap()
foo, cost = chemin()
print(foo)                     
    
