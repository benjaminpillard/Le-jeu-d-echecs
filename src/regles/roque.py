# Ce fichier gère la règle spéciale du roque (petit roque et grand roque)

import config
from regles.echec import roi_en_echec, coup_met_en_echec
import copy


def case_est_attaquee(grille, ligne, colonne, couleur):
    """
    Vérifie si une case précise est attaquée par une pièce adverse.
    Utile pour vérifier que le roi ne traverse aucune case dangereuse pendant le roque.
    """
    est_blanc = couleur == "blanc"

    for l in range(8):
        for c in range(8):
            piece = grille[l][c]
            if piece is None:
                continue

            piece_est_blanche = piece in config.PIECES_BLANCHES

            # On ne regarde que les pièces ADVERSES
            if piece_est_blanche == est_blanc:
                continue

            # On importe calculer_coups ici pour éviter un import circulaire avec game.py
            import game
            coups = game.calculer_coups(piece, l, c, grille)

            if (ligne, colonne) in coups:
                return True

    return False


def petit_roque_possible(grille, couleur, roi_a_bouge, tour_h_a_bouge):
    """
    Vérifie si le petit roque (côté roi, vers la droite) est possible.
    couleur : "blanc" ou "noir"
    roi_a_bouge : True si le roi a déjà bougé
    tour_h_a_bouge : True si la tour du côté roi (colonne 7, la tour "h") a déjà bougé
    """
    # Condition 1 : ni le roi ni la tour n'ont bougé
    if roi_a_bouge or tour_h_a_bouge:
        return False

    # Ligne du roi selon la couleur (7 pour les blancs, 0 pour les noirs)
    ligne = 7 if couleur == "blanc" else 0

    # Condition 2 : les cases entre le roi (colonne 4) et la tour (colonne 7) doivent être vides
    # Ce sont les colonnes 5 et 6
    if grille[ligne][5] is not None or grille[ligne][6] is not None:
        return False

    # Condition 3 : le roi ne doit pas être actuellement en échec
    if roi_en_echec(grille, couleur):
        return False

    # Condition 4 : le roi ne doit traverser aucune case attaquée
    # (colonne 4 = départ, colonne 5 = passage, colonne 6 = arrivée)
    for colonne_test in [4, 5, 6]:
        if case_est_attaquee(grille, ligne, colonne_test, couleur):
            return False

    return True


def grand_roque_possible(grille, couleur, roi_a_bouge, tour_a_a_bouge):
    """
    Vérifie si le grand roque (côté dame, vers la gauche) est possible.
    tour_a_a_bouge : True si la tour du côté dame (colonne 0, la tour "a") a déjà bougé
    """
    if roi_a_bouge or tour_a_a_bouge:
        return False

    ligne = 7 if couleur == "blanc" else 0

    # Les cases entre le roi (colonne 4) et la tour (colonne 0) doivent être vides
    # Ce sont les colonnes 1, 2 et 3
    if grille[ligne][1] is not None or grille[ligne][2] is not None or grille[ligne][3] is not None:
        return False

    if roi_en_echec(grille, couleur):
        return False

    # Le roi traverse les colonnes 4 (départ), 3 (passage), 2 (arrivée)
    # (la colonne 1 n'est pas traversée par le roi, seulement par la tour, donc pas besoin de la vérifier)
    for colonne_test in [4, 3, 2]:
        if case_est_attaquee(grille, ligne, colonne_test, couleur):
            return False

    return True


def appliquer_petit_roque(grille, couleur):
    """
    Effectue réellement le petit roque sur le plateau : déplace le roi de 2 cases,
    et fait "sauter" la tour de l'autre côté du roi.
    """
    ligne = 7 if couleur == "blanc" else 0
    roi = "♔" if couleur == "blanc" else "♚"
    tour = "♖" if couleur == "blanc" else "♜"

    # Déplacement du roi : colonne 4 → colonne 6
    grille[ligne][4] = None
    grille[ligne][6] = roi

    # Déplacement de la tour : colonne 7 → colonne 5
    grille[ligne][7] = None
    grille[ligne][5] = tour


def appliquer_grand_roque(grille, couleur):
    """
    Effectue réellement le grand roque sur le plateau.
    """
    ligne = 7 if couleur == "blanc" else 0
    roi = "♔" if couleur == "blanc" else "♚"
    tour = "♖" if couleur == "blanc" else "♜"

    # Déplacement du roi : colonne 4 → colonne 2
    grille[ligne][4] = None
    grille[ligne][2] = roi

    # Déplacement de la tour : colonne 0 → colonne 3
    grille[ligne][0] = None
    grille[ligne][3] = tour