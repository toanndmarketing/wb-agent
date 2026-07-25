---
name: speckit.status
description: Báo cáo trạng thái dự án: tiến độ tasks, blockers, next steps
---

## 🎯 Mission
Parse tasks.md → tính tiến độ → hiển thị dashboard trực quan.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse tasks.md → đếm checkboxes:
   - `- [X]` = completed
   - `- [ ]` = pending
2. Nhóm theo Phase → tính % mỗi phase.
3. Output dashboard:
   ```
   📊 Progress Dashboard: [Feature Name]
   ═══════════════════════════════════════
   Phase 1: Setup        ████████████████ 100% (4/4)
   Phase 2: Foundation   ████████░░░░░░░░  50% (3/6)
   Phase 3: User Auth    ░░░░░░░░░░░░░░░░   0% (0/5)
   ───────────────────────────────────────
   Total:                ███████░░░░░░░░░  47% (7/15)
   ```
4. List tasks đang pending (tiếp theo cần làm).

## 📤 Output
- Console: Dashboard visualization

## 🚫 Guard Rails
- KHÔNG thay đổi tasks.md — chỉ đọc và báo cáo.