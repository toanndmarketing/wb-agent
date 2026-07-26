---
name: speckit.debug-crawler
description: Kích hoạt khi user cần scan toàn bộ website để tìm lỗi UI/UX ẩn (JS, Console), lỗi mạng, hoặc SEO Onpage sử dụng Puppeteer + Stealth. Tool này giúp phát hiện các lỗi mà user không thể trình bày rõ ràng. Phân làm 2 cấp độ Debug.
---
# Hướng Dẫn Vận Hành Tool Puppeteer SEO & UI Scanner

Skill này hướng dẫn Agent cách triển khai và chạy một crawler dựa trên Puppeteer + Stealth để debug chuyên sâu một website. Tuy nhiên, để tối ưu thời gian xử lý, quy trình gỡ lỗi phải chia làm 2 cấp (2 Tiers).

## 1. Mục Đích Kích Hoạt
- Bắt tận tay các lỗi vỡ layout, ảnh lỗi, Hydration errors, React/Vue exceptions.
- Quét và trích xuất cấu trúc H1-H6, Schema.org, thẻ Meta SEO.
- Vượt qua WAF/Cloudflare nhờ sử dụng `puppeteer-extra-plugin-stealth`.

## 2. Phân Cấp Debug (Workflow 2 Cấp Độ) Bắt Buộc

Tuyệt đối tuân thủ nguyên tắc "Từ nhẹ đến nặng" để tiết kiệm thời gian (Time-to-resolution).

### Cấp Độ 1 (Tier 1): Debug Tiêu Chuẩn (Lightweight)
- **Khi nào áp dụng**: Áp dụng mặc định cho mọi bug UI/UX, SEO cơ bản khi mới tiếp nhận.
- **Hành động**: 
  - AI đọc code trực tiếp bằng `view_file` / `grep_search`.
  - Phân tích logic code, CSS, hoặc DOM Tree tại chỗ.
  - Sửa trực tiếp nếu nhìn thấy lỗi (sai logic, thiếu tag, sai class).
- **Kết quả**: Nếu lỗi được xử lý -> Kết thúc. Nếu fix mãi vẫn không hết, hoặc lỗi ở dạng "chạy thật mới bị mà nhìn code không ra", **chuyển sang Cấp Độ 2**.

### Cấp Độ 2 (Tier 2): Debug Chuyên Sâu (Heavyweight Crawler)
- **Khi nào áp dụng**: Cấp 1 bó tay, bug ẩn không sinh log, hoặc User chủ động yêu cầu "scan/audit toàn bộ website", "truy vết lỗi".
- **Quy trình vận hành Crawler**:
  1. Hỏi User URL gốc cần scan và tuỳ chọn quét Desktop hay Mobile.
  2. Để tối ưu dung lượng, KHÔNG `npm install` puppeteer lại từ đầu ở mỗi dự án. Hãy chạy `npm link puppeteer puppeteer-extra puppeteer-extra-plugin-stealth` tại thư mục `tmp/` để dùng bản cài global. Sau đó tạo Script Tạm (`tmp/debug_crawler.js`) với cấu hình `puppeteer-extra-plugin-stealth` chống block. KHÔNG xả rác ra project chính.
  3. Cài cắm các bẫy rập: `page.on('console')`, `page.on('pageerror')`, `page.on('response')` (bắt mã lỗi >= 400). Trích xuất thẻ SEO và gọi `screenshot()`.
  4. Thực thi file bằng Node.js và đọc kết quả quét.
  5. Viết báo cáo Tiếng Việt, tổng kết lỗi ẩn, trả về Link Clickable dạng `[Mở thư mục Screenshots](file:///C:/path/to/tmp/screenshots/)` để User kiểm tra trực quan.
