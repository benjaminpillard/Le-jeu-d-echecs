NB_CASES = 8
MARGE = 30
ZONE_CAPTURE = 50

TAILLE_CASE = 650 // NB_CASES
LARGEUR_PLATEAU = NB_CASES * TAILLE_CASE
LARGEUR_ECRAN = LARGEUR_PLATEAU + MARGE
HAUTEUR_ECRAN = LARGEUR_PLATEAU + MARGE + (ZONE_CAPTURE * 2)
DECALAGE_HAUT = ZONE_CAPTURE

# Décalage pour centrer le plateau dans la fenêtre (recalculé à chaque redimensionnement)
DECALAGE_X = 0
DECALAGE_Y = 0

# Couleurs de base
BLANC = (255, 255, 255)
VERT_SELECTION = (186, 202, 68)  # vert clair, plus doux que le vert des cases foncées)
NOIR = (0, 0, 0)
GRIS_SHADOW = (63, 63, 63)
GRIS_CLAIR = (220, 220, 220)
ROUGE_ECHEC = (220, 40, 40)

# Palette façon chess.com
FOND_SOMBRE = (49, 46, 43)            # gris-vert foncé du fond général
VERT_CASE = (118, 150, 86)            # cases foncées du plateau
BEIGE_CASE = (238, 238, 210)          # cases claires du plateau
VERT_BOUTON = (129, 182, 76)          # vert vif pour les boutons
VERT_BOUTON_SURVOL = (152, 202, 102)  # légèrement plus clair
BLANC_TEXTE = (255, 255, 255)
CARTE_FOND = (62, 58, 54)  # légèrement plus clair que FOND_SOMBRE, pour les cartes du menu
COULEUR_BULLET = (220, 90, 70)
COULEUR_BLITZ = (230, 160, 50)
COULEUR_RAPIDE = (80, 140, 200)

LETTRES = "abcdefgh"

PIECES_BLANCHES = "♙♖♗♘♕♔"
PIECES_NOIRES = "♟♜♞♝♛♚"

VALEURS_PIECES = {
    "♙": 1, "♟": 1,
    "♘": 3, "♞": 3,
    "♗": 3, "♝": 3,
    "♖": 5, "♜": 5,
    "♕": 9, "♛": 9,
    "♔": 0, "♚": 0,
}


def recalculer_dimensions(largeur_fenetre, hauteur_fenetre):
    global TAILLE_CASE, LARGEUR_PLATEAU, LARGEUR_ECRAN, HAUTEUR_ECRAN, DECALAGE_HAUT, DECALAGE_X, DECALAGE_Y

    espace_disponible_largeur = largeur_fenetre - MARGE
    espace_disponible_hauteur = hauteur_fenetre - MARGE - (ZONE_CAPTURE * 2)

    espace_disponible = min(espace_disponible_largeur, espace_disponible_hauteur)

    TAILLE_CASE = max(espace_disponible // NB_CASES, 20)

    LARGEUR_PLATEAU = NB_CASES * TAILLE_CASE
    LARGEUR_ECRAN = LARGEUR_PLATEAU + MARGE
    HAUTEUR_ECRAN = LARGEUR_PLATEAU + MARGE + (ZONE_CAPTURE * 2)
    DECALAGE_HAUT = ZONE_CAPTURE

    DECALAGE_X = (largeur_fenetre - LARGEUR_ECRAN) // 2
    DECALAGE_Y = (hauteur_fenetre - HAUTEUR_ECRAN) // 2