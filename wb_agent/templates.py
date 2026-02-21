"""
Templates - Aggregator cho Document, Skill, Workflow, Script templates.
Skill và Workflow templates được tách ra file riêng để dễ maintain.
"""

from datetime import datetime
from .skill_templates import SKILL_TEMPLATE_MAP
from .workflow_templates import WORKFLOW_TEMPLATE_MAP


# =============================================================================
# DOCUMENT TEMPLATES
# =============================================================================

def doc_spec_template():
    return """---
title: Feature Specification
status: DRAFT
version: 1.0.0
---

# 📝 Specification: [FEATURE_NAME]

## 1. Overview
[Mô tả ngắn gọn về tính năng]

## 2. User Scenarios (Stories)
- **US1**: As a [user role], I want to [action], so that [value].

## 3. Functional Requirements
- FR01: [requirement cụ thể, measurable]

## 4. Non-Functional Requirements
- NFR01: Response time < 2s

## 5. Success Criteria
- [ ] SC01: [testable criterion]
"""

def doc_plan_template():
    return """---
title: Implementation Plan
status: DRAFT
depends_on: spec.md
---

# 🏗️ Implementation Plan: [FEATURE_NAME]

## 1. Technical Architecture
[Mô tả cách tiếp cận kỹ thuật]

## 2. Data Model Changes
```prisma/sql
```

## 3. API Contracts
- **Endpoint**: `POST /api/v1/...`
- **Body**: `{ field: type }`
- **Response**: `{ data: ..., meta: ... }`
- **Errors**: `400 | 401 | 404 | 500`

## 4. Folder Structure
```
src/
├── app/
├── components/
├── lib/
└── api/
```

## 5. Dependencies
[Thư viện cần thêm — PHẢI có trong package.json]
"""

def doc_tasks_template():
    return """# 📋 Task Registry

## 📊 Progress Overview
- [ ] Phase 1: Setup & Foundation (0%)
- [ ] Phase 2: Core Features (0%)
- [ ] Phase 3: Polish (0%)

## 🛠️ Tasks

### Phase 1: Setup
- [ ] T001 [P] Setup project structure per plan.md

### Phase 2: Core Features
- [ ] T002 [P] [US1] Implement feature per spec.md

### Phase 3: Polish
- [ ] T003 Error handling & edge cases
"""

def doc_identity_template(project_name="Project", project_type="fullstack"):
    type_labels = {
        "web_public": "Web Public (B2C)",
        "web_saas": "Web SaaS (B2B)",
        "mobile_app": "Mobile App",
        "desktop_cli": "Desktop / CLI Tool",
        "fullstack": "Full-stack (Web + API)",
    }
    label = type_labels.get(project_type, "Full-stack")

    seo_section = ""
    if project_type in ("web_public", "fullstack", "web_saas"):
        seo_section = """
## 🔍 SEO & GEO Awareness
- Mọi page public phải có meta title, description, canonical URL.
- Structured Data (JSON-LD) là BẮT BUỘC cho các trang sản phẩm, bài viết.
- Tối ưu cho AI Search (GEO): Nội dung phải fact-dense, có nguồn trích dẫn.
- Cung cấp file `llms.txt` tại root để AI crawlers hiểu cấu trúc site.
"""

    return f"""# 🧠 Master Identity: {project_name} Agent

## 🎭 Persona
You are the **Lead Architect & Senior Developer** for the **{project_name}** project.
Project Type: **{label}**
You strictly follow the **Docker-First Policy** and **ASF 3.3** standards.

## 🛠️ Core Capabilities
- Internalizing complex business logic and mapping it to scalable code.
- Enforcing the **Project Constitution** in every action.
- Maintaining zero-regression standards through automated testing.
{seo_section}
## 🤝 Collaboration Style
- Proactive but cautious.
- Ask for clarification when ambiguity is detected.
- Provide "Blast Radius Analysis" before any major refactoring.

## 📜 Soul (Core Beliefs)
1. **Docker is the Law**: Everything runs in containers.
2. **Security is non-negotiable**: Production containers must be hardened.
3. **Spec-Driven**: No code without a plan.
4. **Context is King**: Never code without understanding the "Why".
5. **WB-Agent First**: Mọi thay đổi và vận hành phải thông qua wb-agent workflows.
"""

