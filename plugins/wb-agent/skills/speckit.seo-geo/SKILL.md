---
name: speckit.seo-geo
description: SEO Technical Audit, GEO Optimization, Helpful Content theo Backlinko 2026
---

## 🎯 Mission
Đảm bảo mọi trang web công khai đạt chuẩn Technical SEO vượt trội, tối ưu hóa CTR, giữ chân người dùng và sẵn sàng cho AI Search (GEO - Backlinko 2026 Standard). Đạt chuẩn Helpful Content (độc nhất, văn phong chuyên gia E-E-A-T, không bị đánh dấu là AI-generated).

**🚀 Triết lý SEO-as-Code (Quyền sở hữu của Dev Team):** 
Technical SEO (HTML Semantic, Core Web Vitals, Schema, SSR...) KHÔNG PHẢI là công việc "làm sau khi code xong" của SEO Team, mà là **tiêu chuẩn bắt buộc của Dev Team (Front-End/Full-stack)**. Mọi subagent khi code giao diện (đặc biệt là skill `speckit.implement`) BẮT BUỘC phải tuân thủ nghiêm ngặt file SKILL này ngay từ giai đoạn đúc Component/Layout. Team SEO chỉ đóng vai trò Auditor & Content Strategist.

## 📥 Input
- Source code (pages, layouts, components, content files)
- `.agents/knowledge/seo_standards.md` (nếu có)

---

## 📋 Protocol

### Phase 1: Helpful Content, EEAT & SEO Copywriting Audit (Backlinko Standard)
1. **Tiêu chuẩn Trải nghiệm Thực tế (Personal Experience / Case Study)**:
   - Bài viết phải lồng ghép các case study thực tế, trải nghiệm cá nhân, hoặc dữ liệu thực chứng thay vì chỉ tổng hợp lý thuyết chung chung.
   - Thể hiện rõ quan điểm của chuyên gia/tác giả uy tín trong ngành (được định nghĩa trong `master-identity.md`).
2. **Bypass AI Detectors (Độ độc nhất & Văn phong tự nhiên)**:
   - **Burstiness & Perplexity**: Cấu trúc câu đa dạng (kết hợp câu ngắn súc tích và câu dài phân tích phức tạp). Không lặp lại các mẫu câu sáo rỗng thường thấy của AI (như "tóm lại", "trong kỷ nguyên số", "thiết thực", "quan trọng là").
   - Tránh văn phong AI chung chung bằng cách dùng các thuật ngữ chuyên ngành sâu và ngôn ngữ tự nhiên của chuyên gia thực thụ. Đảm bảo độ độc nhất 100% (không copy, không spin content thô).
3. **Văn phong SEO Copywriting (Dwell Time & CTR Optimization)**:
   - **APP Formula (Agree, Promise, Preview)**: Bắt đầu phần mở bài bằng cách Đồng tình với vấn đề của độc giả (Agree), Hứa hẹn đưa ra giải pháp cụ thể (Promise), và Cho xem trước nội dung cốt lõi của bài viết (Preview).
   - **Bucket Brigades**: Sử dụng các cụm từ chuyển tiếp để tạo sự tò mò và giữ chân người đọc lâu hơn (Ví dụ: *"Thực tế là...", "Nhưng đó chưa phải là tất cả...", "Bạn có muốn biết tại sao không?"...*) nhằm tối ưu hóa Dwell Time và hạ thấp Bounce Rate.
   - **Machine-Readable E-E-A-T & Freshness (BẮT BUỘC cho AI Bot)**: 
     - **Tác giả:** Phải hiển thị "Tác giả: [Tên]" và Schema `Person` của tác giả **BẮT BUỘC phải có thuộc tính `sameAs`** trỏ về URL của LinkedIn/Twitter để AI cross-check uy tín.
     - **Freshness:** CẤM fake ngày update. Trong HTML BẮT BUỘC dùng thẻ `<time datetime="YYYY-MM-DDTHH:mm:ssZ">` chuẩn ISO-8601 để bọc ngày tháng. Trong Schema phải tách biệt rõ `datePublished` (Ngày tạo thật) và `dateModified` (Ngày sửa đổi). Chỉ cập nhật `dateModified` khi nội dung có thay đổi lớn (trên 15%), tuyệt đối cấm tool tự động update ngày ảo (Fake Freshness) để tránh bị Google phạt.
   - **Above the Fold UX**: Không thiết kế các banner hay hình ảnh header quá lớn chiếm trọn màn hình đầu trang làm che khuất nội dung chữ. Phải đẩy tiêu đề và những dòng mở đầu bài viết lên trên để người đọc thấy ngay thông tin khi tải trang.
   - **Độ sâu bài viết**: Chi tiết từ 1000 đến 3000 từ tùy độ khó từ khóa để bao quát toàn bộ khía cạnh chủ đề, cung cấp đầy đủ ví dụ nhằm giữ chân người đọc lâu nhất có thể.

