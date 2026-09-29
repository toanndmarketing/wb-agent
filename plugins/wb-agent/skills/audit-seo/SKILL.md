---
name: audit-seo
description: "Audit SEO & UI/UX toàn diện website (Hỏi chọn cấp độ Static/Dynamic/Hunter/Batch/Live-Domain + Quét lỗi)"
---

# 🔍 /audit-seo — Quy Trình Audit SEO & UI/UX Toàn Diện

> **Mục tiêu**: Rà soát, tìm bug SEO & UI/UX trên 1 hoặc nhiều website / live domain, xuất báo cáo điểm số và danh sách fix ưu tiên.

---

## 🛑 BẮT BUỘC: TRẠM XÁC NHẬN BAN ĐẦU (INTERACTIVE CONFIRMATION GATE)

Khi lệnh này được kích hoạt (hoặc gõ `/audit-seo`), Agent **TUYỆT ĐỐI KHÔNG TỰ Ý CHẠY NGAY**. Bắt buộc phải hỏi User xác nhận 1 trong 5 Chế Độ Audit dưới đây:

### Trích xuất Trắc Nghiệm Chọn Mode Audit:

```
🔍 Anh muốn chạy Audit SEO & UI/UX theo chế độ nào?

1️⃣ Cấp 1 — Static Scan (Quét tĩnh Source Code):
   ⚡ Siêu nhanh, không cần build. Check hardcode secrets, thẻ <a> thiếu title, href="#", <a> bọc div, thiếu alt/dimensions, ảnh PNG/JPG chưa nén WebP.

2️⃣ Cấp 2 — Dynamic Browser Audit (Single Site - Local build):
   🌐 Build + Puppeteer browser test 1 site. Check DOM (H1, Canonical, Schema), Console errors, UI/UX (GEO box, FAQ Accordion, Navigation), Core Web Vitals (LCP, CLS, INP).

3️⃣ Cấp 3 — Hunter Deep Audit (Rà soát chuyên sâu Source):
   🎯 Single site full scan + Lighthouse CLI + Sitemap vs DB Cross-check + Ghost URLs + Orphan Pages + Keyword Cannibalization toàn site.

4️⃣ Cấp 4 — Live Domain Crawler (Quét Domain Thực Tế Đang Chạy - 100% 0 API):
   🌐 Crawl URL thực tế online (Sitemap.xml, Broken Links 404/5xx, Redirect chains, Onpage H1/Title/Meta/Schema JSON-LD, Orphan Pages, Image Alt).

5️⃣ Batch Mode — Audit hàng loạt (10+ Dự án):
   🚀 Tự quét toàn bộ workspace, phát hiện tất cả project, build và audit từng site lần lượt → Xuất 1 Báo cáo Tổng Hợp batch-audit-summary.md.
```

Agent tóm tắt lại: *"Anh chọn Chế độ [1/2/3/4/5] cho trang [URL/Workspace]. Em bắt đầu chạy nhé?"* → **Chờ User xác nhận mới thực thi.**

---

## 📋 Chi Tiết Các Chế Độ Audit (Sau Khi User Chọn)

### Mode 1: Static Code Audit (`--level 1`)
- Không cần build project, chỉ đọc AST & Source code. 
- **Bắt buộc**: Phải chạy lệnh Linter `node C:\Users\Opengate\.gemini\config\scripts\anchor-seo-auditor.cjs` (hoặc `npm run audit:seo`) để quét các lỗi SEO thẻ `<a>` ẩn (như thiếu title, thẻ a bọc div, mũi tên trong link text).
- Output: Lập báo cáo `code-audit-report.md`.

### Mode 2: Dynamic Browser Audit (`--level 2`)
- Build + Puppeteer browser thực tế. Output: `qa-audit-report.md` + Screenshots.

### Mode 3: Hunter Deep Audit (`--level 3`)
- Triệu hồi Đội Đặc Nhiệm rà soát hệ thống lớn. Output: `qa-audit-report.md` + `fix-checklist.md`.

