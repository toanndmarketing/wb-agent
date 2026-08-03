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

### Phase 0: 🚨 MANDATORY Deep Context Scan & Anti-Surface-Fix Protocol ⭐
1. **Deep Context Scan (Nạp Sâu Context & Báo cáo Audit SEO/Architecture)**:
   - TRƯỚC KHI tiến hành audit, fix bug hay tư vấn technical SEO, BẮT BUỘC dùng `list_dir` / `view_file` rà soát toàn bộ các file Báo cáo Audit SEO gần nhất (`seo_*.md`, `seo-audit-report.md`), tài liệu workflow dự án (ví dụ `12-seo-geo.md`), spec kiến trúc sitemap index, router structure, và `master-identity.md`.
   - TUYỆT ĐỐI KHÔNG đọc lướt rồi suy diễn hoặc dựa vào 1 file thô lẻ loi.
2. **Anti-Surface Fix Protocol (Chống Sửa Nông / Sửa Triệu Chứng Bề Nổi)**:
   - CẤM chỉ fix bề nổi trước mắt (ví dụ: thấy sitemap bị lỗi port hay cache thì chỉ sửa tạm mà quên kiểm tra kiến trúc Sitemap Index bắt buộc trong tài liệu dự án).
   - Mọi thay đổi Technical SEO (Sitemap Index vs Single Sitemap, Canonical, Schema, Robots) BẮT BUỘC phải khớp 100% với Kiến trúc Quy chuẩn & Audit Reports của dự án. Nếu phát hiện code đang vi phạm kiến trúc quy chuẩn (ví dụ sitemap monolithic thay vì Sitemap Index), BẮT BUỘC phải refactor theo đúng kiến trúc chuẩn.

### Phase 1: Canonicalization & Multi-Signal Consolidation (Google Canonical Guide)
Google xác định Canonical URL dựa trên sự tổng hợp của nhiều tín hiệu kỹ thuật. Dev Team BẮT BUỘC phải đồng bộ 100% các tín hiệu này để tránh lỗi "Duplicate content without user-selected canonical" trên GSC:
1. **Cấu hình Thẻ Canonical HTML & HTTP Headers**:
   - Mọi trang công khai (Index, Hub, Detail, Sub-silos, Articles) BẮT BUỘC có đúng 1 thẻ `<link rel="canonical" href="{BASE_URL}{PATH}">` nằm trong `<head>` (Sử dụng `alternates: { canonical: ... }` trong Next.js/Astro metadata).
   - **File tĩnh/PDF:** Đối với file PDF hoặc hình ảnh tĩnh, BẮT BUỘC gửi HTTP Response Header: `Link: <{BASE_URL}{FILE_PATH}>; rel="canonical"`.
   - **Absolute URLs Only:** 100% URL trong thẻ canonical phải là **Absolute URL** chứa đầy đủ giao thức `https://` và domain chính. Tuyệt đối CẤM dùng Relative URL (`/path/`).
2. **Title Suffix Sanitation & Brand Formatting (Chống Trùng Lặp & Keyword Stuffing)**:
   - `SITE_NAME` và đuôi Brand Suffix trên Metadata Title BẮT BUỘC dùng tên dạng liền thương hiệu `LocalWeatherRadar` (hoặc `${SITE_NAME}` tương ứng `LocalWeatherRadar` / `LocalWeatherRadar.online`).
   - CẤM lặp từ khóa Brand tách rời (`Local Weather Radar`) ở đuôi title khi phần đầu title đã chứa các từ `Weather` hoặc `Radar`, tránh gây rác từ khóa (Keyword Stuffing, ví dụ: `... Weather Radar | Local Weather Radar`).
   - Khi cài đặt layout metadata template `%s | ${SITE_NAME}`, trong từng trang riêng lẻ BẮT BUỘC phải lọc bỏ (strip) các cụm từ trùng lặp ở đuôi (như `| Category Name`, `| Brand Name`) trước khi truyền title vào metadata để tránh tiêu đề bị lặp đuôi 2 lần (`Title | Brand | Brand`).
3. **Đồng bộ Tín hiệu Trailing Slash & Self-Canonical**:
   - Khi hệ thống bật `trailingSlash: true` (Next.js/Astro), tất cả thẻ `canonical`, `og:url`, `sitemap.xml`, thẻ Schema và `<a href="...">` PHẦI ĐỒNG BỘ 100% có dấu `/` ở cuối (`https://domain.com/silo/page/`).
   - Nếu canonical thiếu `/` khiến Googlebot nhận HTTP 308 Redirect, Google sẽ báo lỗi "Canonical points to a redirect target".
