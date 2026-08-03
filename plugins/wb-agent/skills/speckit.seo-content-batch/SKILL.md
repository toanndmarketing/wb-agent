---
name: speckit.seo-content-batch
description: Quy trình gen content hàng loạt độc bản (Unique Content) cho SEO/GEO với Gemini Flash Lite, xử lý chống AI, bám sát dữ liệu thực tế và rate limit.
---

# 🤖 SPECKIT.SEO-CONTENT-BATCH

Skill này định nghĩa Quy chuẩn Khởi tạo, Thiết kế Prompt, và Cơ chế Chạy Script Hàng loạt (Batch Processing) cho các dự án cần sinh ra nội dung (Content) ĐỘC BẢN (Unique, Non-AI) số lượng lớn.

## 1. BỘ QUY TẮC TOÀN CẦU KHI GEN CONTENT ĐỘC BẢN (GLOBAL CONTENT TEAM RULES)

Để Google và User đánh giá cao chất lượng nội dung, mọi Prompt và Script Batch BẮT BUỘC phải ép LLM tuân thủ 7 Luật thép sau:

### 1.1. Naturalness & No Keyword Stuffing (Google Loves Organic Flow)
- Meta Title, Meta Description và toàn bộ bài viết BẮT BUỘC phải diễn đạt 100% tự nhiên, mượt mà, cuốn hút như nhà báo/chuyên gia du lịch viết.
- **CẤM TUYỆT ĐỐI**: Nhồi nhét từ khóa thô (Keyword Stuffing), lặp đi lặp lại tên địa điểm/thương hiệu một cách máy móc trong mọi câu.

### 1.2. Dynamic & Category-Aware Heading Structure (Strict Anti-Templating Rule)
- CẤM TUYỆT ĐỐI dùng tiêu đề dập khuôn tĩnh hay mẫu khung cố định cho mọi bài viết (ví dụ: cấm dùng lại "Why Choose [X]", "Core Features", "Introduction", "Final Verdict" hàng loạt).
- Tiêu đề `<h2>` và `<h3>` BẮT BUỘC phải sinh động và tự động điều chỉnh theo từng mảng/ngành cụ thể (Category-Aware Headings):
  - **Mảng Game / Giải trí**: Tập trung vào Gameplay loop, đồ họa, hệ thống điều khiển, trải nghiệm thực tế (ví dụ: `<h2>Gameplay Loop & Mobile Controls</h2>`).
  - **Mảng Công cụ / Tool / Productivity**: Tập trung vào giải quyết nỗi đau người dùng, tốc độ xử lý, tính năng cốt lõi (ví dụ: `<h2>Solving Daily Workflow Bottlenecks</h2>`).
  - **Mảng Giáo dục / Học tập**: Tập trung vào phương pháp học, lộ trình kiến thức, tính năng offline (ví dụ: `<h2>Curriculum Structure & Interactive Learning</h2>`).
  - **Mảng Địa điểm / Review Du lịch**: Tập trung vào món ăn, không gian, vị trí, giờ cao điểm.

### 1.3. Deep Grounding in Real Metadata & Entities (Chống Thin Content)
- Bài viết BẮT BUỘC phải trích xuất và nạp trực tiếp toàn bộ Metadata thực tế từ Database vào Prompt: **Tên nhà phát triển/Thương hiệu** (`developer`/`brand`), **Đánh giá & Điểm số** (`score`/`ratings`), **Lượt tải / Lượt truy cập** (`installs`/`views`), **Phân khúc giá / Tiền tệ** (`price`/`currency`), **Phiên bản cập nhật** (`version`).
- Việc lồng ghép các chỉ số thực tế này đảm bảo mỗi bài viết sinh ra đều chứa **Dữ liệu kiểm chứng độc bản (Data-Driven Facts)**, giúp vượt qua Google Thin Content & Helpful Content System.

