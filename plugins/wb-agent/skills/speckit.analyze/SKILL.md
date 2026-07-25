---
name: speckit.analyze
description: Phân tích codebase, tech stack, architecture để đánh giá hiện trạng dự án
---

## 🎯 Mission
Đảm bảo spec.md, plan.md, tasks.md không mâu thuẫn và phủ hết requirements.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. **Coverage Check**: Mỗi User Scenario trong spec → phải có task(s) trong tasks.md.
2. **Conflict Check**: Plan nói dùng tech A nhưng tasks lại reference tech B → BÁO LỖI.
3. **Constitution Check**: So plan.md với constitution.md → phát hiện violations.
4. **Completeness Check**: Mỗi data model trong plan → phải có task tạo model + migration.
5. **Output bảng Gap Analysis**:
   ```
   | Spec Requirement | Plan Section | Task ID | Status |
   |------------------|-------------|---------|--------|
   | User login       | Auth flow   | T005    | ✅ OK  |
   | Payment          | -           | -       | ❌ GAP |
   ```
6. Tính Coverage Score: `(matched / total) × 100%`.

## 📤 Output
- Console: Gap Analysis table + Coverage Score
- File: `.agent/memory/analyze-report.md`

## 🚫 Guard Rails
- CHỈ báo cáo — KHÔNG tự ý sửa artifacts.
- Mỗi gap phải chỉ rõ artifact nào thiếu.