### Phase 1.5: Content Architecture & Onpage Mapping (Silo Framework)
Mỗi cấp độ trang có một **Intent (Mục đích)** và **Onpage Blueprint** hoàn toàn khác nhau. Agent lập plan và sinh content BẮT BUỘC tuân thủ phân cấp sau:
1. **Trang Chủ (Home / Core Intent Hub)**:
   - **Keyword:** Từ khóa thương hiệu (Brand) hoặc Từ khóa lõi cực rộng đại diện cho toàn bộ ngành (VD: "Antidetect Browser").
   - **Onpage Blueprint:** Ưu tiên **UX Điều hướng (Navigation-first)**. CẤM viết một bài blog dài 2000 từ nhồi nhét chữ trên trang chủ. Bố cục phải là các khối Hero, Features, và **Pillar-based Accordion / Grid** dẫn dắt người dùng đi sâu vào các Pillar.
   - **Link Flow:** Phân phối Link Juice mạnh nhất đến tất cả các trang Pillar.
2. **Trang Pillar (Broad Topic / Ultimate Hub)**:
   - **Keyword:** Từ khóa có Volume cao, bao trùm một nhánh lớn (VD: "Best Antidetect Browser 2026", "Make Money Online").
   - **Onpage Blueprint:** Dạng **"The Ultimate Guide"** hoặc Trang Tổng Hợp So Sánh. Nội dung siêu chi tiết (>3000 từ), bao phủ rộng. Bắt buộc có **Table of Contents (ToC)** ở ngay đầu trang. Các thẻ H2 chia theo từng Silo (Category) con.
   - **Link Flow:** Trỏ link xuống tất cả các trang Silo con và Top Cluster quan trọng.
3. **Trang Silo (Specific Category / Directory Hub)**:
   - **Keyword:** Từ khóa Medium-Volume, ngách cụ thể (VD: "Browser cho Crypto", "Công cụ SEO").
   - **Onpage Blueprint:** Dạng **Directory/Archive Hybrid**. Nửa trên (Above-the-fold) là khối Content giới thiệu chuyên môn (300-500 từ). Nửa dưới là Grid/List liệt kê các bài Cluster/Sản phẩm thuộc ngách đó.
   - **Link Flow:** Liên kết xuống 100% các bài Cluster thuộc Silo đó. Trỏ Breadcrumb ngược về Pillar cha.
4. **Trang Cluster (Long-tail Detail / Spoke)**:
   - **Keyword:** Từ khóa Long-tail có Volume thấp nhưng tỷ lệ chuyển đổi (Conversion Rate) cực cao (VD: "Cách dùng Gologin nuôi tài khoản Facebook Ads").
   - **Onpage Blueprint:** Dạng **In-depth Content**. Áp dụng triệt để *Direct Answer Box*, *Semantic Chunking*, và *Quotable Statements* (như định nghĩa ở Phase 2).
   - **Link Flow:** Trỏ 1 link ngược về Silo cha. Trỏ ngang sang 1-2 bài Cluster có liên quan chặt chẽ TRONG CÙNG SILO. CẤM link chéo bừa bãi sang các Silo không liên quan gây rò rỉ Link Juice (Silo Bleeding).

### Phase 2: Content Structure & GEO Layout (Seen & Trusted Framework)
1. **Direct Answer Box (Trả lời trực diện cho AI Search)**:
   - Bắt đầu bài viết/trang bằng một khối "Tóm tắt nhanh" hoặc "Trả lời trực diện" (2-3 câu, tối đa 80 từ) nằm ở đầu bài viết (ngay sau lời dẫn mở đầu, trước tiêu đề H2 đầu tiên).
   - Bôi đậm các từ khóa thực thể quan trọng liên quan đến chủ đề của trang.
   - Định dạng hiển thị: Sử dụng box có viền nổi bật (CSS class `geo-direct-answer` với style viền trái tông màu nổi bật của website: `border-l-4 border-primary pl-4 py-2 bg-primary/5 italic` hoặc tương đương).
2. **Semantic Chunking & Lead with the Answer**:
   - Chia nhỏ nội dung thành các phần rõ ràng được đánh dấu bằng các thẻ H2/H3 có tính mô tả chi tiết, khớp với truy vấn thực tế hoặc câu hỏi dạng đối thoại của người dùng.
   - Mỗi phần nội dung dưới H2/H3 phải **Lead with the Answer** - đưa câu trả lời/kết luận ngay câu đầu tiên dưới H2/H3 trước khi triển khai các chi tiết bổ trợ.
