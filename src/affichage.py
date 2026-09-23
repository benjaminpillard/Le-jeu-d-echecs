import pygame
import config
import horloge

font_coord = None
font_menu = None
font_titre = None
font_categorie = None
font_logo = None
TAILLE_MINI = 20


def init_police():
    global font_coord, font_menu, font_titre, font_categorie, font_logo
    font_coord = pygame.font.SysFont("arial", 20)
    font_menu = pygame.font.SysFont("arial", 20, bold=True)
    font_titre = pygame.font.SysFont("arial", 42, bold=True)
    font_categorie = pygame.font.SysFont("arial", 26, bold=True)
    font_logo = pygame.font.SysFont("segoeuisymbol", 70)


def dessiner_plateau(fenetre, grille, images, case_selectionnee, coups_possibles, captures_blanc, captures_noir, case_roi_echec, temps_blanc, temps_noir, trait_aux_blancs, couleur_joueur):
    fenetre.fill(config.FOND_SOMBRE)

    dx = config.DECALAGE_X
    dy = config.DECALAGE_Y

    pygame.draw.rect(fenetre, config.FOND_SOMBRE, (dx, dy, config.LARGEUR_ECRAN, config.ZONE_CAPTURE))
    pygame.draw.rect(fenetre, config.FOND_SOMBRE, (dx, dy + config.HAUTEUR_ECRAN - config.ZONE_CAPTURE, config.LARGEUR_ECRAN, config.ZONE_CAPTURE))

    for ligne in range(config.NB_CASES):
        for colonne in range(config.NB_CASES):
            ligne_aff, colonne_aff = case_vers_affichage(ligne, colonne, couleur_joueur)

            if (ligne, colonne) == case_roi_echec:
                couleur = config.ROUGE_ECHEC
            elif (ligne, colonne) == case_selectionnee:
                couleur = config.VERT_SELECTION
            elif (ligne + colonne) % 2 == 0:
                couleur = config.VERT_CASE
            else:
                couleur = config.BEIGE_CASE

            pygame.draw.rect(
                fenetre,
                couleur,
                (dx + config.MARGE + colonne_aff * config.TAILLE_CASE, dy + config.DECALAGE_HAUT + ligne_aff * config.TAILLE_CASE, config.TAILLE_CASE, config.TAILLE_CASE)
            )

            piece = grille[ligne][colonne]
            if piece is not None:
                fenetre.blit(
                    images[piece],
                    (dx + config.MARGE + colonne_aff * config.TAILLE_CASE, dy + config.DECALAGE_HAUT + ligne_aff * config.TAILLE_CASE)
                )

            if (ligne, colonne) in coups_possibles:
                centre_x = dx + config.MARGE + colonne_aff * config.TAILLE_CASE + config.TAILLE_CASE // 2
                centre_y = dy + config.DECALAGE_HAUT + ligne_aff * config.TAILLE_CASE + config.TAILLE_CASE // 2

                if piece is None:
                    pygame.draw.circle(fenetre, config.GRIS_SHADOW, (centre_x, centre_y), config.TAILLE_CASE // 8)
                else:
                    surface_teinte = pygame.Surface((config.TAILLE_CASE, config.TAILLE_CASE), pygame.SRCALPHA)
                    surface_teinte.fill((*config.GRIS_SHADOW, 120))
                    fenetre.blit(
                        surface_teinte,
                        (dx + config.MARGE + colonne_aff * config.TAILLE_CASE, dy + config.DECALAGE_HAUT + ligne_aff * config.TAILLE_CASE)
                    )

    dessiner_coordonnees(fenetre) 
    dessiner_captures(fenetre, images, captures_blanc, captures_noir)
    dessiner_horloges(fenetre, temps_blanc, temps_noir, trait_aux_blancs, couleur_joueur)


def dessiner_coordonnees(fenetre):
    dx = config.DECALAGE_X
    dy = config.DECALAGE_Y

    for ligne in range(config.NB_CASES):
        assert font_coord is not None
        texte = font_coord.render(str(8 - ligne), True, config.BLANC_TEXTE)
        rect = texte.get_rect(center=(dx + config.MARGE // 2, dy + config.DECALAGE_HAUT + ligne * config.TAILLE_CASE + config.TAILLE_CASE // 2))
        fenetre.blit(texte, rect)

    for colonne in range(config.NB_CASES):
        assert font_coord is not None
        texte = font_coord.render(config.LETTRES[colonne], True, config.BLANC_TEXTE)
        rect = texte.get_rect(center=(dx + config.MARGE + colonne * config.TAILLE_CASE + config.TAILLE_CASE // 2, dy + config.DECALAGE_HAUT + config.LARGEUR_PLATEAU + config.MARGE // 2))
        fenetre.blit(texte, rect)


def dessiner_captures(fenetre, images, captures_blanc, captures_noir):
    dx = config.DECALAGE_X
    dy = config.DECALAGE_Y

    for i, piece in enumerate(captures_noir):
        image_mini = pygame.transform.scale(images[piece], (TAILLE_MINI, TAILLE_MINI))
        fenetre.blit(image_mini, (dx + config.MARGE + i * (TAILLE_MINI + 2), dy + 10))

    valeur_captures_noir = sum(config.VALEURS_PIECES[p] for p in captures_noir)
    if valeur_captures_noir > 0:
        assert font_coord is not None
        texte = font_coord.render(f"+{valeur_captures_noir}", True, config.BLANC_TEXTE)
        fenetre.blit(texte, (dx + config.MARGE + len(captures_noir) * (TAILLE_MINI + 2) + 5, dy + 15))

    for i, piece in enumerate(captures_blanc):
        image_mini = pygame.transform.scale(images[piece], (TAILLE_MINI, TAILLE_MINI))
        fenetre.blit(image_mini, (dx + config.MARGE + i * (TAILLE_MINI + 2), dy + config.HAUTEUR_ECRAN - config.ZONE_CAPTURE + 10))

    valeur_captures_blanc = sum(config.VALEURS_PIECES[p] for p in captures_blanc)
    if valeur_captures_blanc > 0:
        assert font_coord is not None
        texte = font_coord.render(f"+{valeur_captures_blanc}", True, config.BLANC_TEXTE)
        fenetre.blit(texte, (dx + config.MARGE + len(captures_blanc) * (TAILLE_MINI + 2) + 5, dy + config.HAUTEUR_ECRAN - config.ZONE_CAPTURE + 15))


def gerer_promotion_pygame(fenetre, couleur_actuelle, images):
    largeur_boite, hauteur_boite = 320, 100
    x_boite = (fenetre.get_width() - largeur_boite) // 2
    y_boite = (fenetre.get_height() - hauteur_boite) // 2

    if couleur_actuelle == "blanc":
        options = ["♕", "♖", "♗", "♘"]
    else:
        options = ["♛", "♜", "♝", "♞"]

    en_promotion = True
    choix_final = None

    while en_promotion:
        pygame.draw.rect(fenetre, (240, 240, 240), (x_boite, y_boite, largeur_boite, hauteur_boite))
        pygame.draw.rect(fenetre, (0, 0, 0), (x_boite, y_boite, largeur_boite, hauteur_boite), 3)

        zones_boutons = []
        for i, symbole in enumerate(options):
            x_btn = x_boite + 15 + (i * 75)
            y_btn = y_boite + 15
            w_btn, h_btn = 65, 70
            rect_btn = pygame.Rect(x_btn, y_btn, w_btn, h_btn)
            zones_boutons.append((rect_btn, symbole))

            pygame.draw.rect(fenetre, (200, 200, 200), rect_btn)
            pygame.draw.rect(fenetre, (100, 100, 100), rect_btn, 1)

            image_piece = pygame.transform.scale(images[symbole], (w_btn - 10, h_btn - 10))
            image_rect = image_piece.get_rect(center=rect_btn.center)
            fenetre.blit(image_piece, image_rect)

        pygame.display.flip()

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                position_souris = evenement.pos
                for rect_btn, symbole in zones_boutons:
                    if rect_btn.collidepoint(position_souris):
                        choix_final = symbole
                        en_promotion = False

    return choix_final


def dessiner_horloges(fenetre, temps_blanc, temps_noir, trait_aux_blancs, couleur_joueur):
    dx = config.DECALAGE_X
    dy = config.DECALAGE_Y

    texte_blanc = horloge.formater_temps(temps_blanc)
    texte_noir = horloge.formater_temps(temps_noir)

    couleur_blanc_texte = config.VERT_BOUTON if trait_aux_blancs else config.BLANC_TEXTE
    couleur_noir_texte = config.VERT_BOUTON if not trait_aux_blancs else config.BLANC_TEXTE

    surface_blanc = font_menu.render(texte_blanc, True, couleur_blanc_texte) # pyright: ignore[reportOptionalMemberAccess]
    surface_noir = font_menu.render(texte_noir, True, couleur_noir_texte) # type: ignore

    position_haut = (dx + config.LARGEUR_ECRAN - 90, dy + 15)
    position_bas = (dx + config.LARGEUR_ECRAN - 90, dy + config.HAUTEUR_ECRAN - config.ZONE_CAPTURE + 15)

    if couleur_joueur == "noir":
        fenetre.blit(surface_blanc, position_haut)
        fenetre.blit(surface_noir, position_bas)
    else:
        fenetre.blit(surface_noir, position_haut)
        fenetre.blit(surface_blanc, position_bas)

def dessiner_fin_de_partie(fenetre, message):
    largeur_ecran = fenetre.get_width()
    hauteur_ecran = fenetre.get_height()

    voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
    voile.fill((0, 0, 0, 180))
    fenetre.blit(voile, (0, 0))

    largeur_boite, hauteur_boite = 360, 220
    x_boite = (largeur_ecran - largeur_boite) // 2
    y_boite = (hauteur_ecran - hauteur_boite) // 2

    pygame.draw.rect(fenetre, config.CARTE_FOND, (x_boite, y_boite, largeur_boite, hauteur_boite), border_radius=14)

    assert font_categorie is not None
    texte = font_categorie.render(message, True, config.BLANC_TEXTE)
    texte_rect = texte.get_rect(center=(largeur_ecran // 2, y_boite + 50))

    if texte_rect.width > largeur_boite - 30:
        police_reduite = pygame.font.SysFont("arial", 18, bold=True)
        texte = police_reduite.render(message, True, config.BLANC_TEXTE)
        texte_rect = texte.get_rect(center=(largeur_ecran // 2, y_boite + 50))

    fenetre.blit(texte, texte_rect)

    largeur_bouton, hauteur_bouton = 220, 50
    x_bouton = largeur_ecran // 2 - largeur_bouton // 2

    rect_rejouer = pygame.Rect(x_bouton, y_boite + 100, largeur_bouton, hauteur_bouton)
    pygame.draw.rect(fenetre, config.VERT_BOUTON, rect_rejouer, border_radius=8)
    assert font_menu is not None
    texte_rejouer = font_menu.render("Rejouer", True, config.BLANC_TEXTE)
    fenetre.blit(texte_rejouer, texte_rejouer.get_rect(center=rect_rejouer.center))

    rect_menu = pygame.Rect(x_bouton, y_boite + 160, largeur_bouton, hauteur_bouton)
    pygame.draw.rect(fenetre, config.GRIS_SHADOW, rect_menu, border_radius=8)
    assert font_menu is not None
    texte_menu = font_menu.render("Menu principal", True, config.BLANC_TEXTE)
    fenetre.blit(texte_menu, texte_menu.get_rect(center=rect_menu.center))

    return rect_rejouer, rect_menu

def case_vers_affichage(ligne, colonne, couleur_joueur):
    """
    Convertit une position logique (ligne, colonne) en position d'affichage,
    en inversant le plateau si le joueur a les noirs.
    """
    if couleur_joueur == "noir":
        return 7 - ligne, 7 - colonne
    return ligne, colonne