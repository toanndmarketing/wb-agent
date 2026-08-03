---
name: seo-preflight-card
description: "SEO Preflight Card — Bộ Checklist DUY NHẤT (Single Source of Truth) bắt buộc khi Code hoặc Audit mọi Page. Merge từ 10 Case Audit (teamwork) + 9 Quy Tắc Onpage (seo-technical) + Anti-Cannibalization (seo-content). Đọc file này THAY VÌ đọc lại 3 skill trên."
---

# 🛡️ SEO PREFLIGHT CARD — Checklist Bắt Buộc Khi Code / Audit Mọi Page

> **Vai trò**: Đây là **Single Source of Truth** duy nhất cho tất cả quy tắc SEO + Frontend Performance mà Dev/Builder/QA Tester phải tuân thủ khi tạo mới, chỉnh sửa, hoặc audit bất kỳ page nào.
> Nếu cần tra cứu lý do chi tiết / best practices sâu → Đọc [speckit.seo-technical](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.seo-technical/SKILL.md) (Deep Reference).

---

## A. PRE-CODE GATE (Kiểm tra TRƯỚC khi viết dòng code đầu tiên)

- [ ] **A1 — Target Keyword**: Page này đã có Target Keyword chỉ định trong `spec.md` hoặc `silo-content-map.md` chưa? → Nếu KHÔNG → **DỪNG, hỏi User**.
- [ ] **A2 — Anti-Cannibalization**: Target Keyword có trùng với page khác không? Homepage (`/`) và Directory Hub **CẤM dùng chung bộ từ khóa**. Trang chủ tập trung Brand + Platform, Hub tập trung Directory/Catalog Index.
- [ ] **A3 — Page Type**: Xác định page thuộc loại nào (Home / Pillar / Silo / Cluster / Blog) → quyết định Schema JSON-LD tương ứng.

---

## B. POST-CODE CHECK — 19 Hạng Mục Kiểm Tra Sau Khi Code Xong

### Nhóm 1: URL & Canonical (Crawlability)
- [ ] **B1 — Trailing Slash & Clean URL**: Khai báo `trailingSlash: true`. URL không redirect chain 308. Pretty URLs (kebab-case, CẤM query parameter).
- [ ] **B5 — Absolute Canonical & Meta Robots**: Thẻ `<link rel="canonical">` phải là Absolute URL (`https://domain.com/path/`). Meta robots `index, follow` cho public page. Canonical, og:url, sitemap đồng bộ 100% trailing slash.

### Nhóm 2: Content Structure (Semantic HTML)
- [ ] **B2 — Dynamic Meta Title & Description**: Title 30-60 chars (keyword chính sát đầu), Description 120-158 chars, mỗi page UNIQUE. CẤM duplicate suffix (Brand lặp 2 lần). CẤM ngắn dưới 90 chars hoặc dài quá 155 chars ở Description.
- [ ] **B3 — Single H1 & Heading Hierarchy**: Duy nhất 1 `<h1>` per page. Phân cấp H1→H2→H3 chuẩn. CẤM `<a>` bọc khối H2/H3 (chỉ bọc tiêu đề + CSS `after:absolute after:inset-0`).
- [ ] **B4 — Consolidated GEO Direct Answer Hero**: Hợp nhất đoạn mô tả chính dưới H1 vào làm CHÍNH khung `<GeoDirectAnswer html="..." />`. CẤM tách rời 1 `<p>` thô + 1 GEO box trùng lặp.

### Nhóm 3: Schema & Structured Data
- [ ] **B6 — Multi-layer Schema JSON-LD**: Tiêm qua `<script type="application/ld+json">` dùng `dangerouslySetInnerHTML`. Tối thiểu: `WebPage` + `BreadcrumbList`. Tùy loại page thêm: `Organization`, `WebSite`, `FAQPage`, `Article`, `SoftwareApplication`. 100% URL trong Schema là Absolute. CẤM Microdata/RDFa inline.
- [ ] **B8 — FAQ Visual Accordion**: Có FAQPage Schema → BẮT BUỘC render Accordion UI (Framer Motion / CSS) có đóng/mở mượt. CẤM hardcode UI tĩnh phẳng.