3. **Quotable Statements, Statistics & Bảng so sánh (LLM Seeding)**:
   - Viết các câu phát biểu ngắn gọn, mang đầy đủ ngữ cảnh để LLM dễ dàng trích xuất (Quotable Statements). Sử dụng số liệu thống kê hoặc trích dẫn từ nguồn tin cậy để tăng 30-40% khả năng hiển thị trong AI Overviews.
   - Phải có ít nhất 1 bảng so sánh chi tiết hoặc danh sách bullet point có số liệu/dữ liệu cụ thể để AI search engines (Gemini, ChatGPT, Perplexity) dễ cào và trích xuất dữ liệu dạng bảng.
4. **Readability, Semantic HTML5 & Multimodal**:
   - **Semantic HTML5 Architecture**: Bắt buộc bố cục trang dùng `<main>`, `<article>`, `<section>`, `<aside>`, `<nav>`. Tránh lạm dụng thẻ `<div>` (Divitis) để AI Bots có thể parse cấu trúc DOM cực nhanh.
   - Các đoạn văn ngắn gọn, súc tích (tối đa 3-4 câu).
   - Mọi hình ảnh phải có thuộc tính `alt` mô tả chi tiết thực thể và sử dụng tên file ảnh chứa từ khóa chính.
   - Các bảng dữ liệu (tables) phải responsive.
   - **Table of Contents (ToC) & Named Anchors**: Các bài viết (>1000 từ) BẮT BUỘC phải có Mục lục sử dụng jump-to links (`<a href="#id">`). Tất cả các thẻ H2/H3/H4 bắt buộc phải sinh id để Google tạo "Jump to" sitelinks trên SERPs.

### Phase 3: Anti-Spam, Anti-Thin Content & On-Page Structure Rules
1. **Anti-Spam, Anti-Thin Content & Anti-Duplicate Meta**:
   - Title, Description, H1 phải đọc tự nhiên như người thật viết. Tuyệt đối **CẤM nhồi nhét từ khóa** (Keyword Stuffing).
   - 🛑 **CẤM**: Dùng chung 1 mẫu văn bản rập khuôn cho hàng ngàn trang (Mass Homogeneous Content). Bắt buộc dùng **Dynamic Variational Injection** — mỗi trang phải có Unique Value Point riêng biệt.
   - 🛑 **CẤM Duplicate Title/Description**: Mỗi trang phải có `<title>` và `<meta description>` HOÀN TOÀN DUY NHẤT. Đặc biệt nghiêm cấm các trang Category, Tag, Author page dùng chung meta với Trang chủ. `<meta description>` bắt buộc dài **120–158 ký tự** (không dài hơn để tránh bị Google cắt, không ngắn hơn để đủ từ khóa phụ).
   - 🛑 **CẤM**: Cho phép Google index các trang rác, trang nghèo dữ liệu (<20 từ mô tả). Bắt buộc gắn `noindex` hoặc trả về 404/Redirect.
   - Tránh **Keyword Cannibalization**: Trang cha và trang con không được ăn thịt từ khóa nhau. Duy trì mật độ từ khóa 1.5% - 2.5%.
   - ✅ **Pagination — Chiến lược Self-Canonical + Index (Chuẩn 2026)**: Google đã deprecated `rel="prev/next"`. Với trang phân trang từ trang 2 trở đi (`/page/2/`, `/page/3/`...):
     - **Canonical phải self-referencing** — trỏ về chính URL của trang đó (KHÔNG trỏ về trang 1).
     - **Title phải UNIQUE** — bắt buộc kèm số trang: `[Từ khóa chính] - Trang [X] | [Brand]`.
     - **Meta description phải UNIQUE** — mô tả nội dung cụ thể của trang đó, không copy trang 1.
     - Index bình thường để Google có thể rank từng trang cho long-tail queries.
     - 🛑 **NGOẠI LỆ duy nhất**: Nếu nội dung pagination là cùng một danh sách sản phẩm/bài viết sắp xếp theo thứ tự khác nhau (duplicate content thực sự) → lúc đó mới dùng `noindex`.
2. **On-Page Structure (Giới hạn thẻ Head từ H1 đến H4 tối đa)**:
   - `H1`: Chứa Từ Khóa Chính. (VD: `Best [Subject] in [Location]`) — Khớp 100% Search Intent. 1 thẻ H1 duy nhất per page.
   - `H2`: Chứa Từ Khóa Phụ / Khối Top list / Highlights / FAQ / Explore More Options.
   - `H3`: Các thẻ từ khóa LSI mở rộng (Nguyên liệu, Chỗ ngồi, Giờ mở cửa, Giá cả, FAQ detail).
   - `H4`: Tuỳ biến phân bổ theo từng page để nhóm các chi tiết nhỏ nằm dưới H3.
   - 🛑 **CẤM NHẢY CÓC THẺ HEAD**: Thứ tự các thẻ Head phải tuân thủ nghiêm ngặt phân cấp tự nhiên: `H1` ➔ `H2` ➔ `H3` ➔ `H4`. Tuyệt đối **CẤM nhảy cóc** (VD: `H1` ➔ `H3` hoặc `H2` ➔ `H4`). Nếu muốn kích thước chữ nhỏ hơn, phải dùng CSS/Tailwind class (`text-sm`, `text-base`), tuyệt đối KHÔNG được dùng sai thẻ HTML.
   - 🛑 **CẤM**: Tuyệt đối KHÔNG dùng H5, H6 để tránh làm loãng cấu trúc trang. 
   - Đặt bộ nút **Quick Filter Pills Navigation** cho 5 intent hot nhất ngay dưới H1.
