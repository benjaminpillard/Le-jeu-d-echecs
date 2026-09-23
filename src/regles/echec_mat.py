from regles.echec import roi_en_echec, coup_met_en_echec
import game
import config

def echec_et_mat(grille, couleur):
    # D'abord, le roi doit être en échec pour qu'il y ait échec et mat
    if not roi_en_echec(grille, couleur):
        return False

    est_blanc = couleur == "blanc"

    # On parcourt toutes les pièces du joueur en échec
    for ligne in range(8):
        for colonne in range(8):
            piece = grille[ligne][colonne]

            if piece is None:
                continue

            piece_est_blanche = piece in config.PIECES_BLANCHES

            # On ne s'intéresse qu'aux pièces du joueur en échec
            if piece_est_blanche != est_blanc:
                continue

            # On regarde tous les coups possibles pour cette pièce
            coups = game.calculer_coups(piece, ligne, colonne, grille)

            for (nouvelle_ligne, nouvelle_colonne) in coups:
                # Si au moins un coup permet de sortir de l'échec, ce n'est pas mat
                if not coup_met_en_echec(grille, ligne, colonne, nouvelle_ligne, nouvelle_colonne, couleur):
                    return False

    # Aucune pièce n'a de coup qui sauve le roi : c'est échec et mat
    return True