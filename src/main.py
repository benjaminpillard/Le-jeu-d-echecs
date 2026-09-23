import pygame
import random
import threading
import config
import plateau
import affichage
import game
import menu
import ia

from regles import echec
from regles import echec_mat
from regles import roque
from regles import prise_en_passant
from regles import promotion


# ================================================================
# INITIALISATION
# ================================================================

pygame.init()
affichage.init_police()

if not ia.initialiser():
    print("Attention : Stockfish n'a pas pu être lancé.")

fenetre = pygame.display.set_mode(
    (config.LARGEUR_ECRAN, config.HAUTEUR_ECRAN),
    pygame.RESIZABLE
)

pygame.display.set_caption("Plateau d'Échecs")

config.recalculer_dimensions(config.LARGEUR_ECRAN, config.HAUTEUR_ECRAN)

images = plateau.charger_images()

police_reflexion = pygame.font.SysFont("arial", 24, bold=True)


# ================================================================
# ÉTAT DU JEU
# ================================================================

etat = "menu"  # "menu", "choix_adversaire", "partie"

rectangles_boutons_menu = []
mode_choisi = None

rect_joueur_vs_joueur = None
rect_joueur_vs_ia = None


# ================================================================
# IA
# ================================================================

contre_ia = False
couleur_ia = None
PROFONDEUR_IA = 3

# --- Gestion du calcul en arrière-plan (thread) ---
ia_thread = None
ia_calcul_en_cours = False
ia_resultat = [None]  # liste utilisée comme "boîte" partagée entre threads


def ia_calculer_en_arriere_plan(couleur, rbb, rnb, ta1, th1, ta8, th8, dcd, temps_reflexion):
    """
    Fonction exécutée dans un thread séparé : elle appelle Stockfish
    et range le résultat dans ia_resultat[0] une fois trouvé.
    """
    resultat = ia.obtenir_coup(
        plateau.grille, couleur, rbb, rnb, ta1, th1, ta8, th8, dcd,
        temps_reflexion=temps_reflexion
    )
    ia_resultat[0] = resultat # type: ignore


# ================================================================
# SÉLECTION
# ================================================================

case_selectionnee = None
coups_possibles = []


# ================================================================
# TOUR
# ================================================================

trait_aux_blancs = True


# ================================================================
# FIN DE PARTIE
# ================================================================

partie_terminee = False
message_fin_partie = ""

rect_rejouer = None
rect_menu = None


# ================================================================
# ROQUE
# ================================================================

roi_blanc_a_bouge = False
roi_noir_a_bouge = False

tour_a1_a_bouge = False
tour_h1_a_bouge = False

tour_a8_a_bouge = False
tour_h8_a_bouge = False


# ================================================================
# PRISE EN PASSANT
# ================================================================

dernier_coup_double = None


# ================================================================
# CAPTURES
# ================================================================

captures_blanc = []
captures_noir = []


# ================================================================
# HORLOGE
# ================================================================

temps_blanc = 0
temps_noir = 0
increment = 0
dernier_tick = 0


# ================================================================
# CONVERSION PIXEL -> CASE
# ================================================================

def pixel_vers_case(x, y):
    couleur_joueur = (
        "noir" if couleur_ia == "blanc" else "blanc"
    ) if contre_ia else "blanc"

    colonne_aff = (x - config.DECALAGE_X - config.MARGE) // config.TAILLE_CASE
    ligne_aff = (y - config.DECALAGE_Y - config.DECALAGE_HAUT) // config.TAILLE_CASE

    if couleur_joueur == "noir":
        return (7 - ligne_aff, 7 - colonne_aff)

    return (ligne_aff, colonne_aff)


# ================================================================
# MISE À JOUR DES MOUVEMENTS
# ================================================================

def mettre_a_jour_mouvements(piece, anc_ligne, anc_colonne):
    global roi_blanc_a_bouge, roi_noir_a_bouge
    global tour_a1_a_bouge, tour_h1_a_bouge, tour_a8_a_bouge, tour_h8_a_bouge

    if piece == "♔":
        roi_blanc_a_bouge = True
    elif piece == "♚":
        roi_noir_a_bouge = True
    elif piece == "♖" and (anc_ligne, anc_colonne) == (7, 0):
        tour_a1_a_bouge = True
    elif piece == "♖" and (anc_ligne, anc_colonne) == (7, 7):
        tour_h1_a_bouge = True
    elif piece == "♜" and (anc_ligne, anc_colonne) == (0, 0):
        tour_a8_a_bouge = True
    elif piece == "♜" and (anc_ligne, anc_colonne) == (0, 7):
        tour_h8_a_bouge = True


# ================================================================
# RÉINITIALISER LA PARTIE
# ================================================================