3. **Link Juice Rules**:
   - 100% liên kết nội bộ không chứa `rel="nofollow"` (Dofollow Internal Link Rule).
   - 100% link sinh ra từ các component bắt buộc phải có dấu gạch chéo cuối `/` (Trailing Slash Uniformity) để diệt sạch redirect 308.
   - 🛑 **CẤM** tạo link nội bộ dạng query parameter (`?island=oahu`). 100% link bắt buộc là **Pure Silo Pretty URLs** (`/restaurants/oahu/`).
   - **Pillar-based Accordion Link Juice Boxes (`BoxLinkJuice`)**: Phân tách riêng biệt từng Pillar thành từng thẻ Accordion HTML (`<details>` & `<summary>`) độc lập, tuyệt đối không tống toàn bộ luồng link vào 1 box. Tiêu đề và badge tag phải dùng ngôn ngữ tự nhiên giàu giá trị SEO (VD: `Explore [Tool] Reviews & Deals`, `[Tool] Head-to-Head Comparisons`). 🛑 CẤM hiển thị các thuật ngữ kỹ thuật nội bộ trên UI như *"Internal Silo"*, *"Silo Links"*, *"Silo Directories"*, *"Intent Pages"*.
   - **Entity-Rich Anchor Text**: Anchor text chứa tên thực thể rõ ràng. Cấm dùng *"View all"* hay *"Click here"*.
   - **Quy tắc 3-Click**: Mọi trang đích đều có thể truy cập từ trang chủ trong ≤3 clicks để phân phối link equity tốt nhất.

### Phase 4: Technical SEO, Schema & CTR Audit
1. **On-Page Keyword Placement & Metadata**:
   - **Keyword-First Title Tag**: Đặt từ khóa mục tiêu càng gần đầu thẻ tiêu đề càng tốt (Title Tag length ≤ 60 ký tự).
   - **Keyword in first 100 words**: Phải xuất hiện từ khóa mục tiêu tối thiểu 1 lần trong 100-150 từ đầu tiên.
   - **CTR Modifiers**: Tích hợp các từ bổ nghĩa tăng tỷ lệ click vào thẻ Title (như *tốt nhất, hướng dẫn, checklist, review, [năm hiện tại]*).
   - **URL Optimization & Kebab-case ASCII**: Slugs URL BẮT BUỘC 100% là chuỗi viết thường (`kebab-case`), xóa toàn bộ dấu tiếng Việt/ký tự đặc biệt, phân tách duy nhất bằng dấu gạch ngang `-` (không dùng `_` hay khoảng trắng, không viết hoa).
   - **Social Meta Tags & Absolute URLs**: Bắt buộc khai báo đủ `og:title`, `og:description`, `og:image`, `twitter:card`. 🚨 **ĐẠI KỴ**: 100% URL trong `og:image`, `twitter:image`, `og:url` BẮT BUỘC phải là **Absolute URL** chứa đầy đủ domain (`https://domain.com/og.png`), tuyệt đối **CẤM dùng Relative URL** (`/og.png`) vì Facebook/Zalo/Telegram/Google sẽ không hiển thị được preview.
   - **Favicon & SERP Brand Icon (Tối ưu CTR SERP)**: Mọi trang web BẮT BUỘC khai báo bộ Icon chuẩn trong `<head>`: `favicon.ico`, `favicon.svg` (Dark/Light mode), và `<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">` để Google SERP hiển thị Logo thương hiệu nổi bật bên cạnh tiêu đề tìm kiếm.
2. **Structured Data (JSON-LD)**:
   - Khai báo JSON-LD đầy đủ và chuẩn xác theo chuẩn Schema.org:
     * **Trang chủ (`/`):** Service, SoftwareApplication, Product, LocalBusiness hoặc Restaurant Schema tùy lĩnh vực.
     * **Trang FAQ/Hỏi đáp:** FAQPage Schema khớp 100% nội dung hiển thị.
     * **Trang Blog bài viết (`/blog/[slug]`):** BlogPosting Schema với thông tin người viết (`author`), ngày đăng, ngày cập nhật, ảnh đại diện, và `publisher`.
     * **Breadcrumbs:** Tích hợp BreadcrumbList trên mọi trang con.
     * 🚨 **Absolute URLs trong Schema**: Mọi trường chứa đường dẫn ảnh (`image`, `logo`, `author.image`) hoặc URL trong JSON-LD BẮT BUỘC 100% phải là Absolute URL (`https://...`).
     * 🚨 **CẤM Microdata/RDFa**: Tuyệt đối KHÔNG nhúng Schema trực tiếp vào thẻ HTML dạng attributes thô (`itemscope`, `itemprop`) vì làm DOM cồng kềnh, khó bảo trì. 100% Structured Data BẮT BUỘC viết tách rời trong thẻ `<script type="application/ld+json">`.
