## Hackathon26
# SPACEMAN ROCKET NAVIGATION

Repository for McGill W2026 Physics Hackathon

Maxim DeJong, William Gray, Saabir Yousuf

---

## Running the game

```
python312 main.py
```

Requires Python 3.12 and pygame 2.6+. All paths are relative so the game must be launched from the project root.

---

## Project structure

```
Hackathon26/
├── main.py              # Entry point and game loop
├── logic/
│   ├── bodies.py        # Physics: Static_body, Moving_body, Explosion, gravity simulation
│   └── constants.py     # Shared constants (screen size, physics params, game states)
├── display/
│   ├── assets.py        # Loads and scales all sprite images into IMAGES dict
│   ├── button.py        # Reusable Button widget with hover/click states
│   ├── vector_field.py  # Gravitational field visualization (arrow grid)
│   └── windows.py       # Screen drawing for each game state (landing, tutorial, win)
└── assets/
    ├── fonts/
    │   └── PixelPurl.ttf
    └── sprites/
        ├── planets/     # planet1–8 PNGs
        ├── stars/       # bigstar, midstar, smallstar PNGs
        ├── explosions/  # explosion1–3 PNGs
        ├── rocket.png
        ├── asteroid.png
        ├── goal.png
        └── goalAura.png
```

## Changelog

### Map system
- Added `maps/` directory — game levels are stored as `.json` files.
- Added `logic/map_loader.py` — loads and lists map files.
- The tutorial/intro screen now shows a map picker (`←`/`→` arrow keys to cycle).
- `main.py` builds `game_bodies` from the selected map JSON instead of hardcoded values.
- Added `mapBuilder.py` — standalone map editor. Run it separately to create new maps:
  ```
  python312 mapBuilder.py
  ```
  Place planets from the right sidebar onto the canvas, set a map name, and click Save. Maps are written to `maps/` and immediately available in the game.

### Gameplay additions
- **2x Speed boost** — after BLAST OFF, an orange "2x SPEED" button appears. Clicking it doubles the rocket's current velocity. One use per launch; turns grey ("BOOSTED") after use.
- **Reset button** — when the rocket crashes, the BLAST OFF slot switches to a red "RESET" button. Clicking it returns to the pre-launch state so asteroids can be repositioned before the next attempt. The `R` key also resets at any time.

### Physics / collision fixes
- Planet collision radii were mismatched against their visual size (35 px vs 70 px sprites). Corrected to 65 px, aligned to the visible planet edge.
- `Static_body` now accepts an optional `physical_radius` in metres — auto-converts to screen pixels via `scale`. Real solar-system radii are used for all planets (`_R_JUPITER`, `_R_EARTH`, etc.) with a 65 px minimum to keep planets hittable at game scale.

### Refactor (post-hackathon cleanup)
- Separated code into `logic/` (physics, constants) and `display/` (rendering, UI, assets) packages.
- Moved all sprites into `assets/sprites/` with subfolders by type (planets, stars, explosions).
- Moved the font into `assets/fonts/`.
- Inlined `planets.py` body definitions directly into `main.py`.
- Deleted unused files: `main2.py`, `main3.py`, `BallBounce.py`, `MovingStatic.py`, `planets.py`.
