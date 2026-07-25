---
name: speckit.diff
description: So sánh diff giữa các version, phân tích impact của thay đổi
---

## 🎯 Mission
So sánh 2 versions của artifact → highlight thay đổi → đánh giá impact.

## 📥 Input
- 2 files hoặc 2 versions cần so sánh (spec, plan, tasks, code)

## 📋 Protocol
1. Đọc cả 2 versions.
2. So sánh section-by-section:
   - ➕ **Added**: Sections/requirements mới
   - ➖ **Removed**: Sections/requirements bị xóa
   - ✏️ **Changed**: Sections có nội dung thay đổi
3. Impact Analysis: Mỗi thay đổi ảnh hưởng artifact nào downstream?
   - VD: Thêm field trong spec → cần update plan → cần thêm tasks
4. Output bảng tóm tắt.

## 📤 Output
- Console: Diff summary table
- File: `.agent/memory/diff-report.md` (nếu cần lưu)

## 🚫 Guard Rails
- CHỈ so sánh và báo cáo — KHÔNG tự ý sửa artifacts.