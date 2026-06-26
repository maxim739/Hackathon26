import pygame

# Dictionary to store our loaded Surface objects
IMAGES = {}

def load_assets():
    """Call this function once AFTER pygame.display.set_mode()"""
    # Use a helper list to load everything at once
    planet_files = ["planet1", "planet2", "planet3",
                    "planet5", "planet6", "planet7",
                    "planet8",]

    star_files = ["bigstar","midstar", "smallstar",
                  ]

    other_files = ["rocket"]

    raw = pygame.image.load("assets/sprites/rocket.png").convert_alpha()
    IMAGES["rocket"] = pygame.transform.scale(raw, (120, 120))

    for name in star_files:
        path = f"assets/sprites/stars/{name}.png"
        # 1. Load the raw image
        raw_img = pygame.image.load(path).convert_alpha()
        # 2. Scale different than planets and store in our dictionary
        IMAGES[name] = pygame.transform.scale(raw_img, (30, 30))

    for name in planet_files:
        path = f"assets/sprites/planets/{name}.png"
        # 1. Load the raw image
        raw_img = pygame.image.load(path).convert_alpha()
        # 2. Scale and store in our dictionary
        IMAGES[name] = pygame.transform.scale(raw_img, (180, 180))

    raw_goal = pygame.image.load("assets/sprites/goalAura.png").convert_alpha()
    IMAGES["goalAura"] = pygame.transform.scale(raw_goal, (180, 180))

    raw_asteroid = pygame.image.load("assets/sprites/asteroid.png").convert_alpha()
    IMAGES["asteroid"] = pygame.transform.scale(raw_asteroid, (45, 45))

    # Rotated images
    IMAGES["rotatedRocket"] = pygame.transform.rotate(IMAGES["rocket"], 285)
