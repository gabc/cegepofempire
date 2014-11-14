# Petit fichier contenant des fonctions que je suis incapable de placer dans une classe
import math

def roundtenth(x):
    """arrondi a la dizaine vers le bas 9 -> 0, 15 -> 10"""
    return x if x % 10 == 0 else x - x % 10

def trouveCase(x, y):
    """Avec une coordonnée en pixel, retrouve la case"""
    cx = math.trunc(x/20)
    cy = math.trunc(y/20)
    return (cx,cy)

def trouvePixel(x, y):
    """Avec les coordonnée d'une case, retrouve les pixels de son centre"""
    px = x * 20 + 10
    py = y * 20 + 10