4. **Pagination Canonical Strategy (Chuẩn 2026)**:
   - Google đã deprecated `rel="prev/next"`. Các trang từ trang 2 trở đi (`/page/2/`, `/page/3/`...):
     - **Canonical phải Self-Referencing** — Trỏ về chính URL của trang đó (KHÔNG trỏ ngược về trang 1).
     - **Title & Meta Description phải UNIQUE** — Bắt buộc kèm số trang: `[Từ khóa] - Trang [X] | [Brand]`.
5. **Sitemap Clean URL Protocol (CRAWL BUDGET & CLEAN URL SPECIFICATION)**:
   - 100% tệp Sitemap Index (`/sitemap.xml`) CẤM TUYỆT ĐỐI việc hiển thị đường dẫn dạng API (`/api/sitemaps/...`) trong các thẻ `<loc>`.
   - Tất cả Sub-sitemaps trong `<loc>` BẮT BUỘC phải dùng đường dẫn tệp XML sạch chuẩn quốc tế (ví dụ: `/sitemap-static.xml`, `/sitemap-top.xml`, `/sitemap-apps-1.xml`, `/sitemap-alternative-1.xml`).
   - Trong Next.js/Astro, BẮT BUỘC cấu hình `rewrites()` trong file config (như `next.config.ts`) để map ngầm từ `/sitemap-:type-:chunk.xml` về route handler backend (`/api/sitemaps/:type/:chunk`).

### Phase 2: Crawlability vs Indexability Rules (Google Robots & Indexing)
1. **Phân biệt Rạch ròi Crawlability vs Indexability**:
   - **`robots.txt`**: Kiểm soát **Crawlability (Khả năng cào)**. Nếu trang bị block trong `robots.txt`, Googlebot sẽ KHÔNG cào trang đó, nhưng trang **VẪN CÓ THỂ BỊ INDEX** nếu có external link trỏ về (hiển thị không có snippet).
   - **`<meta name="robots" content="noindex">`**: Kiểm soát **Indexability (Khả năng lập chỉ mục)**. Muốn Google nhận thẻ `noindex` để xóa trang khỏi SERP, trang **BẮT BUỘC PHẢI KHÔNG BỊ BLOCK TRONG ROBOTS.TXT** để Googlebot cào và đọc thẻ `noindex`.
2. **Resource Hints (Preconnect & Preload)**:
   - Ảnh LCP Hero/Header màn hình đầu tiên BẮT BUỘC khai báo `fetchpriority="high"` (và bỏ `loading="lazy"`) hoặc dùng `<link rel="preload" as="image" href="..." fetchpriority="high">`.
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
4. **Quy chuẩn AggregateRating & Third-Party Reviews (Chuẩn Review Snippet)**:
   - **CẤM DÙNG DATA CRAWL TRONG SCHEMA**: Theo Google Review Snippet Guidelines, TUYỆT ĐỐI CẤM lấy điểm số hoặc bình luận crawl từ nền tảng thứ 3 (Google Maps, TripAdvisor, Yelp, Facebook, v.v.) để nhúng vào thuộc tính `AggregateRating` và mảng `Review` của LocalBusiness/Restaurant/Product Schema. Việc lạm dụng (fake organic reviews) sẽ dẫn đến hình phạt Manual Action.
   - **CHỈ DÙNG FIRST-PARTY DATA**: Các biến số `AggregateRating` và `Review` trong JSON-LD BẮT BUỘC CHỈ ĐƯỢC tính toán từ dữ liệu (Comments/Ratings) do người dùng đánh giá trực tiếp trên website nội bộ (First-party Database). 
   - **Xử lý UI so với Schema**: Nếu chưa có dữ liệu local, bắt buộc ẩn/bỏ trống thẻ `AggregateRating` trong Schema JSON-LD. Ngược lại ở phần giao diện màn hình (UI/UX), VẪN được phép hiển thị điểm Crawl bình thường (kèm logo nguồn) để phục vụ người dùng trải nghiệm nội dung.

### Phase 4: Core Web Vitals, Mobile UX & Image Optimization
1. **Core Web Vitals Benchmarks (Bắt buộc)**:
   - **LCP (Largest Contentful Paint)** < 2.5s
   - **INP (Interaction to Next Paint)** < 200ms
   - **CLS (Cumulative Layout Shift)** < 0.1
