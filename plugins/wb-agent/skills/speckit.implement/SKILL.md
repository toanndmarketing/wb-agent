---
name: speckit.implement
description: Implement code theo tasks.md với IRONCLAD Protocols và TDD
---

## 🎯 Mission
Implement code theo tasks.md, tuân thủ IRONCLAD Protocols và **Deviation Rules** để tự vận hành khi gặp lỗi.

## 📋 Protocol

### IRONCLAD Protocols:
1. **Blast Radius**: Phân tích rủi ro dựa trên số lượng file ảnh hưởng.
2. **Strategy**: Chọn sửa trực tiếp hoặc Strangler Pattern.
3. **TDD**: Tạo script repro fail -> code -> pass.
4. **Context Anchoring**: Re-read constitution mỗi 3 tasks.
5. **Build Gate**: LUÔN chạy tsc/build sau mỗi task.

### Component Discovery (Chống Reinvent the Wheel) ⭐
- TRƯỚC KHI tạo UI Component mới (như Button, Card), BẮT BUỘC rà soát `src/components/` hoặc `src/ui/`.
- Nếu đã có component tương tự, PHẢI import và xài lại. Chỉ viết mới khi không thể extend component cũ.

### 🚨 MANDATORY: Deep Context Scan & Anti-Surface-Fix Protocol ⭐
- **Deep Context Scan (Nạp Sâu Context & Audit Reports)**:
  - TRƯỚC KHI thực thi bất kỳ task nào, BẮT BUỘC dùng `list_dir` / `view_file` rà soát triệt để các file Báo cáo Audit gần nhất trong dự án (ví dụ `seo_*.md`, `debug-report.md`, `.agent/specs/`, `docs/`, các file workflow markdown như `12-seo-geo.md`...) cùng với file `master-identity.md` / `workflow_config.json`.
  - TUYỆT ĐỐI KHÔNG đọc lướt rồi suy diễn hoặc chỉ dựa trên thông tin bề nổi.
- **Anti-Surface Fix (Chống Sửa Nông / Sửa Triệu Chứng Bề Nổi)**:
  - CẤM dừng lại ở việc fix lỗi bề nổi/triệu chứng trước mắt (ví dụ: thấy lỗi port/cache/syntax/1 file monolithic thì nhảy vào fix ngay tại đó mà bỏ qua đối chiếu kiến trúc sitemap index, route hierarchy, spec dự án).
  - Mọi thay đổi BẮT BUỘC phải đối chiếu xem code hiện tại có tuân thủ đúng Kiến trúc Quy chuẩn trong Báo cáo Audit & Workflow dự án hay không. Nếu phát hiện code vi phạm kiến trúc quy chuẩn (ví dụ: sitemap đang monolithic trong khi doc/audit yêu cầu Sitemap Index), BẮT BUỘC phải refactor đúng kiến trúc chuẩn trong doc, KHÔNG ĐƯỢC sửa chữa tạm bợ.

### Living Documentation Loop (Chống Drift) ⭐
- Khi code xong và chuẩn bị pass task, PHẢI đối chiếu lại code thực tế với `spec.md` gốc.
- Nếu có sự thay đổi về luồng logic, DB schema, hay tham số API so với Spec ban đầu, BẮT BUỘC update ngược (Reverse Update) thay đổi đó vào file `spec.md`. Đảm bảo Spec luôn đúng với Code.

### Deviation Rules (Tự xử trí khi lệch hướng) ⭐
- **Bug detected**: Tự động sửa nếu nằm trong scope, hoặc tạo task mới nếu nghiêm trọng.
- **Missing Critical**: Nếu thiếu config/file quan trọng, tự động bổ sung ngay.
- **Blocker**: Nếu kẹt, tự thực hiện "Root Cause Analysis" trước khi hỏi người dùng.
- **Arch Change**: Nếu cần đổi kiến trúc, PHẢI hỏi người dùng.

- **🛡️ SEO PREFLIGHT CARD (BẮT BUỘC ĐỌC & TUÂN THỦ KHI TẠO/SỬA MỌI ROUTE/PAGE)**:
  Mọi Agent khi code bất kỳ Page nào BẮT BUỘC đọc và đối chiếu đầy đủ Checklist trong [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md) — Bộ 13 hạng mục SEO Onpage & GEO (Single Source of Truth). Không cần đọc thêm `speckit.seo-technical` trừ khi cần tra cứu sâu.

### Self-Check Protocol
- Mọi task chỉ hoàn thành khi vượt qua Build Gate (không lỗi Type, không lỗi Docker).
- **SEO & Layout Check**: Phải đối chiếu nhanh DOM/Component sinh ra đã thỏa mãn các thẻ H1, meta title và Schema JSON-LD yêu cầu hay chưa.

## 🚫 Guard Rails
- KHÔNG commit code lỗi build.
- **ZERO-TRUST SECRETS**: KHÔNG hard-code sensitive info (API Key, DB URL, Token) vào bất kỳ file code nào. Mọi cấu hình nhạy cảm BẮT BUỘC dùng biến môi trường (`process.env.VAR` hoặc `import.meta.env`). Chỉ được sinh file `.env.example` với giá trị rỗng.
- **CẤM HARDCODE KHI TẠO / SỬA RULE & SKILL**: Mọi rule hay skill được tiếp thu hoặc bổ sung vào hệ thống BẮT BUỘC phải trừu tượng hóa thành nguyên lý tổng quát (Generic Standard), TUYỆT ĐỐI CẤM gán cứng (hardcode) tên miền, URL, credentials, hay câu chữ riêng của từng dự án cụ thể.
- KHÔNG tạo component UI trùng lặp nếu hệ thống đã có sẵn (Ví dụ: Không tạo `BlogCard` nếu `Card` đã thỏa mãn).