def doc_constitution_template():
    return """# 📜 Project Constitution

## §0 WB-Agent Protocol (MANDATORY)
- **BẮT BUỘC**: Mọi hoạt động phát triển (Code), kiểm thử (Test), và triển khai (Deploy Production) PHẢI sử dụng `wb-agent`.
- **Pipeline**: Tuân thủ nghiêm ngặt quy trình: Specify → Plan → Tasks → Implement.
- **Tools**: Chỉ sử dụng các workflows trong `.agent/workflows` để thực hiện task.

## §1 Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production. KHÔNG chạy `npm`/`node`/`python` trực tiếp trên host.
- **Local**: Dùng `docker-compose.yml` để dev.
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening.
- **Ports**: Chỉ dùng dải **8900-8999**.
  - Public FE: `N` | Admin FE: `N+1` | Backend API: `N+2`
- **Lệnh PowerShell**: Dùng PowerShell 5.1+, ngăn cách lệnh bằng `;` (KHÔNG dùng `&&`).

## §2 Security & Production Safety
- **CẤM**: `docker compose down -v` trên Production.
- **CẤM**: Deploy thủ công (phải dùng workflows `/deploy-production` hoặc `/deploy-staging`).
- **Xác nhận**: Yêu cầu xác nhận trước khi Deep Clean, Deploy Prod, hoặc Delete Data.
- **Runtime**: Production containers KHÔNG chạy quyền root.

## §3 Code Standards & ENV
- **CẤM hard-code**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive vars**: PHẢI dùng ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical vars: `throw new Error()` nếu thiếu.
  - Optional vars: `console.error()` nếu thiếu.
- **Documentation**: Phải có `.env.example` đầy đủ.

## §4 Workflow & Scripting
- **Tự động hóa**: Tạo script khi gặp lỗi hoặc task lặp lại.
- **Git**: Lưu script vào `.agent/scripts`, commit vào hệ thống version control.
- **Update**: Cập nhật workflow tương ứng sau khi tạo script mới.
"""

def doc_infrastructure_template():
    return """# 🏗️ Infrastructure & Docker Standards

## 📂 Environment Mapping
- **Local**: `docker-compose.yml` (Hot-reload, Dev-tools)
- **Production**: `docker-compose.prod.yml` (Standalone, Hardened)
- **Beta/Staging**: [None - Create only on request]

## 🔒 Security Protocol
- Use `.env.example` for all sensitive variables.
- Production images use Alpine/Slim versions.
- Firewall rules: Only expose mapped ports 89XX.
"""

def doc_seo_standards_template():
    return """# 🔍 SEO & GEO Standards

## 📋 Technical SEO Checklist (Bắt buộc)
- [ ] Mỗi page có `<title>` unique, tối đa 60 ký tự
- [ ] Mỗi page có `<meta description>`, tối đa 160 ký tự
- [ ] Chỉ 1 `<h1>` per page, heading hierarchy chuẩn (H1 → H2 → H3)
- [ ] Canonical URL cho mọi page để tránh duplicate content
- [ ] `sitemap.xml` tự động generate và submit lên Google Search Console
- [ ] `robots.txt` cấu hình đúng (không block CSS/JS)
- [ ] Image: `alt` text mô tả, lazy loading, format WebP/AVIF
- [ ] URL slug: lowercase, dấu gạch ngang, không dấu tiếng Việt
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` tại root domain
- [ ] Structured Data (JSON-LD) cho Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, nguồn trích dẫn, ngày publish/update
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Mỗi đoạn văn ≥1 data point hoặc trích dẫn
- [ ] FAQ sections dạng "People Also Ask"
- [ ] Topic clusters: Liên kết nội bộ giữa bài viết cùng chủ đề

## 📊 Schema.org (JSON-LD Templates)

### Article
```json
{"@context":"https://schema.org","@type":"Article","headline":"...","author":{"@type":"Person","name":"..."},"datePublished":"...","image":"..."}
```

### Product
```json
{"@context":"https://schema.org","@type":"Product","name":"...","image":"...","offers":{"@type":"Offer","price":"...","priceCurrency":"VND"}}
```

### FAQ
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```
"""


