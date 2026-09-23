from pieces.pions import coup_pion_blanc, coup_pion_noir
from pieces.tour import coup_tour_blanc, coup_tour_noir
from pieces.fou import coup_fou_blanc, coup_fou_noir
from pieces.dame import coup_dame_blanc, coup_dame_noir
from pieces.cavalier import coup_cavalier_blanc, coup_cavalier_noir
from pieces.roi import coup_roi_blanc, coup_roi_noir

def calculer_coups(piece, ligne, colonne, grille):
    if piece == "♙":
        return coup_pion_blanc(ligne, colonne, grille)
    elif piece == "♟":
        return coup_pion_noir(ligne, colonne, grille)
    elif piece == "♖":
        return coup_tour_blanc(ligne, colonne, grille)
    elif piece == "♜":
        return coup_tour_noir(ligne, colonne, grille)
    elif piece == "♗":
        return coup_fou_blanc(ligne, colonne, grille)
    elif piece == "♝":
        return coup_fou_noir(ligne, colonne, grille)
    elif piece == "♕":
        return coup_dame_blanc(ligne, colonne, grille)
    elif piece == "♛":
        return coup_dame_noir(ligne, colonne, grille)
    elif piece == "♘":
        return coup_cavalier_blanc(ligne, colonne, grille)
    elif piece == "♞":
        return coup_cavalier_noir(ligne, colonne, grille)
    elif piece == "♔":
        return coup_roi_blanc(ligne, colonne, grille)
    elif piece == "♚":
        return coup_roi_noir(ligne, colonne, grille)
    else:
        return []