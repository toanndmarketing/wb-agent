---
name: speckit.seo-technical
description: Technical SEO Audit, Canonicalization Signals, Core Web Vitals, JSON-LD Schema, Crawlability & Local Tunneling Debugging theo chuẩn Google Search Central 2026
---

## 🎯 Mission
Đảm bảo mọi trang web công khai đạt chuẩn Technical SEO vượt trội, tối ưu hóa CTR, giữ chân người dùng và sẵn sàng cho AI Search (GEO / SGE - Google Search Central 2026 Standard). Đạt chuẩn Helpful Content (độc nhất, văn phong chuyên gia E-E-A-T, không bị đánh dấu là AI-generated).

**🚀 Triết lý SEO-as-Code (Quyền sở hữu của Dev Team):** 
Technical SEO (HTML Semantic, Core Web Vitals, Canonical Signals, Schema JSON-LD, SSR...) KHÔNG PHẢI là công việc "làm sau khi code xong" của SEO Team, mà là **tiêu chuẩn bắt buộc của Dev Team (Front-End/Full-stack)**. Mọi subagent khi code giao diện (đặc biệt là skill `speckit.implement`) BẮT BUỘC phải tuân thủ nghiêm ngặt file SKILL này ngay từ giai đoạn đúc Component/Layout. Team SEO chỉ đóng vai trò Auditor & Content Strategist.

## 🧩 Specialized Sub-Skills Architecture (Tránh Trùng Lặp & Nặng Context)
Để tránh nặng context khi làm việc trực tiếp với codebase website, kiến thức SEO đã được bóc tách thành 3 Skill chuyên biệt theo đúng giai đoạn:
1. **`speckit.seo-strategy`**: Dùng ở giai đoạn Khởi tạo Dự án — Chọn Domain, TLD Neutrality, Audit Domain cũ (Search Console Manual Actions & Expired Domain Abuse), Phân tích Niche/Mảng làm, 301 Multi-Domain Consolidation.
2. **`speckit.seo-content`**: Dùng ở giai đoạn Lập Chiến lược Content — Phân tích Từ khóa, Mapping Search Intent, Cấu trúc Silo/Pillar/Cluster, Tối ưu Title Link & Control Snippets (`max-snippet`, `data-nosnippet`).
3. **`speckit.seo-technical`** *(Skill này)*: Dùng ở giai đoạn Lập trình & Audit Website — Tập trung thuần túy vào Technical SEO, HTML Semantic, Canonical Signals, Core Web Vitals, JSON-LD Schema, Link Juice, Crawlability & Local Tunneling Debugging.

---

## 📥 Input
- Source code (pages, layouts, components, content files)
- `.agents/knowledge/seo_standards.md` (nếu có)

---

## 📋 Protocol

### Phase 1: Canonicalization & Multi-Signal Consolidation (Google Canonical Guide)
Google xác định Canonical URL dựa trên sự tổng hợp của nhiều tín hiệu kỹ thuật. Dev Team BẮT BUỘC phải đồng bộ 100% các tín hiệu này để tránh lỗi "Duplicate content without user-selected canonical" trên GSC:
1. **Cấu hình Thẻ Canonical HTML & HTTP Headers**:
   - Mọi trang công khai BẮT BUỘC có đúng 1 thẻ `<link rel="canonical" href="https://domain.com/path/">` nằm trong `<head>`.
   - **File tĩnh/PDF:** Đối với file PDF hoặc hình ảnh tĩnh, BẮT BUỘC gửi HTTP Response Header: `Link: <https://domain.com/downloads/file.pdf>; rel="canonical"`.
   - **Absolute URLs Only:** 100% URL trong thẻ canonical phải là **Absolute URL** chứa đầy đủ giao thức `https://` và domain chính. Tuyệt đối CẤM dùng Relative URL (`/path/`).
