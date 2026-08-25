---
name: seo
description: Skill chuyên dụng cho Fix Code, SEO, Metadata, Onpage, Schema và AI Content Generation.
triggers:
  - "fix code"
  - "tối ưu seo"
  - "metadata"
  - "onpage"
  - "schema"
  - "viết bài"
  - "generate content"
od:
  mode: workflow
  craft:
    requires: []
  design_system:
    requires: false
---

# 🚀 SEO & Content Generation Skill

Skill này hướng dẫn Agent các bước để xử lý mọi tác vụ liên quan đến SEO, cấu trúc Onpage và viết nội dung AI. 

## Cập Nhật Thuật Toán Mới Nhất (August 2026 Spam Update)
Bản cập nhật tháng 8/2026 (rollout từ 18/08/2026) của Google tập trung càn quét các chiến thuật **Spam** trên quy mô toàn cầu, ảnh hưởng trực tiếp đến Ranking. 

**🔥 BẮT BUỘC KHI NGHIÊN CỨU DỰ ÁN MỚI (CHỐT CẤU TRÚC & NỘI DUNG):**
Khi Team Phân tích SEO lập Spec hoặc Thiết kế kiến trúc (Silo/Cluster) cho dự án mới, phải thiết kế dựa trên hệ thống phòng thủ SpamBrain:
1. **Phòng thủ Thin Content (Nội dung mỏng):** Không tạo ra hàng nghìn trang (pSEO) có nội dung rập khuôn, chỉ thay đổi mỗi tên địa phương/từ khóa. Mọi trang đích (landing page) phải có "Unique Value" (Dữ liệu đặc thù, bảng biểu, so sánh thực tế).
2. **Phòng thủ Manipulative Link-building (Thao túng liên kết):** Cấu trúc Internal Link (Silo) phải tự nhiên, đi theo luồng hành trình người dùng (Link Juice đi từ Home -> Pillar -> Silo -> Cluster). Tuyệt đối cấm tạo các module "Tag Cloud" nhồi nhét link chéo vô tội vạ.
3. **Phòng thủ AI Slop (Nội dung rác):** Toàn bộ quy trình sinh nội dung (Content Generation Pipeline) phải được thiết kế theo dạng Data-Driven (truyền data thực, số liệu API, JSON vào prompt) để ép AI phân tích, thay vì để AI tự do "bịa" chữ (Hallucinate).
4. **Phòng thủ Programmatic Template Spam (Metadata Title & Description Độc bản Tự nhiên đa ngành):**
   - **CẤM TUYỆT ĐỐI công thức máy móc rập khuôn**: Cấm các template ghép cứng biến số vô hồn (như `[Tên] - [Địa chỉ], [Thành phố]`, `[Sản phẩm] ([Danh mục]) - Giá & Đánh giá`, `[Dịch vụ] tại [Địa phương] - Báo giá`). Hàng nghìn URL cùng 1 khung cú pháp chỉ tráo biến số sẽ bị Google SpamBrain nhận diện là Scaled Content Abuse / Boilerplate Spam.
   - **Quy chuẩn SEO Title (Văn xuôi Thực thể - Entity-Dense Natural Prose)**:
     + Bắt buộc viết thành **1 câu văn xuôi hoàn chỉnh có nghĩa, tự nhiên, 100% unique** (đóng vai trò là một headline thu hút, giải quyết đúng Search Intent).
     + Kết hợp linh hoạt theo ngữ cảnh ngành hàng: **[Thực thể chính (Tên Thương hiệu / Đối tượng / Sản phẩm / Dịch vụ)] + [Ngữ cảnh phân loại (Vị trí Local / Danh mục / Phân khúc)] + [Thực thể khác biệt hóa mạnh nhất (Tính năng độc quyền / USP / Điểm nhấn trải nghiệm / Điểm nổi bật)]**.
     + Độ dài: **BẮT BUỘC DƯỚI 70 KÝ TỰ** (Lý tưởng SERP: 50 – 65 ký tự).
     + Tuyệt đối KHÔNG dùng ngoặc vuông `[]` hoặc lạm dụng dấu gạch đứng `|`.
   - **Quy chuẩn Meta Description**:
     + Viết 1-2 câu văn xuôi hấp dẫn, tự nhiên, giàu thông tin thực thể (135 – 158 ký tự), phản ánh đúng giá trị trang và kết thúc bằng một lời kêu gọi hành động (Call-To-Action - CTA) phù hợp với Search Intent.
     + CẤM triệt để các câu boilerplate mẫu rác (như `Xem chi tiết tại X để đọc đánh giá...`, `Khám phá ngay danh sách Y tại Z...`).
   - **Đồng bộ Timestamp Sitemap (`<lastmod>`)**:
     + Mỗi khi update hoặc chạy pipeline sinh/sửa metadata hàng loạt, BẮT BUỘC cập nhật trường thời gian (`updatedAt = new Date()`) trong Database để file `sitemap.xml` tự động render `<lastmod>` mới nhất, giúp bot tìm kiếm nhận diện bài được làm mới và cào lại tự nhiên.

