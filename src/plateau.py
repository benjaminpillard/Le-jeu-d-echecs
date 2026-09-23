import pygame
import config

grille = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
]

def charger_images():
    taille = (config.TAILLE_CASE, config.TAILLE_CASE)
    return {
        "♙": pygame.transform.scale(pygame.image.load("assets/pions_blanc.png"), taille),
        "♟": pygame.transform.scale(pygame.image.load("assets/pions_noir.png"), taille),
        "♖": pygame.transform.scale(pygame.image.load("assets/tour_blanc.png"), taille),
        "♜": pygame.transform.scale(pygame.image.load("assets/tour_noir.png"), taille),
        "♘": pygame.transform.scale(pygame.image.load("assets/chevalier_blanc.png"), taille),
        "♞": pygame.transform.scale(pygame.image.load("assets/chevalier_noir.png"), taille),
        "♗": pygame.transform.scale(pygame.image.load("assets/fou_blanc.png"), taille),
        "♝": pygame.transform.scale(pygame.image.load("assets/fou_noir.png"), taille),
        "♕": pygame.transform.scale(pygame.image.load("assets/reine_blanc.png"), taille),
        "♛": pygame.transform.scale(pygame.image.load("assets/reine_noir.png"), taille),
        "♔": pygame.transform.scale(pygame.image.load("assets/roi_blanc.png"), taille),
        "♚": pygame.transform.scale(pygame.image.load("assets/roi_noir.png"), taille),
    }