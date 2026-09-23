import pygame

from pieces.pions import coup_pion_blanc, coup_pion_noir

# Initialisation de pygame 
pygame.init()

# Création de la fenêtre 
fenetre = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("jeu d'échecs")

# Taille d'une case 
taille_case = 1000 // 8

# Police pour les pièces 
font = pygame.font.SysFont("segoeuisymbol",100)

# Représentation du plateau

plateau = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    [None, None, None, None, None, None, None, None], 
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"], 
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
]

# Boucle principal du jeu 
running = True

while running : 

    # Gestion des événements
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Dessin du plateau 
    for ligne in range(8):
        for colonne in range(8):

            # Choix de la couleur de la case
            if (ligne + colonne) %2 == 0 :
                couleur = (181, 136, 99)
            else :
                couleur = (240, 217, 181)

            # Dessine de la case 
            pygame.draw.rect(
                fenetre,
                couleur,
                (
                    colonne * taille_case,
                    ligne * taille_case,
                    taille_case,
                    taille_case
                )
            )

            # Récuperation de la pièce 
            piece = plateau[ligne][colonne]

            # Affichage de la pièce
            if piece is not None : 

                texte = font.render(
                    piece,
                    True,
                    (0, 0, 0)
                )

                fenetre.blit(
                    texte,
                    (
                        colonne * taille_case + 15,
                        ligne * taille_case + 5
                    )
                )

    # Mise à jour de l'écran
    pygame.display.flip()

# Fermeture du pygame
pygame.quit()