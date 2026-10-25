#!/usr/bin/env python3
"""
SAIF AI Futuristic Visual Asset Generator — 10-Second Storyboard Edition
Palette: Jet Black (#05070B) × Cerulean Blue Neon (#00A6FF) × Neon Rose (#FF3D81)
Supporting Neutrals: Deep Charcoal (#0B1018), Steel Gray (#8995A7), Soft White (#EAF3FF)

Produces:
1. assets/github-banner.png (1500x500px Ultra-HD Static Banner)
2. assets/github-motion.gif (960x320px 10-Second Looping Animation with 5-Phase Storyboard)
3. assets/github-motion-fallback.png (960x320px High-Resolution Fallback Frame)
4. assets/project-portfolio.png (Concept Thumbnail)
5. assets/project-attendance.png (Concept Thumbnail)
6. assets/project-pos.png (Concept Thumbnail)
7. assets/project-automation.png (Concept Thumbnail)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
BASE_DIR = os.path.dirname(REPO_DIR) if os.path.basename(REPO_DIR) == "SaifSaeed-12" else REPO_DIR

# Local source core image
LOCAL_SOURCE_CORE = os.path.join(REPO_DIR, "assets", "saif-ai-core-source.jpg")
FALLBACK_SOURCE_CORE = r"C:\Users\IQRA TRADERS\.gemini\antigravity-ide\brain\c85c6d22-1b6b-4a95-b1e1-44485999aa28\saif_ai_core_centerpiece_1792927930660.jpg"

def get_core_path():
    if os.path.exists(LOCAL_SOURCE_CORE):
        return LOCAL_SOURCE_CORE
    alt_local = os.path.join(BASE_DIR, "assets", "saif-ai-core-source.jpg")
    if os.path.exists(alt_local):
        return alt_local
    if os.path.exists(FALLBACK_SOURCE_CORE):
        return FALLBACK_SOURCE_CORE
    return None

# Strict Palette
JET_BLACK = (5, 7, 11)           # #05070B
DEEP_CHARCOAL = (11, 16, 24)     # #0B1018
CERULEAN_BLUE = (0, 166, 255)    # #00A6FF
NEON_ROSE = (255, 61, 129)       # #FF3D81
SOFT_WHITE = (234, 243, 255)     # #EAF3FF
STEEL_GRAY = (137, 149, 167)     # #8995A7
BORDER_MUTED = (28, 38, 52)      # #1C2634

def get_font(name="segoeuib.ttf", size=32):
    try:
        p = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    except Exception:
        pass
    return ImageFont.load_default()

def draw_circuit_grid(draw, width, height, step=40, color=(16, 24, 36, 50)):
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=color, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=color, width=1)

def draw_corner_ticks(draw, rect, length=14, color=CERULEAN_BLUE, width=2):
    x0, y0, x1, y1 = rect
    draw.line([(x0, y0), (x0 + length, y0)], fill=color, width=width)
    draw.line([(x0, y0), (x0, y0 + length)], fill=color, width=width)
    draw.line([(x1 - length, y0), (x1, y0)], fill=color, width=width)
    draw.line([(x1, y0), (x1, y0 + length)], fill=color, width=width)
    draw.line([(x0, y1), (x0 + length, y1)], fill=color, width=width)
    draw.line([(x0, y1 - length), (x0, y1)], fill=color, width=width)
    draw.line([(x1 - length, y1), (x1, y1)], fill=color, width=width)
    draw.line([(x1, y1 - length), (x1, y1)], fill=color, width=width)

def draw_rotated_ellipse(draw, center, rx, ry, angle_deg, outline, width=1):
    cx, cy = center
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    num_pts = 72
    points = []
    for i in range(num_pts + 1):
        theta = (2 * math.pi * i) / num_pts
        ex = rx * math.cos(theta)
        ey = ry * math.sin(theta)
        rx_rot = ex * cos_a - ey * sin_a
        ry_rot = ex * sin_a + ey * cos_a
        points.append((cx + rx_rot, cy + ry_rot))
        
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=outline, width=width)

def create_static_banner():
    width, height = 1500, 500
    banner = Image.new("RGBA", (width, height), JET_BLACK + (255,))
    
    # Circuit Grid
    grid_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_layer)
    draw_circuit_grid(g_draw, width, height, step=45, color=(18, 28, 42, 65))
    banner = Image.alpha_composite(banner, grid_layer)

    # Composite AI Core on Right
    core_path = get_core_path()
    if core_path and os.path.exists(core_path):
        core_img = Image.open(core_path).convert("RGBA")
        ch = 480
        cw = int(core_img.width * (ch / float(core_img.height)))
        core_resized = core_img.resize((cw, ch), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (cw, ch), 0)
        mask_pix = mask.load()
        fade_w = int(cw * 0.42)
        for y in range(ch):
            yf = 1.0
            if y < 20: yf = y / 20.0
            elif y > ch - 20: yf = (ch - y) / 20.0
            for x in range(cw):
                if x < fade_w:
                    xf = 0.5 - 0.5 * math.cos((x / float(fade_w)) * math.pi)
                else:
                    xf = 1.0
                mask_pix[x, y] = int(255 * xf * yf)
                
        pos_x = width - cw + 10
        pos_y = (height - ch) // 2
        banner.paste(core_resized, (pos_x, pos_y), mask)

    # Ambient Volumetric Bloom
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([width - 560, height - 370, width + 50, height + 160], fill=(0, 166, 255, 38))
    g_draw.ellipse([width - 360, height - 280, width, height + 50], fill=(255, 61, 129, 22))
    glow = glow.filter(ImageFilter.GaussianBlur(75))
    banner = Image.alpha_composite(banner, glow)

    # Holographic Ring Overlay
    holo = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(holo)
    core_cx = width - 260
    core_cy = height // 2
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 220, 65, -28, CERULEAN_BLUE + (120,), width=2)
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 195, 48, 42, STEEL_GRAY + (90,), width=1)
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 180, 40, 75, NEON_ROSE + (140,), width=2)
    banner = Image.alpha_composite(banner, holo)

    # Frame & Architecture
    draw = ImageDraw.Draw(banner)
    margin = 16
    draw.rectangle([margin, margin, width - margin, height - margin], outline=BORDER_MUTED, width=1)
    draw_corner_ticks(draw, [margin, margin, width - margin, height - margin], length=16, color=CERULEAN_BLUE, width=2)

    # Typography
    f_badge = get_font("segoeui.ttf", 13)
    f_name = get_font("segoeuib.ttf", 48)
    f_sub = get_font("segoeuib.ttf", 18)
    f_quote = get_font("segoeuil.ttf", 17)
    f_tagline = get_font("segoeuib.ttf", 14)
    f_mono = get_font("consola.ttf", 11)

    start_x = 85

    # Top Status Badge
    draw.ellipse([start_x, 88, start_x + 8, 96], fill=NEON_ROSE)
    draw.text((start_x + 18, 85), "SAIF AI // COMMAND INTERFACE", fill=CERULEAN_BLUE, font=f_badge)
    draw.text((start_x + 360, 85), "● SYSTEM_ONLINE", fill=CERULEAN_BLUE, font=f_mono)

    # Exact Name: SYED SAIF BIN SAEED
    name_str = "SYED SAIF BIN SAEED"
    nx = start_x
    ny = 120
    for char in name_str:
        draw.text((nx, ny), char, fill=SOFT_WHITE, font=f_name)
        bbox = f_name.getbbox(char)
        cw = (bbox[2] - bbox[0]) if bbox else 24
        nx += cw + 4

    # Gradient Accent Bar
    bar_y = 195
    bar_w = 580
    for i in range(bar_w):
        r_ratio = i / float(bar_w)
        r = int(CERULEAN_BLUE[0] * (1 - r_ratio) + NEON_ROSE[0] * r_ratio)
        g = int(CERULEAN_BLUE[1] * (1 - r_ratio) + NEON_ROSE[1] * r_ratio)
        b = int(CERULEAN_BLUE[2] * (1 - r_ratio) + NEON_ROSE[2] * r_ratio)
        draw.line([(start_x + i, bar_y), (start_x + i, bar_y + 1)], fill=(r, g, b))

    # Exact Roles
    sub_y = 215
    draw.text((start_x, sub_y), "FULL STACK DEVELOPER", fill=SOFT_WHITE, font=f_sub)
    draw.text((start_x + 250, sub_y), "•", fill=CERULEAN_BLUE, font=f_sub)
    draw.text((start_x + 270, sub_y), "CREATIVE DEVELOPER", fill=SOFT_WHITE, font=f_sub)
    draw.text((start_x + 510, sub_y), "•", fill=NEON_ROSE, font=f_sub)
    draw.text((start_x + 530, sub_y), "AUTOMATION", fill=SOFT_WHITE, font=f_sub)

    # Exact Taglines
    draw.text((start_x, 265), '"Building Intelligent Digital Experiences."', fill=STEEL_GRAY, font=f_quote)
    draw.text((start_x, 310), "CODE. CREATE. AUTOMATE. EVOLVE.", fill=CERULEAN_BLUE, font=f_tagline)

    # Bottom Metadata
    bot_y = 405
    draw.line([(start_x, bot_y - 12), (start_x + 620, bot_y - 12)], fill=(22, 32, 45), width=1)
    meta_txt = "HOST: SaifSaeed-12  ·  SYS_ID: SAIF_AI_V2.0  ·  STATUS: OPERATIONAL"
    draw.text((start_x, bot_y), meta_txt, fill=STEEL_GRAY, font=f_mono)

    # Save to both target locations
    out_dirs = [os.path.join(REPO_DIR, "assets")]
    if REPO_DIR != BASE_DIR:
        out_dirs.append(os.path.join(BASE_DIR, "assets"))
    else:
        out_dirs.append(os.path.join(REPO_DIR, "SaifSaeed-12", "assets"))

    for out_d in out_dirs:
        os.makedirs(out_d, exist_ok=True)
        target = os.path.join(out_d, "github-banner.png")
        banner.save(target, "PNG", optimize=True)
        print(f"Generated Static Banner: {target}")

def render_storyboard_frame(t, width=960, height=320, core_base=None, is_fallback=False):
    frame = Image.new("RGBA", (width, height), JET_BLACK + (255,))
    
    awakening = 1.0
    if not is_fallback:
        if t < 0.20:
            awakening = 0.45 + 0.55 * (t / 0.20)
        elif t > 0.90:
            awakening = 1.0 - 0.55 * ((t - 0.90) / 0.10)
    
    # 1. Subtle Circuit Grid with Dynamic Illumination
    grid_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_img)
    grid_alpha = int(35 * awakening)
    draw_circuit_grid(g_draw, width, height, step=36, color=(18, 28, 42, grid_alpha))
    
    if not is_fallback and 0.10 <= t <= 0.45:
        p_t = (t - 0.10) / 0.35
        pulse_x = int(50 + p_t * (width - 320))
        for line_y in [75, 140, 210, 275]:
            g_draw.line([(pulse_x - 30, line_y), (pulse_x, line_y)], fill=(0, 166, 255, int(120 * (1 - abs(p_t - 0.5) * 2))), width=2)
    frame = Image.alpha_composite(frame, grid_img)

    # 2. Procedural Floating Particles
    particle_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(particle_layer)
    core_cx = width - 210
    core_cy = height // 2
    
    for i in range(20):
        phase_offset = (i * 0.314159)
        speed = 1.0 + (i % 3) * 0.5
        orb_t = (t * speed + phase_offset) % 1.0
        angle = orb_t * 2 * math.pi
        
        rx = 90 + (i % 5) * 18
        ry = 32 + (i % 4) * 8
        tilt = -25 + (i % 3) * 20
        rad_tilt = math.radians(tilt)
        
        ex = rx * math.cos(angle)
        ey = ry * math.sin(angle)
        px = core_cx + (ex * math.cos(rad_tilt) - ey * math.sin(rad_tilt))
        py = core_cy + (ex * math.sin(rad_tilt) + ey * math.cos(rad_tilt))
        
        is_front = math.sin(angle) > 0
        p_size = 2 if is_front else 1
        p_color = CERULEAN_BLUE if (i % 4 != 0) else NEON_ROSE
        p_alpha = int((180 if is_front else 70) * awakening)
        p_draw.ellipse([px - p_size, py - p_size, px + p_size, py + p_size], fill=p_color + (p_alpha,))
        
    frame = Image.alpha_composite(frame, particle_layer)

    # 3. Metallic-Glass AI Core with 3D Lateral Float & Perspective
    if core_base:
        cw, ch = core_base.size
        sway_x = int(math.sin(t * 2 * math.pi) * 4) if not is_fallback else 0
        float_y = int(math.cos(t * 2 * math.pi) * 3) if not is_fallback else 0
        
        core_pos_x = width - cw + 20 + sway_x
        core_pos_y = (height - ch) // 2 + float_y
        
        mask = Image.new("L", (cw, ch), 0)
        mask_pix = mask.load()
        fade_w = int(cw * 0.45)
        for y in range(ch):
            yf = 1.0
            if y < 15: yf = y / 15.0
            elif y > ch - 15: yf = (ch - y) / 15.0
            for x in range(cw):
                if x < fade_w:
                    xf = 0.5 - 0.5 * math.cos((x / float(fade_w)) * math.pi)
                else:
                    xf = 1.0
                mask_pix[x, y] = int(255 * xf * yf * awakening)
                
        frame.paste(core_base, (core_pos_x, core_pos_y), mask)

    # 4. Multi-Axis Rotating Holographic Rings
    holo_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(holo_layer)
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 135, 42, -28, CERULEAN_BLUE + (int(110 * awakening),), width=2)
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 120, 32, 42, STEEL_GRAY + (int(80 * awakening),), width=1)
    
    rose_ring_alpha = int((140 + 60 * math.sin(t * 2 * math.pi)) * awakening)
    draw_rotated_ellipse(h_draw, (core_cx, core_cy), 110, 26, 75, NEON_ROSE + (rose_ring_alpha,), width=2)
    
    orb_angle1 = t * 2 * math.pi * 2
    r1_x = core_cx + 135 * math.cos(orb_angle1) * math.cos(math.radians(-28)) - 42 * math.sin(orb_angle1) * math.sin(math.radians(-28))
    r1_y = core_cy + 135 * math.cos(orb_angle1) * math.sin(math.radians(-28)) + 42 * math.sin(orb_angle1) * math.cos(math.radians(-28))
    h_draw.ellipse([r1_x - 3, r1_y - 3, r1_x + 3, r1_y + 3], fill=SOFT_WHITE + (int(220 * awakening),))
    
    frame = Image.alpha_composite(frame, holo_layer)

    # 5. Volumetric Ambient Glow & Energy Nucleus Pulse
    pulse_b = int((30 + 14 * math.sin(t * 2 * math.pi)) * awakening)
    if not is_fallback and 0.60 <= t <= 0.80:
        surge = math.sin(((t - 0.60) / 0.20) * math.pi)
        pulse_b += int(35 * surge)

    glow_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(glow_img)
    gl_draw.ellipse([width - 340, height - 230, width + 40, height + 90], fill=(0, 166, 255, pulse_b))
    gl_draw.ellipse([width - 220, height - 170, width, height + 40], fill=(255, 61, 129, int(pulse_b * 0.65)))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(38))
    frame = Image.alpha_composite(frame, glow_img)

    # 6. Floating Holographic HUD Panels (Phase 3 & 4)
    if not is_fallback and 0.35 <= t <= 0.85:
        hud_t = math.sin(((t - 0.35) / 0.50) * math.pi)
        hud_alpha = int(140 * hud_t)
        if hud_alpha > 10:
            hud_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            hd_draw = ImageDraw.Draw(hud_layer)
            hd_draw.rounded_rectangle([core_cx - 195, core_cy - 110, core_cx - 105, core_cy - 45], radius=3, fill=(11, 16, 24, int(hud_alpha * 0.7)), outline=CERULEAN_BLUE + (hud_alpha,), width=1)
            hd_draw.line([(core_cx - 185, core_cy - 85), (core_cx - 115, core_cy - 85)], fill=STEEL_GRAY + (hud_alpha,), width=1)
            hd_draw.line([(core_cx - 185, core_cy - 70), (core_cx - 130, core_cy - 70)], fill=NEON_ROSE + (hud_alpha,), width=1)
            hd_draw.rounded_rectangle([core_cx - 210, core_cy + 55, core_cx - 120, core_cy + 105], radius=3, fill=(11, 16, 24, int(hud_alpha * 0.7)), outline=NEON_ROSE + (int(hud_alpha * 0.8),), width=1)
            hd_draw.line([(core_cx - 200, core_cy + 80), (core_cx - 130, core_cy + 80)], fill=CERULEAN_BLUE + (hud_alpha,), width=1)
            frame = Image.alpha_composite(frame, hud_layer)

    # 7. Animated Holographic Scanning Beam (Phase 4: Energy Scan)
    if not is_fallback:
        scan_t = (t - 0.60) / 0.20
        if 0.0 <= scan_t <= 1.0:
            beam_x = int(30 + scan_t * (width - 80))
            laser_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            l_draw = ImageDraw.Draw(laser_layer)
            for dx in range(-28, 29):
                alpha = int(32 * (1.0 - abs(dx) / 28.0))
                l_draw.line([(beam_x + dx, 10), (beam_x + dx + 15, height - 10)], fill=(0, 166, 255, alpha), width=1)
            l_draw.line([(beam_x, 10), (beam_x + 15, height - 10)], fill=(255, 61, 129, 120), width=2)
            laser_layer = laser_layer.filter(ImageFilter.GaussianBlur(3))
            frame = Image.alpha_composite(frame, laser_layer)

    # 8. Frame Architecture & Corner Ticks
    draw = ImageDraw.Draw(frame)
    draw.rectangle([8, 8, width - 8, height - 8], outline=BORDER_MUTED, width=1)
    draw_corner_ticks(draw, [8, 8, width - 8, height - 8], length=10, color=CERULEAN_BLUE, width=1)

    # 9. Futuristic Typography Overlay
    f_badge = get_font("segoeui.ttf", 11)
    f_name = get_font("segoeuib.ttf", 34)
    f_sub = get_font("segoeuib.ttf", 13)
    f_quote = get_font("segoeuil.ttf", 12)
    f_tagline = get_font("segoeuib.ttf", 11)
    f_mono = get_font("consola.ttf", 10)

    start_x = 55

    pulse_rose = int(180 + 75 * math.sin(t * 2 * math.pi)) if not is_fallback else 255
    draw.ellipse([start_x, 48, start_x + 6, 54], fill=(255, 61, 129, pulse_rose))
    draw.text((start_x + 14, 45), "SAIF AI // COMMAND INTERFACE", fill=CERULEAN_BLUE, font=f_badge)
    draw.text((start_x + 280, 45), "● SYSTEM_ONLINE", fill=CERULEAN_BLUE, font=f_mono)

    draw.text((start_x, 72), "SYED SAIF BIN SAEED", fill=SOFT_WHITE, font=f_name)

    bar_y = 126
    bar_w = 460
    draw.line([(start_x, bar_y), (start_x + bar_w, bar_y)], fill=(26, 36, 48), width=1)
    if not is_fallback:
        hl_pos = int((t * 540) % bar_w)
        draw.line([(start_x + max(0, hl_pos - 40), bar_y), (start_x + min(bar_w, hl_pos + 40), bar_y)], fill=CERULEAN_BLUE, width=2)
    else:
        draw.line([(start_x, bar_y), (start_x + 140, bar_y)], fill=CERULEAN_BLUE, width=2)

    sub_y = 142
    draw.text((start_x, sub_y), "FULL STACK DEVELOPER  •  CREATIVE DEVELOPER  •  AUTOMATION", fill=SOFT_WHITE, font=f_sub)

    draw.text((start_x, 178), '"Building Intelligent Digital Experiences."', fill=STEEL_GRAY, font=f_quote)
    draw.text((start_x, 208), "CODE. CREATE. AUTOMATE. EVOLVE.", fill=CERULEAN_BLUE, font=f_tagline)

    draw.text((start_x, 265), "HOST: SaifSaeed-12  ·  SYS_ID: SAIF_AI  ·  MODE: ONLINE", fill=STEEL_GRAY, font=f_mono)

    return frame

def create_motion_banner():
    width, height = 960, 320
    core_path = get_core_path()
    core_base = None
    if core_path and os.path.exists(core_path):
        c = Image.open(core_path).convert("RGBA")
        ch = 300
        cw = int(c.width * (ch / float(c.height)))
        core_base = c.resize((cw, ch), Image.Resampling.LANCZOS)

    out_dirs = [os.path.join(REPO_DIR, "assets")]
    if REPO_DIR != BASE_DIR:
        out_dirs.append(os.path.join(BASE_DIR, "assets"))
    else:
        out_dirs.append(os.path.join(REPO_DIR, "SaifSaeed-12", "assets"))

    # 1. Static Fallback
    fallback = render_storyboard_frame(0.0, width, height, core_base=core_base, is_fallback=True)
    for out_d in out_dirs:
        os.makedirs(out_d, exist_ok=True)
        fp = os.path.join(out_d, "github-motion-fallback.png")
        fallback.convert("RGB").save(fp, "PNG", optimize=True)
        print(f"Generated Motion Fallback: {fp}")

    # 2. 10-Second Looping Animation
    total_frames = 50
    frames = []
    print(f"Rendering {total_frames} frames for 10-second storyboard animation...")
    for f in range(total_frames):
        t = f / float(total_frames)
        f_img = render_storyboard_frame(t, width, height, core_base=core_base, is_fallback=False)
        rgb_f = f_img.convert("RGB")
        paletted = rgb_f.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(paletted)

    for out_d in out_dirs:
        os.makedirs(out_d, exist_ok=True)
        gp = os.path.join(out_d, "github-motion.gif")
        frames[0].save(
            gp,
            save_all=True,
            append_images=frames[1:],
            duration=200,
            loop=0,
            optimize=True
        )
        size_kb = os.path.getsize(gp) / 1024
        print(f"Generated 10s Looping GIF: {gp} ({size_kb:.1f} KB)")

def create_project_thumbnail(title, category, stack, filename, accent_color=CERULEAN_BLUE, details=None):
    width, height = 700, 360
    img = Image.new("RGBA", (width, height), JET_BLACK + (255,))
    
    grid_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_img)
    draw_circuit_grid(g_draw, width, height, step=35, color=(20, 30, 44, 40))
    img = Image.alpha_composite(img, grid_img)

    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, width - 6, height - 6], fill=None, outline=BORDER_MUTED, width=1)
    draw_corner_ticks(draw, [6, 6, width - 6, height - 6], length=12, color=accent_color, width=1)

    f_title = get_font("segoeuib.ttf", 24)
    f_cat = get_font("segoeuib.ttf", 11)
    f_mono = get_font("consola.ttf", 11)
    f_badge = get_font("segoeui.ttf", 11)

    draw.rounded_rectangle([32, 25, 230, 50], radius=4, fill=(11, 16, 24), outline=accent_color, width=1)
    draw.text((45, 31), category.upper(), fill=accent_color, font=f_cat)

    draw.rounded_rectangle([width - 220, 25, width - 32, 50], radius=4, fill=(20, 12, 18), outline=NEON_ROSE, width=1)
    draw.text((width - 208, 31), "CONCEPT // IN DEV", fill=NEON_ROSE, font=f_cat)

    draw.text((32, 68), title, fill=SOFT_WHITE, font=f_title)
    draw.line([(32, 106), (width - 32, 106)], fill=(24, 34, 48), width=1)
    draw.line([(32, 106), (160, 106)], fill=accent_color, width=2)

    draw.rounded_rectangle([32, 122, width - 32, 275], radius=6, fill=(10, 14, 20), outline=(24, 34, 48), width=1)

    if details == "portfolio":
        draw.text((50, 138), "> THREE.JS VIEWPORT // 60 FPS SPATIAL CANVAS", fill=CERULEAN_BLUE, font=f_mono)
        draw.ellipse([460, 145, 590, 250], outline=CERULEAN_BLUE, width=2)
        draw.ellipse([490, 165, 560, 230], outline=NEON_ROSE, width=1)
        draw.line([(60, 185), (320, 185)], fill=STEEL_GRAY, width=1)
        draw.line([(60, 210), (280, 210)], fill=STEEL_GRAY, width=1)
        draw.line([(60, 235), (360, 235)], fill=accent_color, width=1)
    elif details == "attendance":
        draw.text((50, 138), "> ATTENDANCE MATRIX // REALTIME AUDIT & VERIFY", fill=CERULEAN_BLUE, font=f_mono)
        draw.rounded_rectangle([490, 140, 580, 255], radius=6, fill=(14, 20, 28), outline=accent_color, width=1)
        draw.rounded_rectangle([500, 160, 570, 180], radius=2, fill=(24, 36, 52))
        draw.rounded_rectangle([500, 190, 570, 230], radius=2, fill=(18, 26, 38))
        for idx in range(3):
            draw.rectangle([60, 175 + idx * 26, 420, 191 + idx * 26], fill=(14, 20, 30), outline=(28, 40, 56))
            draw.rectangle([60, 175 + idx * 26, 170 + idx * 75, 191 + idx * 26], fill=accent_color if idx == 0 else (28, 55, 80))
    elif details == "pos":
        draw.text((50, 138), "> POS TERMINAL // TRANSACTION STREAM & INVENTORY", fill=CERULEAN_BLUE, font=f_mono)
        for r in range(2):
            for c in range(3):
                draw.rounded_rectangle([60 + c * 105, 170 + r * 44, 155 + c * 105, 204 + r * 44], radius=4, fill=(14, 22, 32), outline=accent_color if (r==0 and c==1) else (28, 40, 56))
        draw.rounded_rectangle([435, 145, 615, 255], radius=4, fill=(14, 18, 26), outline=NEON_ROSE, width=1)
        draw.text((450, 158), "ORDER_ID: #9021", fill=NEON_ROSE, font=f_mono)
        draw.line([(450, 178), (600, 178)], fill=(34, 46, 62), width=1)
    elif details == "automation":
        draw.text((50, 138), "> N8N WORKFLOW // WEBHOOK & REST PIPELINE", fill=CERULEAN_BLUE, font=f_mono)
        nodes = [(95, 205, "WEBHOOK"), (255, 205, "FILTER/MAP"), (430, 175, "MYSQL DB"), (430, 235, "REST API")]
        for nx, ny, nlbl in nodes:
            draw.rounded_rectangle([nx - 42, ny - 15, nx + 42, ny + 15], radius=4, fill=(18, 28, 42), outline=NEON_ROSE if "WEBHOOK" in nlbl else CERULEAN_BLUE, width=1)
            draw.text((nx, ny - 6), nlbl, fill=SOFT_WHITE, font=f_mono, anchor="mm")
        draw.line([(137, 205), (213, 205)], fill=CERULEAN_BLUE, width=2)
        draw.line([(297, 205), (388, 175)], fill=CERULEAN_BLUE, width=1)
        draw.line([(297, 205), (388, 235)], fill=CERULEAN_BLUE, width=1)

    draw.text((32, 292), "PLANNED ARCHITECTURE:", fill=STEEL_GRAY, font=f_mono)
    bx = 32
    for tag in stack:
        bbox = f_badge.getbbox(tag)
        tw = (bbox[2] - bbox[0]) + 16
        draw.rounded_rectangle([bx, 312, bx + tw, 336], radius=4, fill=(12, 17, 24), outline=(26, 38, 52), width=1)
        draw.text((bx + 8, 317), tag, fill=SOFT_WHITE, font=f_badge)
        bx += tw + 8

    out_dirs = [os.path.join(REPO_DIR, "assets")]
    if REPO_DIR != BASE_DIR:
        out_dirs.append(os.path.join(BASE_DIR, "assets"))
    else:
        out_dirs.append(os.path.join(REPO_DIR, "SaifSaeed-12", "assets"))

    for out_d in out_dirs:
        os.makedirs(out_d, exist_ok=True)
        target = os.path.join(out_d, filename)
        img.save(target, "PNG", optimize=True)
        print(f"Generated Thumbnail: {target}")

def generate_all():
    print("=====================================================")
    print("SAIF AI Visual Asset Pipeline Starting...")
    print("=====================================================")
    create_static_banner()
    create_motion_banner()
    
    print("\nGenerating Concept Thumbnails...")
    create_project_thumbnail(
        title="Personal Portfolio",
        category="Creative 3D Portfolio",
        stack=["React", "Three.js", "GSAP", "Vite"],
        filename="project-portfolio.png",
        accent_color=CERULEAN_BLUE,
        details="portfolio"
    )
    create_project_thumbnail(
        title="Smart Attendance System",
        category="Mobile & Web Utility",
        stack=["React Native", "Expo", "JavaScript", "Firebase"],
        filename="project-attendance.png",
        accent_color=CERULEAN_BLUE,
        details="attendance"
    )
    create_project_thumbnail(
        title="Fast Food POS",
        category="Desktop POS Terminal",
        stack=["Python", "PySide6", "MySQL", "SQLAlchemy", "PyInstaller"],
        filename="project-pos.png",
        accent_color=NEON_ROSE,
        details="pos"
    )
    create_project_thumbnail(
        title="Workflow Automation",
        category="Data Pipeline Engine",
        stack=["n8n", "REST APIs", "Webhooks", "MySQL"],
        filename="project-automation.png",
        accent_color=CERULEAN_BLUE,
        details="automation"
    )
    print("=====================================================")
    print("All SAIF AI Visual Assets Generated Successfully!")
    print("=====================================================")

if __name__ == "__main__":
    generate_all()
