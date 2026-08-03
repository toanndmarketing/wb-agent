---
name: add-module
description: "Thêm module/trang mới vào dự án (Hỏi xác nhận phạm vi + Check Anti-Cannibalization)"
---

# 🧩 /add-module — Quy Trình Thêm Module / Trang Mới

> **Mục tiêu**: Thêm module, route hoặc trang mới vào dự án có sẵn mà KHÔNG làm ảnh hưởng đến cấu trúc SEO hiện tại.

---

## 🛑 BẮT BUỘC: TRẠM XÁC NHẬN BAN ĐẦU (INTERACTIVE CONFIRMATION GATE)

Khi lệnh này được kích hoạt, Agent **TUYỆT ĐỐI KHÔNG TỰ Ý CHẠY NGAY**. Bắt buộc phải hỏi User xác nhận 2 điểm:

1. **Phạm vi công việc**:
   - Thêm Trang/Route mới hoàn toàn (VD: Trang Blog mới, Trang dịch vụ mới)
   - Thêm Component/Widget vào trang đã có sẵn (VD: Thêm FAQ Accordion, Thêm Live Search)
2. **Target Keyword & Route Cha (Silo)**:
   - Xác định từ khóa chính của module mới
   - Xác định thuộc Silo Category nào

Agent tóm tắt lại: *"Chốt lại: Thêm [Route/Widget X] vào Silo [Y] với Keyword chính là [Z]. Anh duyệt OK không?"* → **Chờ User duyệt "OK" mới bắt đầu code.**

---

## 📋 Quy Trình Thực Thi (Sau Khi User Duyệt OK)

1. **Pre-code Gate (Anti-Cannibalization A1-A3)**:
   - Rà soát Target Keyword của module mới xem có bị trùng với Homepage hoặc Hub hiện tại hay không.

2. **Triển Khai Code (`speckit.implement`)**:
   - Code module mới theo chuẩn Semantic HTML (Single H1, GEO Hero box, Dynamic Meta Title/Desc). Thẻ `<a>` có `title="..."`, KHÔNG bọc toàn bộ card `<div>`.

3. **Post-code Verification ([seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md))**:
   - Kiểm tra 19 hạng mục SEO Onpage & Performance trước khi báo hoàn tất.