### Nhóm 4: Internal Linking & Navigation
- [ ] **B7 — Internal Links 3 Chiều**: Link Pillar↔Silo↔Cluster qua component `<RelatedLinks>`. Anchor text ngữ nghĩa, không link gãy. CẤM Self-Referencing Links. CẤM Duplicate Links trong 1 Card.
- [ ] **B12 — Breadcrumb Terminal Span**: Phần tử cuối Breadcrumb = `<span aria-current="page">`, CẤM link tự thân.
- [ ] **B13 — Pure Anchor Text & Link Hygiene**:
  - `<Link>` CHỈ bọc đúng tiêu đề H2/H3, kết hợp CSS `after:absolute after:inset-0 after:z-20` để phủ vùng click toàn Card.
  - CẤM `<a>` bọc toàn bộ Card (ví dụ CẤM: `<a href="..."><div><img/><h3/><p/></div></a>`).
  - 100% thẻ `<a>` / `<Link>` BẮT BUỘC có thuộc tính `title="..."` mô tả ngắn gọn đích đến.
  - Link ngoài site: `target="_blank" rel="noopener noreferrer"`.
- [ ] **B14 — Zero Dead Links & Ghost Anchors**:
  - CẤM tuyệt đối `href="#"`, `href=""`, `href="javascript:void(0)"`.
  - Mọi `<a>` phải trỏ tới URL thực tế có nội dung (HTTP 200).
  - Nếu element chỉ cần hành vi click (toggle, modal, tab) → dùng `<button>` thay vì `<a>`.

### Nhóm 5: Performance, Image & Core Web Vitals
- [ ] **B9 — Soft 404 Contract**: Slug/data rỗng → `notFound()` trả HTTP 404 thực sự. CẤM render UI lỗi kèm HTTP 200.
- [ ] **B10 — Image Pipeline & Format Enforcement**:
  - **Format bắt buộc**: 100% ảnh content/UI phải là **WebP** (hoặc AVIF). CẤM dùng PNG/JPG thô chưa convert. Khi dùng `generate_image` hoặc tool tạo ảnh → output PHẢI là WebP.
  - **Dimensions chống CLS**: 100% `<img>` khai báo đủ `width` + `height` (px thật). Dùng Next.js `<Image>` component với `sizes` prop cho responsive.
  - **Alt ngữ nghĩa**: 100% `<img>` có dynamic `alt` mô tả nội dung thực (CẤM `alt=""`, CẤM `alt="image"`, CẤM `alt="photo"`).
  - **LCP Hero**: Ảnh Above-the-fold: `fetchpriority="high"` + `loading="eager"` (BỎ `lazy`). Hoặc `<link rel="preload" as="image" href="..." fetchpriority="high">`.
  - **Nén dung lượng**: Ảnh content ≤ 80KB. OG Image 1200×630 ≤ 100KB.
- [ ] **B11 — Top Padding Clearance**: Container gốc có `pt-24 lg:pt-28` (hoặc `pt-20`) tránh Header fixed đè Breadcrumbs và H1.
- [ ] **B17 — Core Web Vitals Contract (FE Code PHẢI đạt)**:
  - **LCP < 2.5s**: Preload font + Hero image. Critical CSS inline hoặc tải đầu. CẤM lazy load ảnh Above-the-fold.
  - **CLS < 0.1**: Mọi `<img>`, `<video>`, `<iframe>` có `width`+`height` cố định. Font: `font-display: swap`. Skeleton loader cho async content. CẤM inject DOM gây nhảy layout sau khi paint.
  - **INP < 200ms**: Event handlers nặng phải `debounce` / `requestAnimationFrame` / React `startTransition`. CẤM `onClick` chạy sync > 100ms.
  - **Resource Hints**: `<link rel="preconnect" href="https://fonts.googleapis.com">`, `<link rel="preconnect" href="https://api.domain.com">` cho mọi domain API client-side.
  - **Viewport**: `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">`. CẤM chặn zoom.
  - **Mobile Tap Targets**: Nút bấm, icon, card links tối thiểu `48×48px`, cách nhau ≥ `8px`.