2. **Images — Chống CLS & LCP Delay (BẮT BUỘC)**:
   - Tất cả thẻ `<img>` PHẢI khai báo đầy đủ cả 3: `width`, `height` (px thật), và `loading="lazy"`.
   - Ảnh Hero/Logo Header màn hình đầu tiên (Above-the-fold) BẮT BUỘC dùng `fetchpriority="high"` (hoặc `fetchPriority="high"`) và BỎ `loading="lazy"`.
   - Sử dụng định dạng WebP/AVIF hiện đại.
3. **Mobile Tap Targets & Viewport**:
   - Viewport meta CẤM chặn zoom: `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">`.
   - Nút bấm, Icon Social, Card Links trên mobile BẮT BUỘC có kích thước tối thiểu `48x48px` và cách nhau ít nhất `8px` để khắc phục lỗi GSC "Clickable elements too close together".

### Phase 5: Link Juice Flow, Silo Internal Linking, URL Slug, Clean Link & FAQ Accordion Rules
1. **Dofollow Internal Link Rule**: 100% liên kết nội bộ KHÔNG chứa `rel="nofollow"`.
2. **Quy chuẩn Read-Rules-First, Clean Link Protocol, First Link Priority & Anti-Spam**:
   - **Bắt buộc đọc luật trước khi code module mới**: Mọi Subagent/Developer khi code thêm trang hoặc UI component BẮT BUỘC phải đọc và tuân thủ quy chuẩn điều hướng link.
   - **Cấm Self-Referencing Links (Link trỏ trùng 100% URL trang hiện tại)**: Tuyệt đối CẤM chèn thẻ `<Link>` hoặc `<a href="...">` trỏ về chính URL trang hiện tại (VD: Trang chủ `/` không được chứa thẻ `<a href="/">` trong đoạn văn body text; Trang chi tiết bài viết/sản phẩm không được bọc link về chính URL trang đó).
   - **Cấm Duplicate Links Trong 1 Container/Card**: Mỗi URL đích chỉ được bọc link DUY NHẤT 1 lần trong mỗi khối card/container. Cấm vừa bọc thẻ Link ở Tiêu đề card, vừa bọc thẻ Link ở nút button bên trong cùng 1 card.
   - **First Link Priority (Khắc phục Trùng Link Trang Chủ)**: Trong khu vực Header, Logo là liên kết DUY NHẤT trỏ về Trang chủ (`href="/"`). Nút CTA phải trỏ sang anchor widget (`/#section-id`) hoặc trang Hub/Category tương ứng.
   - **Cấm Nhồi Thẻ Title & HTML Bloat**: TUYỆT ĐỐI KHÔNG chèn thuộc tính `title="..."` dài dòng / nhồi nhét câu văn từ khóa rác trên các thẻ `<a>` / `<Link>`.
   - **Breadcrumb Terminal Element**: Phần tử cuối cùng trong thanh Breadcrumbs biểu thị trang hiện tại BẮT BUỘC dùng thẻ `<span>` (`aria-current="page"`), TUYỆT ĐỐI CẤM bọc thẻ `<Link>`.
3. **Quy chuẩn Visual FAQ Accordion**:
   - Mọi trang rendering phần FAQ (`FAQPage` Schema) BẮT BUỘC dùng component chuẩn Accordion (có hiệu ứng đóng/mở mượt qua Framer Motion / CSS State).
   - CẤM HARDCODE UI TĨNH: Tuyệt đối CẤM tự viết block FAQ bằng thẻ HTML/Tailwind ad-hoc (như background tĩnh, text phẳng hiển thị 100% không đóng/mở được).
4. **Global Slug & URL Optimization Rule (Chuẩn Đa Ngôn Ngữ i18n)**: 
   - **Pretty URLs**: 100% link nội bộ không dùng query parameter (`?cate=1`). Bắt buộc dùng URL đẹp (`/category/item/slug/`).
   - **Định dạng Kebab-case**: Slug BẮT BUỘC viết thường (lowercase) và phân tách từ bằng dấu gạch ngang (`-`). Cấm dùng gạch dưới (`_`) hay viết liền.
   - **Xử lý Đa ngôn ngữ (Non-Latin & Latin)**: 
     - *Với hệ Latin (Anh, Việt...)*: Loại bỏ hoàn toàn dấu (diacritics), chuyển về ký tự cơ bản.
     - *Với hệ Non-Latin (Nhật, Thái, Ả Rập, Trung...)*: Ưu tiên giữ nguyên ký tự bản địa (UTF-8 URL-encoded). BẮT BUỘC loại bỏ emoji và dấu câu.
   - **Độ dài & Stopwords**: Giới hạn tối đa 60 ký tự hoặc tập trung vào 3-5 từ khóa cốt lõi.
   - **301 Redirect Protection**: Cập nhật Slug bài viết/sản phẩm đã publish BẮT BUỘC phải Redirect 301 từ URL cũ sang URL mới.
