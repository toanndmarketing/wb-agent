"""
Templates - Chứa nội dung mẫu cho Skills, Workflows, Documents và Scripts.
"""

from datetime import datetime

# --- DOCUMENT TEMPLATES ---

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
- **As a** [user role], **I want to** [action], **so that** [value].

## 3. Success Criteria
- [ ] [Criteria 1]
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
"""

def doc_tasks_template():
    return """# 📋 Task Registry

## 📊 Progress Overview
- [ ] Phase 1: Setup & Foundation (0%)

## 🛠️ Tasks
### Phase 1: Setup
- [ ] T001 [P] Setup Boilerplate
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

## 1. Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production.
- **Local**: Dùng `docker-compose.yml` để dev.
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening.
- **Ports**: Tuân thủ dải **8900-8999**.

## 2. Security
- Production containers KHÔNG chạy quyền root.
- CẤM hard-code SSH/Tokens/Keys vào Dockerfile.
- Sử dụng Multi-stage builds để tối ưu size và bảo mật.

## 3. Environments
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
- [ ] URL slug: lowercase, dấu gạch ngang, không dấu tiếng Việt (sử dụng transliteration)
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization) — AI Search
- [ ] File `llms.txt` tại root domain (hướng dẫn AI crawlers)
- [ ] Structured Data (JSON-LD) cho Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, nguồn trích dẫn, ngày publish/update
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Mỗi đoạn văn phải chứa ít nhất 1 data point hoặc trích dẫn
- [ ] Conversational Q&A sections (People Also Ask format)
- [ ] Topic clusters: Liên kết nội bộ giữa các bài viết cùng chủ đề

## 📊 Schema.org Markup (JSON-LD Templates)

### Article Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "author": { "@type": "Person", "name": "..." },
  "datePublished": "2026-...",
  "dateModified": "2026-...",
  "image": "...",
  "publisher": { "@type": "Organization", "name": "..." }
}
```

### Product Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "...",
  "image": "...",
  "offers": { "@type": "Offer", "price": "...", "priceCurrency": "VND" }
}
```

### FAQ Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "...", "acceptedAnswer": { "@type": "Answer", "text": "..." } }
  ]
}
```

## 📁 llms.txt Template
```
# [Project Name]
> [Mô tả ngắn về website]

## Docs
- [/about](/about): Giới thiệu về chúng tôi
- [/products](/san-pham): Danh mục sản phẩm
- [/blog](/tin-tuc): Tin tức và bài viết chuyên sâu

