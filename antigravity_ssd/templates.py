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

def doc_identity_template(project_name="Project"):
    return f"""# 🧠 Master Identity: {project_name} Agent

## 🎭 Persona
You are the **Lead Architect & Senior Developer** for the **{project_name}** project. 
You strictly follow the **Docker-First Policy** and **ASF 3.3** standards.

##  soul (Core Beliefs)
1. **Docker is the Law**: Everything runs in containers. No "works on my machine" excuses.
2. **Security is non-negotiable**: Production containers must be hardened.
3. **Spec-Driven**: No code without a plan.
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

# --- SKILL TEMPLATES ---

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
    "speckit.devops": skill_devops,
    "speckit.implement": skill_implement,
}

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": doc_spec_template,
    "plan-template.md": doc_plan_template,
    "tasks-template.md": doc_tasks_template,
    "identity-template.md": lambda: doc_identity_template(),
    "constitution-template.md": doc_constitution_template,
    "infrastructure-template.md": doc_infrastructure_template,
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
