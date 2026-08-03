---
name: speckit.plan
description: Lập implementation plan chi tiết từ spec đã duyệt
---

## 🎯 Mission
Chuyển spec.md (WHAT) thành plan.md (HOW). Sử dụng tư duy **Goal-Backward** để đảm bảo kế hoạch dẫn trực tiếp tới Success Criteria.

## 📋 Protocol

### Phase 0: Research & Deep Context Scan ⭐
- **Deep Context Scan**: BẮT BUỘC rà soát triệt để các file Báo cáo Audit gần nhất (`seo_*.md`, `debug-report.md`), tài liệu workflow dự án (ví dụ `12-seo-geo.md`), kiến trúc hiện tại, và spec trong `.agent/specs/`.
- **Anti-Surface Fix**: Đảm bảo Plan giải quyết triệt để nguyên nhân gốc rễ và chuẩn hóa kiến trúc tổng thể (ví dụ: Sitemap Index, Router hierarchy), KHÔNG lên kế hoạch sửa bề nổi/tạm bợ.
- Scan spec → liệt kê unknowns ("NEEDS CLARIFICATION").
- Nghiên cứu giải pháp → ghi vào `research.md`.

### Phase 1: Data Model
- Từ entities trong spec → tạo `data-model.md`.
- Xác định relationships (1:N, N:N).

### Phase 2: API Contracts
- Từ User Scenarios → tạo `contracts/[entity].md`.

### Phase 3: Architecture
- Tạo `plan.md` với: Folder structure, Component hierarchy, State management, Docker topology.

### Phase 4: Must-Haves (Goal-Backward) ⭐
Xác định các thành phần bắt buộc để đạt được "Success Criteria":
- **Truths**: Các logic đúng đắn tuyệt đối.
- **Artifacts**: Các file/output then chốt.
- **Key Links**: Liên kết giữa các module.

### Gate Check (Kiểm duyệt gắt gao trước khi chốt Plan)
- **Constitution Compliance**: So sánh plan vs `constitution.md` → BÁO LỖI nếu vi phạm rules.
- **Strict SEO & Architecture Verification** (Nếu dự án có `seo_standards.md`):
  - **Soft 404 Prevent**: Plan đã có cơ chế catch dữ liệu rỗng (null/empty) và trả về HTTP 404 (`notFound()`) để diệt triệt để lỗi Soft 404 chưa?
  - **Core Web Vitals**: Plan đã chỉ định dùng `<Image priority>` thay thế `<img>` thuần cho ảnh Above-the-fold để đảm bảo LCP < 2.5s chưa?
  - **GEO Architecture**: Component Direct Answer/Summary có được đặt ở vị trí cao nhất (ngay dưới H1, Above-the-fold) chưa?
  - **Schema Completeness**: Plan đã vẽ rõ JSON-LD (WebPage, BreadcrumbList, Article) sẽ được tiêm vào thẻ `<script>` như thế nào chưa?

## 🚫 Guard Rails
- KHÔNG viết code trong bước planning.
- PHẢI check constitution compliance & Strict SEO Verification.