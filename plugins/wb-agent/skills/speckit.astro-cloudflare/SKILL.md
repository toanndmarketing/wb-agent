---
name: speckit.astro-cloudflare
description: Astro + Cloudflare + D1 SEO & GEO Blueprint Standard (Mẫu chuẩn khởi tạo dự án)
---

# 🚀 THE ULTIMATE BLUEPRINT: ASTRO + CLOUDFLARE + D1 (SEO & GEO STANDARD)

**Phiên bản:** 1.0 (Dành cho việc nhân bản & audit các dự án mới)
**Tech Stack:** Astro 5, Cloudflare Pages, Cloudflare D1 (SQLite), Drizzle ORM, TailwindCSS.

Tài liệu này là quy chuẩn tối thượng để xây dựng một website vệ tinh, affiliate, hoặc blog đạt điểm tuyệt đối 100/100 Technical SEO và tối ưu hóa cho AI Search (GEO - Generative Engine Optimization).

---

## 🏗️ 1. INFRASTRUCTURE & ARCHITECTURE

- **No Docker Policy**: Tận dụng 100% sức mạnh Serverless của Cloudflare. Chạy trực tiếp qua Node.js (`npm run dev`) kết hợp Wrangler CLI.
- **Drizzle ORM & D1**: Dữ liệu lưu trữ phân tán tại Edge (Cloudflare D1). Schema phải được quy hoạch chặt chẽ, tối ưu index cho các cột lookup (slug, category_id).
- **Môi trường (ENV)**: 
  - Không hard-code cấu hình, API keys, URLs.
  - Phải có file `.env.example`. Check `Astro.locals.runtime.env` an toàn để truy cập biến môi trường D1 trong các logic server-side.

---

## 🔍 2. ON-PAGE SEO & TECHNICAL CONFIG

### 2.1 Cấu hình Lõi (Core Config)
- **Trailing Slash Uniformity & SSR Middleware 301 Redirect**: 
  - Bắt buộc khai báo `trailingSlash: 'always'` trong file `astro.config.mjs`.
  - **Astro SSR 301 Redirect Middleware (`src/middleware.ts`)**: Trong chế độ SSR (`output: 'server'`), bắt buộc tạo file `src/middleware.ts` bằng `defineMiddleware` để phát hiện mọi truy vấn trang thiếu dấu `/` ở cuối (loại trừ static files, extensions, `/_astro/`, `/api/`) và thực hiện **HTTP 301 Moved Permanently** redirect về URL có slash (VD: `/tool/claude-ai` -> `HTTP 301` -> `/tool/claude-ai/`).
  - Mọi hàm sinh `canonical` hay link nội bộ đều phải bảo vệ/ép dấu `/` ở cuối (VD: `https://domain.com/path/`). Tuyệt đối không để xảy ra rủi ro 308 Redirect Loop.
- **Canonical URL**: Thẻ `<link rel="canonical">` phải tự động trỏ chuẩn xác 100% đến URL hiện tại, đồng bộ hoàn toàn với sitemap.
- **Auto-Noindex**: Nếu bài viết/trang có nội dung nghèo nàn (< 200 chữ hoặc dữ liệu trống), bắt buộc tự động chèn `<meta name="robots" content="noindex, nofollow">` để bảo vệ Crawl Budget.

### 2.2 Schema Markup (JSON-LD 100%)
- **Tuyệt đối cấm dùng Microdata** (`itemscope`, `itemprop`) trên HTML thô. 
- Mọi dữ liệu có cấu trúc phải được khai báo dạng **JSON-LD** truyền thẳng vào `<head>` của `BaseLayout.astro`.
- **Cấu trúc bắt buộc**:
  - Mọi trang con: `BreadcrumbList`.
  - Trang chủ: `WebSite` / `Organization`.
  - Trang công cụ/sản phẩm: `SoftwareApplication` / `Product` kèm `AggregateRating`.
  - Trang blog: `Article` / `BlogPosting`.
  - Trang review/so sánh: `FAQPage` nếu có mục hỏi đáp.