2. **Đồng bộ Tín hiệu Trailing Slash & Self-Canonical**:
   - Khi hệ thống bật `trailingSlash: true` (Next.js/Astro), tất cả thẻ `canonical`, `og:url`, `sitemap.xml`, thẻ Schema và `<a href="...">` PHẢI ĐỒNG BỘ 100% có dấu `/` ở cuối (`https://domain.com/silo/page/`).
   - Nếu canonical thiếu `/` khiến Googlebot nhận HTTP 308 Redirect, Google sẽ báo lỗi "Canonical points to a redirect target".
3. **Pagination Canonical Strategy (Chuẩn 2026)**:
   - Google đã deprecated `rel="prev/next"`. Các trang từ trang 2 trở đi (`/page/2/`, `/page/3/`...):
     - **Canonical phải Self-Referencing** — Trỏ về chính URL của trang đó (KHÔNG trỏ ngược về trang 1).
     - **Title & Meta Description phải UNIQUE** — Bắt buộc kèm số trang: `[Từ khóa] - Trang [X] | [Brand]`.

### Phase 2: Crawlability vs Indexability Rules (Google Robots & Indexing)
1. **Phân biệt Rạch ròi Crawlability vs Indexability**:
   - **`robots.txt`**: Kiểm soát **Crawlability (Khả năng cào)**. Nếu trang bị block trong `robots.txt`, Googlebot sẽ KHÔNG cào trang đó, nhưng trang **VẪN CÓ THỂ BỊ INDEX** nếu có external link trỏ về (hiển thị không có snippet).
   - **`<meta name="robots" content="noindex">`**: Kiểm soát **Indexability (Khả năng lập chỉ mục)**. Muốn Google nhận thẻ `noindex` để xóa trang khỏi SERP, trang **BẮT BUỘC PHẢI KHÔNG BỊ BLOCK TRONG ROBOTS.TXT** để Googlebot cào và đọc thẻ `noindex`.
2. **Resource Hints (Preconnect & Preload)**:
   - Ảnh LCP Hero màn hình đầu tiên BẮT BUỘC dùng `<link rel="preload" as="image" href="..." fetchpriority="high">`.
   - Khai báo `<link rel="preconnect" href="https://api.domain.com">` cho các domain API Client-side để giảm TTFB.
3. **Prevent Soft 404 in SSR (Chống Soft 404)**:
   - Trong các trang SSR (Next.js, Astro SSR), khi dữ liệu rỗng hoặc Slug/ID không tồn tại, Server BẮT BUỘC trả về HTTP Status Code `404 Not Found` (dùng `notFound: true` hoặc `return Astro.rewrite('/404')`).
   - Tuyệt đối CẤM trả về HTTP 200 OK kèm giao diện 404 UI vì Googlebot sẽ phạt hàng loạt lỗi Soft 404 trên GSC.

### Phase 3: Structured Data (JSON-LD) & Machine Readability
1. **Quy chuẩn JSON-LD Tách Rời**:
   - 100% Structured Data BẮT BUỘC viết trong thẻ `<script type="application/ld+json">`.
   - 🛑 **CẤM Microdata/RDFa**: Tuyệt đối không nhúng attributes thô (`itemscope`, `itemprop`) vào thẻ HTML vì làm cồng kềnh DOM.
2. **Các Schema Bắt Buộc theo Cấp Trang**:
   - **Trang chủ (`/`):** Organization / WebSite / LocalBusiness Schema với logo, sameAs social links.
   - **Trang FAQ (`/faq`):** FAQPage Schema khớp 100% văn bản hiển thị trên màn hình.
   - **Trang Bài viết (`/blog/[slug]`):** BlogPosting / Article Schema chứa `author` (với `sameAs` LinkedIn), `datePublished`, `dateModified` (ISO-8601).
   - **Breadcrumb:** BreadcrumbList trên mọi trang con, khớp 100% với cấp HTML Breadcrumb.
3. **Absolute URLs trong Schema**:
   - Tất cả thuộc tính `image`, `logo`, `url`, `item` trong JSON-LD BẮT BUỘC 100% phải là Absolute URL (`https://...`).

