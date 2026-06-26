import pygame
import sys
import os

def _asset(path):
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, path)

# Dictionary to store our loaded Surface objects
IMAGES = {}

def load_assets():
    """Call this function once AFTER pygame.display.set_mode()"""
    planet_files = ["planet1", "planet2", "planet3",
                    "planet5", "planet6", "planet7",
                    "planet8",]

    star_files = ["bigstar", "midstar", "smallstar"]

    raw = pygame.image.load(_asset("assets/sprites/rocket.png")).convert_alpha()
    IMAGES["rocket"] = pygame.transform.scale(raw, (120, 120))

    for name in star_files:
        path = _asset(f"assets/sprites/stars/{name}.png")
        raw_img = pygame.image.load(path).convert_alpha()
        IMAGES[name] = pygame.transform.scale(raw_img, (30, 30))

    for name in planet_files:
        path = _asset(f"assets/sprites/planets/{name}.png")
        raw_img = pygame.image.load(path).convert_alpha()
        IMAGES[name] = pygame.transform.scale(raw_img, (180, 180))

    raw_goal = pygame.image.load(_asset("assets/sprites/goalAura.png")).convert_alpha()
    IMAGES["goalAura"] = pygame.transform.scale(raw_goal, (180, 180))

    raw_asteroid = pygame.image.load(_asset("assets/sprites/asteroid.png")).convert_alpha()
    IMAGES["asteroid"] = pygame.transform.scale(raw_asteroid, (45, 45))

    # Rotated images
    IMAGES["rotatedRocket"] = pygame.transform.rotate(IMAGES["rocket"], 285)