### Mode 4: Live Domain Crawler (`--live`)
- Crawl domain production thực tế (0 API):
  `node "C:\Users\Opengate\.gemini\config\scripts\live-seo-auditor.mjs" <URL> --max-pages=50`
- Output: `live-seo-report.md` (Điểm SEO Health Score, Critical 404, Orphan pages, Duplicate Title/H1, Schemas, Actionable checklist).

### Mode 5: Batch Audit Multi-Projects (`--batch`)
- Quét đồng loạt tất cả dự án trong workspace. Output: `batch-audit-summary.md` (Báo cáo tổng hợp điểm số + lỗi Critical từng site).

---

## 📊 Bảng Điểm & Tiêu Chí Chấm ([seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md))
- Lỗi 🔴 Critical: -10đ đến -15đ/lỗi.
- Lỗi 🟡 Warning: -3đ đến -5đ/lỗi.
- **Score ≥ 80 → ✅ PASS** | **Score < 80 → ❌ BLOCK DEPLOY**.

---

## 🧬 Mode 6: Content Semantic Audit (`--level 6` hoặc `--semantic`)

> **Bài học Core Update 09/2026**: Các mode 1-5 chỉ kiểm tra **cú pháp & cấu trúc kỹ thuật**, hoàn toàn BỎ SÓT các lỗi về **ngữ nghĩa, factual accuracy, AI batch footprint** — chính là nguyên nhân bị Google phạt.

### Khi nào BẮT BUỘC chạy Mode 6:
- Sau khi pipeline AI sinh content batch (>= 3 bài)
- Sau khi refactor/batch-update hàng loạt bài viết
- Khi Google Core Update / Spam Update xảy ra và site bị ảnh hưởng

### 6 Checkpoint bắt buộc:

| # | Checkpoint | Phát hiện gì | Cách quét |
|:---:|:---|:---|:---|
| 1 | **AI Template Fingerprint** | Thẻ `geo-direct-answer` HTML cứng trong markdown, intro word-for-word > 3 bài, description rập khuôn > 3 bài | Regex scan toàn bộ `content/posts/` |
| 2 | **Batch Timestamp Footprint** | > 5 bài cùng `updatedAt` chính xác đến giây, hoặc `updatedAt < createdAt` (nghịch lý thời gian) | Parse frontmatter, group by timestamp |
| 3 | **Content Loop Detection** | Bảng/đoạn markdown bị lặp >= 2 lần trong cùng 1 file (AI generation loop) | Hash từng block markdown, phát hiện duplicate |
| 4 | **Duplicate Canonical Cross-Check** | 1 bài xuất hiện >= 2 URL khác nhau trong sitemap (cả 2 tự canonical về chính nó) | Parse sitemap.js output, group by content source |
| 5 | **Cannibalization Deep Scan** | >= 2 bài cùng target exact match keyword (title + H1 + description overlap > 60%) | TF-IDF similarity matrix trên title + description |
| 6 | **Factual Accuracy Spot Check** | Lỗi sai kiến thức chuyên ngành (ngũ hành, phân loại sao, thuật ngữ bịa) | Agent review ngẫu nhiên 10% bài hoặc script pattern match blacklist terms |

### Blacklist Terms (Auto-Flag nếu phát hiện):
- Gán sai nhóm sao: `sát tinh` đi kèm `Lộc Tồn|Thiên Khôi|Thiên Việt|Tả Phù|Hữu Bật`
- Ngũ hành sai chiều: `Mộc sinh Thủy|Thổ khắc Hỏa|Kim sinh Hỏa|Thủy sinh Kim`
- Thuật ngữ bịa: `Thái Bạch` (trên thiên bàn Tử Vi), `song cô` = cát tinh
- Bát Tự sai: nhầm `Niên Trụ` = `Nhật Chủ`

### Output: `content-semantic-audit.md`
- Danh sách file + dòng + loại lỗi + mức độ (Critical / Warning)
- Tổng điểm Content Quality Score (0-100)
- **Score < 70 → ❌ BLOCK DEPLOY** (nghiêm ngặt hơn technical audit)

