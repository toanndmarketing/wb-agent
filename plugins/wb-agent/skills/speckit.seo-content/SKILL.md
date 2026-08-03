---
name: speckit.seo-content
description: Nghiên cứu Phân tích Từ khóa, Cấu trúc Silo/Pillar/Cluster, Mapping Search Intent, Tối ưu Title Links, Control Snippets & Generative AI Search (GEO) theo chuẩn Google Search Central 2026
---

## 🎯 Mission
Cung cấp quy trình chuyên sâu chuẩn hóa giúp Content Strategist, SEO Specialist và Copywriter thực hiện: Nghiên cứu Phân tích Từ khóa, Lập bản đồ Search Intent (Ý định tìm kiếm), Thiết kế Kiến trúc Nội dung phân tầng (Pillar - Silo - Cluster), Tối ưu hóa Title Links & Snippets hiển thị trên SERP theo chuẩn Google Official, và Tối ưu hóa cho AI Search Engines (Generative AI Optimization - GEO / SGE).

## 📥 Input
- Seed Keywords (Từ khóa hạt giống) / Chủ đề ngành hàng
- Persona độc giả mục tiêu & Mục tiêu chuyển đổi (Business Intent)
- Dữ liệu đối thủ cạnh tranh trên SERP

---

## 📋 Protocol

### Phase 1: Phân tích Từ Khóa & Search Intent Mapping (Google Standard)
1. **Bản đồ 4 Nhóm Search Intent (Ý Định Tìm Kiếm)**:
   Mỗi truy vấn tìm kiếm của người dùng đại diện cho một Intent cụ thể. Bài viết BẮT BUỘC thiết kế Onpage Blueprint khớp 100% Intent đó:
   - **Informational Intent (Tìm kiếm Thông tin)**: "là gì", "cách làm", "hướng dẫn", "tại sao", "ví dụ". -> Bài Blog Guide/Glossary.
   - **Commercial Investigation Intent (Điều tra Thương mại / So sánh)**: "tốt nhất", "top 10", "so sánh", "đánh giá", "review". -> Trang Pillar So Sánh, Top List.
   - **Transactional Intent (Hành động Mua hàng / Chuyển đổi)**: "giá bao nhiêu", "bảng giá", "mua", "đặt phòng". -> Trang Sản Phẩm, Pricing, Landing Page.

### 🛡️ Anti-Keyword Cannibalization Protocol (Chống Ăn Thịt Từ Khóa & Intent Mapping)
1. **Tuyệt đối CẤM Trang Chủ (`/`) và Trang Directory/Catalog Hub (`/{niche}-directory/` hoặc `/{niche}-api/`) dùng chung bộ từ khóa (Target Keywords)**.
2. **Quy chuẩn Phân Tách Search Intent Bắt Buộc giữa Homepage và Directory/Catalog Hub**:
   - **Trang Chủ (`/`)**:
     - **Role / Search Intent**: Core Brand Landing Page & Primary Platform Service (B2B SaaS / Product Platform).
     - **Target Keyword Scope Pattern**: `{brand_name}`, `real time {service_type} api`, `{service_type} rest api service`, `{brand_name} platform`.
     - **Onpage Content Focus**: Tuyên ngôn vị thế thương hiệu (Value Proposition), Hiệu năng hệ thống (Latency/SLA), Developer Experience, Bảng tính năng cốt lõi và Chuyển đổi chính (CTA / Free Tier / Pricing).
     - **Metadata Title Rule**: Khai báo `title: { absolute: "{brand_name} — {core_value_proposition}" }` để ghi đè `title.template` ở Root Layout, diệt triệt để lỗi lặp Brand Suffix.
   - **Trang Directory / Catalog Hub (`/{niche}-directory/` hoặc `/{niche}-api/`)**:
     - **Role / Search Intent**: Catalog Directory Index / Coverage Hub (Nơi tập trung điều hướng toàn bộ danh mục sản phẩm, thực thể địa lý, dịch vụ hoặc dữ liệu chuyên ngành).
     - **Target Keyword Scope Pattern**: `{service_type} directory`, `all {niche_entity} list`, `{service_type} coverage index`, `{service_type} endpoints catalog`.
     - **Onpage Content Focus**: Danh mục tra cứu phủ rộng toàn bộ các phân vùng/thực thể/sub-services, bộ lọc tìm kiếm (Filter/Search), điều hướng phân cấp Silo/Cluster.
     - **Metadata Title Rule**: Khai báo tiêu đề tập trung vào tính chất Directory/Catalog Index: `{brand_name} {service_type} Directory — All {niche_entity} Coverage`.