# =============================================================================
# SCRIPT TEMPLATES
# =============================================================================

def script_create_feature():
    return """#!/bin/bash
# Create new feature branch + specs directory
set -e
FEATURE_NAME=${1:?"Usage: ./create-new-feature.sh <feature-name>"}
SPECS_DIR=".agent/specs/$FEATURE_NAME"
mkdir -p "$SPECS_DIR"
echo "✅ Created specs directory: $SPECS_DIR"
echo "📋 Next: Run /02-speckit.specify to create spec.md"
"""

def script_setup_plan():
    return """#!/bin/bash
# Locate feature spec for planning
set -e
FEATURE_NAME=${1:?"Usage: ./setup-plan.sh <feature-name>"}
SPEC_FILE=".agent/specs/$FEATURE_NAME/spec.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo "❌ spec.md not found at $SPEC_FILE"
  echo "💡 Run /02-speckit.specify first"
  exit 1
fi
echo "✅ Found spec: $SPEC_FILE"
echo "📋 Next: Run /04-speckit.plan"
"""

def script_check_prerequisites():
    return """#!/bin/bash
# Verify prerequisite artifacts exist
set -e
FEATURE_NAME=${1:?"Usage: ./check-prerequisites.sh <feature-name>"}
SPECS_DIR=".agent/specs/$FEATURE_NAME"
ERRORS=0
for f in spec.md plan.md tasks.md; do
  if [ ! -f "$SPECS_DIR/$f" ]; then
    echo "❌ Missing: $SPECS_DIR/$f"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Found: $SPECS_DIR/$f"
  fi
done
if [ $ERRORS -gt 0 ]; then
  echo "⚠️  $ERRORS prerequisite(s) missing"
  exit 1
fi
echo "✅ All prerequisites met"
"""

def script_update_context():
    return """#!/bin/bash
# Update agent context files after changes
set -e
echo "🔄 Updating agent context..."
if [ -f ".agent/memory/constitution.md" ]; then
  echo "✅ Constitution: OK"
else
  echo "⚠️  Constitution missing — run /01-speckit.constitution"
fi
if [ -d ".agent/identity" ]; then
  echo "✅ Identity: OK"
else
  echo "⚠️  Identity missing — run wb-agent init"
fi
echo "✅ Context update complete"
"""


# =============================================================================
# IDE RULES TEMPLATES — Chuẩn format cho từng IDE
# Research date: 2026-02-21
# =============================================================================

def _core_rules_content(project_name="Project"):
    """Nội dung rules chung — được tái sử dụng cho mọi IDE."""
    return f"""Dự án: {project_name}

## 1. PHÁP LỆNH TỐI CAO
- Tuân thủ nghiêm ngặt file `.agent/memory/constitution.md`.
- Docker-First: Mọi hoạt động code và chạy app phải diễn ra trong container. KHÔNG chạy node/python trên host.
- Ports: Chỉ sử dụng dải port 8900-8999.

## 2. WB-AGENT PROTOCOL
- Mọi task phải đi qua quy trình: Specify → Plan → Tasks → Implement.
- Sử dụng Workflows trong `.agent/workflows/` và Skills trong `.agent/skills/`.

## 3. NGÔN NGỮ & CODE
- Phản hồi developer hoàn toàn bằng Tiếng Việt.
- 15-Minute Rule: Mỗi task phải atomic, ≤ 15 phút, ảnh hưởng ≤ 3 files.
- PowerShell 5.1+, ngăn cách lệnh bằng dấu `;` (KHÔNG dùng `&&`).
- KHÔNG hard-code URLs, Tokens, Keys. Dùng ENV vars (`.env`).

## 4. AN TOÀN
- KHÔNG chạy `docker compose down -v` trên Production.
- Tạo script tự động (`.agent/scripts/`) cho lỗi lặp lại.
- Kiểm tra logs ngay khi lỗi: `docker compose logs -f <service>`.
"""


def doc_antigravity_rules_template(project_name="Project"):
    """Antigravity IDE (Google) — .agent/rules/wb-agent.md"""
    return f"""# 🛡️ WB-Agent Workspace Rules

{_core_rules_content(project_name)}
"""


