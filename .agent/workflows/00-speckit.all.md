---
description: Full Pipeline (Specify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Steps

1. **@speckit.map** — (NẾU dự án cũ) Quét cấu trúc và hiểu codebase hiện tại.
   - Output: `.agent/codebase/` docs.

2. **@speckit.specify** — Tạo spec.md từ mô tả feature và giải quyết các điểm mơ hồ (Clarity Check).
   - Output: `.agent/specs/[feature]/spec.md`.

3. **@speckit.roadmap** — Cập nhật `.agent/ROADMAP.md` với Phase/Milestone mới.

4. **@speckit.plan** — Tạo kiến trúc (Goal-Backward).
   - Output: plan.md, must_haves.

5. **@speckit.tasks** — Breakdown thành atomic tasks (Task Anatomy).
   - Output: tasks.md.

6. **@speckit.analyze** — Kiểm tra tính nhất quán 360 độ.

## Success Criteria
- ✅ spec.md, plan.md, tasks.md tồn tại và nhất quán
- ✅ Không vi phạm Constitution