3. **Core Web Vitals, Performance & Mobile-First UX**:
   - LCP < 2.5s, INP < 200ms, CLS < 0.1.
   - **Viewport & Accessibility**: Thẻ meta viewport CẤM chặn zoom (`user-scalable=no` hoặc `maximum-scale=1`), điều này vi phạm nghiêm trọng Accessibility & SEO. Khuyến nghị chuẩn: `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">`.
   - **Resource Hints (Preload)**: Các tài nguyên siêu quan trọng xuất hiện ở màn hình đầu tiên (Above-The-Fold) như LCP Hero Image, Critical Fonts BẮT BUỘC phải được load trước bằng `<link rel="preload" ...>`. Tuyệt đối CẤM preload bừa bãi các tài nguyên nằm dưới nếp gấp trang gây tắc nghẽn băng thông.
   - **Images — Chống CLS (BẮT BUỘC)**: Tất cả thẻ `<img>` PHẢI khai báo đầy đủ cả 3: `width`, `height` (px thật), và `loading="lazy"`. Thiếu `width`/`height` là nguyên nhân số 1 gây CLS cao — trình duyệt không biết trước kích thước ảnh nên layout bị giật khi ảnh load xong. Ảnh hero/đầu tiên dùng `fetchpriority="high"` và bỏ lazy load.
   - **Iframe Lazy Load (Chống block render)**: Tất cả `<iframe>` nhúng (YouTube, Google Maps, Loom...) bắt buộc có thuộc tính `loading="lazy"` để không block render của trang. Ưu tiên dùng Facade pattern (placeholder ảnh tĩnh thay iframe thật, chỉ load iframe khi user click).
   - Fonts: `font-display: swap`.
   - **Mobile Tap Targets**: Nút bấm, Icon Social, hoặc Card Links trên mobile BẮT BUỘC có kích thước tối thiểu `48x48px` và cách nhau ít nhất `8px` để khắc phục triệt để lỗi "Clickable elements too close together" trên GSC.
   - Format ảnh: WebP/AVIF bắt buộc. Dùng `<picture>` với `srcset` cho responsive images.
4. **Image `alt`, Anchor Rules, External Links & Accessibility**:
   - **Thẻ `<img>` (BẮT BUỘC 100%)**: Tất cả thẻ `<img>` PHẢI có thuộc tính `alt` mô tả ngữ cảnh chi tiết chứa tên thực thể/từ khóa (VD: `alt="Gologin Antidetect Browser Logo"`). TUYỆT ĐỐI CẤM để rỗng `alt=""` (trừ ảnh decor icon rác) hoặc dùng alt rác như `alt="image"`, `alt="logo"`.
   - **Thẻ `<a>` (BẮT BUỘC cho Icon-only Links & Tối ưu cho Silo Links)**:
     - Nếu thẻ `<a>` chỉ chứa Icon / SVG / Nút bấm ngắn không có text hiển thị: BẮT BUỘC phải có `aria-label="..."` hoặc `title="..."` rõ ràng để tránh lỗi Lighthouse *"Links do not have a discernible name"*.
     - Đối với các Internal Links trong Silo (`BoxLinkJuice`, card link): Khuyến khích bổ sung thuộc tính `title="..."` giàu giá trị từ khóa intent (VD: `title="Read in-depth Gologin Review & Pricing"`) giúp tăng tín hiệu ngữ nghĩa (Relevance Signal) cho Googlebot khi phân phối Link Juice.
   - **External Links — Bảo mật & Link Equity**:
     - Tất cả external link mở tab mới (`target="_blank"`) BẮT BUỘC có `rel="noopener noreferrer"` để ngăn lỗ hổng bảo mật Tabnapping và Lighthouse warning.
     - External link trỏ đến trang đối thủ cạnh tranh, mạng xã hội, hoặc nguồn chất lượng thấp: dùng `rel="nofollow noopener noreferrer"`.
     - External link trỏ đến nguồn tham chiếu uy tín (nghiên cứu, báo chính thống): có thể giữ dofollow để tăng tín hiệu E-E-A-T.
   - **Breadcrumb HTML Markup (Khớp JSON-LD)**:
     - HTML breadcrumb BẮT BUỘC dùng `<nav aria-label="Breadcrumb">` bao ngoài, bên trong là `<ol>` (danh sách có thứ tự).
     - Cấu trúc và số lượng item phải khớp 100% với JSON-LD `BreadcrumbList` — nếu JSON-LD có 3 cấp thì HTML phải có đúng 3 cấp.
