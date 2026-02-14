import pygame

# Dictionary to store our loaded Surface objects
IMAGES = {}

def load_assets():
    """Call this function once AFTER pygame.display.set_mode()"""
    # Use a helper list to load everything at once
    planet_files = ["planet1", "planet2", "planet3", 
                    "planet5", "planet6", "planet7",
                    "planet8", "goalAura",]
    
    other_files = ["rocket"]

    raw = pygame.image.load("sprites/rocket.png").convert_alpha()
    IMAGES["rocket"] = pygame.transform.scale(raw, (120, 120))
    
    for name in planet_files:
        path = f"sprites/{name}.png"
        # 1. Load the raw image
        raw_img = pygame.image.load(path).convert_alpha()
        # 2. Scale and store in our dictionary
        IMAGES[name] = pygame.transform.scale(raw_img, (180, 180))

    # Rotated images
    IMAGES["rotatedRocket"] = pygame.transform.rotate(IMAGES["rocket"], 285)
