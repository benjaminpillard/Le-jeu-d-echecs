# Gère la promotion du pion en dame quand il atteint la dernière ligne

def pion_doit_promouvoir(piece, ligne):
    """
    Vérifie si un pion doit être promu : pion blanc arrivé ligne 0,
    ou pion noir arrivé ligne 7.
    """
    if piece == "♙" and ligne == 0:
        return True
    if piece == "♟" and ligne == 7:
        return True
    return False


def promouvoir(grille, ligne, colonne, couleur):
    """
    Remplace le pion par une dame (version simplifiée : toujours une dame,
    la promotion en tour/fou/cavalier est possible aux échecs mais plus rare).
    """
    grille[ligne][colonne] = "♕" if couleur == "blanc" else "♛"
    grille[ligne][colonne] = "♘" if couleur == "blanc" else "♞"
    grille[ligne][colonne] = "♖" if couleur == "blanc" else "♜"
    grille[ligne][colonne] = "♗" if couleur == "blanc" else "♝"
