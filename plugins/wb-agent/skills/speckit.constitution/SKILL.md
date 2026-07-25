---
name: speckit.constitution
description: Tạo và quản lý constitution.md — bộ luật dự án
---

## 🎯 Mission
Tạo và duy trì constitution.md — "luật tối cao" mà mọi agent phải tuân thủ.

## 📥 Input
- Developer cung cấp: tech stack, principles, constraints
- `.agent/knowledge_base/infrastructure.md` (nếu có)

## 📋 Protocol
1. Thu thập từ developer:
   - Tech stack (frameworks, DB, language)
   - Docker ports (trong range 8900-8999)
   - Coding principles (VD: No hardcode, API-first)
   - Security requirements
2. Tạo/cập nhật `.agent/memory/constitution.md` với sections BẮT BUỘC:
   - **§1 Infrastructure**: Docker-first policy, port allocation, environments
   - **§2 Security**: No root containers, no hardcoded secrets, multi-stage builds
   - **§3 Code Standards**: Language, naming conventions, ENV policy
   - **§4 Non-Negotiables**: Danh sách rules KHÔNG BAO GIỜ được vi phạm
   - **§5 Monorepo Rules** (nếu monorepo):
     - Shared Package Contract: type exports là source of truth
     - Build Independence: mỗi app phải compile độc lập
     - Package exports phải match actual file structure
   - **§6 Docker Deployment Rules**:
     - CẤM volume shadowing (`- .:/app`) trong production/beta
     - Dockerfile COPY paths phải tồn tại
     - CMD entrypoint phải match với build output
     - Next.js apps phải có thư mục `public/`
   - **§7 Build-time Safety** (nếu Next.js):
     - SSG pages (sitemap, generateStaticParams): API calls phải try-catch
     - fetchApi phải return null/empty nếu API_URL undefined
   - **§8 Pre-Deploy Checklist**:
     - `docker compose build` thành công
     - Tất cả services `Up` (không `Restarting`)
     - Health check: 200 OK
3. Validate: Mỗi section phải có ít nhất 1 rule cụ thể, không chung chung.

## 📤 Output
- File: `.agent/memory/constitution.md`

## 🚫 Guard Rails
- Constitution KHÔNG chứa implementation details (HOW) — chỉ chứa rules (WHAT).
- Mỗi rule phải testable (có thể verify bằng code/check).