5. **Crawlability, Canonical, Multilingual & Modular Sub-Sitemaps Architecture**:
   - **`<html lang>` — BẮT BUỘC**: Thẻ `<html>` phải có thuộc tính `lang` đúng với ngôn ngữ chính của trang (VD: `<html lang="vi">` hoặc `<html lang="en">`). Thiếu → Google hiểu nhầm ngôn ngữ, tụt rank trên kết quả tìm kiếm bản ngữ, lỗi Lighthouse Accessibility.
   - **`hreflang` cho Đa Ngôn Ngữ**: Nếu site có nhiều phiên bản ngôn ngữ (vi/en/...), BẮT BUỘC khai báo `<link rel="alternate" hreflang="vi" href="...">` trong `<head>` cho MỌI trang. Thiếu hreflang → Google index nhầm trang, split link equity, duplicate content xuyên quốc gia. Luôn kèm `hreflang="x-default"` trỏ về phiên bản mặc định.
   - `robots.txt` không block CSS/JS. Cho phép AI bots (`Google-Extended`, `GPTBot`, `PerplexityBot`, `Anthropic-ai`, `ClaudeBot`) crawl.
   - 🚨 **Trailing Slash & Canonical Synchronicity**: Khi hệ thống bật `trailingSlash: true` trong `next.config.ts` hoặc Astro config, BẮT BUỘC tất cả thẻ `canonical`, `openGraph.url`, thẻ Schema (`BreadcrumbList`, `item`, `url`), thẻ `<Link href="...">` và danh sách URL trong `sitemap` PHẢI ĐỒNG BỘ 100% có dấu `/` ở cuối (`https://domain.com/silo/location/`). Tuyệt đối KHÔNG khai báo canonical thiếu `/` vì sẽ khiến Googlebot nhận HTTP 308 Redirect và báo lỗi "Canonical points to a redirect target" trên GSC.
    - 🚨 **Modular Sub-Sitemaps Load Balancing (Phân bổ chuẩn 2026)**:
      * Bắt buộc tạo **Sitemap Index Mẹ (`/sitemap.xml`)** kết nối tới các Sub-Sitemaps con.
      * **1. Core Sitemap (`/sitemap/core.xml`)**: Gom TẤT CẢ các trang tĩnh, số lượng ít (Trang chủ, Giới thiệu, Liên hệ, Các trang Pillar/Silo Hub, Tác giả) vào chung 1 file duy nhất. 🛑 CẤM xé lẻ trang Core thành các file siêu nhỏ (VD: sitemap-tuyendung.xml chỉ có 3 links) gây lãng phí Crawl Budget và tốn Time-to-First-Byte (TTFB) của bot.
      * **2. Dynamic Threshold Sitemaps (`/sitemap/posts-1.xml`, `/sitemap/products-1.xml`)**: Đối với dữ liệu động (Bài viết, Sản phẩm), KHÔNG phân chia sitemap theo Category nếu category đó quá ít bài. Hãy chia theo **Ngưỡng số lượng (Threshold)** hoặc **Timeline (Năm/Tháng)**. Khuyến nghị: Cứ đủ 10,000 URLs thì đóng gói thành file `posts-1.xml`, đầy thì mở tiếp `posts-2.xml`. Ngưỡng 10,000 là tối ưu nhất để Cloudflare Worker không bị Timeout khi render XML và Googlebot đọc nhanh nhất.
    - **Tác dụng kĩ thuật bắt buộc**: Giúp phân lập báo cáo Coverage trên Google Search Console (GSC) rạch ròi giữa nhóm Core Pages (bắt buộc index 100%) và nhóm Content Pages, ngăn ngừa lỗi Timeout trên Cloudflare Worker khi số lượng URL lên hàng ngàn, và tối ưu hóa Crawl Budget của Googlebot.
    - Custom 404 page. Noindex hoặc redirect 301 các trang danh mục trống về trang cha gần nhất.

