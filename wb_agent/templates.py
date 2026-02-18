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
"""

def doc_constitution_template():
    return """# 📜 Project Constitution

## §1 Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production.
- **Local**: Dùng `docker-compose.yml` để dev.
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening.
- **Ports**: Tuân thủ dải **8900-8999**.

## §2 Security
- Production containers KHÔNG chạy quyền root.
- CẤM hard-code SSH/Tokens/Keys vào Dockerfile hoặc source code.
- Sử dụng Multi-stage builds để tối ưu size và bảo mật.
- Sensitive vars PHẢI dùng ENV (`.env` local, server ENV prod).

## §3 Code Standards
- CẤM hard-code: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- Dùng ENV vars với prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- Critical vars: `throw new Error()` nếu thiếu.
- Optional vars: `console.error()` nếu thiếu.

## §4 Environments
- Chỉ khởi tạo `local` và `production` mặc định.
- `beta` hoặc `staging` chỉ tạo khi có yêu cầu cụ thể.
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
