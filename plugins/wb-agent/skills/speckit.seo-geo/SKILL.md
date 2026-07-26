---
name: speckit.seo-geo
description: SEO Technical Audit, GEO Optimization, Helpful Content theo Backlinko 2026
---

## 🎯 Mission
Đảm bảo mọi trang web công khai đạt chuẩn Technical SEO vượt trội, tối ưu hóa CTR, giữ chân người dùng và sẵn sàng cho AI Search (GEO - Backlinko 2026 Standard). Đạt chuẩn Helpful Content (độc nhất, văn phong chuyên gia E-E-A-T, không bị đánh dấu là AI-generated).

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
   - **Above the Fold UX**: Không thiết kế các banner hay hình ảnh header quá lớn chiếm trọn màn hình đầu trang làm che khuất nội dung chữ. Phải đẩy tiêu đề và những dòng mở đầu bài viết lên trên để người đọc thấy ngay thông tin khi tải trang.
   - **Độ sâu bài viết**: Chi tiết từ 1000 đến 3000 từ tùy độ khó từ khóa để bao quát toàn bộ khía cạnh chủ đề, cung cấp đầy đủ ví dụ nhằm giữ chân người đọc lâu nhất có thể.

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
4. **Readability & Multimodal**:
   - Các đoạn văn ngắn gọn, súc tích (tối đa 3-4 câu).
   - Mọi hình ảnh phải có thuộc tính `alt` mô tả chi tiết thực thể và sử dụng tên file ảnh chứa từ khóa chính.
   - Các bảng dữ liệu (tables) phải responsive.

### Phase 3: Anti-Spam, Anti-Thin Content & On-Page Structure Rules
1. **Anti-Spam & Anti-Thin Content**:
   - Title, Description, H1 phải đọc tự nhiên như người thật viết. Tuyệt đối **CẤM nhồi nhét từ khóa** (Keyword Stuffing).
   - 🛑 **CẤM**: Dùng chung 1 mẫu văn bản rập khuôn cho hàng ngàn trang (Mass Homogeneous Content). Bắt buộc dùng **Dynamic Variational Injection** — mỗi trang phải có Unique Value Point riêng biệt.
   - 🛑 **CẤM**: Cho phép Google index các trang rác, trang nghèo dữ liệu (<20 từ mô tả). Bắt buộc gắn `noindex` hoặc trả về 404/Redirect.
   - Tránh **Keyword Cannibalization**: Trang cha và trang con không được ăn thịt từ khóa nhau. Duy trì mật độ từ khóa 1.5% - 2.5%.
2. **On-Page Structure (H1-H2-H3)**:
   - `H1`: `Best [Subject] in [Location]` — Không vướng số, khớp 100% Search Intent. 1 thẻ H1 duy nhất per page.
   - `H2`: Khối Top list / Highlights / FAQ / Explore More Options.
   - `H3`: Các thẻ từ khóa phụ LSI (Nguyên liệu, Chỗ ngồi, Giờ mở cửa, Giá cả, FAQ detail).
   - Đặt bộ nút **Quick Filter Pills Navigation** cho 5 intent hot nhất ngay dưới H1.
3. **Link Juice Rules**:
   - 100% liên kết nội bộ không chứa `rel="nofollow"` (Dofollow Internal Link Rule).
   - 100% link sinh ra từ các component bắt buộc phải có dấu gạch chéo cuối `/` (Trailing Slash Uniformity) để diệt sạch redirect 308.
   - 🛑 **CẤM** tạo link nội bộ dạng query parameter (`?island=oahu`). 100% link bắt buộc là **Pure Silo Pretty URLs** (`/restaurants/oahu/`).
   - **Pillar-based Accordion Link Juice Boxes (`BoxLinkJuice`)**: Phân tách riêng biệt từng Pillar thành từng thẻ Accordion HTML (`<details>` & `<summary>`) độc lập, tuyệt đối không tống toàn bộ luồng link vào 1 box. Tiêu đề và badge tag phải dùng ngôn ngữ tự nhiên giàu giá trị SEO (VD: `Explore [Tool] Reviews & Deals`, `[Tool] Head-to-Head Comparisons`). 🛑 CẤM hiển thị các thuật ngữ kỹ thuật nội bộ trên UI như *"Internal Silo"*, *"Silo Links"*, *"Silo Directories"*, *"Intent Pages"*.
   - **Entity-Rich Anchor Text**: Anchor text chứa tên thực thể rõ ràng. Cấm dùng *"View all"* hay *"Click here"*.
   - **Quy tắc 3-Click**: Mọi trang đích đều có thể truy cập từ trang chủ trong ≤3 clicks để phân phối link equity tốt nhất.

### Phase 4: Technical SEO, Schema & CTR Audit
1. **On-Page Keyword Placement**:
   - **Keyword-First Title Tag**: Đặt từ khóa mục tiêu càng gần đầu thẻ tiêu đề càng tốt (Title Tag length ≤ 60 ký tự).
   - **Keyword in first 100 words**: Phải xuất hiện từ khóa mục tiêu tối thiểu 1 lần trong 100-150 từ đầu tiên.
   - **CTR Modifiers**: Tích hợp các từ bổ nghĩa tăng tỷ lệ click vào thẻ Title (như *tốt nhất, hướng dẫn, checklist, review, [năm hiện tại]*).
   - **URL Optimization**: Tạo URL ngắn gọn, chứa từ khóa chính.