### Phase 2: Quy Tắc Vàng Biên Tập Nội Dung Độc Bản (Global Content Team Rules)
1. **Naturalness & Anti-Keyword Stuffing**:
   - Meta Title, Meta Description và bài viết BẮT BUỘC tự nhiên 100%, không lặp từ khóa máy móc.
2. **Anti-Templating & Dynamic H2/H3**:
   - CẤM dập khuôn khung bài. Mọi địa điểm/sản phẩm phải có cấu trúc Heading (`<h2>`, `<h3>`) độc bản phù hợp với ngữ cảnh thực tế.
3. **Deep Data Grounding**:
   - Bắt buộc khai thác dữ liệu từ: Review thực tế của khách hàng, món ăn/menu đặc sản, tên con đường, khu vực và loại hình dịch vụ.
4. **RAW HTML Format**:
   - Nội dung bài xuất dạng Raw HTML thô (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`) giúp giao diện tự động parse làm **Mục lục (Table of Contents - TOC)**.
5. **No AI Buzzwords**:
   - CẤM các từ AI sáo rỗng: *nestled, tapestry, delve, hidden gem, testament to, moreover, in conclusion, mouth-watering, unforgettable, beacon of, vibrant hub, boasts...*
6. **EEAT & Imperfect Sentiment Rule**:
   - Bắt buộc đưa vào chi tiết cảm quan góc nhìn thứ nhất và 1-2 nhận xét/kinh nghiệm thực tế (nhược điểm nhỏ) để đạt điểm uy tín Google EEAT.
7. **Project Niche Prompt Analysis Protocol (Bắt Buộc Phân Tích Prompt Ngách Dự Án)**:
   - **CẤM DÙNG PROMPT CHUNG CHUNG**: Trước khi gen content cho bất kỳ dự án nào, Agent phải đọc/khởi tạo file đặc tả ngách `.agents/specs/niche-content-spec.md` để phân tích 4 yếu tố đặc thù: **Địa lý & Giao thông local (GEO Anchors)**, **Tiền tệ & Phân khúc giá**, **Thuật ngữ ngách (Niche Lingo)**, và **Chân dung người dùng**.
   - Công thức Prompt hoàn chỉnh: `[Global Content Rules]` + `[Project Niche Spec]` = `[Prompt Tối Ưu Cuối Cùng]`.

### Phase 3: Title Links & Control Snippets (Google Guidelines 2026)
1. **Quy tắc Thẻ `<title>`**:
   - Mọi trang có đúng 1 thẻ `<title>`, độ dài **< 60 ký tự**. Từ khóa chính sát đầu.
   - Format chung: `[Primary Keyword] - [CTR Modifier] | [Brand Name]`
   - **Đặc thù Homepage (Trang chủ)**: BẮT BUỘC theo Format `[Tên Brand] - [Làm gì], [Local nào] cho [Đối tượng nào] ([Chất lượng ra sao])`. Độ dài từ **60 đến 70 ký tự**.
2. **Quy tắc Meta Description**:
   - Độ dài: **120 – 158 ký tự**. Độc nhất cho từng trang, chứa từ khóa + UVP + CTA tự nhiên.
3. **Advanced Meta Robots Snippets**:
   ```html
   <meta name="robots" content="max-snippet:160, max-image-preview:large, max-video-preview:30">
   ```

### Phase 4: Generative AI Search Optimization (GEO Standard)
1. **Trực diện hóa Nội dung (Direct Answer First)**:
   - Đoạn mở đầu chứa khối **Direct Answer Box** trả lời thẳng vào vấn đề (<80 từ), bôi đậm các thực thể cốt lõi (Entities).
2. **Semantic Chunking & Lead with the Answer**:
   - Đưa ra câu trả lời/kết luận ngay câu đầu tiên dưới mỗi H2/H3.
3. **Semantic Triples & Machine-Readable Data**:
   - Viết câu Chủ ngữ - Vị ngữ - Bổ ngữ rõ ràng. Thêm ít nhất 1 bảng HTML (`<table>`) chứa dữ liệu thật (bảng giá, thông số, so sánh).

---

## 📤 Output
- Bản ma trận Phân tích Từ khóa & Intent Mapping (Silo Content Map).
- Bộ Metadata chuẩn hóa (Title Links, Meta Description, Custom Snippet Meta Tags, Direct Answer text).
- Nội dung Raw HTML chuẩn SEO/GEO không trùng lặp.
