---
name: live-seo-audit
description: "Crawl & Audit SEO Technical + Onpage thực tế trên Live Domain (100% Thư viện Local - 0 API Key)"
triggers:
  - "audit live domain"
  - "quét domain"
  - "quét website"
  - "audit seo live"
  - "tìm bug seo thực tế"
  - "check broken links live"
---

# 🔍 /live-seo-audit — Crawl & Audit SEO Live Domain

> **Mục tiêu**: Tự động crawl toàn bộ domain đang chạy online (Live URL), quét sitemap, bóc tách onpage (Title, Meta, H1-H6, Schema JSON-LD, Canonical, Robots, Images alt), phát hiện Broken links (404/5xx), Redirect chains, Trang mồ côi (Orphan pages) và tính điểm SEO Health Score. Hoàn toàn chạy bằng thư viện Node.js local, **không cần bất kỳ API key bên thứ 3 nào**.

---

## 🚀 Cách Kích Hoạt & Lệnh Chạy

Khi User yêu cầu quét một website hoặc gõ `/live-seo-audit <URL>`:

### 1. Lệnh Quét Mặc Định (Fast Crawl 50 pages):
```powershell
node "C:\Users\Opengate\.gemini\config\scripts\live-seo-auditor.mjs" <URL_DOMAIN> --max-pages=50 --output="live-seo-report.md"
```

### 2. Lệnh Quét Mở Rộng (Nhiều trang / Tuỳ chỉnh Concurrency):
```powershell
node "C:\Users\Opengate\.gemini\config\scripts\live-seo-auditor.mjs" <URL_DOMAIN> --max-pages=200 --concurrency=10 --output="live-seo-report.md"
```

---

## 📊 Tiêu Chí Phân Tích & Báo Cáo

Script tự động phân loại các vấn đề thành 3 cấp độ:

### 🔴 1. Critical Bugs (Chặn Index / Phạt nặng):
- **Broken Links / Lỗi 4xx/5xx**: URL nội bộ hoặc liên kết ngoài trả về lỗi.
- **Thiếu thẻ `<title>` hoặc thẻ `<h1>`**: Trang bị khuyết tiêu đề cấu trúc chính.
- **Thẻ `noindex` đặt nhầm**: Các trang đích bị chặn index ngoài ý muốn.
- **Lỗi cú pháp Schema JSON-LD**: `application/ld+json` bị lỗi parse JSON (Invalid format).
- **Lỗi Sitemap.xml**: URL trong sitemap nhưng truy cập thực tế lại bị lỗi 404/500.

### 🟡 2. Warnings (Ảnh hưởng Ranking & UX):
- **Trùng lặp Title / Trùng lặp H1 (Cannibalization)**: Nhiều URL dùng chung 1 tiêu đề.
- **Chứa nhiều hơn 1 thẻ `<h1>`**: Vi phạm chuẩn 1 H1 duy nhất trên page.
- **Thiếu Meta Description**: Không có đoạn mô tả hiển thị trên kết quả tìm kiếm.
- **Trang Mồ Côi (Orphan Pages)**: Trang có trong Sitemap nhưng không nhận được link nội bộ nào.
- **Canonical Mismatch**: Thẻ canonical trỏ sai so với URL thực tế.
- **Hình ảnh thiếu `alt`**: Mất cơ hội SEO Google Images.
- **Thin Content**: Trang quá ngắn (< 250 từ).

### 🟢 3. Actionable Fix Checklist:
- Tự động sinh danh sách việc cần làm (Checklist markdown) để Agent hoặc Dev tick chọn và tiến hành fix code ngay.

---

## 📋 Quy Trình Thực Thi Của Agent

1. **Nhận URL mục tiêu**: Chuẩn hóa URL (đảm bảo có `https://`).
2. **Chạy Script**: Thực thi lệnh PowerShell gọn (1 dòng duy nhất).
3. **Đọc & Trình Bày Báo Cáo**: Đọc file `live-seo-report.md` vừa xuất, tóm tắt điểm số SEO Health (0-100), nêu bật top 3 lỗi Critical cần fix ngay, và gửi kèm link file clickable `[live-seo-report.md](file:///path/to/live-seo-report.md)`.

---

## 🧬 Content Semantic Checks (BẮT BUỘC bổ sung từ 09/2026)

> **Lỗ hổng cũ**: Live crawler chỉ quét HTML output (title, meta, schema, broken links) nhưng KHÔNG phát hiện: duplicate canonical trong sitemap, AI batch footprint, content loop, factual errors.

### Khi crawl Live Domain, BẮT BUỘC kiểm tra thêm:

| # | Check | Cách phát hiện | Severity |
|:---:|:---|:---|:---:|
| 1 | **Duplicate Canonical** — 2+ URL cùng nội dung đều self-canonical | So sánh canonical tag vs actual URL vs sitemap entries | 🔴 Critical |
| 2 | **Sitemap Ghost URLs** — URL trong sitemap trả 301/404 | Cross-check sitemap.xml vs HTTP status | 🔴 Critical |
| 3 | **Batch Timestamp** — Nhiều trang cùng `dateModified` chính xác đến giây trong Schema JSON-LD | Parse `dateModified` từ JSON-LD, group by exact value | 🟡 Warning |
| 4 | **Template Fingerprint** — Nhiều trang cùng exact meta description hoặc cùng first paragraph | Hash description + first 200 chars body, phát hiện cluster > 3 | 🟡 Warning |
| 5 | **Canonical Mismatch** — Canonical trỏ relative (`./`) thay vì absolute URL | Check canonical tag format | 🔴 Critical |

### Actionable Output bổ sung:
- Danh sách URL duplicate canonical + đề xuất URL nào giữ, URL nào redirect
- Danh sách cluster bài trùng description + đề xuất rewrite
- **Nếu phát hiện >= 3 lỗi Critical semantic → Cảnh báo: "Site có nguy cơ bị Google Spam Update đánh"**

