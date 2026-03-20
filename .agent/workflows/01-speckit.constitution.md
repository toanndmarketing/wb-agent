---
description: Thiết lập/cập nhật Constitution (Source of Law)
---

# 📜 Constitution Setup

## Pre-conditions
- `.agent/` directory đã tồn tại (chạy `wb-agent init` trước)

## Steps

1. **@speckit.constitution** — Thu thập thông tin từ developer:
   - Tech stack (language, framework, DB)
   - Docker port range (mặc định 8900-8999)
   - Coding principles (VD: No hardcode, Docker-first)
   - Security requirements
2. Tạo/cập nhật `.agent/memory/constitution.md`
3. Validate: Mỗi section có ≥1 rule cụ thể

## Success Criteria
- ✅ `constitution.md` tồn tại với ≥4 sections
- ✅ Mỗi rule testable (không chung chung)
