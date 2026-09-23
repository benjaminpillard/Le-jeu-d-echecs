import copy
import config
import game


def trouver_roi(grille, couleur):
    roi = "♔" if couleur == "blanc" else "♚"

    for ligne in range(8):
        for colonne in range(8):
            if grille[ligne][colonne] == roi:
                return ligne, colonne

    return None


def roi_en_echec(grille, couleur):
    position_roi = trouver_roi(grille, couleur)

    if position_roi is None:
        return True

    ligne_roi, colonne_roi = position_roi

    for ligne in range(8):
        for colonne in range(8):
            piece = grille[ligne][colonne]

            if piece is None:
                continue

            est_blanche = piece in config.PIECES_BLANCHES

            if (couleur == "blanc" and est_blanche) or (couleur == "noir" and not est_blanche):
                continue

            coups = game.calculer_coups(piece, ligne, colonne, grille)
            if (ligne_roi, colonne_roi) in coups:
                return True

    return False


def coup_met_en_echec(grille, anc_ligne, anc_colonne, ligne, colonne, couleur):
    grille_test = copy.deepcopy(grille)

    piece = grille_test[anc_ligne][anc_colonne]
    grille_test[ligne][colonne] = piece
    grille_test[anc_ligne][anc_colonne] = None

    return roi_en_echec(grille_test, couleur)