2. **Structured Data (JSON-LD)**:
   - Khai báo JSON-LD đầy đủ và chuẩn xác theo chuẩn Schema.org:
     * **Trang chủ (`/`):** Service, SoftwareApplication, Product, LocalBusiness hoặc Restaurant Schema tùy lĩnh vực.
     * **Trang FAQ/Hỏi đáp:** FAQPage Schema khớp 100% nội dung hiển thị.
     * **Trang Blog bài viết (`/blog/[slug]`):** BlogPosting Schema với thông tin người viết (`author`), ngày đăng, ngày cập nhật, ảnh đại diện, và `publisher`.
     * **Breadcrumbs:** Tích hợp BreadcrumbList trên mọi trang con.
3. **Core Web Vitals & Performance**:
   - LCP < 2.5s, INP < 200ms, CLS < 0.1.
   - Images: WebP/AVIF, lazy loading, explicit width/height. Ảnh hero/đầu tiên phải có `priority` hoặc `fetchpriority="high"`, cấm lazy load.
   - Fonts: `font-display: swap`.
4. **Crawlability, Canonical & Modular Sub-Sitemaps Architecture (Tastehi Standard)**:
   - `robots.txt` không block CSS/JS. Cho phép AI bots (`Google-Extended`, `GPTBot`, `PerplexityBot`, `Anthropic-ai`, `ClaudeBot`) crawl.
   - 🚨 **Trailing Slash & Canonical Synchronicity**: Khi hệ thống bật `trailingSlash: true` trong `next.config.ts` hoặc Astro config, BẮT BUỘC tất cả thẻ `canonical`, `openGraph.url`, thẻ Schema (`BreadcrumbList`, `item`, `url`), thẻ `<Link href="...">` và danh sách URL trong `sitemap` PHẢI ĐỒNG BỘ 100% có dấu `/` ở cuối (`https://domain.com/silo/location/`). Tuyệt đối KHÔNG khai báo canonical thiếu `/` vì sẽ khiến Googlebot nhận HTTP 308 Redirect và báo lỗi "Canonical points to a redirect target" trên GSC.
    - 🚨 **Modular Sub-Sitemaps Architecture (Chuẩn SEO & pSEO 2026)**:
      * Bắt buộc phải tạo **Sitemap Index Mẹ (`/sitemap.xml`)** kết nối tới các Sub-Sitemaps con.
      * **1. Core Sitemap (`/sitemap/core.xml`)**: Chứa toàn bộ các trang khung xương cốt lõi (Trang chủ, Pages cố định, Categories, Khối lớp, Môn học, Sitemap Tra Cứu A-Z...). CẤM xé lẻ trang Core thành các file siêu nhỏ (<20 URLs) gây lãng phí Crawl Budget.
      * **2. Pillar-Silo Group Sitemaps (`/sitemap/lessons.xml` hoặc `/sitemap/[entity].xml`)**: Chứa các trang nội dung chi tiết theo từng Pillar/Silo. Khi số lượng bài trong một group vượt quá ngưỡng (>50,000 URLs hoặc dung lượng >50MB), tự động phân tách tiếp thành các file con hợp lý (`lessons-1.xml`, `lessons-2.xml`...).
    - **Tác dụng kĩ thuật bắt buộc**: Giúp phân lập báo cáo Coverage trên Google Search Console (GSC) rạch ròi giữa nhóm Core Pages (bắt buộc index 100%) và nhóm Content Pages, ngăn ngừa lỗi Timeout trên Cloudflare Worker khi số lượng URL lên hàng ngàn, và tối ưu hóa Crawl Budget của Googlebot.
    - Custom 404 page. Noindex hoặc redirect 301 các trang danh mục trống về trang cha gần nhất.

### Phase 5: Internal Linking Strict Rules
1. **Giới hạn Tần suất (Max 1 Link per Destination)**: Mỗi URL đích chỉ liên kết tối đa 1 lần trong toàn bộ nội dung bài viết.
2. **Vị Trí Liên Kết (First Occurrence Only)**: Chỉ chèn liên kết vào từ khóa xuất hiện lần đầu tiên.
3. **Vùng Loại Trừ (Exclusion Zones)**: Tuyệt đối không chèn liên kết trong H1, H2, H3, Frontmatter, Code blocks, thẻ Script JSON-LD, hoặc cấu trúc bảng biểu.
4. **Ngăn Chặn Liên Kết Tự Thân & Lồng Nhau (No Self-Linking & Nested Links)**: Tuyệt đối không tự liên kết hoặc lồng link.
5. **MÃ NGUỒN AN TOÀN**: Tuyệt đối KHÔNG viết mã Markdown link bên trong các thẻ HTML thô. Phải sử dụng thẻ anchor HTML dạng `<a href="URL">AnchorText</a>`.

### Phase 6: Google Search Console (GSC) & Indexability Troubleshooting
1. **Kiểm tra trạng thái Indexability**:
   - **Crawl allowed**: Phải đảm bảo file `robots.txt` không chặn Googlebot/AI bots đối với các trang quan trọng.
   - **Indexing allowed**: Đảm bảo các trang đích không có thẻ `<meta name="robots" content="noindex">` hoặc header `X-Robots-Tag: noindex`.
   - **Canonicalization**: Kiểm tra xem `canonical` URL khai báo có khớp hoàn toàn với URL thật và Google-selected canonical không. Tránh lỗi duplicate content.
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

---

## 📤 Output
- File: `.agents/specs/seo-audit-report.md` (được tạo bởi crawler) hoặc `.agents/specs/seo-geo-report.md` (nếu phân tích thủ công).
- Verdict: Score 0-100, danh sách các lỗi 🔴 Critical, 🟡 Warning, 🟢 Info và giải pháp fix.

## 🚫 Guard Rails
- KHÔNG tự động sửa đổi code trong bước audit này — chỉ tạo báo cáo và hướng dẫn sửa lỗi.
- Đảm bảo mọi trang công khai được quét qua cả 7 Phase.
- Nếu SEO Score < 85 hoặc có lỗi 🔴 Critical → Đánh giá FAIL và block deploy.