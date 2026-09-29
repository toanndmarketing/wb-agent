#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brand Showcase HTML Generator
Generates an executive interactive presentation page with one-click download links for all brand assets.
"""

import sys
import os

TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bản Gốc Nhận Diện Thương Hiệu 3D Master — {brand_name}</title>
  <link rel="icon" type="image/png" href="{assets_dir}/favicon.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .glass-panel {{ background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(56, 189, 248, 0.2); }}
  </style>
</head>
<body class="bg-[#050811] text-slate-200 min-h-screen py-12 px-4 sm:px-8 space-y-16 antialiased">

  <header class="max-w-6xl mx-auto text-center space-y-4">
    <div class="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-400/30 px-4 py-1.5 rounded-full text-xs font-bold text-emerald-400 uppercase tracking-widest">
      <i class="fa-solid fa-circle-check"></i> BẢN CHÍNH THỨC ĐÃ DUYỆT (PRODUCTION MASTER SUITE)
    </div>
    <h1 class="text-3xl sm:text-5xl font-black text-white tracking-tight">
      BỘ TÀI SẢN THƯƠNG HIỆU <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-cyan-300 to-white">{brand_name}</span>
    </h1>
    <p class="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
      Hệ thống nhận diện chuẩn quốc tế: Tối giản quyền lực, chuẩn lưới hình học và trọn bộ file chuẩn sản xuất.
    </p>
  </header>

  <main class="max-w-6xl mx-auto space-y-14">

    <!-- 1. FULL HORIZONTAL LOGO -->
    <section class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-mono text-sky-400 font-bold uppercase tracking-wider">HẠNG MỤC 01</span>
          <h2 class="text-xl sm:text-2xl font-black text-white">Logo Ngang Master (Horizontal Full Lockup)</h2>
        </div>
        <span class="text-xs text-slate-400">Tách nền trong suốt • Sẵn sàng cho Web/App</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Light Mode -->
        <div class="bg-white rounded-3xl p-8 shadow-2xl space-y-4 text-slate-900 border border-slate-200">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <span class="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
              <i class="fa-solid fa-sun text-amber-500"></i> Nền Sáng (Header Website)
            </span>
            <span class="text-[11px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded">{brand_slug}-logo-light-mode.webp</span>
          </div>
          <div class="py-8 flex items-center justify-center bg-[#f8fafc] rounded-2xl border border-slate-100">
            <img src="{assets_dir}/{brand_slug}-logo-light-mode.webp" alt="{brand_name} Light Logo" class="h-14 sm:h-16 w-auto drop-shadow-md hover:scale-105 transition duration-300" />
          </div>
          <div class="flex items-center justify-between text-xs text-slate-500 pt-1">
            <span>Ứng dụng: Header trang chủ, hóa đơn, ấn phẩm in</span>
            <a href="{assets_dir}/{brand_slug}-logo-light-mode.png" download class="text-sky-600 font-bold hover:underline flex items-center gap-1">
              <i class="fa-solid fa-download"></i> Tải PNG Gốc
            </a>
          </div>
        </div>

        <!-- Dark Mode -->
        <div class="bg-[#0b101d] rounded-3xl p-8 shadow-2xl space-y-4 text-white border border-slate-800">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <span class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <i class="fa-solid fa-moon text-sky-400"></i> Nền Tối (Footer & Dark Theme)
            </span>
            <span class="text-[11px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">{brand_slug}-logo-dark-mode.webp</span>
          </div>
          <div class="py-8 flex items-center justify-center bg-[#070b14] rounded-2xl border border-slate-800/60">
            <img src="{assets_dir}/{brand_slug}-logo-dark-mode.webp" alt="{brand_name} Dark Logo" class="h-14 sm:h-16 w-auto drop-shadow-[0_4px_24px_rgba(2,132,199,0.45)] hover:scale-105 transition duration-300" />
          </div>
          <div class="flex items-center justify-between text-xs text-slate-400 pt-1">
            <span>Ứng dụng: Footer web, vỏ case, video intro</span>
            <a href="{assets_dir}/{brand_slug}-logo-transparent.png" download class="text-sky-400 font-bold hover:underline flex items-center gap-1">
              <i class="fa-solid fa-download"></i> Tải PNG Gốc
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. EMBLEM & ICONS -->
    <section class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-mono text-sky-400 font-bold uppercase tracking-wider">HẠNG MỤC 02</span>
          <h2 class="text-xl sm:text-2xl font-black text-white">Biểu Tượng 3D Master (Square Emblem 1:1)</h2>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="glass-panel p-6 rounded-3xl space-y-4 flex flex-col items-center text-center">
          <div class="w-full aspect-square bg-[#03060d] rounded-2xl p-6 flex items-center justify-center border border-slate-800">
            <img src="{assets_dir}/{brand_slug}-emblem-transparent.webp" alt="{brand_name} Transparent Emblem" class="w-44 h-44 object-contain drop-shadow-[0_8px_32px_rgba(2,132,199,0.5)]" />
          </div>
          <div>
            <h3 class="font-bold text-white text-sm">Emblem Trong Suốt (Alpha PNG)</h3>
            <p class="text-xs text-slate-400 mt-0.5">Dập nổi lên mọi chất liệu, tem nhôm, linh kiện</p>
          </div>
          <a href="{assets_dir}/{brand_slug}-emblem-transparent.png" download class="text-xs text-sky-400 font-bold hover:underline flex items-center gap-1">
            <i class="fa-solid fa-download"></i> Tải PNG Trong Suốt
          </a>
        </div>

        <div class="glass-panel p-6 rounded-3xl space-y-4 flex flex-col items-center text-center">
          <div class="w-full aspect-square bg-black rounded-2xl overflow-hidden border border-slate-800 flex items-center justify-center">
            <img src="{assets_dir}/{brand_slug}-emblem-master.webp" alt="{brand_name} Master Avatar" class="w-full h-full object-cover" />
          </div>
          <div>
            <h3 class="font-bold text-white text-sm">Avatar / App Icon Chuẩn (1024px)</h3>
            <p class="text-xs text-slate-400 mt-0.5">Avatar Zalo OA, Fanpage, Youtube, TikTok</p>
          </div>
          <a href="{assets_dir}/{brand_slug}-emblem-master.jpg" download class="text-xs text-sky-400 font-bold hover:underline flex items-center gap-1">
            <i class="fa-solid fa-download"></i> Tải File Gốc (1024x1024px)
          </a>
        </div>

        <div class="glass-panel p-6 rounded-3xl space-y-4 flex flex-col justify-between">
          <div class="space-y-3">
            <h3 class="font-bold text-white text-sm flex items-center gap-2">
              <i class="fa-solid fa-box-open text-sky-400"></i> Gói Icon Web & Trình Duyệt
            </h3>
            <div class="space-y-2 pt-2 text-xs">
              <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <span><strong>favicon.ico</strong></span>
                <span class="text-slate-500">16, 32, 48, 64px</span>
              </div>
              <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <span><strong>favicon.png</strong></span>
                <span class="text-slate-500">32 x 32px</span>
              </div>
              <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                <span><strong>apple-touch-icon.png</strong></span>
                <span class="text-slate-500">180 x 180px</span>
              </div>
            </div>
          </div>
          <div class="p-3 bg-sky-500/10 border border-sky-400/20 rounded-xl text-center text-[11px] text-sky-300">
            ✔ Tích hợp trực tiếp vào mã nguồn website
          </div>
        </div>
      </div>
    </section>

    <!-- 3. SOCIAL BANNER -->
    <section class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-mono text-sky-400 font-bold uppercase tracking-wider">HẠNG MỤC 03</span>
          <h2 class="text-xl sm:text-2xl font-black text-white">Ảnh Chia Sẻ Mạng Xã Hội (OpenGraph Image 1200x630)</h2>
        </div>
      </div>
      <div class="rounded-3xl overflow-hidden shadow-2xl border border-slate-800">
        <img src="{assets_dir}/og-image.webp" alt="{brand_name} OG Banner" class="w-full h-auto object-cover" />
      </div>
    </section>

  </main>

  <footer class="max-w-6xl mx-auto text-center text-xs text-slate-500 pt-8 border-t border-slate-800">
    © 2026 {brand_name} • Hệ Thống Nhận Diện Thương Hiệu Đã Chuẩn Hóa Sản Xuất
  </footer>

</body>
</html>
"""

def generate_showcase(output_file, brand_name, brand_slug, assets_dir="images"):
    html_content = TEMPLATE.format(
        brand_name=brand_name,
        brand_slug=brand_slug,
        assets_dir=assets_dir
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated Brand Showcase HTML: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_brand_showcase.py <output_html> <brand_name> [brand_slug] [assets_dir]")
        sys.exit(1)
    
    out_html = sys.argv[1]
    name = sys.argv[2]
    slug = sys.argv[3] if len(sys.argv) > 3 else "brand"
    assets = sys.argv[4] if len(sys.argv) > 4 else "images"
    generate_showcase(out_html, name, slug, assets)
