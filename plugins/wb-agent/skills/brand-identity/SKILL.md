---
name: brand-identity
description: Thiết kế hệ thống nhận diện thương hiệu & logo đẳng cấp quốc tế (Visual Identity System, Geometric Grid, 3D Master Render, Production Asset Suite).
---

# 💎 Brand Identity & Logo Design Skill

Skill chuyên biệt đảm trách việc nghiên cứu, sáng tạo và chuẩn hóa toàn diện **Hệ Thống Nhận Diện Thương Hiệu (Visual Identity System)** và **Bộ Logo Chuẩn Sản Xuất (Production Master Suite)** theo quy chuẩn của các Design Agency hàng đầu thế giới (Pentagram, Landor, Chermayeff & Geismar).

---

## 1. Triết Lý Thiết Kế Cốt Lõi (Anti-Amateur Principles)

Tuyệt đối bài trừ các lỗi thiết kế nghiệp dư (amateur/clip-art):
- ❌ **CẤM chi tiết vụn vặt, râu ria**: Không vẽ các chấm tròn vi mạch giả tạo, hình bánh răng lộn xộn, sóng lượn vô nghĩa hay các icon có sẵn rẻ tiền.
- ❌ **CẤM gạch chân rập khuôn**: Không dùng các thanh chữ nhật gạch dưới chữ một cách lười biếng.
- ❌ **CẤM vẽ tự do không lưới (No-Grid)**: Không tùy tiện đặt các góc vát ngẫu hứng. Mọi đường nét bắt buộc phải nằm trên hệ lưới hình học toán học.
- ✔️ **Tối giản quyền lực (Monolithic Power)**: Khối hình học tinh khiết, chắc chắn, dứt khoát.
- ✔️ **Không gian âm (Negative Space)**: Lồng ghép các chữ cái hoặc biểu tượng thông qua các nhát cắt không gian âm tinh tế, sắc bén.
- ✔️ **Chuẩn góc & đường gióng**: Mọi góc vát phải tuân theo 45° hoặc 60°, các đỉnh và chân chữ chạm cùng đường gióng (Baseline & X-height alignment).

---

## 2. Quy Trình 4 Bước Chuẩn Hóa Thương Hiệu (Brand Genesis Pipeline)

### Bước 1: Khảo Sát Định Vị & Ngũ Hành (Brand DNA & Metaphor)
1. **Thông tin cốt lõi**: Tên thương hiệu, Domain, Lĩnh vực hoạt động, Tệp khách hàng mục tiêu, Tính cách thương hiệu (Luxury, Hi-End, Minimalist, Friendly, Cyberpunk...).
2. **Phong thủy / Ngũ hành (nếu có)**: Xác định Dụng Thần (ví dụ Kim - Thủy, Mộc - Hỏa...). 
   - Quy đổi sang chất liệu và màu sắc thượng hạng (ví dụ: Hành Kim = Titanium CNC phay xước, Chrome bạc; Hành Thủy = Kính Sapphire phát quang, Xanh Cobalt sâu thẳm, Đen Obsidian).

### Bước 2: Dựng Lưới Hình Học & Phác Thảo Monogram (The Master Grid)
1. Xây dựng Monogram biểu tượng trên hệ lưới toạ độ (12pt / 24x24 units).
2. Thiết lập quy chuẩn:
   - Cắt vát chuẩn 45°/60°.
   - Độ dày nét đồng nhất (Uniform optical stroke width).
   - Khoảng thở tối thiểu (Minimum clearspace = 1X).
3. Định nghĩa Typography:
   - **Primary Font (Logotype)**: Chữ cái in hoa dày dặn, hình học (Geometric Sans-Serif như Montserrat, Inter, Orbitron, Michroma).
   - **Secondary Font (Tagline/Subtitle)**: Nét thanh, dãn cách ký tự rộng (Letter-spacing / Tracking $\ge$ 3.0).

### Bước 3: Tạo Phối Cảnh 3D & Bản Vẽ Kỹ Thuật Visual Identity System
Gọi tool `generate_image` để tạo ra 2 hình ảnh mỏ neo chất lượng 8K:
1. **Ảnh 1: 3D Masterpiece Render**:
   - Prompt mẫu: `Ultra-premium brand identity logo design for '[BRAND_NAME]' [INDUSTRY] company. Minimalist geometric monogram logo combining letters [LETTERS], crafted from precision CNC brushed titanium metal and glowing deep sapphire blue crystalline glass. Luxurious matte obsidian dark background, professional studio lighting, subtle ambient edge rim light, sharp clean lines, sophisticated corporate tech branding, award-winning logo design, 8k resolution, photorealistic mockup on luxury dark textured card.`
2. **Ảnh 2: Bản Vẽ Visual Identity System Sheet (Giống ảnh mẫu chuẩn)**:
   - Prompt mẫu: `Professional corporate identity brand guidelines presentation sheet for '[BRAND_NAME]' brand. Shows the minimalist geometric [LETTERS] monogram logo in clean 2D vector flat style on pure white background on the left, and dark mode on the right. Accurate clean vector lines, precise geometric grid construction lines, color swatches [COLOR_1] and [COLOR_2], modern bold typography '[BRAND_NAME] - [TAGLINE]', sleek design agency portfolio presentation.`

### Bước 4: Tự Động Hóa Xuất Trọn Bộ File Sản Xuất (Production Master Suite)
Chạy script tự động hóa tích hợp sẵn của skill:
```powershell
python C:\Users\Opengate\.gemini\config\skills\brand-identity\scripts\generate_brand_assets.py "<input_master_image>" "<output_directory>" "<brand_slug>"
```

Script sẽ tự động sinh trọn bộ:
1. `[brand_slug]-logo-light-mode.webp` & `.png` (Nền sáng Header web, tương phản cao, tách nền)
2. `[brand_slug]-logo-dark-mode.webp` & `.png` (Nền tối Footer web, phát quang, tách nền)
3. `[brand_slug]-emblem-transparent.webp` & `.png` (Biểu tượng vuông 1:1 tách nền để in tem nhôm, khắc laser)
4. `[brand_slug]-emblem-master.jpg` & `.webp` (Avatar MXH 1024x1024)
5. `favicon.ico` (Đa kích thước 16, 32, 48, 64px) & `favicon.png` (32px)
6. `apple-touch-icon.png` (180x180px cho iOS)
7. `og-image.webp` (1200x630px chia sẻ mạng xã hội)
8. `brand-showcase.html` (Trang web trình diễn tương tác với các nút tải về trực tiếp từng file gốc).

---

## 3. Checklist Bàn Giao Tài Sản Cho Dự Án

Mỗi khi hoàn thành một bộ Brand Logo, Agent phải đảm bảo các đầu ra sau:
- [ ] Ảnh Render 3D Master & Bản vẽ Visual Identity System lưu trong `images/`.
- [ ] Các file logo Light/Dark mode được nhúng thẳng vào Header & Footer của website.
- [ ] Thẻ `<head>` của các trang HTML/Next.js có đầy đủ: `favicon.ico`, `favicon.png`, `apple-touch-icon.png`, `og:image`.
- [ ] Tạo trang `brand-showcase.html` (hoặc `logo-preview.html`) để khách hàng/user kiểm tra và tải file.
- [ ] Xuất tài liệu `BRAND-GUIDELINES.md` ghi rõ mã màu HEX, RGB, CMYK, thông số font chữ và quy cách sử dụng.
