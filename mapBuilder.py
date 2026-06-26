"""
Rocket Man - Map Builder
A standalone pygame tool for creating and saving game maps.
Run with: python312 mapBuilder.py
"""

import pygame
import sys
import json
import os
import math

# ---------------------------------------------------------------------------
# Constants (mirrored from logic/constants.py — no imports from logic/)
# ---------------------------------------------------------------------------
SCREEN_W = 1300
SCREEN_H = 800

CANVAS_W = 1050
CANVAS_H = 750

SIDEBAR_X = 1050
SIDEBAR_W = SCREEN_W - SIDEBAR_X   # 250

G = 6.67430e-11
SCALE = 6e-11
ROCKET_MASS = 8.681e+25

DEFAULT_PLANET_MASS = 5.972e30
DEFAULT_PLANET_RADIUS_M = 6.37e6
GOAL_MASS = 8e28
GOAL_RADIUS_M = 1.74e6

ROCKET_START_X = 100
ROCKET_START_Y = 100

VF_STEP = 20          # grid spacing for vector field
VF_ARROW_SIZE = 5     # half-size of the arrow triangle

ASSETS_BASE = os.path.join(os.path.dirname(__file__), "assets", "sprites")
MAPS_DIR = os.path.join(os.path.dirname(__file__), "maps")

# Sidebar palette entries: (sprite_key, label, is_goal)
PALETTE = [
    ("planet1", "Planet 1", False),
    ("planet2", "Planet 2", False),
    ("planet3", "Planet 3", False),
    ("planet4", "Planet 4", False),
    ("planet5", "Planet 5", False),
    ("planet6", "Planet 6", False),
    ("planet7", "Planet 7", False),
    ("planet8", "Planet 8", False),
    ("goalAura", "GOAL",     True),
]

THUMB_SIZE = 60
THUMB_PAD  = 8
LABEL_H    = 18

# Colors
COLOR_BG_CANVAS  = (10, 10, 25)
COLOR_BG_SIDEBAR = (25, 25, 45)
COLOR_SIDEBAR_SEP= (60, 60, 100)
COLOR_ARROW      = (80, 80, 80)
COLOR_TEXT       = (220, 220, 220)
COLOR_TEXT_DIM   = (130, 130, 160)
COLOR_THUMB_BG   = (40, 40, 70)
COLOR_THUMB_HOV  = (70, 70, 120)
COLOR_THUMB_SEL  = (100, 100, 180)
COLOR_BTN_SAVE   = (50, 180, 80)
COLOR_BTN_CLEAR  = (180, 60, 60)
COLOR_BTN_HOVER  = (255, 255, 100)
COLOR_INPUT_BG   = (20, 20, 40)
COLOR_INPUT_BOR  = (80, 80, 140)
COLOR_INPUT_ACT  = (120, 120, 220)
COLOR_ROCKET_MRK = (255, 220, 50)
COLOR_GOAL_RING  = (50, 255, 180)
COLOR_PLACED_HL  = (255, 80, 80)


# ---------------------------------------------------------------------------
# Asset loading
# ---------------------------------------------------------------------------

def load_images():
    """Load and scale all planet/goal/rocket sprites. Returns a dict."""
    images = {}

    # Planets
    for i in range(1, 9):
        name = f"planet{i}"
        path = os.path.join(ASSETS_BASE, "planets", f"{name}.png")
        try:
            raw = pygame.image.load(path).convert_alpha()
            images[name] = raw
        except Exception:
            # Fallback: coloured circle surface
            surf = pygame.Surface((128, 128), pygame.SRCALPHA)
            pygame.draw.circle(surf, (100 + i * 15, 80, 200 - i * 15), (64, 64), 60)
            images[name] = surf

    # goalAura
    goal_path = os.path.join(ASSETS_BASE, "goalAura.png")
    try:
        raw = pygame.image.load(goal_path).convert_alpha()
        images["goalAura"] = raw
    except Exception:
        surf = pygame.Surface((128, 128), pygame.SRCALPHA)
        pygame.draw.circle(surf, (50, 255, 180), (64, 64), 60)
        images["goalAura"] = surf

    # Rocket
    rocket_path = os.path.join(ASSETS_BASE, "rocket.png")
    try:
        raw = pygame.image.load(rocket_path).convert_alpha()
        images["rocket"] = pygame.transform.scale(raw, (36, 36))
    except Exception:
        surf = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (255, 220, 50), [(18, 0), (36, 36), (18, 28), (0, 36)])
        images["rocket"] = surf

    return images