def reinitialiser_partie():
    global plateau, case_selectionnee, coups_possibles, trait_aux_blancs
    global partie_terminee, message_fin_partie
    global roi_blanc_a_bouge, roi_noir_a_bouge
    global tour_a1_a_bouge, tour_h1_a_bouge, tour_a8_a_bouge, tour_h8_a_bouge
    global dernier_coup_double, captures_blanc, captures_noir
    global temps_blanc, temps_noir, increment, dernier_tick
    global ia_thread, ia_calcul_en_cours, ia_resultat

    import importlib
    importlib.reload(plateau)

    case_selectionnee = None
    coups_possibles = []
    trait_aux_blancs = True
    partie_terminee = False
    message_fin_partie = ""
    roi_blanc_a_bouge = False
    roi_noir_a_bouge = False
    tour_a1_a_bouge = False
    tour_h1_a_bouge = False
    tour_a8_a_bouge = False
    tour_h8_a_bouge = False
    dernier_coup_double = None
    captures_blanc = []
    captures_noir = []

    temps_blanc = mode_choisi["temps"] # type: ignore
    temps_noir = mode_choisi["temps"] # type: ignore
    increment = mode_choisi["increment"] # type: ignore
    dernier_tick = pygame.time.get_ticks()

    ia_thread = None
    ia_calcul_en_cours = False
    ia_resultat = [None]


# ================================================================
# JOUER UN COUP NORMAL
# ================================================================

def jouer_coup(anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle):
    global trait_aux_blancs, dernier_coup_double, partie_terminee, message_fin_partie

    piece = plateau.grille[anc_ligne][anc_colonne]

    piece_capturee = plateau.grille[ligne][colonne]
    if piece_capturee is not None:
        if couleur_actuelle == "blanc":
            captures_blanc.append(piece_capturee)
        else:
            captures_noir.append(piece_capturee)

    plateau.grille[ligne][colonne] = piece
    plateau.grille[anc_ligne][anc_colonne] = None
    mettre_a_jour_mouvements(piece, anc_ligne, anc_colonne)

    if promotion.pion_doit_promouvoir(piece, ligne):
        if contre_ia and couleur_actuelle == couleur_ia:
            promotion.promouvoir(plateau.grille, ligne, colonne, couleur_actuelle)
        else:
            symbole_choisi = affichage.gerer_promotion_pygame(fenetre, couleur_actuelle, images)
            plateau.grille[ligne][colonne] = symbole_choisi

    if piece in ("♙", "♟") and abs(ligne - anc_ligne) == 2:
        dernier_coup_double = (ligne, colonne)
    else:
        dernier_coup_double = None

    trait_aux_blancs = not trait_aux_blancs

    couleur_adverse = "blanc" if trait_aux_blancs else "noir"
    if echec_mat.echec_et_mat(plateau.grille, couleur_adverse):
        partie_terminee = True
        message_fin_partie = f"Échec et mat ! Les {couleur_actuelle}s gagnent."


# ================================================================
# JOUER UN COUP DE L'IA
# ================================================================

def jouer_coup_ia(anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle, promotion_ia=None):
    global trait_aux_blancs, dernier_coup_double, partie_terminee, message_fin_partie
    global temps_blanc, temps_noir

    piece = plateau.grille[anc_ligne][anc_colonne]

    if piece is None:
        return False

    if piece in ("♔", "♚") and abs(colonne - anc_colonne) == 2:
        if colonne == 6:
            roque.appliquer_petit_roque(plateau.grille, couleur_actuelle)
        else:
            roque.appliquer_grand_roque(plateau.grille, couleur_actuelle)

        mettre_a_jour_mouvements(piece, anc_ligne, anc_colonne)
        dernier_coup_double = None

        if couleur_actuelle == "blanc":
            temps_blanc += increment
        else:
            temps_noir += increment

        trait_aux_blancs = not trait_aux_blancs
        return True

    est_prise_en_passant = (
        piece in ("♙", "♟")
        and colonne != anc_colonne
        and plateau.grille[ligne][colonne] is None
    )

    if est_prise_en_passant:
        piece_capturee = plateau.grille[anc_ligne][colonne]
        if piece_capturee is not None:
            if couleur_actuelle == "blanc":
                captures_blanc.append(piece_capturee)
            else:
                captures_noir.append(piece_capturee)

        prise_en_passant.appliquer_prise_en_passant(
            plateau.grille, anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle
        )

        dernier_coup_double = None

        if couleur_actuelle == "blanc":
            temps_blanc += increment
        else:
            temps_noir += increment

        trait_aux_blancs = not trait_aux_blancs
        return True

    jouer_coup(anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle)
    return True


