#!/usr/bin/env python3
"""
3D Isometric Contribution Graph Generator for Syed Saif Bin Saeed (SaifSaeed-12)
Renders a wide, cinematic 3D isometric voxel contribution calendar with glowing pillars.
Outputs:
- assets/profile-3d-contrib.png
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Canvas dimensions
WIDTH = 1200
HEIGHT = 500

# Color Palette (Minimal Metallic & Electric Blue Theme)
BG_COLOR = (8, 9, 11)           # #08090B
SURFACE_COLOR = (14, 16, 20)    # #0E1014
BORDER_COLOR = (36, 40, 50)     # #242832
TEXT_PRIMARY = (245, 245, 245)  # #F5F5F5
TEXT_MUTED = (161, 166, 176)    # #A1A6B0
SILVER_ACCENT = (191, 199, 213) # #BFC7D5
ELECTRIC_BLUE = (121, 217, 255) # #79D9FF
EMERALD_GREEN = (0, 229, 153)   # Standard GitHub Green

# Voxel palette
INACTIVE_TOP = (20, 23, 29)
INACTIVE_LEFT = (12, 14, 18)
INACTIVE_RIGHT = (16, 18, 23)

ACTIVE_PALETTE = [
    # Level 1 (Initial activity)
    {"top": (30, 80, 110), "left": (18, 48, 68), "right": (24, 64, 88)},
    # Level 2 (Moderate)
    {"top": (50, 130, 175), "left": (32, 85, 115), "right": (40, 105, 145)},
    # Level 3 (High)
    {"top": (80, 185, 235), "left": (52, 125, 165), "right": (66, 155, 200)},
    # Level 4 (Radiant Electric Blue / Emerald)
    {"top": (121, 217, 255), "left": (75, 155, 195), "right": (95, 185, 225)},
]

def iso_coords(col, row, height_px=0, ox=600, oy=255, step_x=16, step_y=3, row_x=-8, row_y=11):
    """
    Computes screen coordinate for a grid cell in wide isometric perspective
    col: 0..51 (52 weeks)
    row: 0..6 (7 days)
    """
    sx = ox + (col - 26) * step_x + (row - 3) * row_x
    sy = oy + (col - 26) * step_y + (row - 3) * row_y - height_px
    return sx, sy

def draw_iso_voxel(draw, col, row, h_px=3, level=0, ox=600, oy=255, rw=6, rh=3):
    bx, by = iso_coords(col, row, height_px=0, ox=ox, oy=oy)
    tx, ty = iso_coords(col, row, height_px=h_px, ox=ox, oy=oy)
    
    if level == 0:
        c_top = INACTIVE_TOP
        c_left = INACTIVE_LEFT
        c_right = INACTIVE_RIGHT
        outline_top = (32, 37, 46)
        outline_side = (22, 25, 32)
    else:
        p = ACTIVE_PALETTE[min(level - 1, len(ACTIVE_PALETTE) - 1)]
        c_top = p["top"]
        c_left = p["left"]
        c_right = p["right"]
        outline_top = ELECTRIC_BLUE
        outline_side = (40, 95, 130)

    # Left face (from base to top)
    if h_px > 0:
        left_poly = [
            (tx - rw, ty),
            (tx, ty + rh),
            (bx, by + rh),
            (bx - rw, by)
        ]
        draw.polygon(left_poly, fill=c_left, outline=outline_side)

        # Right face
        right_poly = [
            (tx, ty + rh),
            (tx + rw, ty),
            (bx + rw, by),
            (bx, by + rh)
        ]
        draw.polygon(right_poly, fill=c_right, outline=outline_side)

    # Top face
    top_poly = [
        (tx, ty - rh),
        (tx + rw, ty),
        (tx, ty + rh),
        (tx - rw, ty)
    ]
    draw.polygon(top_poly, fill=c_top, outline=outline_top)

def generate_3d_graph():
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR + (255,))
    
    # Fonts
    try:
        font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
        font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
        font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 11)
        font_month = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 11)
    except Exception:
        font_title = font_sub = font_mono = font_month = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    # Outer Architectural Frame
    margin = 12
    draw.rectangle([margin, margin, WIDTH - margin, HEIGHT - margin], outline=BORDER_COLOR, width=1)
    
    # Corner ticks
    tl = 14
    for x, y, dx, dy in [
        (margin, margin, 1, 1),
        (WIDTH - margin, margin, -1, 1),
        (margin, HEIGHT - margin, 1, -1),
        (WIDTH - margin, HEIGHT - margin, -1, -1)
    ]:
        draw.line([(x, y), (x + dx * tl, y)], fill=ELECTRIC_BLUE, width=1)
        draw.line([(x, y), (x, y + dy * tl)], fill=ELECTRIC_BLUE, width=1)

    # Header section
    draw.ellipse([42, 38, 50, 46], fill=ELECTRIC_BLUE)
    draw.text((60, 32), "3D ISOMETRIC CONTRIBUTION CALENDAR", fill=TEXT_PRIMARY, font=font_title)
    draw.text((62, 58), "SaifSaeed-12  //  YEAR-TO-DATE ISOMETRIC CONTRIBUTION MAPPING", fill=TEXT_MUTED, font=font_sub)
    draw.text((WIDTH - 270, 36), "● 3D_CALENDAR_ENGINE: ACTIVE", fill=ELECTRIC_BLUE, font=font_mono)
    draw.line([(40, 84), (WIDTH - 40, 84)], fill=(28, 32, 40), width=1)

    # Activity matrix setup: 52 weeks x 7 days
    weeks = 52
    days = 7
    grid = [[0 for _ in range(days)] for _ in range(weeks)]

    # Actual contributions from screenshot (October 2026 commits)
    grid[50][1] = 2  # Level 2
    grid[50][4] = 3  # Level 3
    grid[51][2] = 4  # Level 4 (Pillar)
    grid[51][5] = 2  # Level 2

    ox, oy = 600, 240
    rw, rh = 7, 4

    # Background ambient glow behind active pillars
    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    for col in range(weeks):
        for row in range(days):
            if grid[col][row] > 0:
                gx, gy = iso_coords(col, row, height_px=30, ox=ox, oy=oy)
                glow_draw.ellipse([gx - 45, gy - 25, gx + 45, gy + 25], fill=(121, 217, 255, 80))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, glow_layer)
    draw = ImageDraw.Draw(img)

    # Month Labels along the top edge of the grid
    months = ["Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    for i, m in enumerate(months):
        col_idx = int(i * (52 / 12.0) + 1)
        mx, my = iso_coords(col_idx, 0, height_px=0, ox=ox, oy=oy)
        draw.text((mx - 10, my - 24), m, fill=SILVER_ACCENT, font=font_month)

    # Day labels on the left edge
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for row_idx, d_name in day_labels:
        dx, dy = iso_coords(0, row_idx, height_px=0, ox=ox, oy=oy)
        draw.text((dx - 34, dy - 6), d_name, fill=TEXT_MUTED, font=font_month)

    # Draw isometric voxels (ordered from back-to-front by row then col)
    for row in range(days):
        for col in range(weeks):
            lvl = grid[col][row]
            if lvl == 0:
                h_px = 3
            elif lvl == 1:
                h_px = 14
            elif lvl == 2:
                h_px = 24
            elif lvl == 3:
                h_px = 34
            else:
                h_px = 46  # Majestic glowing 3D pillar
            draw_iso_voxel(draw, col, row, h_px=h_px, level=lvl, ox=ox, oy=oy, rw=rw, rh=rh)

    # Bottom Legend & Status
    leg_y = HEIGHT - 50
    draw.text((45, leg_y), "CONTRIBUTION LEVEL:", fill=SILVER_ACCENT, font=font_mono)
    draw.text((195, leg_y), "LESS", fill=(110, 118, 130), font=font_mono)

    lx = 240
    # Inactive swatch
    draw.rectangle([lx, leg_y + 1, lx + 12, leg_y + 13], fill=INACTIVE_TOP, outline=BORDER_COLOR)
    lx += 18
    for lvl in range(4):
        draw.rectangle([lx, leg_y + 1, lx + 12, leg_y + 13], fill=ACTIVE_PALETTE[lvl]["top"], outline=ELECTRIC_BLUE)
        lx += 18
    draw.text((lx + 4, leg_y), "MORE", fill=ELECTRIC_BLUE, font=font_mono)

    draw.text((WIDTH - 430, leg_y), "AUTO-SYNC: AUTOMATED VIA .github/workflows/profile-3d.yml", fill=(95, 105, 120), font=font_mono)

    # Save to both folders
    out_paths = [
        os.path.join(BASE_DIR, "assets", "profile-3d-contrib.png"),
        os.path.join(BASE_DIR, "SaifSaeed-12", "assets", "profile-3d-contrib.png")
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, "PNG", optimize=True)
        print(f"Generated 3D contribution graph: {p}")

if __name__ == "__main__":
    generate_3d_graph()
