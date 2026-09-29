#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brand Identity Asset Generator
Automatically processes 3D Master Logo into production-ready Web/Mobile/Print assets:
- Alpha transparent PNG/WebP (Tight Bounding Box)
- Light & Dark mode variations
- Square Emblem & App Icon (1024x1024)
- Multi-size Favicon.ico (16, 32, 48, 64) & Favicon.png (32x32)
- Apple Touch Icon (180x180)
- OpenGraph Social Banner (1200x630)
"""

import sys
import os
from PIL import Image
import numpy as np

def extract_alpha_tight(img, threshold_low=26, threshold_high=46, padding=12):
    """Smoothly separates background and tightly crops to content bounding box."""
    rgba = img.convert('RGBA')
    arr = np.array(rgba, dtype=np.float32)
    
    # Calculate max channel brightness
    max_c = np.maximum(np.maximum(arr[:, :, 0], arr[:, :, 1]), arr[:, :, 2])
    alpha = np.clip((max_c - threshold_low) / (threshold_high - threshold_low) * 255.0, 0, 255)
    arr[:, :, 3] = alpha
    
    res = Image.fromarray(arr.astype(np.uint8))
    bbox = res.getbbox()
    if bbox:
        x1 = max(0, bbox[0] - padding)
        y1 = max(0, bbox[1] - padding)
        x2 = min(res.width, bbox[2] + padding)
        y2 = min(res.height, bbox[3] + padding)
        res = res.crop((x1, y1, x2, y2))
    return res

def make_light_mode_variant(logo_rgba):
    """Darkens white/light subtitle text for perfect contrast on light backgrounds."""
    arr = np.array(logo_rgba)
    h, w, _ = arr.shape
    sub_start_y = int(h * 0.68)
    sub_area = arr[sub_start_y:, :, :]
    
    # Identify bright subtitle pixels
    mask = (sub_area[:, :, 0] > 140) & (sub_area[:, :, 1] > 140) & (sub_area[:, :, 2] > 140) & (sub_area[:, :, 3] > 40)
    sub_area[mask, 0] = 30  # R: Dark Slate #1E293B
    sub_area[mask, 1] = 41  # G
    sub_area[mask, 2] = 59  # B
    return Image.fromarray(arr)

def process_brand(horizontal_img_path, emblem_img_path, output_dir, brand_slug="brand"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"=== PROCESSING BRAND ASSETS FOR: {brand_slug.upper()} ===")
    
    # 1. Process Horizontal Logo
    if os.path.exists(horizontal_img_path):
        raw_h = Image.open(horizontal_img_path)
        logo_trans = extract_alpha_tight(raw_h, threshold_low=28, threshold_high=48)
        
        dark_png = os.path.join(output_dir, f"{brand_slug}-logo-dark-mode.png")
        dark_webp = os.path.join(output_dir, f"{brand_slug}-logo-dark-mode.webp")
        logo_trans.save(dark_png, "PNG")
        logo_trans.save(dark_webp, "WEBP", quality=95)
        print(f"[OK] Horizontal Dark Mode: {dark_webp} ({logo_trans.size})")
        
        # Light Mode Variant
        light_logo = make_light_mode_variant(logo_trans)
        light_png = os.path.join(output_dir, f"{brand_slug}-logo-light-mode.png")
        light_webp = os.path.join(output_dir, f"{brand_slug}-logo-light-mode.webp")
        light_logo.save(light_png, "PNG")
        light_logo.save(light_webp, "WEBP", quality=95)
        print(f"[OK] Horizontal Light Mode: {light_webp} ({light_logo.size})")

        # OpenGraph Banner (1200x630)
        og_canvas = Image.new("RGB", (1200, 630), (7, 11, 20))
        target_w = 1100
        ratio = target_w / raw_h.width
        scaled = raw_h.resize((target_w, int(raw_h.height * ratio)), Image.Resampling.LANCZOS)
        x_pos = (1200 - scaled.width) // 2
        y_pos = (630 - scaled.height) // 2
        og_canvas.paste(scaled, (x_pos, y_pos))
        og_path = os.path.join(output_dir, "og-image.webp")
        og_canvas.save(og_path, "WEBP", quality=90)
        print(f"[OK] OpenGraph Social Banner: {og_path} (1200x630)")

    # 2. Process Square Emblem
    if os.path.exists(emblem_img_path):
        raw_e = Image.open(emblem_img_path)
        emblem_trans = extract_alpha_tight(raw_e, threshold_low=20, threshold_high=42)
        
        emblem_trans_png = os.path.join(output_dir, f"{brand_slug}-emblem-transparent.png")
        emblem_trans_webp = os.path.join(output_dir, f"{brand_slug}-emblem-transparent.webp")
        emblem_trans.save(emblem_trans_png, "PNG")
        emblem_trans.save(emblem_trans_webp, "WEBP", quality=95)
        print(f"[OK] Transparent Emblem: {emblem_trans_webp} ({emblem_trans.size})")
        
        # 1:1 Square Solid Master (1024x1024)
        sq_size = max(raw_e.size)
        sq = Image.new("RGB", (sq_size, sq_size), (0, 0, 0))
        sq.paste(raw_e, ((sq_size - raw_e.width) // 2, (sq_size - raw_e.height) // 2))
        
        master_jpg = os.path.join(output_dir, f"{brand_slug}-emblem-master.jpg")
        master_webp = os.path.join(output_dir, f"{brand_slug}-emblem-master.webp")
        sq.save(master_jpg, "JPEG", quality=95)
        sq.save(master_webp, "WEBP", quality=95)
        print(f"[OK] Master Square Avatar: {master_webp} ({sq_size}x{sq_size})")

        # Favicon ICO (Multi-size: 16, 32, 48, 64)
        ico_path = os.path.join(output_dir, "favicon.ico")
        sq.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
        print(f"[OK] Multi-size Favicon ICO: {ico_path}")

        # Favicon PNG (32x32)
        fav32 = sq.resize((32, 32), Image.Resampling.LANCZOS)
        fav32_path = os.path.join(output_dir, "favicon.png")
        fav32.save(fav32_path, "PNG")
        print(f"[OK] Favicon PNG: {fav32_path} (32x32)")

        # Apple Touch Icon (180x180)
        apple180 = sq.resize((180, 180), Image.Resampling.LANCZOS)
        apple_path = os.path.join(output_dir, "apple-touch-icon.png")
        apple180.save(apple_path, "PNG")
        print(f"[OK] Apple Touch Icon: {apple_path} (180x180)")

    print("\n=== ALL ASSETS GENERATED SUCCESSFULLY! ===")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_brand_assets.py <horizontal_img> <emblem_img> <output_dir> [brand_slug]")
        sys.exit(1)
        
    h_img = sys.argv[1]
    e_img = sys.argv[2]
    out_dir = sys.argv[3]
    slug = sys.argv[4] if len(sys.argv) > 4 else "brand"
    process_brand(h_img, e_img, out_dir, slug)