5. **Pure Anchor Text for Card Components**:
   - 🛑 **CẤM** dùng thẻ `<a>` bọc toàn bộ thẻ Card (gồm ảnh, tiêu đề, mô tả dài).
   - **Bắt buộc dùng Pseudo-element link trick**: Thẻ `<a>` chỉ bọc đúng tiêu đề H2/H3, kết hợp CSS class `after:absolute after:inset-0` để mở rộng vùng click ra toàn bộ Card mà vẫn giữ Anchor Text tinh khiết.
6. **Giới hạn 3-Click**: Mọi trang đích đều có thể truy cập từ trang chủ trong ≤3 clicks.
7. **BỘ 9 QUY TẮC CHỦ ĐỘNG ONPAGE & GEO BẮT BUỘC KHI TẠO/SỬA MỌI ROUTE/PILLAR**:
   > 📋 **Bản gọn (Compact Checklist)** đã được merge vào [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md). Phần dưới đây là **Deep Reference** chỉ cần đọc khi tra cứu lý do chi tiết.

   Mọi Agent/Developer khi khởi tạo hoặc chỉnh sửa bất kỳ Route/Page nào BẮT BUỘC phải thực thi ĐẦY ĐỦ 9 hạng mục Onpage & GEO sau ngay từ lần code đầu tiên:
   - ① **Top Padding Clearance**: Container gốc luôn có `pt-24 lg:pt-28` (hoặc `pt-20`) tránh bị Header fixed đè lấp Breadcrumbs và H1.
   - ② **Full Metadata & Canonical**: Khai báo đủ `title`, `description`, `alternates.canonical`, và `openGraph` (title, description, url, siteName, type).
   - ③ **Single H1**: Đúng 1 thẻ `<h1>` duy nhất mỗi trang, phân cấp `<h2>`, `<h3>` chuẩn.
   - ④ **CONSOLIDATED GEO DIRECT ANSWER HERO**: BẮT BUỘC hợp nhất đoạn mô tả chính dưới H1 vào làm CHÍNH khung `<GeoDirectAnswer html="..." />`. CẤM tách rời 1 đoạn `<p>` thô rồi lại chèn thêm 1 box GEO trùng lặp gây rác UI và tốn diện tích.
   - ⑤ **Visual FAQ Accordion**: BẮT BUỘC chèn component `<FAQSection title="..." faqs={...} />`. CẤM tạo Schema FAQPage mà bỏ quên giao diện UI.
   - ⑥ **Bộ 3 Schema.org JSON-LD**: Nhúng script JSON-LD cho `@type: "WebPage"`, `@type: "BreadcrumbList"`, và `@type: "FAQPage"`.
   - ⑦ **Breadcrumb Terminal Span**: Phần tử cuối Breadcrumb biểu thị trang hiện tại BẮT BUỘC dùng thẻ `<span>` (`aria-current="page"`), CẤM dùng link tự thân.
   - ⑧ **Link Title & Target**: Thẻ Link/Menu BẮT BUỘC có `title="..."` rõ ràng. Link chuyển Layer trên Widget mở new tab (`target="_blank" rel="noopener noreferrer"`).
   - ⑨ **PURE ANCHOR TEXT & PSEUDO-ELEMENT OVERLAY**: CẤM dùng thẻ `<Link>` / `<a>` làm khung bọc ngoài toàn bộ Card chứa nhiều thẻ `<div>`. Thẻ `<Link>` CHỈ bọc đúng duy nhất tiêu đề H2/H3 hoặc tên địa danh, kết hợp CSS `after:absolute after:inset-0 after:z-20` để phủ vùng click toàn bộ Card.

