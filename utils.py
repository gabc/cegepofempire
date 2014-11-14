# Petit fichier contenant des fonctions que je suis incapable de placer dans une classe
def roundtenth(x):
    """arrondi a la dizaine vers le bas 9 -> 0, 15 -> 10"""
    return x if x % 10 == 0 else x - x % 10