def make_thumbnail(img, size=THUMB_SIZE):
    """Return a scaled copy of img fitting inside size x size."""
    w, h = img.get_size()
    ratio = min(size / w, size / h)
    new_w = max(1, int(w * ratio))
    new_h = max(1, int(h * ratio))
    return pygame.transform.smoothscale(img, (new_w, new_h))


def make_placed_sprite(img, radius_m, is_goal):
    """Return a display-sized copy of img scaled by SCALE."""
    display_r = max(12, int(radius_m * SCALE))
    if is_goal:
        display_r = max(18, display_r)
    diam = display_r * 2
    diam = max(24, min(diam, 160))
    return pygame.transform.smoothscale(img, (diam, diam))


# ---------------------------------------------------------------------------
# Vector field helpers
# ---------------------------------------------------------------------------

def compute_vector_field(bodies, cols, rows, step):
    """Return a 2D list [cols][rows] of (fx, fy) net gravity vectors."""
    grid = [[(0.0, 0.0)] * rows for _ in range(cols)]
    for cx in range(cols):
        for cy in range(rows):
            sx = cx * step
            sy = cy * step
            fx = 0.0
            fy = 0.0
            for b in bodies:
                dx = (b["x"] - sx) / SCALE
                dy = (b["y"] - sy) / SCALE
                dist_sq = dx * dx + dy * dy + 0.1
                dist = math.sqrt(dist_sq)
                fm = (G * b["mass"] * ROCKET_MASS) / dist_sq
                fx += fm * (dx / dist)
                fy += fm * (dy / dist)
            grid[cx][cy] = (fx, fy)
    return grid


