---
description: Tạo Feature Specification và giải quyết mơ hồ (spec.md)
---

# 📝 Feature Specification & Clarity

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại

## Steps

1. Developer mô tả feature bằng ngôn ngữ tự nhiên
2. **@speckit.specify** — Parse mô tả → tạo spec.md chuẩn hóa
3. Chạy Clarity Check để phát hiện các yếu tố mơ hồ:
   - Đặt tối đa 3 câu hỏi CRITICAL dưới dạng bảng A/B/C options để developer lựa chọn.
   - Tự động giải quyết các điểm MINOR và cập nhật lại spec.md với nhãn `[CLARIFIED]`.

## Success Criteria
- ✅ spec.md có ≥1 User Scenario
- ✅ Mỗi scenario có Actor + Action + Value
- ✅ Không còn ngôn ngữ mơ hồ (vague language) trong spec.md
- ✅ Success Criteria là testable
