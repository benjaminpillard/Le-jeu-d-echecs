
from pygame import init


def formater_temps(secondes):
    """
    Convertit un nombre de secondes en chaine de mm:ss pour l'affcihage.
    Ne descend jamais en dessous de 00:00.
    """
    secondes = max(0, secondes)
    minutes = int(secondes) // 60
    sec = int(secondes)% 60
    return f"{minutes:02d}:{sec:02d}"
