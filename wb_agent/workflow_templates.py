"""
Workflow Templates - Nội dung chi tiết cho 22 workflows.
Mỗi workflow có: Pre-conditions, Steps với gate checks, Success criteria.
"""


def wf_00_all():
    return """---
description: Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Pre-conditions
- `.agent/memory/constitution.md` đã tồn tại (chạy `/01-speckit.constitution` trước)

## Steps

1. **@speckit.specify** — Tạo spec.md từ mô tả feature
   - Input: Developer mô tả feature bằng ngôn ngữ tự nhiên
   - Output: `.agent/specs/[feature]/spec.md`

2. **GATE**: Kiểm tra spec.md có đủ User Scenarios + Success Criteria?
   - Nếu THIẾU → quay lại step 1

3. **@speckit.clarify** — Giải quyết mơ hồ
   - Output: Updated spec.md (mọi ambiguity resolved)

4. **@speckit.plan** — Tạo kiến trúc kỹ thuật
   - Output: plan.md, data-model.md, contracts/

5. **GATE**: Plan có vi phạm Constitution?
   - Nếu CÓ → báo lỗi, yêu cầu fix

6. **@speckit.tasks** — Breakdown thành atomic tasks
   - Output: tasks.md

7. **@speckit.analyze** — Kiểm tra consistency
   - Output: Coverage score + Gap analysis

## Success Criteria
- ✅ spec.md, plan.md, tasks.md tồn tại và nhất quán
- ✅ Coverage score ≥ 90%
- ✅ Không vi phạm Constitution
"""


def wf_01_constitution():
    return """---
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
"""


def wf_02_specify():
    return """---
description: Tạo Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại

## Steps

1. Developer mô tả feature bằng ngôn ngữ tự nhiên
2. **@speckit.specify** — Parse mô tả → tạo spec.md chuẩn hóa
3. Review output: spec.md phải có Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md có ≥1 User Scenario
- ✅ Mỗi scenario có Actor + Action + Value
- ✅ Success Criteria là testable
"""


def wf_03_clarify():
    return """---
description: Giải quyết mơ hồ trong Specification
---

# 🔍 Ambiguity Resolution

## Pre-conditions
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.clarify** — Scan spec.md tìm ambiguity
2. Hỏi developer tối đa 3 câu CRITICAL (bảng A/B/C options)
3. Auto-fix MINOR issues
4. Update spec.md với `[CLARIFIED]` markers

## Success Criteria
- ✅ Không còn vague language trong spec.md
- ✅ Mọi boundary conditions defined
"""


def wf_04_plan():
    return """---
description: Tạo Technical Plan (plan.md)
---

# 🏗️ Technical Planning

## Pre-conditions
- `.agent/specs/[feature]/spec.md` tồn tại (đã clarified)
- `.agent/memory/constitution.md` tồn tại

## Steps

1. **@speckit.plan** — Chuyển spec (WHAT) → plan (HOW):
   - Phase 0: Research unknowns → research.md
   - Phase 1: Data model → data-model.md
   - Phase 2: API contracts → contracts/*.md
   - Phase 3: Architecture → plan.md
2. **GATE**: So sánh plan vs constitution
   - Vi phạm? → BÁO LỐI, yêu cầu fix

## Success Criteria
- ✅ plan.md có folder structure + component hierarchy
- ✅ data-model.md có entity definitions
- ✅ Không vi phạm constitution
"""


def wf_05_tasks():
    return """---
description: Tạo Task Breakdown (tasks.md)
---

# 📋 Task Breakdown

## Pre-conditions
- `.agent/specs/[feature]/plan.md` tồn tại
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.tasks** — Breakdown plan → atomic tasks
2. Verify:
   - Mỗi task ≤15 phút
   - Mỗi task có file path
   - Dependency ordering đúng
   - Phase structure đúng (Setup → Foundation → Features → Polish)

## Success Criteria
- ✅ tasks.md có ≥1 phase
- ✅ Mỗi task format: `- [ ] T001 [P] [USx] Description affecting path/file`
- ✅ Không task nào ảnh hưởng >3 files
"""