### Nhóm 6: Brand Assets & Logo
- [ ] **B18 — Logo & Favicon Standards**:
  - **Logo Icon**: Phải dạng **icon không nền (transparent background)**, viền đầy đủ (full stroke/outline). Format ưu tiên **SVG** (vector, scale vô hạn). Nếu raster: WebP/PNG transparent.
  - **Logo Size**: Nén tối ưu ≤ 30KB. Kích thước tối thiểu 100×100px, tối đa 512×512px.
  - **Bộ Favicon đầy đủ** trong `public/`:
    - `favicon.ico` (multi-resolution 16×16, 32×32, 48×48)
    - `favicon-16x16.png` & `favicon-32x32.png` (< 2KB)
    - `apple-touch-icon.png` (180×180px, < 15KB)
    - `site.webmanifest` (khai báo `name`, `short_name`, `icons` [192×192, 512×512], `theme_color`, `background_color`, `display: standalone`)

### Nhóm 7: pSEO Navigation & Search
- [ ] **B15 — Dynamic Navigation Priority (Header & Footer)**:
  - Menu Header và Footer CẤM hardcode tĩnh. BẮT BUỘC render từ data source (Silo Map config / DB).
  - Thứ tự menu: **Tier 1 (Pillar Hubs)** hiển thị trước → **Tier 2 (Top Silos)** → Tier 3 chỉ ở Footer/Mega Menu.
  - Footer: Sitemap Links phân nhóm theo Silo Category + Legal Pages (Privacy, Terms).
  - Header chính: Tối đa 6-8 mục cấp 1 (UX Navigation Rule).
- [ ] **B16 — Silo-Aware Live Search**:
  - Ô search BẮT BUỘC là Live Search có Autocomplete/Suggest khi gõ (debounce ~300ms).
  - Kết quả suggest phân nhóm theo Pillar/Silo Category (ví dụ: nhóm "Dịch vụ", nhóm "Khu vực", nhóm "Blog").
  - BẮT BUỘC có Schema `SearchAction` (Sitelinks Search Box) trên trang chủ.
  - Trang kết quả search (`/search?q=...`): meta `noindex` để bảo vệ Crawl Budget.
- [ ] **B19 — SSR Content & Font Optimization**:
  - 100% nội dung cốt lõi (text, heading, link, ảnh) render từ Server (SSR/SSG). CẤM fetch nội dung chính qua Client-side CSR gây Soft 404 cho Googlebot.
  - Font: Dùng Google Fonts / Self-hosted với `font-display: swap`. Preconnect `fonts.googleapis.com` + `fonts.gstatic.com`. Subset font (latin, vietnamese) để giảm payload.

---

## C. QA AUDIT — Severity Scoring

| Hạng mục vi phạm | Severity | Điểm trừ |
|---|---|---|
| B1, B2, B3, B5, B6, B9 (URL/Content/Schema) | 🔴 Critical | -10đ/lỗi |
| B4, B8 (GEO/FAQ thiếu) | 🔴 Critical | -10đ/lỗi |
| B13 (`<a>` thiếu title / bọc block), B14 (Dead Links `href="#"`) | 🔴 Critical | -10đ/lỗi |
| B17 (CWV vi phạm: LCP > 2.5s / CLS > 0.1 / INP > 200ms) | 🔴 Critical | -10đ/lỗi |
| B10 (Ảnh PNG/JPG thô chưa convert WebP / thiếu alt / thiếu dimensions) | 🔴 Critical | -10đ/lỗi |
| B18 (Logo không đạt chuẩn / thiếu favicon set) | 🟡 Warning | -5đ/lỗi |
| B7 (thiếu Internal Links) | 🟡 Warning | -3đ/lỗi |
| B11, B12, B15, B16, B19 | 🟡 Warning | -3đ/lỗi |
| A1, A2 (thiếu Keyword / Cannibalization) | 🔴 Critical | -15đ/lỗi |
| **Score ≥ 80 → ✅ PASS** | **Score < 80 → ❌ BLOCK DEPLOY** | |