def draw_vector_field(surface, bodies):
    """Draw log-scaled gravitational vector field arrows on surface."""
    if not bodies:
        return

    cols = (CANVAS_W // VF_STEP) + 1
    rows = (CANVAS_H // VF_STEP) + 1

    grid = compute_vector_field(bodies, cols, rows, VF_STEP)

    max_force = 0.0
    min_force = 1e30

    for cx in range(cols):
        for cy in range(rows):
            fx, fy = grid[cx][cy]
            mag = math.sqrt(fx * fx + fy * fy)
            if mag > max_force:
                max_force = mag
            if 0 < mag < min_force:
                min_force = mag

    if max_force <= 0:
        return

    log_max = math.log10(max_force)
    log_min = math.log10(min_force) if min_force < 1e30 else log_max
    log_range = log_max - log_min if log_max != log_min else 1.0

    for cx in range(cols):
        for cy in range(rows):
            fx, fy = grid[cx][cy]
            mag = math.sqrt(fx * fx + fy * fy)
            if mag <= 0:
                continue

            log_mag = math.log10(mag)
            norm = (log_mag - log_min) / log_range
            sharper = norm ** 20
            color_int = int(sharper * 255)
            color_int = max(0, min(255, color_int))
            if color_int < 10:
                continue

            angle = math.atan2(fy, fx)  # radians, pointing toward net force
            cx_px = cx * VF_STEP
            cy_px = cy * VF_STEP

            # Draw a small arrow: a thin triangle pointing in the force direction
            s = VF_ARROW_SIZE
            tip_x = cx_px + math.cos(angle) * s * 2
            tip_y = cy_px + math.sin(angle) * s * 2
            perp = angle + math.pi / 2
            base_x1 = cx_px + math.cos(perp) * s * 0.6
            base_y1 = cy_px + math.sin(perp) * s * 0.6
            base_x2 = cx_px - math.cos(perp) * s * 0.6
            base_y2 = cy_px - math.sin(perp) * s * 0.6

            c = color_int
            color = (c, c, c)
            pygame.draw.polygon(
                surface,
                color,
                [(tip_x, tip_y), (base_x1, base_y1), (base_x2, base_y2)],
            )


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def draw_rounded_rect(surface, color, rect, radius=6, border=0, border_color=None):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)


def draw_text_centered(surface, text, font, color, rect):
    surf = font.render(text, True, color)
    r = surf.get_rect(center=rect.center)
    surface.blit(surf, r)


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class MapBuilder:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Rocket Man - Map Builder")
        self.clock = pygame.time.Clock()

        # Fonts — fall back to system default if PixelPurl not found
        font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PixelPurl.ttf")
        try:
            self.font_label = pygame.font.Font(font_path, 13)
            self.font_ui    = pygame.font.Font(font_path, 16)
            self.font_btn   = pygame.font.Font(font_path, 18)
            self.font_title = pygame.font.Font(font_path, 20)
        except Exception:
            self.font_label = pygame.font.SysFont("Arial", 13)
            self.font_ui    = pygame.font.SysFont("Arial", 16)
            self.font_btn   = pygame.font.SysFont("Arial", 18)
            self.font_title = pygame.font.SysFont("Arial", 20)

        # Images
        self.images = load_images()
        self.thumbnails = {key: make_thumbnail(self.images[key]) for key, _, _ in PALETTE}

        # Pre-scale placed sprites (full display size)
        self.placed_sprites = {}
        for key, _, is_goal in PALETTE:
            if is_goal:
                r = GOAL_RADIUS_M
            else:
                r = DEFAULT_PLANET_RADIUS_M
            self.placed_sprites[key] = make_placed_sprite(self.images[key], r, is_goal)

        # Rocket thumbnail (small)
        self.rocket_icon = self.images["rocket"]

        # State
        self.placed_bodies = []      # list of dicts with x,y,mass,radius_m,sprite,is_goal
        self.held_sprite   = None    # sprite key being dragged from palette
        self.held_is_goal  = False
        self.map_name      = "my_map"
        self.input_active  = False
        self.status_msg    = ""
        self.status_timer  = 0

        # Pre-render canvas vector field surface (SRCALPHA for transparency)
        self.vf_surface = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)
        self._rebuild_vf()

        # Build sidebar geometry
        self._build_sidebar_rects()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_sidebar_rects(self):
        """Pre-compute all sidebar Rect objects."""
        sx = SIDEBAR_X + 10
        sw = SIDEBAR_W - 20

        # Title label
        self.rect_sidebar_title = pygame.Rect(SIDEBAR_X, 0, SIDEBAR_W, 36)

        # Palette thumbnails
        self.palette_rects = []
        y = 40
        for i, (key, label, _) in enumerate(PALETTE):
            r = pygame.Rect(sx, y, sw, THUMB_SIZE + LABEL_H + THUMB_PAD)
            self.palette_rects.append(r)
            y += THUMB_SIZE + LABEL_H + THUMB_PAD + 4

        # Map name input
        self.rect_input_label = pygame.Rect(sx, y + 4, sw, 18)
        y += 22
        self.rect_input = pygame.Rect(sx, y, sw, 28)
        y += 34

        # CLEAR button
        self.rect_clear = pygame.Rect(sx, y, sw, 34)
        y += 40

        # SAVE button
        self.rect_save = pygame.Rect(sx, y, sw, 34)

        # Status area at very bottom of sidebar
        self.rect_status = pygame.Rect(SIDEBAR_X, SCREEN_H - 40, SIDEBAR_W, 40)

    # ------------------------------------------------------------------
    # Vector field
    # ------------------------------------------------------------------

    def _rebuild_vf(self):
        self.vf_surface.fill((0, 0, 0, 0))
        draw_vector_field(self.vf_surface, self.placed_bodies)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self):
        self.screen.fill(COLOR_BG_CANVAS)

        # --- Canvas ---
        # Vector field
        self.screen.blit(self.vf_surface, (0, 0))

        # Canvas border
        pygame.draw.rect(self.screen, COLOR_SIDEBAR_SEP, pygame.Rect(0, 0, CANVAS_W, CANVAS_H), 1)

        # Rocket marker (fixed)
        rkt = self.rocket_icon
        rw, rh = rkt.get_size()
        self.screen.blit(rkt, (ROCKET_START_X - rw // 2, ROCKET_START_Y - rh // 2))
        # Label
        lbl = self.font_label.render("START", True, COLOR_ROCKET_MRK)
        self.screen.blit(lbl, (ROCKET_START_X - lbl.get_width() // 2, ROCKET_START_Y + rh // 2 + 2))

        # Placed bodies
        for body in self.placed_bodies:
            spr = self.placed_sprites[body["sprite"]]
            sw2, sh2 = spr.get_size()
            self.screen.blit(spr, (body["x"] - sw2 // 2, body["y"] - sh2 // 2))
            if body["is_goal"]:
                pygame.draw.circle(
                    self.screen, COLOR_GOAL_RING,
                    (body["x"], body["y"]),
                    sw2 // 2 + 3, 2
                )

        # Dragging ghost
        if self.held_sprite:
            mx, my = pygame.mouse.get_pos()
            spr = self.placed_sprites[self.held_sprite]
            sw2, sh2 = spr.get_size()
            ghost = spr.copy()
            ghost.set_alpha(160)
            self.screen.blit(ghost, (mx - sw2 // 2, my - sh2 // 2))

        # --- Sidebar background ---
        sidebar_rect = pygame.Rect(SIDEBAR_X, 0, SIDEBAR_W, SCREEN_H)
        pygame.draw.rect(self.screen, COLOR_BG_SIDEBAR, sidebar_rect)
        pygame.draw.line(self.screen, COLOR_SIDEBAR_SEP, (SIDEBAR_X, 0), (SIDEBAR_X, SCREEN_H), 2)

        # Sidebar title
        title_surf = self.font_title.render("PALETTE", True, COLOR_TEXT)
        self.screen.blit(title_surf, (SIDEBAR_X + (SIDEBAR_W - title_surf.get_width()) // 2, 10))

        # Palette thumbnails
        mx, my = pygame.mouse.get_pos()
        for i, (key, label, is_goal) in enumerate(PALETTE):
            r = self.palette_rects[i]
            hovered = r.collidepoint(mx, my) and self.held_sprite is None
            selected = self.held_sprite == key

            bg = COLOR_THUMB_SEL if selected else (COLOR_THUMB_HOV if hovered else COLOR_THUMB_BG)
            border_col = COLOR_INPUT_ACT if (selected or hovered) else COLOR_SIDEBAR_SEP
            draw_rounded_rect(self.screen, bg, r, radius=6, border=1, border_color=border_col)

            # Thumbnail image centered horizontally
            thumb = self.thumbnails[key]
            tw, th = thumb.get_size()
            tx = r.x + (r.width - tw) // 2
            ty = r.y + THUMB_PAD // 2
            self.screen.blit(thumb, (tx, ty))

            # Label
            lbl_surf = self.font_label.render(label, True, COLOR_TEXT if hovered or selected else COLOR_TEXT_DIM)
            lx = r.x + (r.width - lbl_surf.get_width()) // 2
            ly = r.y + THUMB_SIZE + THUMB_PAD // 2
            self.screen.blit(lbl_surf, (lx, ly))

        # Map name input label
        lbl = self.font_label.render("Map name:", True, COLOR_TEXT_DIM)
        self.screen.blit(lbl, (self.rect_input_label.x, self.rect_input_label.y))

        # Map name input box
        bor_col = COLOR_INPUT_ACT if self.input_active else COLOR_INPUT_BOR
        draw_rounded_rect(self.screen, COLOR_INPUT_BG, self.rect_input, radius=4, border=1, border_color=bor_col)
        name_surf = self.font_ui.render(self.map_name, True, COLOR_TEXT)
        self.screen.blit(name_surf, (self.rect_input.x + 6, self.rect_input.y + (self.rect_input.height - name_surf.get_height()) // 2))
        # Cursor blink
        if self.input_active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cx_ = self.rect_input.x + 6 + name_surf.get_width()
            cy_ = self.rect_input.y + 4
            pygame.draw.line(self.screen, COLOR_TEXT, (cx_, cy_), (cx_, cy_ + self.rect_input.height - 8), 1)

        # CLEAR button
        hov_clear = self.rect_clear.collidepoint(mx, my)
        draw_rounded_rect(self.screen, COLOR_BTN_CLEAR, self.rect_clear, radius=6,
                          border=1, border_color=COLOR_BTN_HOVER if hov_clear else COLOR_SIDEBAR_SEP)
        draw_text_centered(self.screen, "CLEAR", self.font_btn, COLOR_TEXT, self.rect_clear)

        # SAVE button
        hov_save = self.rect_save.collidepoint(mx, my)
        draw_rounded_rect(self.screen, COLOR_BTN_SAVE, self.rect_save, radius=6,
                          border=1, border_color=COLOR_BTN_HOVER if hov_save else COLOR_SIDEBAR_SEP)
        draw_text_centered(self.screen, "SAVE", self.font_btn, COLOR_TEXT, self.rect_save)

        # Body count hint
        count_txt = f"{len(self.placed_bodies)} bodies placed"
        ct = self.font_label.render(count_txt, True, COLOR_TEXT_DIM)
        self.screen.blit(ct, (SIDEBAR_X + (SIDEBAR_W - ct.get_width()) // 2, self.rect_save.bottom + 6))

        # Status message
        if self.status_msg and self.status_timer > 0:
            st = self.font_ui.render(self.status_msg, True, (100, 255, 140))
            self.screen.blit(st, (SIDEBAR_X + (SIDEBAR_W - st.get_width()) // 2, SCREEN_H - 30))

        pygame.display.flip()

    # ------------------------------------------------------------------
    # Save / Clear
    # ------------------------------------------------------------------

    def save_map(self):
        name = self.map_name.strip() or "unnamed"
        os.makedirs(MAPS_DIR, exist_ok=True)
        path = os.path.join(MAPS_DIR, f"{name}.json")
        data = {
            "name": name,
            "bodies": list(self.placed_bodies),
            "rocket": {
                "x": ROCKET_START_X,
                "y": ROCKET_START_Y,
                "vx": 0.0,
                "vy": 0.0,
                "mass": ROCKET_MASS,
            },
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        self.status_msg = f"Saved: {name}.json"
        self.status_timer = 180  # frames

    def clear_map(self):
        self.placed_bodies.clear()
        self._rebuild_vf()
        self.status_msg = "Canvas cleared"
        self.status_timer = 120

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.map_name = self.map_name[:-1]
                    else:
                        # Only printable ASCII, max 32 chars
                        if event.unicode and event.unicode.isprintable() and len(self.map_name) < 32:
                            self.map_name += event.unicode
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.held_sprite = None
                        self.held_is_goal = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if event.button == 1:
                    self._handle_left_click(mx, my)

                elif event.button == 3:
                    # Right-click: remove body under cursor
                    self._try_remove_body(mx, my)

    def _handle_left_click(self, mx, my):
        # --- Input box ---
        if self.rect_input.collidepoint(mx, my):
            self.input_active = True
            return
        else:
            self.input_active = False

        # --- SAVE ---
        if self.rect_save.collidepoint(mx, my):
            self.save_map()
            return

        # --- CLEAR ---
        if self.rect_clear.collidepoint(mx, my):
            self.clear_map()
            return

        # --- Palette thumbnails ---
        for i, (key, label, is_goal) in enumerate(PALETTE):
            if self.palette_rects[i].collidepoint(mx, my):
                if self.held_sprite == key:
                    # Toggle off
                    self.held_sprite = None
                    self.held_is_goal = False
                else:
                    self.held_sprite = key
                    self.held_is_goal = is_goal
                return

        # --- Canvas: place body ---
        if self.held_sprite and mx < CANVAS_W and my < CANVAS_H:
            mass = GOAL_MASS if self.held_is_goal else DEFAULT_PLANET_MASS
            radius = GOAL_RADIUS_M if self.held_is_goal else DEFAULT_PLANET_RADIUS_M
            body = {
                "x": mx,
                "y": my,
                "mass": mass,
                "radius_m": radius,
                "sprite": self.held_sprite,
                "is_goal": self.held_is_goal,
            }
            self.placed_bodies.append(body)
            self._rebuild_vf()
            # Keep the sprite selected so user can place more
            return

        # Click on canvas with no sprite held — deselect if outside sidebar
        if mx < CANVAS_W:
            self.held_sprite = None
            self.held_is_goal = False

    def _try_remove_body(self, mx, my):
        """Remove the topmost placed body whose sprite bounding box contains (mx, my)."""
        if mx >= CANVAS_W:
            return
        for i in range(len(self.placed_bodies) - 1, -1, -1):
            body = self.placed_bodies[i]
            spr = self.placed_sprites[body["sprite"]]
            sw2, sh2 = spr.get_size()
            body_rect = pygame.Rect(
                body["x"] - sw2 // 2,
                body["y"] - sh2 // 2,
                sw2,
                sh2,
            )
            if body_rect.collidepoint(mx, my):
                self.placed_bodies.pop(i)
                self._rebuild_vf()
                self.status_msg = f"Removed {body['sprite']}"
                self.status_timer = 90
                return

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        while True:
            self.handle_events()

            if self.status_timer > 0:
                self.status_timer -= 1

            self.draw()
            self.clock.tick(60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Change working directory to the script's folder so relative asset paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = MapBuilder()
    app.run()