def wf_06_analyze():
    return """---
description: Phân tích tính nhất quán giữa artifacts
---

# 🔬 Consistency Analysis

## Pre-conditions
- spec.md, plan.md, tasks.md tồn tại

## Steps

1. **@speckit.analyze** — Cross-check 3 artifacts:
   - Mỗi User Scenario → có tasks?
   - Mỗi data model → có tasks?
   - Conflicts giữa plan và constitution?
2. Output: Gap Analysis table + Coverage Score

## Success Criteria
- ✅ Coverage Score ≥ 90%
- ✅ Không gaps CRITICAL
"""


def wf_07_implement():
    return """---
description: Triển khai code theo tasks (Anti-Regression)
---

# 🛠️ Implementation

## Pre-conditions
- tasks.md tồn tại với tasks chưa complete
- plan.md tồn tại (kiến trúc)
- constitution.md tồn tại (rules)

## Steps

Cho MỖI task `- [ ]` trong tasks.md (theo thứ tự):

1. **@speckit.implement** — Thực thi IRONCLAD Protocols:
   - P1: Blast Radius Analysis → đánh giá risk
   - P2: Strategy Selection → inline edit hoặc Strangler Pattern
   - P3: TDD → repro script fail → code → pass
   - P4: Context Anchoring → re-read constitution mỗi 3 tasks
   - P5: **Build Gate** → chạy `tsc --noEmit` hoặc `docker compose build`
     - Nếu thêm/sửa component props → grep tất cả callers
     - Nếu thêm/sửa type interface → grep tất cả usage
     - Nếu đổi file structure → verify Dockerfile COPY paths
2. Mark `- [X]` khi task pass **VÀ build gate pass**
3. Repeat cho task tiếp theo

## Success Criteria
- ✅ Mọi tasks marked `[X]`
- ✅ Docker build pass
- ✅ Không regression trên tasks đã complete
- ✅ Mọi build gates pass
"""


def wf_08_checker():
    return """---
description: Chạy Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Code đã implement (≥1 task complete)

## Steps

// turbo-all

1. **TypeScript Compile Check** (CRITICAL):
   ```bash
   docker compose build 2>&1 | grep -iE "error|fail|TS[0-9]"
   ```
   Hoặc:
   ```bash
   docker compose exec topdeli-web npx tsc --noEmit
   docker compose exec topdeli-admin npx tsc --noEmit
   docker compose exec topdeli-api npx tsc --noEmit
   ```

2. **Dockerfile Integrity** — Kiểm tra COPY paths:
   - Verify mọi thư mục được COPY tồn tại (đặc biệt `public/`)
   - Verify CMD entrypoint khớp với build output structure
   - Verify KHÔNG có volume mount `.:/app` trong production/beta compose

3. **ENV Compliance** — Scan hard-coded values:
   ```bash
   grep -rn "http://localhost\\|http://127.0.0.1" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   ```

4. **Build-time Safety** — Verify SSG pages:
   ```bash
   grep -rn "await api\\.\\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
   ```
   Mỗi kết quả PHẢI nằm trong try-catch block.

5. **Monorepo Type Contract** — @speckit.checker:
   - Cross-reference shared type exports vs component usage
   - Verify shared package exports match actual file structure

6. **Security Scan**:
   - Tìm `eval()`, `dangerouslySetInnerHTML`, exposed secrets
   - Docker compliance: ports trong range 8900-8999

7. **Output Report** → `.agent/memory/checker-report.md`

## Success Criteria
- ✅ TypeScript compile: 0 errors
- ✅ Docker build: thành công hoàn toàn
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file tồn tại
- ❌ Nếu có bất kỳ 🔴 CRITICAL → BLOCK deploy
"""


def wf_09_tester():
    return """---
description: Chạy Tests & Coverage
---

# 🧪 Testing & Coverage

## Pre-conditions
- Code đã implement

## Steps

1. **@speckit.tester** — Tạo test plan → viết tests → chạy → report
2. Target: Coverage ≥ 80%

## Success Criteria
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ test-report.md tồn tại
"""