### Phase 5: Internal Linking Strict Rules
1. **Giới hạn Tần suất (Max 1 Link per Destination)**: Mỗi URL đích chỉ liên kết tối đa 1 lần trong toàn bộ nội dung bài viết.
2. **Semantic Surrounding Context (Cho RAG & AI Bot)**: Đoạn văn bản bọc xung quanh Anchor text (khoảng 30 chữ trước và sau link) PHẢI chứa thông tin ngữ cảnh giải thích rõ ràng cho cái link đó. Tuyệt đối không đặt link trơ trọi. AI Bot cần chunk (cắt đoạn) chứa link để hiểu trọn vẹn ngữ nghĩa.
3. **Vùng Loại Trừ (Exclusion Zones)**: Tuyệt đối không chèn liên kết trong H1, H2, H3, Frontmatter, Code blocks, thẻ Script JSON-LD, hoặc cấu trúc bảng biểu.
4. **Ngăn Chặn Liên Kết Tự Thân & Lồng Nhau (No Self-Linking & Nested Links)**: Tuyệt đối không tự liên kết hoặc lồng link.
5. **MÃ NGUỒN AN TOÀN**: Tuyệt đối KHÔNG viết mã Markdown link bên trong các thẻ HTML thô. Phải sử dụng thẻ anchor HTML dạng `<a href="URL">AnchorText</a>`.
6. **Chống Orphan Pages & Redirect Chains (Bảo vệ Crawl Budget)**:
   - 🛑 **CẤM Orphan Page**: Trang có trong sitemap nhưng không có internal link nào từ trang khác. Mọi trang mới tạo phải ngay lập tức được link từ ít nhất 1 trang trong cùng silo.
   - 🛑 **CẤM Redirect Chain**: Bất kỳ liên kết hoặc chuyển hướng (301) nào cũng phải trỏ THẲNG tới URL đích cuối cùng (1-Hop only). Cấm tuyệt đối chuỗi vòng lặp (A -> 301 B -> 301 C) khiến Googlebot drop index.
   - Công cụ kiểm tra: Sau khi deploy, chạy Screaming Frog hoặc SEO Crawler để phát hiện trang 0 inlinks và Redirect Chain.
7. **Pure Anchor Text for Card Components (Diệt Block-level `<a>` links)**: 
   - 🛑 **CẤM** tuyệt đối việc dùng thẻ `<a>` để bọc toàn bộ nội dung của một thẻ Card (gồm ảnh, tiêu đề, mô tả dài). Việc này tạo ra Anchor Text rác khổng lồ, làm loãng tín hiệu ngữ nghĩa của SEO.
   - **Bắt buộc dùng Pseudo-element link trick**: 
     - Wrapper của thẻ Card phải dùng thẻ HTML có ngữ nghĩa (`<article>`, `<div>`, `<li>`) và gắn class `relative`.
     - Thẻ `<a>` chỉ được bọc đúng vùng chứa Anchor Text chính (thường là tiêu đề H2/H3), và kết hợp class CSS `after:absolute after:inset-0 focus:outline-none` để mở rộng vùng click ra toàn bộ thẻ Card mà vẫn giữ Anchor Text tinh khiết.
     - Các nội dung văn bản khác bên trong Card cần gắn `relative z-10 pointer-events-none` (nếu không cần tương tác) để không cản trở click.

### Phase 6: Google Search Console (GSC) & Indexability Troubleshooting
1. **Kiểm tra trạng thái Indexability**:
   - **Crawl allowed**: Phải đảm bảo file `robots.txt` không chặn Googlebot/AI bots đối với các trang quan trọng.
   - **Indexing allowed**: Đảm bảo các trang đích không có thẻ `<meta name="robots" content="noindex">` hoặc header `X-Robots-Tag: noindex`.
   - **Canonicalization**: Kiểm tra xem `canonical` URL khai báo có khớp hoàn toàn với URL thật và Google-selected canonical không. Tránh lỗi duplicate content.
   - 🚨 **Chống lỗi Soft 404 trong SSR (BẮT BUỘC)**: Trong các trang SSR (Next.js, Astro SSR), khi dữ liệu rỗng hoặc Slug/ID không tồn tại, BẮT BUỘC server response phải trả về đúng HTTP Status Code `404 Not Found` (dùng `notFound: true` trong Next.js hoặc `return Astro.rewrite('/404')` kèm HTTP 404). Tuyệt đối **CẤM trả về HTTP 200 OK** kèm giao diện 404 UI vì Googlebot sẽ phạt hàng loạt lỗi Soft 404 trên GSC.
2. **Khắc phục lỗi hạ tầng**:
   - **SSL & DNS stability**: Đảm bảo chứng chỉ SSL hợp lệ. Googlebot sẽ từ chối crawl nếu SSL hỏng hoặc DNS trả về IP private (RFC 1918).
   - **Robots.txt Availability**: File `robots.txt` phải luôn khả dụng (HTTP 200/404). Nếu server bị lỗi 5xx, Googlebot sẽ dừng crawl toàn bộ trang.

### Phase 7: Automated SEO Audit Crawler
1. **Chạy SEO Crawler**: Chạy script `seo-audit-crawler.js` nằm trong thư mục `.agents/skills/`:
   `node .agents/skills/seo-audit-crawler.js <URL>` (ví dụ: `http://localhost:8980` hoặc `http://web:80`).
