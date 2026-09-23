import pygame
import config

MODES_PAR_CATEGORIE = {
    "Bullet": [
        {"nom": "1 min", "temps": 60, "increment": 0},
        {"nom": "1+1", "temps": 60, "increment": 1},
        {"nom": "2+1", "temps": 120, "increment": 1},
    ],
    "Blitz": [
        {"nom": "3 min", "temps": 180, "increment": 0},
        {"nom": "3+2", "temps": 180, "increment": 2},
        {"nom": "5 min", "temps": 300, "increment": 0},
    ],
    "Rapide": [
        {"nom": "10 min", "temps": 600, "increment": 0},
        {"nom": "15+10", "temps": 900, "increment": 10},
    ],
}

COULEURS_CATEGORIE = {
    "Bullet": config.COULEUR_BULLET,
    "Blitz": config.COULEUR_BLITZ,
    "Rapide": config.COULEUR_RAPIDE,
}

LARGEUR_BOUTON = 170
HAUTEUR_BOUTON = 52
ESPACE_ENTRE_BOUTONS = 14
ESPACE_ENTRE_COLONNES = 50
PADDING_CARTE = 25
HAUTEUR_ZONE_TITRE_CARTE = 70


def dessiner_menu(fenetre, largeur_ecran, hauteur_ecran, font_titre, font_categorie, font_bouton, font_logo):
    fenetre.fill(config.FOND_SOMBRE)

    rectangles_boutons = []

    # --- Logo (une pièce d'échecs) ---
    logo = font_logo.render("♔", True, config.BLANC_TEXTE)
    logo_rect = logo.get_rect(center=(largeur_ecran // 2, 55))
    fenetre.blit(logo, logo_rect)

    # --- Titre principal ---
    titre = font_titre.render("Choisir un mode de partie", True, config.BLANC_TEXTE)
    titre_rect = titre.get_rect(center=(largeur_ecran // 2, 125))
    fenetre.blit(titre, titre_rect)

    # --- Calcul des dimensions des cartes ---
    nb_colonnes = len(MODES_PAR_CATEGORIE)
    nb_boutons_max = max(len(modes) for modes in MODES_PAR_CATEGORIE.values())

    largeur_carte = LARGEUR_BOUTON + PADDING_CARTE * 2
    hauteur_carte = HAUTEUR_ZONE_TITRE_CARTE + nb_boutons_max * (HAUTEUR_BOUTON + ESPACE_ENTRE_BOUTONS) + PADDING_CARTE

    largeur_totale = nb_colonnes * largeur_carte + (nb_colonnes - 1) * ESPACE_ENTRE_COLONNES
    x_depart = (largeur_ecran - largeur_totale) // 2
    y_depart = 180

    pos_souris = pygame.mouse.get_pos()

    for i, (categorie, modes) in enumerate(MODES_PAR_CATEGORIE.items()):
        x_carte = x_depart + i * (largeur_carte + ESPACE_ENTRE_COLONNES)

        # --- Carte de fond pour cette catégorie ---
        rect_carte = pygame.Rect(x_carte, y_depart, largeur_carte, hauteur_carte)
        pygame.draw.rect(fenetre, config.CARTE_FOND, rect_carte, border_radius=14)

        couleur_categorie = COULEURS_CATEGORIE[categorie]

        # --- Pastille colorée au-dessus du titre de catégorie ---
        centre_pastille = (x_carte + largeur_carte // 2, y_depart + 25)
        pygame.draw.circle(fenetre, couleur_categorie, centre_pastille, 8)

        # --- Titre de la catégorie ---
        texte_categorie = font_categorie.render(categorie, True, config.BLANC_TEXTE)
        rect_categorie = texte_categorie.get_rect(center=(x_carte + largeur_carte // 2, y_depart + 50))
        fenetre.blit(texte_categorie, rect_categorie)

        # --- Boutons de cette catégorie ---
        x_bouton = x_carte + PADDING_CARTE
        for j, mode in enumerate(modes):
            y_bouton = y_depart + HAUTEUR_ZONE_TITRE_CARTE + j * (HAUTEUR_BOUTON + ESPACE_ENTRE_BOUTONS)
            rect = pygame.Rect(x_bouton, y_bouton, LARGEUR_BOUTON, HAUTEUR_BOUTON)
            rectangles_boutons.append((rect, mode))

            if rect.collidepoint(pos_souris):
                couleur_bouton = config.VERT_BOUTON_SURVOL
            else:
                couleur_bouton = config.VERT_BOUTON

            pygame.draw.rect(fenetre, couleur_bouton, rect, border_radius=8)

            texte = font_bouton.render(mode["nom"], True, config.BLANC_TEXTE)
            texte_rect = texte.get_rect(center=rect.center)
            fenetre.blit(texte, texte_rect)

    return rectangles_boutons


def detecter_clic_bouton(pos_clic, rectangles_boutons):
    for rect, mode in rectangles_boutons:
        if rect.collidepoint(pos_clic):
            return mode
    return None

def dessiner_choix_adversaire(fenetre, largeur_ecran, hauteur_ecran, font_titre, font_bouton):
    fenetre.fill(config.FOND_SOMBRE)

    titre = font_titre.render("Contre qui ?", True, config.BLANC_TEXTE)
    titre_rect = titre.get_rect(center=(largeur_ecran // 2, hauteur_ecran // 2 - 100))
    fenetre.blit(titre, titre_rect)

    largeur_bouton, hauteur_bouton = 260, 60
    x_bouton = largeur_ecran // 2 - largeur_bouton // 2
    pos_souris = pygame.mouse.get_pos()

    rect_joueur = pygame.Rect(x_bouton, hauteur_ecran // 2 - 20, largeur_bouton, hauteur_bouton)
    couleur_joueur = config.VERT_BOUTON_SURVOL if rect_joueur.collidepoint(pos_souris) else config.VERT_BOUTON
    pygame.draw.rect(fenetre, couleur_joueur, rect_joueur, border_radius=10)
    texte_joueur = font_bouton.render("Joueur vs Joueur", True, config.BLANC_TEXTE)
    fenetre.blit(texte_joueur, texte_joueur.get_rect(center=rect_joueur.center))

    rect_ia = pygame.Rect(x_bouton, hauteur_ecran // 2 + 60, largeur_bouton, hauteur_bouton)
    couleur_ia_bouton = config.VERT_BOUTON_SURVOL if rect_ia.collidepoint(pos_souris) else config.VERT_BOUTON
    pygame.draw.rect(fenetre, couleur_ia_bouton, rect_ia, border_radius=10)
    texte_ia = font_bouton.render("Contre l'IA", True, config.BLANC_TEXTE)
    fenetre.blit(texte_ia, texte_ia.get_rect(center=rect_ia.center))

    return rect_joueur, rect_ia