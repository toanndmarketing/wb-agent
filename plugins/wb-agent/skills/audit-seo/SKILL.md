---
name: audit-seo
description: "Audit SEO & UI/UX toàn diện website (Hỏi chọn cấp độ Static/Dynamic/Hunter/Batch + Quét lỗi)"
---

# 🔍 /audit-seo — Quy Trình Audit SEO & UI/UX Toàn Diện

> **Mục tiêu**: Rà soát, tìm bug SEO & UI/UX trên 1 hoặc nhiều website, xuất báo cáo điểm số và danh sách fix ưu tiên.

---

## 🛑 BẮT BUỘC: TRẠM XÁC NHẬN BAN ĐẦU (INTERACTIVE CONFIRMATION GATE)

Khi lệnh này được kích hoạt (hoặc gõ `/audit-seo`), Agent **TUYỆT ĐỐI KHÔNG TỰ Ý CHẠY NGAY**. Bắt buộc phải hỏi User xác nhận 1 trong 4 Chế Độ Audit dưới đây:

### Trích xuất Trắc Nghiệm Chọn Mode Audit:

```
🔍 Anh muốn chạy Audit SEO & UI/UX theo chế độ nào?

1️⃣ Cấp 1 — Static Scan (Quét tĩnh Source Code):
   ⚡ Siêu nhanh, không cần build. Check hardcode secrets, thẻ <a> thiếu title, href="#", <a> bọc div, thiếu alt/dimensions, ảnh PNG/JPG chưa nén WebP.

2️⃣ Cấp 2 — Dynamic Browser Audit (Single Site - Mặc định):
   🌐 Build + Puppeteer browser test 1 site. Check DOM (H1, Canonical, Schema), Console errors, UI/UX (GEO box, FAQ Accordion, Navigation), Core Web Vitals (LCP, CLS, INP).

3️⃣ Cấp 3 — Hunter Deep Audit (Rà soát chuyên sâu):
   🎯 Single site full scan + Lighthouse CLI + Sitemap vs DB Cross-check + Ghost URLs + Orphan Pages + Keyword Cannibalization toàn site.

4️⃣ Batch Mode — Audit hàng loạt (10+ Dự án):
   🚀 Tự quét toàn bộ workspace, phát hiện tất cả project, build và audit từng site lần lượt → Xuất 1 Báo cáo Tổng Hợp batch-audit-summary.md.
```

Agent tóm tắt lại: *"Anh chọn Chế độ [1/2/3/4] cho trang [URL/Workspace]. Em bắt đầu chạy nhé?"* → **Chờ User xác nhận mới thực thi.**

---

## 📋 Chi Tiết 4 Chế Độ Audit (Sau Khi User Chọn)

### Mode 1: Static Code Audit (`--level 1`)
- Không cần build project, chỉ đọc AST & Source code. Output: `code-audit-report.md`.

### Mode 2: Dynamic Browser Audit (`--level 2`)
- Build + Puppeteer browser thực tế. Output: `qa-audit-report.md` + Screenshots.

### Mode 3: Hunter Deep Audit (`--level 3`)
- Triệu hồi Đội Đặc Nhiệm rà soát hệ thống lớn. Output: `qa-audit-report.md` + `fix-checklist.md`.

### Mode 4: Batch Audit Multi-Projects (`--batch`)
- Quét đồng loạt tất cả dự án trong workspace. Output: `batch-audit-summary.md` (Báo cáo tổng hợp điểm số + lỗi Critical từng site).

---

## 📊 Bảng Điểm & Tiêu Chí Chấm ([seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md))
- Lỗi 🔴 Critical: -10đ đến -15đ/lỗi.
- Lỗi 🟡 Warning: -3đ đến -5đ/lỗi.
- **Score ≥ 80 → ✅ PASS** | **Score < 80 → ❌ BLOCK DEPLOY**.
