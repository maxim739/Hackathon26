## Hackathon26
# SPACEMAN ROCKET NAVIGATION

Repository for McGill W2026 Physics Hackathon

Maxim DeJong, William Gray, Saabir Yousuf

---

## Next Steps

- Update the map builder — sidebar planet placement, live vector field preview, and save workflow need testing and polish
- Fix the "Game restarted!" spam on startup — `restart_game()` is being called during initialisation when it shouldn't be
- Fix the reset button immediately triggering BLAST OFF — stale `event` variable causes the same click to fire both handlers on the same frame
- Add per-planet mass selection in the map builder — all placed planets currently default to Earth mass
- Add an undo button to the map builder so misplaced planets can be removed without clearing the whole map
- Show the rocket's current trajectory as a dotted path while in flight so players can see where it's heading
- Add a win counter or attempt counter to the HUD so players can track how many tries it took
- Tune physics `dt` — 10 days per step causes the rocket to tunnel through planets at high speed (especially after 2x boost)
- Scale planet sprites to reflect their relative sizes rather than rendering all at the same 140×140px

---

## Building a standalone executable

Run `build.py` on the target platform to produce a single executable with no Python dependency:

```
# Windows
python312 build.py        # produces dist/RocketMan.exe

# macOS / Linux
pip install pygame pyinstaller
python3 build.py          # produces dist/RocketMan
```

PyInstaller must be installed first:
```
pip install pyinstaller --index-url https://pypi.org/simple/
```

**Note:** PyInstaller builds for the OS it runs on — you cannot cross-compile. Each platform requires its own build run. The `build/` and `dist/` directories are generated artefacts and are not committed to the repo.

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
- Planet hitbox radii are now measured from the actual non-transparent pixels of each sprite and stored in `logic/constants.py` under `SPRITE_RADII`. To adjust any planet's hitbox, edit the value for that sprite key there.
- Covers all interactive sprites: `planet1`–`planet8`, `goalAura`, `asteroid`, and `rocket`.
- `Static_body` accepts an optional `physical_radius` in metres for future use with scaled maps.

### Refactor (post-hackathon cleanup)
- Separated code into `logic/` (physics, constants) and `display/` (rendering, UI, assets) packages.
- Moved all sprites into `assets/sprites/` with subfolders by type (planets, stars, explosions).
- Moved the font into `assets/fonts/`.
- Inlined `planets.py` body definitions directly into `main.py`.
- Deleted unused files: `main2.py`, `main3.py`, `BallBounce.py`, `MovingStatic.py`, `planets.py`.