### 1.4. Output Format: RAW HTML (Hỗ trợ Mục lục TOC)
- Trả về `seoContent` dưới dạng **RAW HTML thô** (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`).
- Cấm bọc thẻ `<html>` hay `<body>`. Thẻ `<h2>`/`<h3>` phải rõ nghĩa để giao diện Frontend tự động parse làm **Mục Lục (Table of Contents - TOC)**.

### 1.5. No AI Buzzwords (Banned Clichés List)
- **CẤM TUYỆT ĐỐI** các từ ngữ AI sáo rỗng: *nestled, a rich tapestry, delve into, hidden gem, a testament to, moreover, in conclusion, mouth-watering, unforgettable, beacon of, vibrant hub, boasts, seamlessly, dive into, paradisal*.
- Viết bằng giọng văn báo chí chân thật, sắc sảo, tự nhiên.

### 1.6. EEAT & Imperfect Sentiment Rule (Tạo độ tin cậy với Google)
- Đưa vào các chi tiết cảm quan góc nhìn thứ nhất (không khí, ánh sáng, độ ồn, giờ cao điểm).
- Lồng ghép 1-2 nhận xét/lưu ý thực tế (nhược điểm nhỏ hoặc kinh nghiệm thực tế, ví dụ: *"Khu vực đậu xe hơi hẹp vào cuối tuần"*, *"Nên xếp hàng sớm trước 12h trưa"*). Đánh giá 100% màu hồng sẽ bị Google nghi ngờ.

### 1.7. Project Niche Prompt Analysis Protocol (Bắt Buộc Phân Tích Prompt Ngách Dự Án)
- **CẤM DÙNG PROMPT CHUNG CHUNG**: Không bao giờ dùng 1 prompt rập khuôn cho tất cả các dự án.
- **BẮT BUỘC ĐỌC/LẬP FILE NGHÁCH DỰ ÁN**: Trước khi gen content cho bất kỳ dự án nào, Agent phải chủ động truy xuất hoặc khởi tạo tài liệu Đặc Tả Prompt Ngách (ví dụ: `.agents/specs/niche-content-spec.md` hoặc `.agents/specs/restaurant-review-structure/spec.md`).
- **4 YẾU TỐ BẮT BUỘC PHẢI PHÂN TÍCH CHO PROMPT NGHÁCH DỰ ÁN**:
  1. **Địa lý & Giao thông đặc thù (Local GEO Anchors)**: Đơn vị vận chuyển, bến xe/trạm MRT/hải quan, tên sân bay, cách di chuyển phổ biến của địa phương đó (VD: Singapore/JB thì nhắc Woodlands, Kranji MRT, JB CIQ; Miami thì nhắc Metromover, Calle Ocho).
  2. **Tiền tệ & Mức giá local**: Đơn vị tiền tệ chính (SGD, MYR, USD, VND...), phân cấp phân khúc giá (Budget, Mid-range, Fine Dining).
  3. **Thuật ngữ & Văn hóa ngách (Niche Lingo & Cultural Context)**: Các từ ngữ chuyên môn ngách (VD: Ẩm thực hawker, Kopi-O, Halal certified, Spa wellness, Night market).
  4. **Chân dung người dùng mục tiêu (Audience Persona)**: Khách du lịch gia đình, backpacker, khách công tác cross-border, hay dân địa phương.
- **CÔNG THỨC PROMPT CHUẨN**: `[Bộ Quy Tắc Vàng Global Rules 1.1-1.6]` + `[Phân Tích Prompt Ngách Dự Án 1.7]` = **PROMPT TỐI ƯU CUỐI CÙNG**.

---

## 2. QUẢN LÝ API KEYS TRÊN GLOBAL
Để tiện lợi và không bị rác thư mục mã nguồn dự án, bộ Keys OAuth của Google Gemini (hoặc API keys khác) BẮT BUỘC được lưu tại biến Global của Agent:
- **Đường dẫn**: `C:\Users\Opengate\.gemini\config\credentials\gemini_keys.json`
- Mọi script Batch cần truy xuất file này để load mảng Keys. Nó giúp tận dụng nhiều Keys luân phiên xử lý để nhân hệ số Quota.

## 3. CHIẾN LƯỢC CHẠY BATCH THÔNG MINH (HIGH-THROUGHPUT)
### 3.1. Idempotent Design (Chống chạy đè)
Mọi script chạy Batch **phải có cờ trạng thái** lưu ở Database (ví dụ: `isSeoOptimizedByAgent: boolean`).
- **Fetch**: Query DB chỉ lấy những row `where { isSeoOptimizedByAgent: false }`.
- **Save**: Update row set `isSeoOptimizedByAgent: true`.
- **Lợi ích**: Script có thể Stop/Start bất kỳ lúc nào, đứt mạng hay crash app, lần gõ lệnh tiếp theo nó sẽ tự động bỏ qua những data đã chạy, tiếp tục ngay chỗ bị ngắt.

### 3.2. Ép xung Concurrency với Model Phù Hợp
Với dữ liệu lớn (>1.000 records), TUYỆT ĐỐI KHÔNG dùng Model Pro.
- **Model chuẩn**: Ưu tiên gọi tuyến `gemini-3.5-flash-lite` hoặc `gemini-3.5-flash` qua API. Các model dòng "Flash Lite" sinh text tốc độ cực cao và hạn mức (Quota) miễn phí dồi dào.
- **Concurrency**: Khi có mảng Keys, cấu hình xử lý luân phiên và có khoảng chờ nhẹ giữa các batch để vắt kiệt tối đa băng thông API mà không bị lỗi `429 Too Many Requests`.

### 3.3. Auto-Retry & Auto Model Fallback Logic
Script BẮT BUỘC phải có khối try-catch để bắt lỗi 429 (Rate Limit). Khi gặp 429, không được Crash, mà phải kết hợp 2 kỹ thuật:
1. **Sleep Delay**: `await setTimeout(5000)` để giảm tải cho Key.
2. **Model Rotation (Xoay vòng Model)**: Tự động đổi sang model khác trong mảng dự phòng trước khi gọi lại (đệ quy).

**Mảng các Model Free & Quota lớn đã được verify (NÊN DÙNG):**
```javascript
const FALLBACK_MODELS = [
  'models/gemini-3.5-flash-lite',
  'models/gemini-2.5-flash',
  'models/gemini-2.0-flash-lite',
  'models/gemini-2.0-flash'
];
```

### 3.4. Safe JSON Parsing (Xử lý bóc tách JSON an toàn)
Sử dụng hàm `safeParseJSON` bóc tách sạch khối markdown codeblock ` ```json ... ``` ` và xử lý các ký tự xuống dòng chưa escape trong văn bản HTML trước khi thực hiện `JSON.parse()`.

---

## 4. WORKSPACE-SPECIFIC SCRIPT GENERATION
Vì mỗi dự án có Database Schema và Yêu cầu Prompt khác nhau, Agent không được viết code Batch chung chung, mà BẮT BUỘC thực hiện các bước sau tại từng Workspace cụ thể:
1. **Đọc Project-Specific Rules**: Đọc các file cấu hình tại `.agents/specs/` hoặc `schema.prisma` để hiểu cấu trúc Table cần Update.
2. **Gen File Script Chuyên Biệt**: Dựa vào DB Schema, Agent tạo file script Node.js / TypeScript (ví dụ `generate_content_gemini.ts`) đặt ngay trong thư mục mã nguồn dự án.
3. **Đồng bộ Dual-Sync**: Luôn lưu 1 bản copy script vào `.agents/scripts/` để lưu trữ lâu dài.
