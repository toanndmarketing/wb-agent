---
name: seo-audit
description: Chạy SEO Audit Tool từ bất kỳ project nào — phân tích On-page, Off-page, xuất report có Agent Instructions.
---

# 🔍 SEO Audit Skill

## Mục đích
Cho phép Agent ở BẤT KỲ project nào gọi `google-seo-tool` để audit SEO, nhận report có **AGENT INSTRUCTIONS** và thực thi tối ưu.

## Cách sử dụng

Khi user yêu cầu audit SEO, phân tích SEO, hoặc tối ưu SEO cho project hiện tại:

### Bước 1: Xác định thông tin

Cần xác định 2 thông tin:
- **SITE_URL**: URL website production (ví dụ: `https://livescoreall.com/`)
- **PROJECT_DIR**: Đường dẫn workspace hiện tại (lấy từ user context)

### Bước 2: Chạy SEO Tool

Tool nằm tại: `d:\Project\google-seo-tool\cli.js`

```powershell
# === FULL AUDIT (6 modules an toàn, tự động) ===
node d:\Project\google-seo-tool\cli.js full-audit --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports --max-pages 100

# === MODULES RIÊNG LẺ (chạy khi user yêu cầu cụ thể) ===

# Technical SEO Audit (Toàn bộ trang từ sitemap)
node d:\Project\google-seo-tool\cli.js audit --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports --max-pages 100

# Single Page SEO Audit & Google URL Inspection (Kiểm tra trang cụ thể & trạng thái Google Indexing, lý do chưa index, schema errors)
node d:\Project\google-seo-tool\cli.js audit --site <SITE_URL> --url <TARGET_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports

# Sitemap Health
node d:\Project\google-seo-tool\cli.js sitemap --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports

# Internal Link Graph
node d:\Project\google-seo-tool\cli.js internal --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports --max-pages 100

# Content Decay (cần GSC auth)
node d:\Project\google-seo-tool\cli.js decay --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports

# Top Pages (cần GSC auth)
node d:\Project\google-seo-tool\cli.js top-pages --site <SITE_URL> --output-dir <PROJECT_DIR>\.agent\seo-reports
```

### Bước 3: Đọc Report và Thực Thi

Sau khi chạy xong, đọc file report trong `<PROJECT_DIR>\.agent\seo-reports\`:

1. Mở file `.md` mới nhất trong thư mục `.agent/seo-reports/`
2. Tìm section `## 🤖 AGENT INSTRUCTIONS`
3. Thực thi từng action theo thứ tự priority: `P0-CRITICAL` → `P1-HIGH` → `P2-MEDIUM`

## Các Commands Khả Dụng

### 🟢 An toàn — chạy bất cứ lúc nào
| Command | Chức năng |
|---------|----------|
| `full-audit` | Chạy 6 modules phân tích tự động |
| `audit` | Kiểm tra lỗi kỹ thuật SEO (title, meta, H1, schema...) của toàn bộ trang từ sitemap |
| `audit --url <URL>` | Kiểm tra On-page chi tiết + Google URL Inspection (Trạng thái index, lý do chưa index, Canonical, Schema errors) cho 1 URL cụ thể |
| `sitemap` | Kiểm tra sitemap URLs (404, redirect, 5xx) |
| `internal` | Phân tích internal link graph, orphan pages |
| `decay` | Phát hiện trang sụt traffic (cần GSC) |
| `top-pages` | Dashboard top pages (cần GSC) |
| `geo` | Phân tích theo quốc gia & thiết bị (cần GSC) |

### 🟠 Thủ công — CHỈ khi user yêu cầu
| Command | Chức năng | Lý do manual |
|---------|----------|-------------|
| `outbound` | Audit outbound links | HEAD check external sites |
| `mentions` | Tìm brand mentions | Tốn CSE quota (100/ngày) |
| `broken-links` | Tìm broken link building opportunities | Crawl external sites |
| `content-gap` | So sánh content vs đối thủ | Tốn CSE quota |

### 🔴 CHỈ khi user ra lệnh trực tiếp
| Command | Chức năng | Lý do |
|---------|----------|-------|
| `index` | Submit URLs lên Google Indexing API | GHI dữ liệu, dùng quota |

## Lưu ý quan trọng

- **CWD**: Luôn chạy từ thư mục `d:\Project\google-seo-tool` hoặc dùng absolute path
- **GSC modules** (decay, top-pages, geo): Cần `--site` là URL property GSC (ví dụ `https://example.com/` hoặc `sc-domain:example.com`)
- **Crawler modules** (audit, sitemap, internal, outbound): Có thể dùng `--sitemap` thay cho `--site`
- **Reports**: Mỗi lần chạy tạo 2 file: `.md` (người đọc + agent) và `.json` (data structured)
- **Rate limiting**: Dùng `--concurrency 3 --delay 300` nếu site nhỏ/server yếu
