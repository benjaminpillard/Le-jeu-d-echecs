import config

def coup_pion_blanc(ligne, colonne, grille):
    coups = []

    if 0 <= ligne - 1 <= 7:
        if grille[ligne - 1][colonne] is None:
            coups.append((ligne - 1, colonne))

            if ligne == 6 and grille[ligne - 2][colonne] is None:
                coups.append((ligne - 2, colonne))

    for d_col in [-1, 1]:
        l, c = ligne - 1, colonne + d_col
        if 0 <= l <= 7 and 0 <= c <= 7:
            if grille[l][c] is not None and grille[l][c] in config.PIECES_NOIRES:
                coups.append((l, c))

    return coups


def coup_pion_noir(ligne, colonne, grille):
    coups = []

    if 0 <= ligne + 1 <= 7:
        if grille[ligne + 1][colonne] is None:
            coups.append((ligne + 1, colonne))

            if ligne == 1 and grille[ligne + 2][colonne] is None:
                coups.append((ligne + 2, colonne))

    for d_col in [-1, 1]:
        l, c = ligne + 1, colonne + d_col
        if 0 <= l <= 7 and 0 <= c <= 7:
            if grille[l][c] is not None and grille[l][c] in config.PIECES_BLANCHES:
                coups.append((l, c))

    return coups