### Phase 4: Core Web Vitals, Mobile UX & Image Optimization
1. **Core Web Vitals Benchmarks (Bắt buộc)**:
   - **LCP (Largest Contentful Paint)** < 2.5s
   - **INP (Interaction to Next Paint)** < 200ms
   - **CLS (Cumulative Layout Shift)** < 0.1
2. **Images — Chống CLS (BẮT BUỘC)**:
   - Tất cả thẻ `<img>` PHẢI khai báo đầy đủ cả 3: `width`, `height` (px thật), và `loading="lazy"`.
   - Ảnh Hero màn hình đầu tiên (Above-the-fold) BẮT BUỘC dùng `fetchpriority="high"` và BỎ `loading="lazy"`.
   - Sử dụng định dạng WebP/AVIF hiện đại.
3. **Mobile Tap Targets & Viewport**:
   - Viewport meta CẤM chặn zoom: `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">`.
   - Nút bấm, Icon Social, Card Links trên mobile BẮT BUỘC có kích thước tối thiểu `48x48px` và cách nhau ít nhất `8px` để khắc phục lỗi GSC "Clickable elements too close together".

### Phase 5: Link Juice Flow & Silo Internal Linking Rules
1. **Dofollow Internal Link Rule**: 100% liên kết nội bộ KHÔNG chứa `rel="nofollow"`.
2. **Pure Silo Pretty URLs**: 100% link nội bộ không dùng query parameter (`?cate=1`). Bắt buộc dùng URL đẹp (`/category/item/`).
3. **Pure Anchor Text for Card Components**:
   - 🛑 **CẤM** dùng thẻ `<a>` bọc toàn bộ thẻ Card (gồm ảnh, tiêu đề, mô tả dài).
   - **Bắt buộc dùng Pseudo-element link trick**: Thẻ `<a>` chỉ bọc đúng tiêu đề H2/H3, kết hợp CSS class `after:absolute after:inset-0` để mở rộng vùng click ra toàn bộ Card mà vẫn giữ Anchor Text tinh khiết.
4. **Giới hạn 3-Click**: Mọi trang đích đều có thể truy cập từ trang chủ trong ≤3 clicks.

### Phase 6: Local / Staging Debugging Protocol (Google Debugging Guide)
1. **Testing Localhost via Ngrok Tunnel**:
   - Khi cần test Rich Results, Structured Data hoặc URL Inspection cho ứng dụng đang chạy ở localhost/staging trước khi release:
   - Chạy local server (VD port 8980), mở ngrok tunnel:
     `./ngrok http 8980 --request-header-add ngrok-skip-browser-warning:1`
   - Dán URL ngrok công khai (`https://xxxx.ngrok.io`) vào **Google Rich Results Test** để kiểm tra real-time.
   - Đảm bảo ngrok không tự sinh file `robots.txt` chặn Googlebot.
2. **GSC Error Delay Awareness**:
   - Nhớ rằng Search Console sẽ KHÔNG xóa lỗi ngay lập tức sau khi deploy fix code. Lỗi sẽ tiếp tục hiển thị cho đến khi Googlebot cào lại trang (vài ngày). Dùng **URL Inspection Tool** để gửi yêu cầu recrawl khẩn cấp.

### Phase 7: Automated SEO Audit Crawler
1. **Chạy SEO Crawler**: Chạy script `seo-audit-crawler.js` nằm trong thư mục `.agents/skills/`:
   `node .agents/skills/seo-audit-crawler.js <URL>` (ví dụ: `http://localhost:8980` hoặc `http://web:80`).
2. **Review kết quả**: Sửa mọi lỗi 🔴 Critical và tối ưu hóa các cảnh báo 🟡 Warning để đạt điểm SEO ≥ 90/100 trước khi hoàn thành task.

---

## 📤 Output
- File: `.agents/specs/seo-audit-report.md` (tạo bởi crawler) hoặc `.agents/specs/seo-technical-report.md`.
- Verdict: Score 0-100, danh sách lỗi 🔴 Critical, 🟡 Warning, 🟢 Info và giải pháp fix.
