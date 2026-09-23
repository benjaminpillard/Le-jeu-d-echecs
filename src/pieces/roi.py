import config

def coup_roi_blanc(ligne, colonne, grille):
    coups = []
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    for d_lig, d_col in directions:
        l, c = ligne + d_lig, colonne + d_col
        if 0 <= l < 8 and 0 <= c < 8:
            piece = grille[l][c]
            if piece is None or piece in config.PIECES_NOIRES:
                coups.append((l, c))

    return coups


def coup_roi_noir(ligne, colonne, grille):
    coups = []
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]

    for d_lig, d_col in directions:
        l, c = ligne + d_lig, colonne + d_col
        if 0 <= l < 8 and 0 <= c < 8:
            piece = grille[l][c]
            if piece is None or piece in config.PIECES_BLANCHES:
                coups.append((l, c))

    return coups