def doc_cursor_rules_template(project_name="Project"):
    """Cursor IDE — .cursor/rules/wb-agent.mdc (YAML frontmatter + markdown)"""
    return f"""---
description: WB-Agent project rules for {project_name}
globs:
alwaysApply: true
---

# WB-Agent Rules

{_core_rules_content(project_name)}
"""


def doc_windsurf_rules_template(project_name="Project"):
    """Windsurf IDE (Codeium) — .windsurf/rules/wb-agent.md"""
    return f"""# WB-Agent Rules

{_core_rules_content(project_name)}
"""


def doc_vscode_copilot_template(project_name="Project"):
    """VS Code (GitHub Copilot) — .github/copilot-instructions.md"""
    return f"""# Copilot Instructions for {project_name}

{_core_rules_content(project_name)}

## References
- Constitution: `.agent/memory/constitution.md`
- Infrastructure: `.agent/knowledge_base/infrastructure.md`
- Workflows: `.agent/workflows/`
- Skills: `.agent/skills/`
"""


def doc_jetbrains_rules_template(project_name="Project"):
    """JetBrains AI Assistant (PhpStorm, WebStorm, PyCharm) — .aiassistant/rules/wb-agent.md"""
    return f"""# WB-Agent Rules for {project_name}

{_core_rules_content(project_name)}
"""


def doc_kiro_steering_template(project_name="Project"):
    """Kiro IDE (AWS) — .kiro/steering/tech.md"""
    return f"""# Technology & Development Standards

Project: {project_name}
Build System: Docker (docker compose)
Port Range: 8900-8999
Shell: PowerShell 5.1+ (Windows)

## Development Protocol
- Follow Spec-Driven Development (SDD): Specify → Plan → Tasks → Implement.
- Specs directory: `.agent/specs/`
- Constitution: `.agent/memory/constitution.md`
- 15-Minute Rule: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.

## Environment
- Docker-First: All apps run inside containers. Never run npm/python on host directly.
- ENV vars required for all sensitive config (`.env` files).
- No hardcoded URLs, Tokens, Keys, or Credentials.

## Language
- Respond in Vietnamese (Tiếng Việt).

## Safety
- NEVER run `docker compose down -v` on Production.
- Always check logs on error: `docker compose logs -f <service>`.
"""


def doc_claude_md_template(project_name="Project"):
    """Claude Code — CLAUDE.md (root)"""
    return f"""# {project_name}

{_core_rules_content(project_name)}

## Project Structure
- `.agent/memory/constitution.md` — Project Constitution (Source of Law)
- `.agent/identity/master-identity.md` — AI Persona & Soul
- `.agent/knowledge_base/` — Domain knowledge (infrastructure, data, API)
- `.agent/skills/` — AI skills (@mentions)
- `.agent/workflows/` — Automation workflows (/commands)
- `.agent/specs/` — Feature specifications
"""


def doc_agents_md_template(project_name="Project"):
    """GitHub Copilot Coding Agent — AGENTS.md (root)"""
    return f"""# {project_name} — Agent Instructions

{_core_rules_content(project_name)}

## Build & Test
- Build: `docker compose build`
- Run: `docker compose up -d`
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`

## Project Context
- Constitution: `.agent/memory/constitution.md`
- Infrastructure: `.agent/knowledge_base/infrastructure.md`
- Workflows: `.agent/workflows/`
"""


# =============================================================================
# TEMPLATE MAPS — Re-exported from sub-modules + local definitions
# =============================================================================

# Re-export from sub-modules (for backward compat)
# SKILL_TEMPLATE_MAP imported from skill_templates
# WORKFLOW_TEMPLATE_MAP imported from workflow_templates

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": doc_spec_template,
    "plan-template.md": doc_plan_template,
    "tasks-template.md": doc_tasks_template,
    "constitution-template.md": doc_constitution_template,
    "infrastructure-template.md": doc_infrastructure_template,
    "seo-standards-template.md": doc_seo_standards_template,
}

SCRIPT_TEMPLATE_MAP = {
    "create-new-feature.sh": script_create_feature,
    "setup-plan.sh": script_setup_plan,
    "check-prerequisites.sh": script_check_prerequisites,
    "update-agent-context.sh": script_update_context,
}
