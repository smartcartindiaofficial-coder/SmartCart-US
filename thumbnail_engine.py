import os
import io
import re
import math
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv
from rembg import remove

# Load environment configurations
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, 'Config.env')
load_dotenv(ENV_PATH)

# ─── RADIAL BACKGROUND SHAPE GENERATORS ───

def draw_sunburst_rays(canvas_size, num_rays=28, ray_opacity=35):
    """Generates a geometric transparent sunburst ray pattern radiating from the center."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    ray_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ray_draw = ImageDraw.Draw(ray_layer)
    
    max_radius = int(math.hypot(width, height))
    angle_step = 360 / num_rays
    
    for i in range(0, num_rays, 2):
        start_angle = math.radians(i * angle_step)
        end_angle = math.radians((i + 1) * angle_step)
        
        p1 = (center_x, center_y)
        p2 = (center_x + max_radius * math.cos(start_angle), center_y + max_radius * math.sin(start_angle))
        p3 = (center_x + max_radius * math.cos(end_angle), center_y + max_radius * math.sin(end_angle))
        
        ray_draw.polygon([p1, p2, p3], fill=(255, 255, 255, ray_opacity))
        
    return ray_layer

def draw_radial_dot_burst(canvas_size, num_spokes=28, dots_per_spoke=14, base_opacity=35):
    """Generates a dot matrix pattern that radiates outward from the center along ray paths."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    dot_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    dot_draw = ImageDraw.Draw(dot_layer)
    
    max_radius = max(width, height) // 1.2
    angle_step = 360 / num_spokes
    
    for i in range(num_spokes):
        angle = math.radians(i * angle_step)
        
        for j in range(1, dots_per_spoke + 1):
            t = j / dots_per_spoke
            radius = max_radius * (t ** 1.3)
            
            if radius < 80:
                continue
                
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            dot_size = int(3 + (8 * t))
            opacity = int(base_opacity * (1.2 - t * 0.4))
            
            dot_draw.ellipse(
                [x - dot_size, y - dot_size, x + dot_size, y + dot_size],
                fill=(255, 255, 255, opacity)
            )
            
    return dot_layer

def draw_alternating_waves(canvas_size, num_rings=9, base_opacity=25):
    """Generates expanding concentric waves with highlighted alternating heavy/thick bands."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    wave_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wave_draw = ImageDraw.Draw(wave_layer)
    
    max_radius = max(width, height) // 1.3
    step = max_radius // num_rings
    
    for i in range(1, num_rings + 1):
        radius = i * step
        
        if i % 2 == 0:
            current_width = 8
            current_opacity = int(base_opacity * 1.8)
        else:
            current_width = 3
            current_opacity = base_opacity
            
        wave_draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=(255, 255, 255, current_opacity),
            width=current_width
        )
        
    return wave_layer

def draw_alternating_squares(canvas_size, num_shapes=8, base_opacity=25):
    """Generates expanding nested squares with highlighted alternating heavy borders."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    shape_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shape_draw = ImageDraw.Draw(shape_layer)
    
    max_radius = max(width, height) // 1.4
    step = max_radius // num_shapes
    
    for i in range(1, num_shapes + 1):
        radius = i * step
        x0, y0 = center_x - radius, center_y - radius
        x1, y1 = center_x + radius, center_y + radius
        
        current_width = 8 if i % 2 == 0 else 3
        current_opacity = int(base_opacity * 1.8) if i % 2 == 0 else base_opacity
        
        shape_draw.rectangle(
            [x0, y0, x1, y1],
            outline=(255, 255, 255, current_opacity),
            width=current_width
        )
        
    return shape_layer