def wf_10_reviewer():
    return """---
description: Code Review
---

# 👀 Code Review

## Pre-conditions
- Code đã implement + tests pass

## Steps

1. **@speckit.reviewer** — Review code:
   - Spec compliance, error handling, security, performance
2. Verdict: APPROVE hoặc REQUEST CHANGES

## Success Criteria
- ✅ Verdict: APPROVE
- ✅ Mọi CRITICAL findings đã fix
"""


def wf_11_validate():
    return """---
description: Validate Implementation vs Spec
---

# ✅ Final Validation

## Pre-conditions
- Mọi tasks complete, tests pass, review approved

## Steps

// turbo-all

1. **Tasks Completion Check**:
   - Đọc `tasks.md` → mọi task phải `[X]`
   - Nếu còn `[ ]` hoặc `[/]` → ❌ BLOCKED

2. **TypeScript Build Gate** (CRITICAL):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Nếu build fail → ❌ BLOCKED, liệt kê errors

3. **Runtime Verification**:
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Tất cả services phải `Up` (KHÔNG `Restarting`)
   - Nếu `Restarting` → chạy `docker compose logs <service>` → ❌ BLOCKED

4. **Health Check**:
   ```bash
   curl -s http://localhost:<web_port> | head -c 200  # Public Web
   curl -s http://localhost:<admin_port> | head -c 200  # Admin Panel
   curl -s http://localhost:<api_port>/health  # API
   ```
   Tất cả phải trả về 200

5. **Constitution Compliance**:
   - Verify Monorepo Rules (type contracts)
   - Verify Docker Rules (no volume shadowing in prod)
   - Verify Build-time Safety (try-catch trong SSG)

6. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        N/N ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## Success Criteria
- ✅ Verdict: READY FOR DEPLOY
- ❌ Nếu BẤT KỲ step nào FAIL → BLOCKED (không được deploy)
"""


def wf_12_seo():
    return """---
description: Technical SEO Audit & Optimization
---

# 🔍 SEO Audit

## Pre-conditions
- Public pages đã implement
- `.agent/knowledge_base/seo_standards.md` tồn tại

## Steps

1. **@speckit.seo** — Audit:
   - Meta tags, headings, canonical, structured data
   - Core Web Vitals, crawlability
2. Output: Score 0-100 + issues list
3. Nếu score < 80 → fix issues → re-audit

## Success Criteria
- ✅ SEO Score ≥ 80
- ✅ 0 CRITICAL issues
"""


def wf_13_geo():
    return """---
description: GEO - Tối ưu cho AI Search (ChatGPT, Gemini, Perplexity)
---

# 🤖 GEO Audit

## Pre-conditions
- SEO Audit đã pass (score ≥ 80)

## Steps

1. **@speckit.geo** — Audit:
   - AI crawlability (llms.txt, SSR, JSON-LD)
   - E-E-A-T compliance
   - Content format, topic authority
2. Output: GEO report

## Success Criteria
- ✅ llms.txt tồn tại
- ✅ JSON-LD cho mọi content pages
- ✅ E-E-A-T signals present
"""


def wf_prepare():
    return """---
description: Prep Pipeline (Specify → Clarify → Plan → Tasks → Analyze) — không Implement
---

# 📋 Prep Pipeline

## Pre-conditions
- constitution.md tồn tại

## Steps
1. **@speckit.specify** — Tạo spec.md
2. **@speckit.clarify** — Resolve ambiguity
3. **@speckit.plan** — Tạo plan.md + data-model.md
4. **GATE**: Constitution compliance check
5. **@speckit.tasks** — Tạo tasks.md
6. **@speckit.analyze** — Verify consistency

## Success Criteria
- ✅ spec.md + plan.md + tasks.md tồn tại
- ✅ Coverage ≥ 90%, no constitution violations
- ⏸️ Dừng tại đây — KHÔNG implement
"""


def wf_util_checklist():
    return """---
description: Tạo/validate Requirements Checklist
---

# ✅ Requirements Checklist

## Steps
1. **@speckit.checklist** — Parse spec.md → tạo checklist
2. Link requirements → task IDs
3. Output: checklist.md

## Success Criteria
- ✅ Mỗi requirement linked đến ≥1 task
"""