### 2.3 Hiệu năng (Core Web Vitals)
- Ảnh banner/hero: Dùng `<img fetchpriority="high">` và loại bỏ lazy load.
- Resource Hints: Sử dụng `<ClientRouter />` của Astro để chuyển trang SPA mượt mà không load lại trang.

---

## 🤖 3. GEO (GENERATIVE ENGINE OPTIMIZATION) - CHUẨN AI SEARCH

Để ChatGPT Search, Gemini, Perplexity cào và ưu tiên website của bạn, bắt buộc áp dụng:

1. **Direct Answer Box (Lead with the answer)**
   - Đầu mỗi bài viết (dưới H1) phải có 1 block (VD class `geo-direct-answer`) chứa 2-3 câu tóm tắt nội dung/câu trả lời trực diện.
   - Bôi đậm (`<strong>`) tên thực thể/từ khóa chính.
2. **LLM Seeding Table (Data Structuring)**
   - AI cực kỳ thích đọc bảng. Mọi bài đánh giá, so sánh bắt buộc có thẻ `<table>` HTML tổng hợp dữ liệu (Giá cả, Gói cước "Sweet Spot", Ưu/Nhược điểm).
3. **Anti-Hallucination & Quotable Statements**
   - Viết các câu phát biểu dứt khoát, dùng số liệu thật, không úp mở để AI dễ lấy làm trích dẫn (Citation).

---

## 🕸️ 4. CẤU TRÚC PILLAR - SILO - LINK JUICE

Đây là mạch máu của dự án, quyết định sức mạnh On-site SEO:

### 4.1 Internal Link Strict Rules
- **100% Dofollow**: Không dùng `rel="nofollow"` cho link nội bộ.
- **3-Click Rule**: Bất kỳ trang nào cũng phải được tìm thấy tối đa sau 3 click từ Homepage.
- **No Query Parameters**: Tuyệt đối không dùng URL dạng `?category=seo` để filter. Mọi truy vấn phải đẩy ra URL ảo (Pretty URLs) dạng `/seo/` (Dùng kỹ thuật SSG/SSR dynamic routes của Astro).
- **First Occurrence Only**: Mỗi bài viết chỉ chèn 1 internal link duy nhất vào 1 trang đích ở lần xuất hiện từ khóa đầu tiên.

### 4.2 Kỹ thuật "BoxLinkJuice" (Accordion Silo)
Thay vì chèn một khối text link spam hàng dọc, bắt buộc chia thành 4 trụ cột (Pillars) thông qua thẻ `<details>` và `<summary>` (Accordion HTML) để tiết kiệm diện tích UI nhưng Googlebot vẫn cào được:
1. **Pillar 1 (Tool Intent)**: Review, Coupon, Alternative, Is-it-legit của chính Tool đó.
2. **Pillar 2 (Head-to-Head)**: Các link so sánh "A vs B" trực diện.
3. **Pillar 3 (Peers)**: Top các tool cùng ngách/danh mục.
4. **Pillar 4 (Directories)**: Link trỏ ngược lên trang cha (Category/Silo gốc).

*UI Note:* Tuyệt đối KHÔNG hiển thị thuật ngữ kỹ thuật như *"Internal Silo"* lên frontend, hãy dùng ngôn ngữ user (VD: *"Explore Alternatives"*).

---

## 🗺️ 5. SITEMAP ARCHITECTURE (PSEO STANDARD)

Kiến trúc dành cho website hàng ngàn đến hàng triệu URL (Programmatic SEO):
- **Không gom tất cả vào 1 file `sitemap.xml` duy nhất.**
- Dùng tính năng API Route (`.xml.ts`) của Astro để sinh Dynamic Sitemaps.
- **Sitemap Index (`/sitemap.xml`)**: Đóng vai trò là file Mẹ, trỏ tới các file con.
- **Sitemaps con phân lập theo Silo**:
  - `/sitemap/main.xml` (Trang chủ, Terms, Policy, Contact...)
  - `/sitemap/categories.xml` (Danh mục)
  - `/sitemap/tools.xml` (Chi tiết công cụ)
  - `/sitemap/reviews.xml` (Bài blog review)
  - `/sitemap/comparisons.xml` (So sánh A vs B)
