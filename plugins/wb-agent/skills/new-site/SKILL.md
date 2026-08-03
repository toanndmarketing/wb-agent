---
name: new-site
description: "Khởi tạo dự án pSEO mới từ đầu (Hỏi xác nhận Case/Stack + Full SDD 5 bước)"
---

# 🚀 /new-site — Quy Trình Triển Khai Dự Án pSEO Mới Từ Đầu

> **Mục tiêu**: Tạo khung dự án pSEO mới hoàn toàn tuân thủ SDD (Spec-Driven Development) và 100% tiêu chuẩn SEO Preflight.

---

## 🛑 BẮT BUỘC: TRẠM XÁC NHẬN BAN ĐẦU (INTERACTIVE CONFIRMATION GATE)

Khi lệnh này được kích hoạt, Agent **TUYỆT ĐỐI KHÔNG TỰ Ý THỰC THI NGAY**. Bắt buộc phải trình bày trắc nghiệm/xác nhận để User chọn:

### 1. Hỏi chọn Tech Stack & Mô hình dự án:
- **Lựa chọn A**: Next.js (App Router) + PostgreSQL + Docker (Cho Web App / pSEO quy mô lớn)
- **Lựa chọn B**: Astro + Cloudflare Pages + D1 (Cho trang tĩnh, Blog pSEO siêu nhẹ & siêu nhanh)
- **Lựa chọn C**: Custom / Yêu cầu khác

### 2. Hỏi trạng thái Dữ liệu Từ khóa:
- Đã có file CSV (Semrush / Ahrefs export)
- Đã có danh sách từ khóa thô
- Chưa có từ khóa → Cần Agent chạy `speckit.pseo-niche-research` để nghiên cứu ngách A-Z

### 3. Blueprint Chốt Ý Định:
Agent tóm tắt lại: *"Chốt lại: Khởi tạo site pSEO mảng [X], Stack [Y], Nguồn data [Z]. Anh xác nhận OK để bắt đầu không?"* → **Chờ User duyệt "OK" mới đi tiếp vào Bước 1.**

---

## 📋 Quy Trình Thực Thi 5 Bước (Sau khi User duyệt OK)

### Bước 1: Khai Báo Spec & Tech Stack (`speckit.specify`)
- Ghi đặc tả vào `.agents/specs/spec.md`.

### Bước 2: Thiết Kế Cấu Trúc Pillar-Silo 5 Cấp (`speckit.seo-content`)
- Phân loại Entity & Taxonomy, Intent Mapping, Next.js Route Mapping.
- 🛑 **TRẠM KIỂM DỊCH 1**: Dừng lại trình bày Cây Pillar-Silo chờ User duyệt "OK".

### Bước 3: Lập Tasks.md & Quota Allocation (`speckit.plan`)
- Phân rã task vào `.agents/specs/tasks.md`.

### Bước 4: Triển Khai Code (`speckit.implement` + `seo-preflight-card`)
- Coder triển khai từng module. Đối chiếu ĐẦY ĐỦ 19 hạng mục trong [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md).

### Bước 5: QA Audit & Pre-publish Check (`speckit.qa-audit`)
- 🛑 **TRẠM KIỂM DỊCH 2**: Score ≥ 80/100 VÀ 0 lỗi Critical 🔴 → Mới cho phép Deploy.