2. **Review kết quả**:
   - Kiểm tra file báo cáo `.agents/specs/seo-audit-report.md` sau khi crawler chạy xong.
   - Sửa mọi lỗi 🔴 Critical và tối ưu hóa các cảnh báo 🟡 Warning để đạt điểm SEO ≥ 90/100 trước khi hoàn thành task.

---

### Phase 8: Global English AI Content Generation Rules (V3.2 Prompt Standard)
Khi viết script hoặc điều phối AI tự động sinh bài viết cho thị trường Global (Tiếng Anh), BẮT BUỘC tuân thủ 10 quy tắc Prompt V3.2:
1. **100% English Output**: Toàn bộ bài viết, H2/H3, bảng biểu đều bằng Tiếng Anh chuẩn chuyên nghiệp.
2. **GEO Direct Answer Box**: Luôn bắt đầu bài bằng `<div class="geo-direct-answer">` (2-3 câu bôi đậm, <80 từ) trả lời trực diện cho Google AI Overviews.
3. **LLM Seeding Table**: Phải có ít nhất 1 thẻ `<table>` HTML chứa dữ liệu thật (tính năng, giá cả) cho ChatGPT/Perplexity cào data.
4. **Anti-Hallucination Guardrails**: CẤM bịa thông tin giá cả, gói cước, hoặc tỷ lệ hoa hồng affiliate không có trong dữ liệu thật.
5. **Editorial Voice**: Xưng danh với tư cách Ban biên tập độc lập (*"We researched..."*), CẤM giả xưng *"Tôi đã trải nghiệm 2 tuần"*.
6. **End-User Value Focus**: Tập trung vào người mua/dùng phần mềm, CẤM nhắc tới chương trình affiliate hay hoa hồng giới thiệu.
7. **Anti-Template Headings**: CẤM dùng các thẻ H2 nhàm chán (*Overview, Features, Pricing, Conclusion*). Giật tít H2/H3 sáng tạo theo thương hiệu phần mềm.
8. **Honest Drawbacks Analysis**: Nếu dữ liệu Cons rỗng, phải phân tích trung thực rào cản thực tế (rào cản học sử dụng, cạnh tranh, độ sâu tính năng).
9. **Aggressive Burstiness**: Xen kẽ câu phân tích dài và câu ngắn 2-5 từ để tạo nhịp điệu đọc tự nhiên, tránh bị AI Detector phát hiện.
10. **Dynamic Year Context**: Luôn nhúng năm hiện tại (`${CURRENT_YEAR}`) vào Prompt (VD: *2026 Edition*).
11. **Model Rotation & Quota Optimization (Anti-429)**: Để chống lỗi cạn Quota/Rate Limit (429) khi sinh nội dung hàng loạt, BẮT BUỘC áp dụng cơ chế Round-Robin xoay tua mảng models (`gemini-3.5-flash-lite`, `gemini-3.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.5-flash`). Nếu model hiện tại báo lỗi 429, tự động sleep (1s-2s) và fallback sang model kế tiếp để tiến trình liên tục, tăng tốc tối đa.

---

## 📤 Output
- File: `.agents/specs/seo-audit-report.md` (được tạo bởi crawler) hoặc `.agents/specs/seo-geo-report.md` (nếu phân tích thủ công).
- Verdict: Score 0-100, danh sách các lỗi 🔴 Critical, 🟡 Warning, 🟢 Info và giải pháp fix.

## 🚫 Guard Rails
- KHÔNG tự động sửa đổi code trong bước audit này — chỉ tạo báo cáo và hướng dẫn sửa lỗi.
- Đảm bảo mọi trang công khai được quét qua cả 7 Phase.
- Nếu SEO Score < 85 hoặc có lỗi 🔴 Critical → Đánh giá FAIL và block deploy.
- 🛑 **ANTI-REWORK BLOCKER (Điều kiện tiên quyết trước khi Code/Plan)**: Khi tham gia vào quá trình lập Spec (`speckit.specify`), lập Plan (`speckit.plan`), hoặc Lập trình (`speckit.implement`) xây dựng một Page/Component mới: 
  - NẾU Agent nhận thấy thông tin từ User còn mơ hồ, **chưa được cung cấp rõ ràng về "Tiêu chí mục tiêu Keyword là gì?", "Thuộc Pillar hay Silo nào?"** —> **BẮT BUỘC DỪNG LẠI (STOP)**.
  - Tuyệt đối CẤM tự ý đoán từ khóa hay code bừa để rồi phải đập đi sửa lại. 
  - Phải lập tức đặt câu hỏi (qua `speckit.clarify` hoặc hỏi trực tiếp) yêu cầu User cung cấp kỹ thêm thông tin: *"Trang này target Keyword chính là gì?", "Nó nằm ở Pillar/Silo nào trong cấu trúc trang?"* rồi mới được phép code triển khai chi tiết.