# ================================================================
# BOUCLE PRINCIPALE
# ================================================================

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            config.recalculer_dimensions(event.w, event.h)
            fenetre = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            images = plateau.charger_images()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if etat == "menu":
                mode_trouve = menu.detecter_clic_bouton(event.pos, rectangles_boutons_menu)
                if mode_trouve is not None:
                    mode_choisi = mode_trouve
                    etat = "choix_adversaire"

            elif etat == "choix_adversaire":
                if rect_joueur_vs_joueur is not None and rect_joueur_vs_joueur.collidepoint(event.pos):
                    contre_ia = False
                    couleur_ia = None
                    reinitialiser_partie()
                    etat = "partie"

                elif rect_joueur_vs_ia is not None and rect_joueur_vs_ia.collidepoint(event.pos):
                    contre_ia = True
                    couleur_ia = random.choice(["blanc", "noir"])
                    ia.configurer_difficulte(PROFONDEUR_IA)
                    reinitialiser_partie()
                    etat = "partie"

            elif etat == "partie" and partie_terminee:
                if rect_rejouer is not None and rect_rejouer.collidepoint(event.pos):
                    etat = "choix_adversaire"
                elif rect_menu is not None and rect_menu.collidepoint(event.pos):
                    etat = "menu"

            elif etat == "partie" and not partie_terminee:
                couleur_du_trait = "blanc" if trait_aux_blancs else "noir"

                if contre_ia and couleur_du_trait == couleur_ia:
                    continue

                x, y = event.pos
                ligne, colonne = pixel_vers_case(x, y)

                if not (0 <= ligne < 8 and 0 <= colonne < 8):
                    continue

                if case_selectionnee is None:
                    piece = plateau.grille[ligne][colonne]

                    if piece is not None:
                        est_piece_blanche = piece in config.PIECES_BLANCHES

                        if (trait_aux_blancs and est_piece_blanche) or (not trait_aux_blancs and not est_piece_blanche):
                            case_selectionnee = (ligne, colonne)
                            coups_possibles = game.calculer_coups(piece, ligne, colonne, plateau.grille)

                            if piece in ("♔", "♚"):
                                couleur = "blanc" if trait_aux_blancs else "noir"
                                roi_a_bouge = roi_blanc_a_bouge if couleur == "blanc" else roi_noir_a_bouge
                                tour_h_a_bouge = tour_h1_a_bouge if couleur == "blanc" else tour_h8_a_bouge
                                tour_a_a_bouge = tour_a1_a_bouge if couleur == "blanc" else tour_a8_a_bouge
                                ligne_roque = 7 if couleur == "blanc" else 0

                                if roque.petit_roque_possible(plateau.grille, couleur, roi_a_bouge, tour_h_a_bouge):
                                    coups_possibles.append((ligne_roque, 6))

                                if roque.grand_roque_possible(plateau.grille, couleur, roi_a_bouge, tour_a_a_bouge):
                                    coups_possibles.append((ligne_roque, 2))

                            if piece in ("♙", "♟"):
                                couleur = "blanc" if trait_aux_blancs else "noir"
                                case_ep = prise_en_passant.pion_capturable_en_passant(
                                    plateau.grille, ligne, colonne, couleur, dernier_coup_double
                                )
                                if case_ep is not None:
                                    coups_possibles.append(case_ep)
                else:
                    anc_ligne, anc_colonne = case_selectionnee
                    piece = plateau.grille[anc_ligne][anc_colonne]

                    if (ligne, colonne) in coups_possibles:
                        couleur_actuelle = "blanc" if trait_aux_blancs else "noir"

                        est_roque = piece in ("♔", "♚") and abs(colonne - anc_colonne) == 2

                        est_prise_en_passant = (
                            piece in ("♙", "♟")
                            and colonne != anc_colonne
                            and plateau.grille[ligne][colonne] is None
                        )

                        if est_roque:
                            if colonne == 6:
                                roque.appliquer_petit_roque(plateau.grille, couleur_actuelle)
                            else:
                                roque.appliquer_grand_roque(plateau.grille, couleur_actuelle)
                            mettre_a_jour_mouvements(piece, anc_ligne, anc_colonne)

                            if couleur_actuelle == "blanc":
                                temps_blanc += increment
                            else:
                                temps_noir += increment

                            trait_aux_blancs = not trait_aux_blancs
                            dernier_coup_double = None

                        elif est_prise_en_passant:
                            piece_capturee = plateau.grille[anc_ligne][colonne]
                            if piece_capturee is not None:
                                if couleur_actuelle == "blanc":
                                    captures_blanc.append(piece_capturee)
                                else:
                                    captures_noir.append(piece_capturee)

                            prise_en_passant.appliquer_prise_en_passant(
                                plateau.grille, anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle
                            )

                            if couleur_actuelle == "blanc":
                                temps_blanc += increment
                            else:
                                temps_noir += increment

                            trait_aux_blancs = not trait_aux_blancs
                            dernier_coup_double = None

                        elif not echec.coup_met_en_echec(plateau.grille, anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle):
                            jouer_coup(anc_ligne, anc_colonne, ligne, colonne, couleur_actuelle)

                            if couleur_actuelle == "blanc":
                                temps_blanc += increment
                            else:
                                temps_noir += increment

                    case_selectionnee = None
                    coups_possibles = []

    # ================================================================
    # TOUR DE L'IA — calcul en arrière-plan (thread)
    # ================================================================

    if etat == "partie" and contre_ia and not partie_terminee:
        couleur_du_trait = "blanc" if trait_aux_blancs else "noir"

        if couleur_du_trait == couleur_ia:

            if not ia_calcul_en_cours:
                # On démarre le calcul dans un thread séparé
                ia_calcul_en_cours = True
                ia_resultat[0] = None
                temps_reflexion_aleatoire = random.uniform(1.0, 3.0)

                ia_thread = threading.Thread(
                    target=ia_calculer_en_arriere_plan,
                    args=(
                        couleur_ia,
                        roi_blanc_a_bouge, roi_noir_a_bouge,
                        tour_a1_a_bouge, tour_h1_a_bouge,
                        tour_a8_a_bouge, tour_h8_a_bouge,
                        dernier_coup_double,
                        temps_reflexion_aleatoire
                    )
                )
                ia_thread.start()

            elif not ia_thread.is_alive(): # type: ignore
                # Le thread a fini : on applique le coup trouvé
                coup_ia = ia_resultat[0]
                ia_calcul_en_cours = False

                if coup_ia is not None:
                    (anc_ligne, anc_colonne, ligne, colonne, promotion_ia) = coup_ia # pyright: ignore[reportGeneralTypeIssues]
                    jouer_coup_ia(anc_ligne, anc_colonne, ligne, colonne, couleur_ia, promotion_ia)
                    dernier_tick = pygame.time.get_ticks()

    # ================================================================
    # AFFICHAGE
    # ================================================================

    if etat == "menu":
        rectangles_boutons_menu = menu.dessiner_menu(
            fenetre, fenetre.get_width(), fenetre.get_height(),
            affichage.font_titre, affichage.font_categorie, affichage.font_menu, affichage.font_logo
        )

    elif etat == "choix_adversaire":
        rect_joueur_vs_joueur, rect_joueur_vs_ia = menu.dessiner_choix_adversaire(
            fenetre, fenetre.get_width(), fenetre.get_height(),
            affichage.font_titre, affichage.font_menu
        )

    elif etat == "partie":
        if not partie_terminee:
            maintenant = pygame.time.get_ticks()
            temps_ecoule = (maintenant - dernier_tick) / 1000
            dernier_tick = maintenant

            if trait_aux_blancs:
                temps_blanc -= temps_ecoule
                if temps_blanc <= 0:
                    temps_blanc = 0
                    partie_terminee = True
                    message_fin_partie = "Temps écoulé ! Les noirs gagnent."
            else:
                temps_noir -= temps_ecoule
                if temps_noir <= 0:
                    temps_noir = 0
                    partie_terminee = True
                    message_fin_partie = "Temps écoulé ! Les blancs gagnent."

        couleur_actuelle = "blanc" if trait_aux_blancs else "noir"
        case_roi_echec = None
        if echec.roi_en_echec(plateau.grille, couleur_actuelle):
            case_roi_echec = echec.trouver_roi(plateau.grille, couleur_actuelle)

        couleur_joueur = ("noir" if couleur_ia == "blanc" else "blanc") if contre_ia else "blanc"

        affichage.dessiner_plateau(
            fenetre, plateau.grille, images,
            case_selectionnee, coups_possibles,
            captures_blanc, captures_noir,
            case_roi_echec,
            temps_blanc, temps_noir,
            trait_aux_blancs, couleur_joueur
        )

        # Indicateur animé pendant la réflexion de l'IA
        if ia_calcul_en_cours:
            nb_points = (pygame.time.get_ticks() // 400) % 4
            texte_reflexion = police_reflexion.render(
                "L'IA réfléchit" + "." * nb_points, True, (255, 255, 255)
            )
            rect_reflexion = texte_reflexion.get_rect(
                center=(fenetre.get_width() // 2, fenetre.get_height() - 20)
            )
            fenetre.blit(texte_reflexion, rect_reflexion)

        if partie_terminee:
            rect_rejouer, rect_menu = affichage.dessiner_fin_de_partie(fenetre, message_fin_partie)

    pygame.display.flip()

ia.fermer()
pygame.quit()