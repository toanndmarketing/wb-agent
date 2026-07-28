---
name: speckit.specify
description: Viết spec.md từ yêu cầu user — chuyển WHAT thành tài liệu kỹ thuật
---

## 🎯 Mission
Chuyển mô tả ngôn ngữ tự nhiên → spec.md chuẩn hóa (WHAT, không phải HOW).

## 📥 Input
- Mô tả feature từ developer (text tự do)
- `.agent/memory/constitution.md` (constraints)

## 📋 Protocol
1. Đọc mô tả → trích xuất:
   - **Actors**: Ai tương tác? (User, Admin, System, Guest)
   - **Actions**: Làm gì? (CRUD, search, filter, export)
   - **Data**: Dữ liệu gì? (entities, fields, relationships)
   - **Techstack Constraints (CỰC KỲ QUAN TRỌNG)**: 
     + Framework Frontend/Backend là gì?
     + Database lưu ở đâu? (Supabase, Firebase, Cloud Riêng, AWS RDS, v.v.)
     + Hạ tầng Deploy (Vercel, Cloudflare, VPS tự quản)?
     + *Nếu không tìm thấy thông tin này trong Prompt hoặc `.agent/memory/constitution.md`, BẮT BUỘC PHẢI DỪNG LẠI HỎI USER. Cấm tự ý giả định.*
   - **Constraints**: Giới hạn gì? (auth, permissions, limits)
2. Tạo `.agent/specs/[feature]/spec.md` với format BẮT BUỘC:
   ```markdown
   ---
   title: [Feature Name]
   status: DRAFT
   version: 1.0.0
   created: [date]
   ---
   ## 1. Overview
   [1-2 câu mô tả]

   ## 2. User Scenarios
   - **US1**: As a [actor], I want to [action], so that [value].
   - **US2**: ...

   ## 3. Functional Requirements
   - FR01: [requirement cụ thể, measurable]

   ## 4. Non-Functional & SEO Requirements
   - NFR01: Response time < 2s
   - **SEO & Architecture (BẮT BUỘC ĐỐI VỚI PUBLIC PAGE)**:
     - **Target Keyword:** [Từ khóa chính thức của trang này là gì?]
     - **Silo Architecture:** [Trang này là Home, Pillar, Silo hay Cluster? Nó nằm ở nhánh nào?]
     - *Lưu ý: Nếu User chưa cung cấp 2 thông tin trên, DỪNG LẠI và hỏi rõ User trước khi chốt Spec.*

   ## 5. Success Criteria
   - [ ] SC01: [testable criterion]
   ```
3. Mỗi User Scenario PHẢI có: Actor + Action + Value.
4. Mỗi Functional Requirement PHẢI measurable (có số liệu cụ thể).

## 📤 Output
- File: `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- **NO ASSUMED TECHSTACK**: KHÔNG BAO GIỜ tự ý mặc định Database là Supabase hay Firebase nếu User không nói. Tuyệt đối tuân thủ Techstack do User định đoạt.
- KHÔNG viết implementation details (HOW) — chỉ mô tả WHAT.
- KHÔNG dùng technical jargon trong User Scenarios (business language).
- KHÔNG bỏ qua error cases — mỗi action phải có "khi thất bại thì sao?"