- **Lợi ích**: Giúp theo dõi báo cáo Index Coverage trên Google Search Console theo từng cụm, khoanh vùng được ngách nào đang bị Google làm lơ để khắc phục.

---

## 🛡️ 6. DEEP TECH CHECKPOINTS (CHỐT CHẶN KỸ THUẬT SÂU)

Để ngăn chặn "Tech Debt" và đảm bảo SEO Code ở mức hoàn hảo, quy trình Dev & QA bắt buộc tuân thủ 4 chốt chặn sau:

1. **Zod Validation (Chống rác Metadata)**: Trong `src/content/config.ts`, MỌI schema của Collections đều phải set `seoTitle`, `seoDescription`, `targetKeyword` là **Required**. Nếu file MDX/Markdown thiếu các trường này, Astro Build phải trả về `Build Failed`. Không nhân nhượng với dữ liệu rác.
2. **Asset Management & CLS (Chống tải chậm)**: Nghiêm cấm sử dụng thẻ `<img>` thô. 100% hình ảnh phải đi qua `<Image />` component của Astro hoặc Cloudflare Image Resizing (tự động convert WebP/AVIF). Mọi hình ảnh phải bị ép khai báo `width` và `height` để ngăn ngừa CLS (Cumulative Layout Shift).
3. **Strict Islands Hydration (Chống phình to JS)**: Nghiêm cấm lạm dụng `client:load` cho các component React/Vue/Svelte trong Astro. Ưu tiên `client:visible` (chỉ load khi scroll tới) và `client:idle` (load khi rảnh rỗi).
4. **Schema Validator & Staging Gate**: 
   - Mã JSON-LD sinh ra phải vượt qua Schema Validator Script để check tính hợp lệ của cú pháp.
   - BẮT BUỘC deploy lên Cloudflare Preview (Staging) trước. Agent QA phải chạy Audit trên URL Staging, đạt SEO Score > 90 mới được Merge & Deploy lên Production. Đề phòng lỗi Edge Function runtime.

---

## 🛠️ 7. QUICK AUDIT CHECKLIST CHO DỰ ÁN MỚI
- [ ] `astro.config.mjs` có `trailingSlash: 'always'` chưa?
- [ ] Đã tạo `src/middleware.ts` ép trả về HTTP 301 Moved Permanently Redirect cho các truy vấn thiếu trailing slash chưa?
- [ ] Mọi thẻ form, đặc biệt form tìm kiếm (`<form action="...">`), có trỏ đích kết thúc bằng dấu `/` chưa (VD: `action="/search/"`) để chặn đứng lỗi 308 Redirect Loop?
- [ ] Đã khai báo Schema `SearchAction` (Sitelinks Search Box) độc quyền tại Trang Chủ (`index.astro`) chưa?
- [ ] Trang kết quả tìm kiếm (`search.astro`) đã dùng đúng Schema `@type: "SearchResultsPage"` thay vì WebSite chưa?
- [ ] Truy cập `/test` và `/test/`, canonical URL có đồng nhất về `/test/` chưa?
- [ ] View source trang chi tiết: Có thẻ `<script type="application/ld+json">` chứa `SoftwareApplication` không? Có bị dính `itemscope` trên HTML thô không?
- [ ] Thẻ `H1` -> `H2` -> `H3` có theo đúng trật tự không? Có bị nhảy cóc không?
- [ ] Trang có Direct Answer Box và Table Pricing cho AI cào không?
- [ ] Có URL nào bị lỗi 404/500 nhưng không thiết lập HTTP status code đúng chuẩn trong SSR không?
- [ ] Các trang < 200 chữ có auto sinh thẻ `noindex` không?