**Quy tắc ứng phó bắt buộc (Anti-Spam/Anti-Slop):**
- Cấm nhồi nhét từ khóa, cấm tạo nội dung rác (scaled content abuse) vô giá trị.
- Nội dung AI sinh ra phải tuân thủ nghiêm ngặt văn phong tự nhiên, có số liệu/dữ liệu thực (không Hallucinate).
- Mọi Internal/External Link phải hợp lệ, không thao túng, không spam link.

## Workflow Thực Thi (Bắt buộc theo thứ tự)

1. **Phân tích yêu cầu & Đối chiếu Kiến trúc (Architecture Cross-Check)**
   - Xác định rõ nhiệm vụ là Fix Code Onpage, Setup Schema, hay Generate Content số lượng lớn (Batching).
   - **BẮT BUỘC ĐỐI CHIẾU:** Nếu task liên quan đến Route, Internal Linking, hoặc Component sinh link (vd: `SiblingLinks`, `CuisineLinks`), TRƯỚC KHI code, bắt buộc phải đối chiếu chéo (cross-check) luồng Link Juice với các bản vẽ kiến trúc gốc của dự án (vd: `silo-seo-audit-matrix.md`, `seo-audit.md`). Tuyệt đối không fix bề nổi HTML/syntax nếu luồng Link Juice đi sai mạch chảy kiến trúc (VD: Cấp 2 phải trỏ dọc xuống Cấp 3).
   - Nếu là Generate Content: Không để model tự "bịa" nội dung (Hallucinate). Phải nạp dữ liệu thực tế (Score, Ratings, Installs, Developer...) vào system prompt trước khi viết.

2. **Áp dụng Nguyên Tắc SEO & Content (Anti-AI Slop)**
   - **Văn phong**: Tránh tuyệt đối các cụm từ sáo rỗng của AI (như "In today's digital world", "Delve into", "Tapestry"). Tiêu đề linh hoạt theo ngữ cảnh, không rập khuôn kiểu "Why Choose...".
   - **DOM Structure**: Dùng đầy đủ Heading, Paragraph, List. CẤM dùng thẻ `<a>` để bọc block-level elements lớn (như `<div class="card">`). Dùng CSS pseudo-elements (`::before`/`::after`) để phủ clickable area.
   - **Link Rules**: TẤT CẢ thẻ `<a>` phải có thuộc tính `title` giải thích ngữ cảnh đích đến (không được trùng lặp với nhãn ngắn UI). KHÔNG chèn trực tiếp ký tự trang trí (`→`, icon) vào text của `<a>`, phải bọc trong `<span aria-hidden="true">`. Phải có rel="noopener noreferrer" cho thẻ link ra ngoài. CẤM thẻ `<a>` rỗng (thiếu href hợp lệ hoặc thiếu alt ảnh).

3. **Cấu hình Chiến Thuật Tối Ưu Quota (Chỉ áp dụng khi Generate số lượng lớn)**
   - **Round-Robin Models**: Luân phiên gọi các model để tránh lỗi `429 Too Many Requests`: `gemini-2.5-flash`, `gemini-3.1-flash-lite`, `gemma-4-26b-a4b-it`, `gemma-4-31b-it`.
   - Dòng Gemma giúp đa dạng hóa văn phong, qua mặt bộ lọc Anti-AI của Google.

4. **Khai báo GEO & Schema (Nếu viết bài Markdown)**
   - CẤM chèn HTML/JSON thủ công vào thân bài (Ví dụ `<script type="application/ld+json">` hay `<div class="geo-direct-answer">`).
   - Sử dụng YAML Frontmatter ở đầu bài viết để hệ thống tự động render:
     - `geo_answer`: Tóm tắt nhanh 2-3 câu cho Featured Snippets.
     - `faqs`: Danh sách câu hỏi và câu trả lời.

5. **Kiểm duyệt (SEO Auditor Gate - TRƯỚC KHI BÁO HOÀN THÀNH)**
   - Sau khi code xong (đặc biệt UI Components chứa link), chạy lệnh: `node C:\Users\Opengate\.gemini\config\scripts\anchor-seo-auditor.cjs` (từ root dự án).
   - KHÔNG ĐƯỢC báo hoàn thành nếu Linter báo lỗi. Agent phải tự fix toàn bộ lỗi thẻ `<a>` cho đến khi báo "✅ Tuyệt vời! Toàn bộ thẻ <a> trong dự án đều tuân thủ 100% chuẩn SEO".

6. **Chạy Google SEO Tool (Khi phân tích GSC)**
   - Lệnh: `docker compose run --rm app node gsc-analyzer.js --site "https://<domain-du-an>/" --days 30 --limit 5000` tại `D:\Project\google-seo-tool`.
   - Phân tích báo cáo trong thư mục `reports/` trước khi phản hồi người dùng.