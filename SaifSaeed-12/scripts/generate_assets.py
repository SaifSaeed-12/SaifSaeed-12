#!/usr/bin/env python3
"""
Production Asset Generator for Syed Saif Bin Saeed (SaifSaeed-12)
Theme: Minimal Metallic Edition
Generates:
1. assets/github-banner.png (1600x500px)
2. assets/github-motion.gif (960x280px)
3. assets/github-motion-fallback.png (960x280px)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_BG = r"C:\Users\IQRA TRADERS\.gemini\antigravity-ide\brain\c85c6d22-1b6b-4a95-b1e1-44485999aa28\metallic_3d_banner_bg_1792921226961.jpg"

# Color Palette (Minimal Dark Metallic)
BG_COLOR = (8, 9, 11)           # #08090B (Obsidian Black)
SURFACE_COLOR = (17, 19, 23)     # #111317 (Charcoal Surface)
SURFACE_SEC = (24, 27, 32)       # #181B20
BORDER_COLOR = (40, 44, 52)      # #282C34 (Muted Slate Border)
TEXT_PRIMARY = (245, 245, 245)   # #F5F5F5 (Crisp Platinum White)
TEXT_MUTED = (161, 166, 176)     # #A1A6B0 (Secondary Slate)
SILVER_ACCENT = (191, 199, 213)  # #BFC7D5 (Metallic Silver)
ELECTRIC_BLUE = (121, 217, 255)  # #79D9FF (Electric Blue Highlight)

def get_font(name="segoeuib.ttf", size=32):
    try:
        font_path = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()

def draw_grid(draw, width, height, step=50, color=(22, 25, 32, 60)):
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=color, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=color, width=1)

def draw_corner_ticks(draw, rect, length=14, color=ELECTRIC_BLUE):
    x0, y0, x1, y1 = rect
    draw.line([(x0, y0), (x0 + length, y0)], fill=color, width=1)
    draw.line([(x0, y0), (x0, y0 + length)], fill=color, width=1)
    draw.line([(x1 - length, y0), (x1, y0)], fill=color, width=1)
    draw.line([(x1, y0), (x1, y0 + length)], fill=color, width=1)
    draw.line([(x0, y1), (x0 + length, y1)], fill=color, width=1)
    draw.line([(x0, y1 - length), (x0, y1)], fill=color, width=1)
    draw.line([(x1 - length, y1), (x1, y1)], fill=color, width=1)
    draw.line([(x1, y1 - length), (x1, y1)], fill=color, width=1)

def create_banner():
    width, height = 1600, 500
    banner = Image.new("RGBA", (width, height), BG_COLOR + (255,))
    
    # 1. Subtle Technical Grid
    grid_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)
    draw_grid(grid_draw, width, height, step=48, color=(24, 28, 35, 75))
    banner = Image.alpha_composite(banner, grid_img)
    
    # 2. Composite the 3D Metallic Sculpture
    if os.path.exists(SOURCE_BG):
        sculpture = Image.open(SOURCE_BG).convert("RGBA")
        s_height = 490
        s_width = int(sculpture.width * (s_height / sculpture.height))
        sculpture = sculpture.resize((s_width, s_height), Image.Resampling.LANCZOS)
        
        # Smooth cosine horizontal fade mask from left edge
        mask = Image.new("L", (s_width, s_height), 0)
        mask_pix = mask.load()
        fade_len = int(s_width * 0.45)
        for y in range(s_height):
            # Top/bottom edge safety fade
            y_factor = 1.0
            if y < 30:
                y_factor = y / 30.0
            elif y > s_height - 30:
                y_factor = (s_height - y) / 30.0

            for x in range(s_width):
                if x < fade_len:
                    x_factor = 0.5 - 0.5 * math.cos((x / float(fade_len)) * math.pi)
                else:
                    x_factor = 1.0
                mask_pix[x, y] = int(255 * x_factor * y_factor)

        pos_x = width - s_width + 30
        pos_y = (height - s_height) // 2
        banner.paste(sculpture, (pos_x, pos_y), mask)

    # 3. Ambient Electric Blue Glow (Soft Gaussian Blurred)
    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse([width - 550, height - 320, width + 100, height + 200], fill=(121, 217, 255, 30))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(65))
    banner = Image.alpha_composite(banner, glow_img)
    
    # 4. Architectural Borders & Metadata
    draw = ImageDraw.Draw(banner)
    frame_margin = 16
    draw.rectangle(
        [frame_margin, frame_margin, width - frame_margin, height - frame_margin],
        outline=(34, 38, 47),
        width=1
    )
    draw_corner_ticks(draw, [frame_margin, frame_margin, width - frame_margin, height - frame_margin], length=14, color=ELECTRIC_BLUE)
    
    # 5. Typography Layout
    font_badge = get_font("segoeui.ttf", 13)
    font_name = get_font("segoeuib.ttf", 52)
    font_sub = get_font("segoeuib.ttf", 20)
    font_skills = get_font("segoeui.ttf", 15)
    font_mono = get_font("consola.ttf", 12)
    
    start_x = 90
    
    # Category Tag / Status Indicator
    draw.ellipse([start_x, 102, start_x + 8, 110], fill=ELECTRIC_BLUE)
    draw.text((start_x + 18, 98), "SYED SAIF BIN SAEED  //  ENGINEERING IDENTITY", fill=SILVER_ACCENT, font=font_badge)
    draw.text((start_x + 470, 98), "● SYS_ONLINE", fill=ELECTRIC_BLUE, font=font_mono)
    
    # Primary Name: SYED SAIF BIN SAEED (Editorial letter spacing)
    name_str = "SYED SAIF BIN SAEED"
    nx = start_x
    ny = 138
    for char in name_str:
        draw.text((nx, ny), char, fill=TEXT_PRIMARY, font=font_name)
        bbox = font_name.getbbox(char)
        c_width = (bbox[2] - bbox[0]) if bbox else 26
        nx += c_width + 4
        
    # Metallic Gradient Divider
    bar_y = 218
    bar_width = 560
    for i in range(bar_width):
        ratio = i / float(bar_width)
        r = int(ELECTRIC_BLUE[0] * (1 - ratio) + BORDER_COLOR[0] * ratio)
        g = int(ELECTRIC_BLUE[1] * (1 - ratio) + BORDER_COLOR[1] * ratio)
        b = int(ELECTRIC_BLUE[2] * (1 - ratio) + BORDER_COLOR[2] * ratio)
        draw.line([(start_x + i, bar_y), (start_x + i, bar_y + 1)], fill=(r, g, b))
        
    # Subtitle
    sub_y = 240
    draw.text((start_x, sub_y), "FULL STACK DEVELOPER", fill=SILVER_ACCENT, font=font_sub)
    draw.text((start_x + 270, sub_y), "·", fill=ELECTRIC_BLUE, font=font_sub)
    draw.text((start_x + 295, sub_y), "CREATIVE DEVELOPER", fill=SILVER_ACCENT, font=font_sub)
    draw.text((start_x + 550, sub_y), "·", fill=ELECTRIC_BLUE, font=font_sub)
    draw.text((start_x + 575, sub_y), "AUTOMATION", fill=SILVER_ACCENT, font=font_sub)
    
    # Technology Stack Badges
    pill_y = 295
    pills = ["PHP / LARAVEL", "JAVASCRIPT / REACT", "THREE.JS / GSAP", "N8N AUTOMATION", "MYSQL & APIS"]
    px = start_x
    for pill in pills:
        bbox = font_skills.getbbox(pill)
        pw = (bbox[2] - bbox[0]) + 20
        ph = 28
        draw.rounded_rectangle([px, pill_y, px + pw, pill_y + ph], radius=4, fill=(17, 19, 23), outline=(38, 42, 50), width=1)
        draw.text((px + 10, pill_y + 5), pill, fill=TEXT_MUTED, font=font_skills)
        px += pw + 12
        
    # Technical Footer Coordinates
    bot_y = 390
    draw.line([(start_x, bot_y - 15), (start_x + 650, bot_y - 15)], fill=(28, 32, 38), width=1)
    status_text = "GITHUB: SaifSaeed-12  ·  PROFILE SPEC: MINIMAL METALLIC  ·  EDITION: 2026.1"
    draw.text((start_x, bot_y), status_text, fill=(110, 118, 130), font=font_mono)
    
    # Export Banner
    out_paths = [
        os.path.join(BASE_DIR, "assets", "github-banner.png"),
        os.path.join(BASE_DIR, "SaifSaeed-12", "assets", "github-banner.png")
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        banner.save(p, "PNG", optimize=True)
        print(f"Generated clean banner: {p}")

def render_motion_frame(t, width=960, height=280, show_gleam=True, sculpture_base=None):
    """Renders a single frame of the motion graphic at time t (0.0 to 1.0)"""
    frame = Image.new("RGBA", (width, height), BG_COLOR + (255,))
    
    # 1. Background Grid
    grid_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)
    draw_grid(grid_draw, width, height, step=40, color=(24, 28, 35, 65))
    frame = Image.alpha_composite(frame, grid_img)
    
    # 2. Sculpture with subtle vertical float
    if sculpture_base:
        sw, sh = sculpture_base.size
        float_offset = int(math.sin(t * 2 * math.pi) * 3) if show_gleam else 0
        
        # Soft left fade mask
        mask = Image.new("L", (sw, sh), 0)
        mask_pix = mask.load()
        fade_len = int(sw * 0.45)
        for y in range(sh):
            y_factor = 1.0
            if y < 15:
                y_factor = y / 15.0
            elif y > sh - 15:
                y_factor = (sh - y) / 15.0
            for x in range(sw):
                if x < fade_len:
                    x_factor = 0.5 - 0.5 * math.cos((x / float(fade_len)) * math.pi)
                else:
                    x_factor = 1.0
                mask_pix[x, y] = int(255 * x_factor * y_factor)
                
        pos_x = width - sw + 20
        pos_y = (height - sh) // 2 + float_offset
        frame.paste(sculpture_base, (pos_x, pos_y), mask)
        
    # 3. Soft ambient glow behind sculpture
    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse([width - 320, height - 180, width + 50, height + 90], fill=(121, 217, 255, 25))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(40))
    frame = Image.alpha_composite(frame, glow_img)
    
    # 4. Moving Electric-Blue Gleam Beam
    if show_gleam:
        gleam_t = (t - 0.12) / 0.60
        if 0.0 <= gleam_t <= 1.0:
            gleam_x = int(40 + gleam_t * (width - 120))
            gleam_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            g_draw = ImageDraw.Draw(gleam_layer)
            beam_w = 40
            for dx in range(-beam_w, beam_w + 1):
                fade = 1.0 - (abs(dx) / float(beam_w))
                alpha = int(32 * fade)
                g_draw.line([(gleam_x + dx, 12), (gleam_x + dx + 15, height - 12)], fill=(121, 217, 255, alpha), width=1)
            gleam_layer = gleam_layer.filter(ImageFilter.GaussianBlur(4))
            frame = Image.alpha_composite(frame, gleam_layer)
            
    # 5. UI Borders & Ticks
    draw = ImageDraw.Draw(frame)
    draw.rectangle([8, 8, width - 8, height - 8], outline=(32, 36, 45), width=1)
    draw_corner_ticks(draw, [8, 8, width - 8, height - 8], length=10, color=ELECTRIC_BLUE)
    
    # 6. Typography
    font_name = get_font("segoeuib.ttf", 36)
    font_sub = get_font("segoeuib.ttf", 15)
    font_mono = get_font("consola.ttf", 11)
    
    start_x = 55
    
    # Status Beacon
    pulse_alpha = int(180 + 75 * math.sin(t * 2 * math.pi)) if show_gleam else 255
    draw.ellipse([start_x, 50, start_x + 6, 56], fill=(121, 217, 255, pulse_alpha))
    draw.text((start_x + 16, 47), "SYED SAIF BIN SAEED  //  PORTFOLIO REPOSITORY", fill=SILVER_ACCENT, font=font_mono)
    
    # Name
    draw.text((start_x, 78), "SYED SAIF BIN SAEED", fill=TEXT_PRIMARY, font=font_name)
    
    # Accent Bar
    bar_y = 136
    draw.line([(start_x, bar_y), (start_x + 480, bar_y)], fill=(36, 40, 48), width=1)
    if show_gleam:
        hl_pos = int((t * 540) % 480)
        draw.line([(start_x + max(0, hl_pos - 45), bar_y), (start_x + min(480, hl_pos + 45), bar_y)], fill=ELECTRIC_BLUE, width=1)
    else:
        draw.line([(start_x, bar_y), (start_x + 120, bar_y)], fill=ELECTRIC_BLUE, width=1)
        
    # Subtitle
    sub_y = 154
    draw.text((start_x, sub_y), "FULL STACK DEVELOPER  ·  CREATIVE DEV  ·  AUTOMATION", fill=SILVER_ACCENT, font=font_sub)
    
    # Tech Tags
    tag_y = 194
    tags = "PHP · LARAVEL · JAVASCRIPT · REACT · THREE.JS · GSAP · N8N"
    draw.text((start_x, tag_y), tags, fill=(125, 133, 145), font=font_mono)
    
    # Bottom Status
    draw.text((start_x, 230), "REPO: SaifSaeed-12  ·  METALLIC EDITION  ·  STATUS: VERIFIED", fill=(85, 93, 105), font=font_mono)
    
    return frame

def create_motion_assets():
    width, height = 960, 280
    sculpture_base = None
    if os.path.exists(SOURCE_BG):
        sc = Image.open(SOURCE_BG).convert("RGBA")
        s_height = 270
        s_width = int(sc.width * (s_height / sc.height))
        sculpture_base = sc.resize((s_width, s_height), Image.Resampling.LANCZOS)
        
    # 1. Generate Static Fallback (Pristine, no in-flight gleam artifact)
    fallback_img = render_motion_frame(0.0, width, height, show_gleam=False, sculpture_base=sculpture_base)
    fallback_paths = [
        os.path.join(BASE_DIR, "assets", "github-motion-fallback.png"),
        os.path.join(BASE_DIR, "SaifSaeed-12", "assets", "github-motion-fallback.png")
    ]
    for fp in fallback_paths:
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        fallback_img.convert("RGB").save(fp, "PNG", optimize=True)
        print(f"Generated static fallback: {fp}")
        
    # 2. Generate Looping GIF (28 frames for silky smooth loop and compact size)
    total_frames = 28
    frames = []
    for f in range(total_frames):
        t = f / float(total_frames)
        f_img = render_motion_frame(t, width, height, show_gleam=True, sculpture_base=sculpture_base)
        rgb_f = f_img.convert("RGB")
        paletted = rgb_f.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(paletted)
        
    gif_paths = [
        os.path.join(BASE_DIR, "assets", "github-motion.gif"),
        os.path.join(BASE_DIR, "SaifSaeed-12", "assets", "github-motion.gif")
    ]
    for gp in gif_paths:
        os.makedirs(os.path.dirname(gp), exist_ok=True)
        frames[0].save(
            gp,
            save_all=True,
            append_images=frames[1:],
            duration=65, # ~15.4 fps
            loop=0,
            optimize=True
        )
        size_kb = os.path.getsize(gp) / 1024
        print(f"Generated motion GIF: {gp} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    print("Generating Minimal Metallic assets...")
    create_banner()
    create_motion_assets()
    print("Done!")