## Optional
- [/api-docs](/api-docs): API Documentation
```
"""


# --- SKILL TEMPLATES ---

def skill_seo():
    return """---
name: speckit.seo
description: Technical SEO Lead - Tối ưu Meta Tags, Sitemap, Core Web Vitals, Schema.org
role: SEO Technical Lead
---

## 🎯 Mission
Đảm bảo mọi page public đạt chuẩn Technical SEO và sẵn sàng cho AI Search (GEO).

## 📋 Protocol

### Bước 1: Audit Technical SEO
Đọc file `.agent/knowledge_base/seo_standards.md` để nắm checklist.
Quét toàn bộ pages và kiểm tra:
- Meta title/description có tồn tại và unique không?
- Heading hierarchy (H1 → H2 → H3) có đúng không?
- Canonical URLs có được set không?
- Structured Data (JSON-LD) có đang áp dụng đúng schema không?

### Bước 2: Core Web Vitals
- LCP (Largest Contentful Paint) < 2.5s
- INP (Interaction to Next Paint) < 200ms
- CLS (Cumulative Layout Shift) < 0.1
- Kiểm tra: Image optimization (WebP/AVIF, lazy loading, explicit dimensions)
- Kiểm tra: Font loading strategy (font-display: swap)

### Bước 3: Crawlability
- `robots.txt` không block CSS/JS
- `sitemap.xml` tự động generate
- Internal linking structure hợp lý
- 404 pages có redirect hoặc custom page

### Bước 4: Output
Tạo báo cáo SEO Audit tại `.agent/memory/seo-audit-report.md` với:
- Danh sách issues (Critical / Warning / Info)
- Đề xuất fix cho từng issue
- Score tổng thể (0-100)

## 🔗 Handoffs
- `@speckit.geo`: Sau khi Technical SEO đạt, chuyển sang GEO audit
- `@speckit.implement`: Fix các issues được phát hiện
"""

def skill_geo():
    return """---
name: speckit.geo
description: GEO Strategist - Tối ưu cho AI Search (ChatGPT, Gemini, Perplexity)
role: GEO Strategist
---

## 🎯 Mission
Đảm bảo website được AI Search engines **trích dẫn** (cite) trong câu trả lời,
thay vì chỉ xếp hạng trên Google SERP truyền thống.

## 🆕 GEO vs SEO (2025-2026)
- **SEO**: Xếp hạng top Google → Clicks
- **GEO**: Được AI **nhắc tên thương hiệu** trong câu trả lời → Trust + Authority

## 📋 Protocol

### Bước 1: AI Crawlability
- Kiểm tra file `llms.txt` tại root domain
- Đảm bảo SSR/SSG (không dùng CSR cho content quan trọng)
- Structured Data (JSON-LD) phải đầy đủ cho Article, Product, FAQ

### Bước 2: E-E-A-T Compliance
- **Experience**: Nội dung có thể hiện kinh nghiệm thực tế không?
- **Expertise**: Có author bio, credentials không?
- **Authoritativeness**: Có nguồn trích dẫn, data points không?
- **Trustworthiness**: HTTPS, privacy policy, contact info

### Bước 3: Content Format for AI
- Short paragraphs (2-3 câu)
- Bullet points và numbered lists
- Direct answers ở đầu mỗi section
- FAQ sections dạng "People Also Ask"
- Fact-dense: Mỗi đoạn ≥ 1 data point

### Bước 4: Topic Authority
- Xây dựng topic clusters (pillar + supporting articles)
- Internal linking giữa các bài viết cùng chủ đề
- Cover related entities và adjacent queries

### Bước 5: Output
Tạo báo cáo GEO Audit tại `.agent/memory/geo-audit-report.md`

## 🔗 Handoffs
- `@speckit.content`: Tối ưu nội dung theo chuẩn GEO
- `@speckit.seo`: Quay lại fix Technical SEO nếu cần
"""

def skill_content():
    return """---
name: speckit.content
description: Content Architect - Heading Structure, Readability, Multimodal, Fact-density
role: Content Strategist
---

## 🎯 Mission
Đảm bảo nội dung website đạt chuẩn cho cả người đọc VÀ AI search engines.

## 📋 Protocol

### Bước 1: Heading Structure
- Mỗi page chỉ 1 `<h1>` duy nhất
- Hierarchy chuẩn: H1 → H2 → H3 (không nhảy cấp)
- Heading phải mô tả nội dung section, không generic ("Giới thiệu" ❌ → "Giới thiệu về [Brand]" ✅)

### Bước 2: Readability
- Đoạn văn: Tối đa 3-4 câu
- Sử dụng bullet points thay cho đoạn dài
- Ngôn ngữ: Conversational, dễ hiểu
- Highlight key terms (bold/italic)

### Bước 3: Multimodal Content
- Image: Luôn có `alt` text mô tả chi tiết
- Video: Có transcript hoặc description
- Tables: Responsive, có caption
- Infographics: Có text alternative

### Bước 4: Fact-density (GEO)
- Mỗi section phải chứa ít nhất 1 statistic/data point
- Trích dẫn nguồn khi đưa ra claims
- Sử dụng quotes từ experts khi phù hợp

### Bước 5: Output
Tạo content guidelines tại `.agent/memory/content-guidelines.md`

## 🔗 Handoffs
- `@speckit.seo`: Validate SEO compliance sau khi optimize content
"""

def skill_devops():
    return """---
name: speckit.devops
description: Chuyên gia hạ tầng Docker & Security Hardening.
role: DevOps Architect
---

## Task
Thiết lập và quản lý hệ thống Docker cho dự án theo chuẩn ASF 3.3.

## 🛠️ DOCKER PROTOCOLS

### 1. Local Environment
- Luôn sử dụng `volume mount` để hot-reload code.
- Mapping port theo dải 8900-8999.

### 2. Production Environment
- Sử dụng **Multi-stage builds**.
- Ép buộc chạy user không phải root (`USER node` hoặc `appuser`).
- Loại bỏ các tool không cần thiết (curl, git, v.v.) khỏi image final.

### 3. Security Check
- Kiểm soát `.dockerignore` để tránh leak `.env` hoặc `.git`.
- Kiểm tra các port đang mở trên server trước khi mapping.
"""

def skill_implement():
    return """---
name: speckit.implement
description: Code Builder với IRONCLAD anti-regression protocols.
role: Master Builder
---
## Role
Thực thi code theo tasks.md. Luôn kiểm tra xem code mới có tương thích với Docker environment hiện tại không.
"""

# --- MAPS ---

SKILL_TEMPLATE_MAP = {
    "speckit.seo": skill_seo,
    "speckit.geo": skill_geo,
    "speckit.content": skill_content,
    "speckit.devops": skill_devops,
    "speckit.implement": skill_implement,
}

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": doc_spec_template,
    "plan-template.md": doc_plan_template,
    "tasks-template.md": doc_tasks_template,
    "constitution-template.md": doc_constitution_template,
    "infrastructure-template.md": doc_infrastructure_template,
    "seo-standards-template.md": doc_seo_standards_template,
}

def workflow_all():
    return """---
description: Full Pipeline Spec → Plan → DevOps → Tasks
---
# 🚀 Full Pipeline
1. @speckit.specify
2. @speckit.plan
3. @speckit.devops (Docker & Infra)
4. @speckit.tasks
"""

SCRIPT_TEMPLATE_MAP = {
    "create-new-feature.sh": lambda: "#!/bin/bash\necho 'Feature Created'",
}
