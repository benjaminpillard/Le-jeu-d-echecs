# Gère la règle spéciale de la prise en passant

import config


def pion_capturable_en_passant(grille, ligne, colonne, couleur, dernier_coup_double):
    """
    Vérifie si le pion en (ligne, colonne) peut capturer en passant.
    dernier_coup_double : position (ligne, colonne) du pion adverse qui vient
                          d'avancer de 2 cases, ou None si ce n'est pas le cas.
    Renvoie la case de capture (ligne, colonne) si possible, sinon None.
    """
    if dernier_coup_double is None:
        return None

    ligne_adverse, colonne_adverse = dernier_coup_double

    # Le pion adverse doit être sur la même ligne que notre pion
    if ligne_adverse != ligne:
        return None

    # Le pion adverse doit être sur une colonne adjacente (gauche ou droite)
    if abs(colonne_adverse - colonne) != 1:
        return None

    # La case d'arrivée de la capture est juste derrière le pion adverse
    if couleur == "blanc":
        case_capture = (ligne - 1, colonne_adverse)
    else:
        case_capture = (ligne + 1, colonne_adverse)

    return case_capture


def appliquer_prise_en_passant(grille, anc_ligne, anc_colonne, ligne, colonne, couleur):
    """
    Effectue la capture en passant : déplace le pion et retire le pion adverse capturé.
    """
    piece = grille[anc_ligne][anc_colonne]

    grille[ligne][colonne] = piece
    grille[anc_ligne][anc_colonne] = None

    # Le pion capturé est sur la même ligne que le point de départ, mais colonne d'arrivée
    grille[anc_ligne][colonne] = None