def draw_alternating_ovals(canvas_size, num_shapes=9, base_opacity=25):
    """Generates expanding concentric ovals stretched proportionally to canvas limits."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    shape_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shape_draw = ImageDraw.Draw(shape_layer)
    
    step_w = (width // 1.2) // num_shapes
    step_h = (height // 1.2) // num_shapes
    
    for i in range(1, num_shapes + 1):
        rad_w, rad_h = i * step_w, i * step_h
        x0, y0 = center_x - rad_w, center_y - rad_h
        x1, y1 = center_x + rad_w, center_y + rad_h
        
        current_width = 8 if i % 2 == 0 else 3
        current_opacity = int(base_opacity * 1.8) if i % 2 == 0 else base_opacity
        
        shape_draw.ellipse(
            [x0, y0, x1, y1],
            outline=(255, 255, 255, current_opacity),
            width=current_width
        )
        
    return shape_layer

def draw_alternating_rhombuses(canvas_size, num_shapes=8, base_opacity=25):
    """Generates expanding nested diamond/rhombus frames with highlighted alternating thick lines."""
    width, height = canvas_size
    center_x, center_y = width // 2, height // 2
    
    shape_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    shape_draw = ImageDraw.Draw(shape_layer)
    
    max_radius = max(width, height) // 1.3
    step = max_radius // num_shapes
    
    for i in range(1, num_shapes + 1):
        radius = i * step
        
        top_vertex    = (center_x, center_y - radius)
        right_vertex  = (center_x + radius, center_y)
        bottom_vertex = (center_x, center_y + radius)
        left_vertex   = (center_x - radius, center_y)
        
        current_width = 8 if i % 2 == 0 else 3
        current_opacity = int(base_opacity * 1.8) if i % 2 == 0 else base_opacity
        
        shape_draw.polygon(
            [top_vertex, right_vertex, bottom_vertex, left_vertex],
            outline=(255, 255, 255, current_opacity),
            width=current_width
        )
        
    return shape_layer

# ─── CORE THEME ENGINE ───

def extract_dominant_theme_from_image(product_layer, product_name):
    """Extracts product color profiles, sets gradient palettes, and randomly assigns styles."""
    small_img = product_layer.resize((50, 50))
    pixels = list(small_img.getdata())
    valid_pixels = [p for p in pixels if len(p) == 4 and p[3] > 220]
    
    if not valid_pixels:
        avg_r, avg_g, avg_b = 20, 24, 30
    else:
        avg_r = sum(p[0] for p in valid_pixels) // len(valid_pixels)
        avg_g = sum(p[1] for p in valid_pixels) // len(valid_pixels)
        avg_b = sum(p[2] for p in valid_pixels) // len(valid_pixels)

    bg_base = (max(10, avg_r // 6), max(10, avg_g // 6), max(10, avg_b // 6), 255)
    bg_glow = (min(255, int(avg_r * 0.5)), min(255, int(avg_g * 0.5)), min(255, int(avg_b * 0.5)), 255)

    max_channel = max(bg_glow[0], bg_glow[1], bg_glow[2], 1)
    scale_factor = 230 / max_channel if max_channel < 180 else 1.2
    
    gradient_top = (
        min(255, int(bg_glow[0] * scale_factor + 10)),
        min(255, int(bg_glow[1] * scale_factor + 10)),
        min(255, int(bg_glow[2] * scale_factor + 10)),
        255
    )
    gradient_bottom = (255, 255, 255, 255) 

    # Randomized layout pools
    font_options = ["IMPACT_BEBAS", "TECH_MONTSERRAT", "CREATIVE_POPPINS"]
    bg_options = ["rays", "radial_dots", "alternating_waves", "squares", "ovals", "rhombuses"]

    font_style = random.choice(font_options)
    bg_style = random.choice(bg_options)

    return {
        "bg_base": bg_base,
        "bg_glow": bg_glow,
        "gradient_top": gradient_top,
        "gradient_bottom": gradient_bottom,
        "font_style": font_style,
        "bg_style": bg_style
    }

def download_and_get_fonts(font_style):
    font_dir = os.path.join(SCRIPT_DIR, "fonts")
    os.makedirs(font_dir, exist_ok=True)
    
    font_urls = {
        "Montserrat-Black.ttf": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat-Black.ttf",
        "Poppins-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
        "BebasNeue-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf"
    }
    
    for name, url in font_urls.items():
        p = os.path.join(font_dir, name)
        if os.path.exists(p) and os.path.getsize(p) == 0:
            os.remove(p)
        if not os.path.exists(p):
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    with open(p, "wb") as f: f.write(r.content)
            except Exception: pass

    style_map = {
        "IMPACT_BEBAS": "BebasNeue-Regular.ttf",
        "TECH_MONTSERRAT": "Montserrat-Black.ttf",
        "CREATIVE_POPPINS": "Poppins-Bold.ttf"
    }
    t_file = style_map.get(font_style, style_map["CREATIVE_POPPINS"])
    return os.path.join(font_dir, t_file)

def safe_load_font(font_path, size):
    if font_path and os.path.exists(font_path) and os.path.getsize(font_path) > 0:
        try: return ImageFont.truetype(font_path, size)
        except IOError: pass
    for fallback in ["arialbd.ttf", "arial.ttf", "sans-serif"]:
        try: return ImageFont.truetype(fallback, size)
        except IOError: continue
    return ImageFont.load_default()

def wrap_text_to_lines(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line: lines.append(' '.join(current_line))
            current_line = [word]
    if current_line: lines.append(' '.join(current_line))
    return lines

def draw_gradient_text_block_with_3d_shadow(bg_canvas, text, position, font_path, max_width, top_color, bottom_color, shadow_color=(0, 0, 0, 255), offset=(12, 14)):
    """Renders a single center-aligned text block utilizing a deep 3D offset shadow with full canvas gradient mapping."""
    current_size = 125
    lines = []
    font = None
    line_height = 0
    
    while current_size >= 50:
        font = safe_load_font(font_path, current_size)
        lines = wrap_text_to_lines(text, font, max_width)
        bbox_sample = font.getbbox("XYgq")
        line_height = (bbox_sample[3] - bbox_sample[1]) + 15
        if current_size * len(lines) <= 360:
            break
        current_size -= 4

    canvas_draw = ImageDraw.Draw(bg_canvas)
    start_x, start_y = position
    off_x, off_y = offset
    
    # FIX: Initialize mask layout tracking layer to match full main canvas dimensions (1080x1920)
    mask_layer = Image.new("L", bg_canvas.size, 0)
    m_draw = ImageDraw.Draw(mask_layer)
    
    for i, line in enumerate(lines):
        line_bbox = font.getbbox(line)
        line_width = line_bbox[2] - line_bbox[0]
        center_offset_x = (max_width - line_width) // 2
        
        lx = start_x + center_offset_x
        ly = start_y + (i * line_height)
        
        # 3D Shadow drop
        canvas_draw.text((lx + off_x, ly + off_y), line, fill=shadow_color, font=font)
        # Record font silhouette shape metrics inside full canvas space
        m_draw.text((lx, ly), line, fill=255, font=font)

    # FIX: Structural full-frame canvas gradient mapping brush
    gradient_brush = Image.new("RGBA", bg_canvas.size)
    g_draw = ImageDraw.Draw(gradient_brush)
    
    # Calculate gradient limits specifically around the vertical footprint of the text block
    total_text_height = line_height * len(lines)
    grad_start_y = start_y
    grad_end_y = start_y + total_text_height
    
    for y in range(gradient_brush.height):
        if y < grad_start_y:
            factor = 0.0
        elif y > grad_end_y:
            factor = 1.0
        else:
            factor = (y - grad_start_y) / max(1, (grad_end_y - grad_start_y))
            
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * factor)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * factor)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * factor)
        a = int(top_color[3] + (bottom_color[3] - top_color[3]) * factor)
        g_draw.line([(0, y), (gradient_brush.width, y)], fill=(r, g, b, a))

    # Mask text details smoothly over background canvas
    text_filled_layer = Image.new("RGBA", bg_canvas.size, (0, 0, 0, 0))
    text_filled_layer.paste(gradient_brush, (0, 0), mask=mask_layer)
    bg_canvas.alpha_composite(text_filled_layer)

def generate_thumbnail_multi(asin, product_name, specifications, image_paths_list):
    output_filename = f"tn_{asin}.jpg"
    output_path = os.path.join(SCRIPT_DIR, output_filename)
    
    valid_images = [path for path in image_paths_list if os.path.exists(path)]
    if not valid_images:
        print("❌ Error: No valid source images found.")
        return None

    primary_img_path = valid_images[0]
    print(f"🚀 [Studio Engine] Compiling 3D Overlay Layout for ASIN: {asin}")

    try:
        # ─── PHASE 1: BACKGROUND REMOVAL & CROP ───
        with open(primary_img_path, 'rb') as img_file:
            input_data = img_file.read()
        transparent_bytes = remove(input_data)
        product_layer = Image.open(io.BytesIO(transparent_bytes)).convert("RGBA")

        bounding_box = product_layer.getbbox()
        if bounding_box:
            product_layer = product_layer.crop(bounding_box)

        # ─── PHASE 2: AUTOMATED COLOR THEME EXTRACTION ───
        theme = extract_dominant_theme_from_image(product_layer, product_name)
        title_font_path = download_and_get_fonts(theme["font_style"])

        # ─── PHASE 3: CANVAS BACKGROUND COMPOSITION ───
        bg_canvas = Image.new("RGBA", (1080, 1920), theme["bg_base"])
        canvas_w, canvas_h = bg_canvas.size
        
        vignette = Image.new("L", (1080, 1920), 0)
        v_draw = ImageDraw.Draw(vignette)
        v_draw.ellipse([-250, 150, 1330, 1750], fill=130)
        vignette_blurred = vignette.filter(ImageFilter.GaussianBlur(260))
        
        studio_light = Image.new("RGBA", (1080, 1920), theme["bg_glow"])
        bg_canvas.paste(studio_light, (0, 0), vignette_blurred)

        print(f"🪄 [Layout Engine] Selected style variant: '{theme['bg_style']}'")
        if theme["bg_style"] == "radial_dots":
            overlay_graphic = draw_radial_dot_burst(bg_canvas.size, num_spokes=40, dots_per_spoke=20, base_opacity=35)
        elif theme["bg_style"] == "alternating_waves":
            overlay_graphic = draw_alternating_waves(bg_canvas.size, num_rings=24, base_opacity=25)
        elif theme["bg_style"] == "squares":
            overlay_graphic = draw_alternating_squares(bg_canvas.size, num_shapes=24, base_opacity=25)
        elif theme["bg_style"] == "ovals":
            overlay_graphic = draw_alternating_ovals(bg_canvas.size, num_shapes=24, base_opacity=25)
        elif theme["bg_style"] == "rhombuses":
            overlay_graphic = draw_alternating_rhombuses(bg_canvas.size, num_shapes=24, base_opacity=25)
        else:
            overlay_graphic = draw_sunburst_rays(bg_canvas.size, num_rays=28, ray_opacity=35)
            
            
        bg_canvas.alpha_composite(overlay_graphic)

        # ─── PHASE 4: RENDER TYPOGRAPHY FIRST (Bottom Layer) ───
        clean_title = product_name.strip()
        if theme["font_style"] != "IMPACT_BEBAS" and clean_title.isupper():
            clean_title = clean_title.title()
            
        draw_gradient_text_block_with_3d_shadow(
            bg_canvas=bg_canvas,
            text=clean_title,
            position=(80, 120),
            font_path=title_font_path,
            max_width=canvas_w - 160,
            top_color=theme["gradient_top"],
            bottom_color=theme["gradient_bottom"],
            shadow_color=(0, 0, 0, 255),
            offset=(11, 13)
        )

        # ─── PHASE 5: FIXED ABSOLUTE PRODUCT OVERLAY CENTERING (Top Layer) ───
        # Keeps product safely locked to center-point (1100) and stacks it over the title text
        center_target_x = canvas_w // 2
        center_target_y = 1100  
        
        max_allowed_w = canvas_w - 60   
        max_allowed_h = 1100 
        
        prod_w, prod_h = product_layer.size
        scale_w = max_allowed_w / prod_w
        scale_h = max_allowed_h / prod_h
        final_scale = min(scale_w, scale_h)
        
        target_w = int(prod_w * final_scale * 0.92)
        target_h = int(prod_h * final_scale * 0.92)
            
        product_resized = product_layer.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        pos_x = center_target_x - (target_w // 2)
        pos_y = center_target_y - (target_h // 2)

        # Shadow processing
        shadow_blur = 55
        shadow_mask = product_resized.getchannel('A').resize((target_w + shadow_blur*2, target_h + shadow_blur*2), resample=Image.Resampling.BOX)
        shadow_img = Image.new("RGBA", shadow_mask.size, (2, 2, 4, 235))
        shadow_blurred = Image.composite(shadow_img, Image.new("RGBA", shadow_mask.size), shadow_mask)
        shadow_blurred = shadow_blurred.filter(ImageFilter.GaussianBlur(shadow_blur // 2))
        
        # Paste over the typography layer
        bg_canvas.alpha_composite(shadow_blurred, (pos_x - shadow_blur, pos_y - shadow_blur))
        bg_canvas.alpha_composite(product_resized, (pos_x, pos_y))

        # Output conversion
        final_thumbnail = bg_canvas.convert("RGB")
        final_thumbnail.save(output_path, "JPEG", quality=95)
        print(f"🎉 SUCCESS: Balanced 3D overlay poster with fixed text gradient saved to: {output_path}\n")
        return output_path

    except Exception as e:
        print(f"❌ Dynamic Engine Failed: {e}")
        return None

if __name__ == "__main__":
    # IMPORTANT: Ensure 'bottle_test.jpg' is a clean original product image file asset, 
    # not a previously processed thumbnail containing background frames!
    generate_thumbnail_multi(
        asin="B0FGVCXB92", 
        product_name="Personalized Name Charm Leather Wallet", 
        specifications=[], 
        image_paths_list=[os.path.join(SCRIPT_DIR, "test.jpg")]
    )