### Phase 6: Global i18n, RTL & SSR Strictness Rules
1. **Kiến trúc URL Quốc Tế & Hreflang (Bidirectional Protocol)**:
   - Dùng Sub-directory (/en/, /ar/). Tuyệt đối không dùng URL Parameter.
   - Mọi trang công khai BẮT BUỘC phải khai báo <link rel="alternate" hreflang="xx-XX" href="..." /> trỏ chéo (bidirectional) lẫn nhau. Có khai báo thẻ x-default.
2. **Xử lý UI/UX Trung Đông (RTL)**:
   - Thẻ root HTML bắt buộc có dir="rtl" và lang.
   - CẤM dùng Physical CSS (margin-left). Dùng 100% CSS Logical Properties (margin-inline-start, padding-inline-end).
3. **SSR Strictness (Kiểm soát Render)**:
   - Mọi nội dung cốt lõi của trang (Văn bản, Tiêu đề, Link nội bộ, Ảnh) BẮT BUỘC phải được render từ phía Server (SSR/SSG) lúc Googlebot request. Cấm fetch qua CSR (Client-side) gây Soft 404.

### Phase 7: Local / Staging Debugging Protocol (Google Debugging Guide)
1. **Testing Localhost via Ngrok Tunnel**:
   - Khi cần test Rich Results, Structured Data hoặc URL Inspection cho ứng dụng đang chạy ở localhost/staging trước khi release:
   - Chạy local server (VD port 8980), mở ngrok tunnel:
     `./ngrok http 8980 --request-header-add ngrok-skip-browser-warning:1`
   - Dán URL ngrok công khai (`https://xxxx.ngrok.io`) vào **Google Rich Results Test** để kiểm tra real-time.
   - Đảm bảo ngrok không tự sinh file `robots.txt` chặn Googlebot.
2. **GSC Error Delay Awareness**:
   - Nhớ rằng Search Console sẽ KHÔNG xóa lỗi ngay lập tức sau khi deploy fix code. Lỗi sẽ tiếp tục hiển thị cho đến khi Googlebot cào lại trang (vài ngày). Dùng **URL Inspection Tool** để gửi yêu cầu recrawl khẩn cấp.

### Phase 8: Site-Wide Technical Audit Rules (For Multi-Agent Teamwork)
Khi được kích hoạt quét toàn bộ website (Multi-Agent Teamwork), Technical Agent & Spider Agent phải tuân thủ nghiêm ngặt:
1. **Bảo vệ Crawl Budget (Faceted Search Control)**:
   - Các URL rác sinh ra từ module Bộ Lọc (Filter), Phân loại, Sort (?color=red&size=xl) BẮT BUỘC phải được chặn quét. 
   - Giải pháp: Cài thẻ <meta name="robots" content="noindex, nofollow"> trên các trang kết quả bộ lọc, hoặc cấu hình Disallow trong robots.txt để chống Googlebot sa lầy.
2. **Vệ sinh Liên kết diện rộng (Redirect Chains & Mixed Content)**:
   - 🛑 **CẤM** Redirect Chains (Chuyển hướng nối tiếp >2 bước: A->B->C) và Redirect Loop.
   - 100% Resource (Ảnh tĩnh, JS, CSS) trên toàn site phải load qua https:// (Chống Mixed Content).
   - **Phát hiện Orphan Pages (Trang mồ côi)**: Đối chiếu danh sách URL trong Sitemap với ma trận Internal Link. Mọi trang tồn tại trong Sitemap mà không có bất kỳ Internal Link nào trỏ tới phải bị gạch cờ đỏ (Critical).
3. **Đóng Gói Sitemap.xml (Sitemap Integrity & Anti-Fake Lastmod Protocol)**:
   - sitemap.xml CHỈ ĐƯỢC PHÉP chứa các URL trả về HTTP 200 (OK), và 100% là URL Self-canonical. 
   - Tuyệt đối cấm đẩy URL lỗi 404, 301, hoặc URL chứa thẻ noindex vào Sitemap.
   - **Sitemap Index Phân Mảnh (Sitemap Index Architecture)**: Dự án pSEO hoặc có số lượng URL > 1,000 BẮT BUỘC phải dùng kiến trúc Sitemap Index Mẹ (`/sitemap.xml`) trỏ tới các sitemap con (`/sitemap/core.xml`, `/sitemap/states.xml`, `/sitemap/cities-1.xml`) với kích thước ≤ 35,000 URLs/file (dưới hạn mức 50k của Google).
   - **ANTI-FAKE LASTMOD PROTOCOL**: Thẻ `<lastmod>` trong sitemap BẮT BUỘC phải phản ánh mốc thời gian thay đổi nội dung thực tế (`updatedAt` từ DB) hoặc mốc phát hành cố định (`STABLE_LASTMOD`). TUYỆT ĐỐI CẤM tự sinh `time()` / `new Date()` ngẫu nhiên mỗi lần Googlebot request sitemap, tránh bị Googlebot đánh giá là Unreliable Metadata và bỏ qua thẻ `<lastmod>`.
   - **DRIP RELEASE PROTOCOL**: Đối với dự án pSEO mới ra mắt, BẮT BUỘC dùng cơ chế Staged Drip Release (Phase 1: ~1,500 - 3,000 URLs chất lượng nhất) để xây dựng Trust Score & bảo toàn Crawl Budget, né sạch Google Sandbox trước khi mở rộng Phase 2 & Phase 3.


