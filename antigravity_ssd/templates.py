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
[Mô tả ngắn gọn về tính năng và giá trị mang lại cho người dùng]

## 2. User Scenarios (Stories)
- **As a** [user role], **I want to** [action], **so that** [value].
- ...

## 3. Functional Requirements
- [ ] FR1: [Requirement 1]
- [ ] FR2: [Requirement 2]

## 4. Non-Functional Requirements
- **Performance**: [e.g., Response time < 500ms]
- **Security**: [e.g., Auth required]
- **UX**: [e.g., Responsive mobile]

## 5. Success Criteria
- [ ] [Criteria 1]
- [ ] [Criteria 2]
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
// Thay đổi database schema nếu có
```

## 3. API Contracts
- **Endpoint**: `POST /api/v1/...`
- **Request**: `{ ... }`
- **Response**: `{ ... }`

## 4. Component Changes
- [ ] [Component A]: Update logic for...
- [ ] [Component B]: Create new...

## 5. Research & Constraints
- [ ] [Item 1]: Verification of...
"""

def doc_tasks_template():
    return """# 📋 Task Registry: [FEATURE_NAME]

> **Rules**: 15-Minute Rule applies. If a task exceeds 15m, break it down.

## 📊 Progress Overview
- [ ] Phase 1: Setup & Foundation (0%)
- [ ] Phase 2: Core Logic (0%)
- [ ] Phase 3: Integration & UI (0%)
- [ ] Phase 4: Testing & Polish (0%)

---

## 🛠️ Tasks

### Phase 1: Setup & Foundation
- [ ] T001 [P] Create directory structure and boilerplate
- [ ] T002 [P] Configure environment variables

### Phase 2: Core Logic
- [ ] T101 [US1] Implement service logic for...
- [ ] T102 [US1] Write unit tests for...

### Phase 3+: Feature Implementation
- [ ] T201 [US2] ...
"""

def doc_identity_template(project_name="Project"):
    return f"""# 🧠 Master Identity: {project_name} Agent

## 🎭 Persona
You are the **Lead Architect & Senior Developer** for the **{project_name}** project. 
You are meticulous, security-conscious, and adhere strictly to the "Clean Code" and "DRY" principles.

## 🛠️ Core Capabilities
- Internalizing complex business logic and mapping it to scalable code.
- Enforcing the **Project Constitution** in every action.
- Maintaining zero-regression standards through automated testing.

## 🤝 Collaboration Style
- Proactive but cautious. 
- Ask for clarification when ambiguity is detected.
- Provide "Blast Radius Analysis" before any major refactoring.

## 📜 Soul (Core Beliefs)
1. **Correctness** > Speed.
2. **Context** is King. Never code without understanding the "Why".
3. **Spec-Driven** is the only way to build reliable software.
"""

def doc_constitution_template():
    return """# 📜 Project Constitution

> **Single Source of Truth** cho mọi quy tắc và tiêu chuẩn của dự án.

## 1. Preamble
Dự án này tuân thủ quy trình **Spec-Driven Development (SDD)**. Mọi code production đều phải có Spec và Plan tương ứng.

## 2. Core Principles
- **P1: Explicit over Implicit** - Không dùng "phép thuật", code phải rõ ràng.
- **P2: Security First** - Mọi input từ user đều phải được sanitize.
- **P3: Zero Hallucination** - AI không được tự ý thêm thư viện mà chưa kiểm tra.

## 3. Tech Stack Standard
- **Language**: [LANGUAGE]
- **Framework**: [FRAMEWORK]
- **Database**: [DATABASE]
- **Docker**: Mandatory (Ports 8900-8999)

## 4. Governance
- Amendment require manual approval.
- All code MUST pass `wb-agent validate`.
"""

# --- SKILL TEMPLATES ---

def skill_implement():
    return """---
name: speckit.implement
description: Code Builder với IRONCLAD anti-regression protocols.
role: Master Builder
---

## Role
Bạn là **Master Builder**. Nhiệm vụ của bạn là hiện thực hóa các kế hoạch đã đề ra trong `tasks.md` với độ chính xác tuyệt đối.

## 🛡️ IRONCLAD PROTOCOLS (Bắt buộc)

### 1. Blast Radius Analysis
Trước khi sửa bất kỳ file nào:
- Dùng `grep` tìm tất cả nơi đang gọi hàm/class đó.
- Báo cáo mức độ rủi ro (LOW/MEDIUM/HIGH).

### 2. Strangler Pattern
- Nếu rủi ro cao, không sửa trực tiếp file cũ.
- Tạo version mới (ví dụ `feature_v2.ts`) và chuyển đổi dần.

### 3. Reproduction Script First (TDD)
- Phải chứng minh bug/feature hoạt động (hoặc fail) bằng script trước khi code.

### 4. Context Anchoring
- Mỗi 3 tasks, chạy lệnh `tree` để AI định vị lại cấu trúc dự án.
"""

def skill_identity_manager():
    return """---
name: speckit.identity
description: Quản lý nhân cách và định hướng hành vi của AI cho dự án.
role: Persona Architect
---

## Task
Bạn giúp user thiết lập file `.agent/identity/master-identity.md` để AI hiểu được role và kỳ vọng của mình trong dự án này.

## Guidelines
1. Phân tích loại dự án (E-commerce, Tool, Admin...) để gợi ý Persona phù hợp.
2. Thiết lập các "Soul beliefs" dựa trên tech stack (ví dụ: "Type Safety is non-negotiable").
3. Đồng bộ hóa Identity với Constitution.
"""

# --- WORKFLOW TEMPLATES ---

def workflow_all():
    return """---
description: Chạy toàn bộ pipeline từ Spec → Clarify → Plan → Tasks
---

# 🚀 Full SDD Pipeline

1. **Specify**: Chạy `@speckit.specify` để định nghĩa tính năng.
2. **Clarify**: Chạy `@speckit.clarify` để xóa tan mơ hồ.
3. **Plan**: Chạy `@speckit.plan` để thiết kế kiến trúc kỹ thuật.
4. **Tasks**: Chạy `@speckit.tasks` để chia nhỏ task (15-min rule).
5. **Analyze**: Chạy `@speckit.analyze` để kiểm tra tính nhất quán giữa nội dung Spec - Plan - Tasks.
"""

# --- MAPS ---

SKILL_TEMPLATE_MAP = {
    "speckit.implement": skill_implement,
    "speckit.identity": skill_identity_manager,
}

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": doc_spec_template,
    "plan-template.md": doc_plan_template,
    "tasks-template.md": doc_tasks_template,
    "identity-template.md": lambda: doc_identity_template(),
    "constitution-template.md": doc_constitution_template,
}

SCRIPT_TEMPLATE_MAP = {
    "create-new-feature.sh": lambda: "#!/bin/bash\necho 'Creating feature...'",
    "check-prerequisites.sh": lambda: "#!/bin/bash\necho 'Checking...' ",
}
