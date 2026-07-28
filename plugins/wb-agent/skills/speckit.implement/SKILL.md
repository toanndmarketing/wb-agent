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

### Living Documentation Loop (Chống Drift) ⭐
- Khi code xong và chuẩn bị pass task, PHẢI đối chiếu lại code thực tế với `spec.md` gốc.
- Nếu có sự thay đổi về luồng logic, DB schema, hay tham số API so với Spec ban đầu, BẮT BUỘC update ngược (Reverse Update) thay đổi đó vào file `spec.md`. Đảm bảo Spec luôn đúng với Code.

### Deviation Rules (Tự xử trí khi lệch hướng) ⭐
- **Bug detected**: Tự động sửa nếu nằm trong scope, hoặc tạo task mới nếu nghiêm trọng.
- **Missing Critical**: Nếu thiếu config/file quan trọng, tự động bổ sung ngay.
- **Blocker**: Nếu kẹt, tự thực hiện "Root Cause Analysis" trước khi hỏi người dùng.
- **Arch Change**: Nếu cần đổi kiến trúc, PHẢI hỏi người dùng.

### Self-Check Protocol
- Mọi task chỉ hoàn thành khi vượt qua Build Gate (không lỗi Type, không lỗi Docker).

## 🚫 Guard Rails
- KHÔNG commit code lỗi build.
- **ZERO-TRUST SECRETS**: KHÔNG hard-code sensitive info (API Key, DB URL, Token) vào bất kỳ file code nào. Mọi cấu hình nhạy cảm BẮT BUỘC dùng biến môi trường (`process.env.VAR` hoặc `import.meta.env`). Chỉ được sinh file `.env.example` với giá trị rỗng.
- KHÔNG tạo component UI trùng lặp nếu hệ thống đã có sẵn (Ví dụ: Không tạo `BlogCard` nếu `Card` đã thỏa mãn).