def wf_util_content():
    return """---
description: Content Strategy & Readability Audit
---

# 📝 Content Audit

## Pre-conditions
- Content pages đã tạo

## Steps
1. **@speckit.content** — Audit heading, readability, multimodal, fact-density
2. Output: content-guidelines.md

## Success Criteria
- ✅ Mỗi page có 1 H1, hierarchy đúng
- ✅ Readability guidelines documented
"""


def wf_util_diff():
    return """---
description: So sánh Artifacts (Spec vs Implementation)
---

# 🔀 Artifact Comparison

## Steps
1. **@speckit.diff** — So sánh 2 versions/artifacts
2. Output: Added/Removed/Changed table + impact analysis

## Success Criteria
- ✅ Diff report generated
"""


def wf_util_migrate():
    return """---
description: Migrate Legacy Code — Reverse-engineer codebase hiện có
---

# 🔄 Legacy Migration

## Pre-conditions
- Existing codebase với source code
- constitution.md đã setup (target standards)

## Steps
1. **@speckit.migrate** — Scan codebase:
   - Detect languages, frameworks, dependencies
   - Reverse-engineer data models, routes
   - Tạo draft spec.md
   - Assess tech debt → migration-risk.md
2. Review findings với developer
3. Tiếp tục với `/02-speckit.specify` để thêm features mới

## Success Criteria
- ✅ Draft spec.md tạo từ existing code
- ✅ migration-risk.md với tech debt inventory
"""


def wf_util_quizme():
    return """---
description: Red Team - Đặt câu hỏi phản biện tìm edge cases
---

# 🎯 Red Team Quiz

## Pre-conditions
- spec.md + plan.md tồn tại

## Steps
1. **@speckit.quizme** — Challenge spec+plan:
   - Boundary, concurrency, failure, security, scale questions
   - Max 5 questions, interactive Q&A
2. Nếu phát hiện issues → update spec.md

## Success Criteria
- ✅ Tất cả edge cases đã addressed
"""


def wf_util_status():
    return """---
description: Hiển thị Progress Dashboard
---

# 📊 Progress Dashboard

## Steps
1. **@speckit.status** — Parse tasks.md → hiển thị:
   - Per-phase progress bars
   - Total completion %
   - Pending tasks list

## Success Criteria
- ✅ Dashboard displayed
"""


def wf_util_taskstoissues():
    return """---
description: Sync tasks.md → Issue Tracker
---

# 🔗 Issue Sync

## Pre-conditions
- tasks.md tồn tại

## Steps
1. **@speckit.taskstoissues** — Parse tasks → generate issue export
2. Output: issues-export.md (ready to copy to GitHub/GitLab)

## Success Criteria
- ✅ issues-export.md generated
- ✅ Mỗi task mapped thành 1 issue
"""


# =============================================================================
# WORKFLOW TEMPLATE MAP — Complete mapping cho tất cả 22 workflows
# =============================================================================
WORKFLOW_TEMPLATE_MAP = {
    "00-speckit.all": wf_00_all,
    "01-speckit.constitution": wf_01_constitution,
    "02-speckit.specify": wf_02_specify,
    "03-speckit.clarify": wf_03_clarify,
    "04-speckit.plan": wf_04_plan,
    "05-speckit.tasks": wf_05_tasks,
    "06-speckit.analyze": wf_06_analyze,
    "07-speckit.implement": wf_07_implement,
    "08-speckit.checker": wf_08_checker,
    "09-speckit.tester": wf_09_tester,
    "10-speckit.reviewer": wf_10_reviewer,
    "11-speckit.validate": wf_11_validate,
    "12-speckit.seo": wf_12_seo,
    "13-speckit.geo": wf_13_geo,
    "speckit.prepare": wf_prepare,
    "util-speckit.checklist": wf_util_checklist,
    "util-speckit.content": wf_util_content,
    "util-speckit.diff": wf_util_diff,
    "util-speckit.migrate": wf_util_migrate,
    "util-speckit.quizme": wf_util_quizme,
    "util-speckit.status": wf_util_status,
    "util-speckit.taskstoissues": wf_util_taskstoissues,
}
