---
name: speckit.validate
description: Validate output sau implement: build check, lint, type check
---

## 🎯 Mission
Kiểm tra TOÀN BỘ implementation có đáp ứng spec.md hay không — final gate trước deploy.

## 📥 Input
- Tất cả artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Tasks Completion**: Mọi task trong tasks.md đã `[X]`?
2. **Success Criteria**: Mọi SC trong spec.md đã đạt?
3. **Build Verification** (PHẢI chạy actual command):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Nếu fail → ❌ BLOCKED
4. **Runtime Verification** (PHẢI chạy actual command):
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Tất cả services phải `Up` (KHÔNG `Restarting`)
   - Nếu `Restarting` → chạy `docker compose logs <service>` → ❌ BLOCKED
5. **Health Check** (PHẢI chạy actual command):
   ```bash
   curl -s http://localhost:<web_port> | head -c 200
   curl -s http://localhost:<api_port>/health
   ```
   Tất cả phải trả về 200
6. **Constitution Check**: Không vi phạm rules nào?
7. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        15/15 ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## 📤 Output
- File: `.agent/memory/validation-report.md`
- Verdict: ✅ PASS hoặc ❌ FAIL (kèm danh sách blockers)

## 🚫 Guard Rails
- KHÔNG approve nếu còn task chưa complete.
- KHÔNG approve nếu build fail.
- KHÔNG approve nếu bất kỳ service nào `Restarting`.
- PHẢI chạy actual commands — không chỉ đọc code.