### Phase 9: Automated SEO Audit Crawler
1. **Chạy SEO Crawler**: Chạy script `seo-audit-crawler.js` nằm trong thư mục `.agents/skills/`:
   `node .agents/skills/seo-audit-crawler.js <URL>` (ví dụ: `http://localhost:8980` hoặc `http://web:80`).
2. **Review kết quả**: Sửa mọi lỗi 🔴 Critical và tối ưu hóa các cảnh báo 🟡 Warning để đạt điểm SEO ≥ 90/100 trước khi hoàn thành task.

### Phase 10: Brand Assets, Logo, Favicon, WebManifest & Meta Length Standards (QUY CHUẨN BẮT BUỘC)
1. **Logo & Brand Icons File Size & Quality Rules**:
   - **Tối đa dung lượng (File Size Limit)**: Logo, App Icon (`app_icon.jpg` / `app_icon.png` / `logo.png`) BẮT BUỘC nén tối ưu dưới **30 KB** (TUYỆT ĐỐI CẤM sử dụng file logo thô/chưa nén > 50 KB - 500 KB gây rác băng thông và kéo tụt điểm Core Web Vitals).
   - **Kích thước & Độ nét**: Logo trang web (`logo.png` / `logo.webp` / `logo.svg`) phải đạt kích thước tối thiểu từ 100x100px đến 512x512px để tránh bị báo lỗi mờ/blur/low-quality trên các công cụ audit SEO.
   - **Quy trình Resize & Nén Tự Động**: Khi tạo mới hoặc thay thế bất kỳ logo / app icon nào, BẮT BUỘC dùng script hoặc Python PIL resize về đúng tỉ lệ nét và nén xuống dưới **20 - 30 KB**.
2. **Bộ Favicon Standards & `site.webmanifest`**:
   - Mọi dự án BẮT BUỘC có đầy đủ bộ favicon tĩnh trong thư mục `public/`:
     - `favicon.ico` (Multiresolution 16x16, 32x32, 48x48)
     - `favicon-16x16.png` & `favicon-32x32.png` (Dung lượng < 2 KB)
     - `apple-touch-icon.png` (Kích thước 180x180px, dung lượng < 15 KB)
     - `site.webmanifest` (Khai báo `name`, `short_name`, `icons` [192x192, 512x512], `theme_color`, `background_color`, `display: standalone`).
3. **Quy chuẩn Chiều dài Meta Title & Description (Google SERP Standards 2026)**:
   - **Meta Title Length**: Giới hạn nghiêm ngặt từ **50 - 60 ký tự** (Tối đa 60 chars / ~580px - 600px width).
     - **CẤM DUPLICATE SUFFIX**: Nếu title đã chứa tên thương hiệu hoặc từ khóa thương hiệu (VD: `Local Weather Radar`), CẤM nối thêm đuôi `| ${SITE_NAME}` gây lặp từ và đẩy độ dài vượt quá 60 ký tự.
   - **Meta Description Length**: Giới hạn nghiêm ngặt từ **120 - 155 ký tự** (TUYỆT ĐỐI CẤM ngắn dưới 90 chars hoặc dài quá 155 chars khiến Google SERP cắt cụt `...`).

---

## 📤 Output
- File: `.agents/specs/seo-audit-report.md` (tạo bởi crawler) hoặc `.agents/specs/seo-technical-report.md`.
- Verdict: Score 0-100, danh sách lỗi 🔴 Critical, 🟡 Warning, 🟢 Info và giải pháp fix.

