---
name: speckit.debug
description: Debug lỗi hệ thống: phân tích log, trace root cause, đề xuất fix
---

## 🎯 Mission
Chẩn đoán sự cố hệ thống, tìm nguyên nhân gốc rễ (Root Cause) một cách độc lập và thiết lập kế hoạch sửa lỗi (Fix Plan) an toàn, tránh gây lỗi mới (Anti-Regression).

## 📋 Protocol

### 🔍 Phase 1: Information Gathering & Diagnostics (Thu thập & Chẩn đoán)
1. **Kiểm tra logs hệ thống**:
   - Dùng lệnh `docker compose logs -f <service>` hoặc đọc log files trực tiếp để tìm exception, stack trace, hoặc error codes.
2. **Xác định thời điểm xảy ra lỗi**:
   - Dùng `git log -n 5` hoặc `git diff` để kiểm tra những thay đổi code gần đây.
3. **Phân tích Blast Radius (Phạm vi ảnh hưởng)**:
   - Xác định những modules, APIs, hoặc giao diện nào đang bị ảnh hưởng trực tiếp và gián tiếp bởi lỗi.

### 🧪 Phase 2: Layered Verification Strategy & Reproduction (Tái hiện lỗi)
Áp dụng chiến lược kiểm thử phân lớp từ nhẹ đến nặng để tái hiện lỗi:
1. **Layer 1: Static Verification** (Kiểm tra tĩnh):
   - Chạy các lệnh compile, lint (ví dụ: `npx tsc --noEmit` hoặc compiler check) để phát hiện lỗi kiểu dữ liệu (type mismatch), import sai, hoặc cú pháp.
2. **Layer 2: Unit / Integration Tests**:
   - Viết hoặc chạy test case cục bộ kiểm tra hàm nghi vấn để cô lập lỗi.
3. **Layer 3: Network & HTTP Verification** (Kiểm tra mạng):
   - Sử dụng `curl`, Postman, hoặc script nhỏ để gửi requests trực tiếp đến API endpoints để kiểm tra response.
4. **Layer 4: UI/UX & Browser Verification** (Chỉ dùng khi bắt buộc):
   - Chỉ sử dụng Playwright / Browser Subagent cho các lỗi giao diện phức tạp, hiệu ứng hover/animation hoặc flow đa bước của end-user. Tránh lạm dụng để giảm tải cho host.
5. **Viết Repro Script**: Tạo file code chạy thử ở thư mục scratch (`artifacts/brain/<conversation-id>/scratch/`) để tái hiện lỗi 100% trước khi sửa.

### 🧠 Phase 3: Root Cause Analysis (RCA - Phân tích nguyên nhân)
1. Đọc code hiện tại xung quanh vùng lỗi.
2. Vẽ sơ đồ luồng dữ liệu (data flow) từ input đến điểm phát sinh lỗi.
3. Xác định chính xác lý do lỗi (do logic code sai, thiếu cấu hình ENV, lỗi database, hay tích hợp bên thứ ba).
4. Phải chỉ rõ file và số dòng code (line number) bị lỗi.

### 📝 Phase 4: Proposing Fix Plan & Risk Assessment (Đề xuất & Đánh giá rủi ro)
1. Đề xuất phương án sửa lỗi chi tiết.
2. Đánh giá rủi ro:
   - Nếu sửa lỗi ảnh hưởng **≤ 3 files**: Có thể sửa trực tiếp.
   - Nếu sửa lỗi ảnh hưởng **> 3 files** hoặc làm thay đổi cấu trúc database/kiến trúc hệ thống: **BẮT BUỘC** tạo `implementation_plan.md` và xin xác nhận của người dùng.
3. Quy tắc an toàn: Không thay đổi các phần code không liên quan. Giữ nguyên các comments/docstrings cũ.

### 🛠️ Phase 5: Implementation & Verification (Sửa lỗi & Xác thực lại)
1. Thực thi việc sửa code theo kế hoạch.
2. Chạy lại **Repro Script** để chứng minh lỗi đã được khắc phục hoàn toàn.
3. Chạy build gate (`docker compose build` hoặc `tsc`) để đảm bảo không còn lỗi biên dịch.
4. Kiểm tra lại logs hệ thống để đảm bảo không phát sinh exception mới.

## 📤 Output
- File: `.agent/memory/debug-report.md` chứa:
  - Triệu chứng lỗi (Symptoms).
  - Nguyên nhân gốc rễ (Root Cause) kèm file/line cụ thể.
  - Repro Script (nếu có).
  - Phương án xử lý (Fix Plan).
  - Kết quả xác thực (Verification Results).

## 🚫 Guard Rails
- KHÔNG đoán mò lỗi — phải dựa trên logs, stack trace và thực tế chạy code.
- KHÔNG sửa code trực tiếp khi chưa tìm ra nguyên nhân gốc rễ và có kế hoạch cụ thể.
- KHÔNG lạm dụng Playwright/Browser Subagent cho các tác vụ kiểm tra API hoặc compile.
- KHÔNG deploy code sửa lỗi nếu chưa vượt qua Build Gate.