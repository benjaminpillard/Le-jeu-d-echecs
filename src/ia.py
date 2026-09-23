import chess
import chess.engine


# ============================================================
# CONFIGURATION STOCKFISH
# ============================================================

STOCKFISH_PATH = "C:/Users/Benjamin/Desktop/stockfish/stockfish-windows-x86-64-universal.exe"

engine = None


# ============================================================
# INITIALISATION / FERMETURE
# ============================================================

def initialiser():
    """Lance Stockfish."""

    global engine

    if engine is not None:
        return True

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        print("Stockfish connecté.")
        return True

    except Exception as erreur:
        print("ERREUR STOCKFISH :", erreur)
        engine = None
        return False


def fermer():
    """Ferme Stockfish."""

    global engine

    if engine is not None:
        try:
            engine.quit()
        except Exception:
            pass

        engine = None


# ============================================================
# DIFFICULTÉ
# ============================================================

def configurer_difficulte(niveau):
    """
    Configure Stockfish selon le niveau :

    1 = Débutant
    2 = Facile
    3 = Intermédiaire
    4 = Difficile
    5 = Master
    """

    if engine is None:
        return

    if niveau == 1:

        engine.configure({
            "Skill Level": 0
        })

    elif niveau == 2:

        engine.configure({
            "Skill Level": 5
        })

    elif niveau == 3:

        engine.configure({
            "UCI_LimitStrength": True,
            "UCI_Elo": 1500
        })

    elif niveau == 4:

        engine.configure({
            "UCI_LimitStrength": True,
            "UCI_Elo": 2000
        })

    else:

        engine.configure({
            "UCI_LimitStrength": False,
            "Skill Level": 20
        })


# ============================================================
# CONVERSION DU PLATEAU
# ============================================================

CORRESPONDANCE_PIECES = {

    # Blancs
    "♙": "P",
    "♘": "N",
    "♗": "B",
    "♖": "R",
    "♕": "Q",
    "♔": "K",

    # Noirs
    "♟": "p",
    "♞": "n",
    "♝": "b",
    "♜": "r",
    "♛": "q",
    "♚": "k",
}


def grille_vers_fen(
    grille,
    couleur,
    roi_blanc_a_bouge,
    roi_noir_a_bouge,
    tour_a1_a_bouge,
    tour_h1_a_bouge,
    tour_a8_a_bouge,
    tour_h8_a_bouge,
    dernier_coup_double
):
    """
    Transforme ton plateau Pygame en FEN complète.

    Cela permet à Stockfish de connaître :
    - les pièces
    - le joueur qui doit jouer
    - les droits de roque
    - la prise en passant
    """

    lignes_fen = []

    for ligne in grille:

        ligne_fen = ""
        cases_vides = 0

        for piece in ligne:

            if piece is None:

                cases_vides += 1

            else:

                if cases_vides > 0:
                    ligne_fen += str(cases_vides)
                    cases_vides = 0

                ligne_fen += CORRESPONDANCE_PIECES[piece]

        if cases_vides > 0:
            ligne_fen += str(cases_vides)

        lignes_fen.append(ligne_fen)

    # --------------------------------------------------------
    # TOUR
    # --------------------------------------------------------

    tour = "w" if couleur == "blanc" else "b"

    # --------------------------------------------------------
    # DROITS DE ROQUE
    # --------------------------------------------------------

    droits_roque = ""

    if not roi_blanc_a_bouge:

        if not tour_h1_a_bouge:
            droits_roque += "K"

        if not tour_a1_a_bouge:
            droits_roque += "Q"

    if not roi_noir_a_bouge:

        if not tour_h8_a_bouge:
            droits_roque += "k"

        if not tour_a8_a_bouge:
            droits_roque += "q"

    if droits_roque == "":
        droits_roque = "-"

    # --------------------------------------------------------
    # PRISE EN PASSANT
    # --------------------------------------------------------

    case_en_passant = "-"

    if dernier_coup_double is not None:

        ligne, colonne = dernier_coup_double

        fichiers = "abcdefgh"

        # Le pion blanc vient de monter de 2 cases.
        # La case disponible pour l'EP est derrière lui.
        if grille[ligne][colonne] in ("♙", "♟"):

            if grille[ligne][colonne] == "♙":
                ligne_ep = ligne + 1
            else:
                ligne_ep = ligne - 1

            if 0 <= ligne_ep < 8:
                case_en_passant = (
                    fichiers[colonne] + str(8 - ligne_ep)
                )

    # --------------------------------------------------------
    # FEN
    # --------------------------------------------------------

    position = "/".join(lignes_fen)

    fen = (
        f"{position} "
        f"{tour} "
        f"{droits_roque} "
        f"{case_en_passant} "
        f"0 1"
    )

    return fen


# ============================================================
# OBTENIR UN COUP
# ============================================================

def obtenir_coup(
    grille,
    couleur,
    roi_blanc_a_bouge,
    roi_noir_a_bouge,
    tour_a1_a_bouge,
    tour_h1_a_bouge,
    tour_a8_a_bouge,
    tour_h8_a_bouge,
    dernier_coup_double,
    temps_reflexion=0.3
):
    """
    Demande à Stockfish de choisir un coup.

    Retourne :

        (
            ligne_depart,
            colonne_depart,
            ligne_arrivee,
            colonne_arrivee,
            promotion
        )

    """

    if engine is None:
        return None

    fen = grille_vers_fen(
        grille,
        couleur,
        roi_blanc_a_bouge,
        roi_noir_a_bouge,
        tour_a1_a_bouge,
        tour_h1_a_bouge,
        tour_a8_a_bouge,
        tour_h8_a_bouge,
        dernier_coup_double
    )

    try:

        board = chess.Board(fen)

        if not board.is_valid():
            print("Position FEN invalide :")
            print(fen)
            return None

        resultat = engine.play(
            board,
            chess.engine.Limit(time=temps_reflexion)
        )

        move = resultat.move

        ligne_depart = 7 - chess.square_rank(move.from_square) # type: ignore
        colonne_depart = chess.square_file(move.from_square) # type: ignore

        assert move is not None
        ligne_arrivee = 7 - chess.square_rank(move.to_square)
        colonne_arrivee = chess.square_file(move.to_square) # type: ignore

        promotion = None

        if move.promotion is not None:

            promotion = {
                chess.QUEEN: "Q",
                chess.ROOK: "R",
                chess.BISHOP: "B",
                chess.KNIGHT: "N"
            }.get(move.promotion)

        return (
            ligne_depart,
            colonne_depart,
            ligne_arrivee,
            colonne_arrivee,
            promotion
        )

    except Exception as erreur:

        print("Erreur lors du calcul Stockfish :", erreur)

        return None