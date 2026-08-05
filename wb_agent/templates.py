"""
Templates v2.0 — Chỉ sinh nội dung cho 4 files output + 3 IDE rules.
Không còn skill_templates hay workflow_templates.
"""

from datetime import datetime


# ============================================================================
# 1. MASTER IDENTITY (core output file)
# ============================================================================
def render_master_identity(project_name: str, project_type: str, scan_context: str = "") -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    tech_stack_section = "<!-- Liệt kê tech stack chính: Next.js 15, Prisma, PostgreSQL, Docker... -->"
    if project_type == "Astro (Cloudflare Pages)":
        tech_stack_section = "- Framework: Astro (Cloudflare Serverless)\n- Database: Drizzle ORM + Cloudflare D1\n- Styling: TailwindCSS"
    elif project_type == "Astro (Docker VPS)":
        tech_stack_section = "- Framework: Astro (Node.js SSR Adapter)\n- Database: SQLite (better-sqlite3) in WAL mode\n- ORM: Drizzle ORM\n- Styling: TailwindCSS\n- Infrastructure: Docker (Node Alpine), Nginx Proxy"

    return f"""# 🧠 Master Identity — {project_name}

> **Generated**: {today} | **Type**: {project_type} | **wb-agent**: v2.0

## Tên Dự Án
{project_name}

## Loại Dự Án
{project_type}

## Tech Stack
{tech_stack_section}

## Port Registry
<!-- Quy định ports cho project này -->
| Service | Port | Ghi chú |
|---------|------|---------|
| Frontend | | |
| Admin | | |
| API | | |
| Database | | |

## Server / Deploy
<!-- IP, SSH port, deploy path -->
- **Server**: 
- **Deploy Path**: 
- **SSH**: 

## Credentials Mapping
<!-- Chỉ ghi KEY NAME, không ghi giá trị thật -->
- `DATABASE_URL`: PostgreSQL connection string
- `NEXT_PUBLIC_API_URL`: API base URL

{f"## 🔬 Auto-Detected Context{chr(10)}{scan_context}{chr(10)}" if scan_context else ""}
---
*Source of truth cho toàn bộ cấu hình dự án. AI agent BẮT BUỘC đọc file này trước khi làm bất kỳ task nào.*
"""


# ============================================================================
# 2. CONSTITUTION (project law)
# ============================================================================
def render_constitution(project_name: str, needs_docker: bool, project_type: str = "fullstack") -> str:
    docker_section = ""
    if needs_docker:
        docker_section = """
## Docker & Infrastructure
- Docker-First: Mọi service chạy trong container.
- Port lấy từ biến môi trường (.env), KHÔNG hard-code.
- Production dùng `docker-compose.prod.yml` với multi-stage builds.
- Bind ports tới `127.0.0.1` (localhost only) cho proxied services.
"""

    tech_stack_constitution = """- Framework: \n- Language: \n- Database: \n- ORM: """
    if project_type == "astro_cloudflare":
        tech_stack_constitution = "- Framework: Astro (Cloudflare Serverless)\n- Language: TypeScript / JavaScript\n- Database: Cloudflare D1\n- ORM: Drizzle ORM\n- Deployment: Cloudflare Pages & Workers"
    elif project_type == "astro_vps":
        tech_stack_constitution = "- Framework: Astro (Node.js SSR Adapter)\n- Language: TypeScript / JavaScript\n- Database: SQLite (better-sqlite3) in WAL Mode\n- ORM: Drizzle ORM\n- Deployment: VPS Docker + Nginx Proxy"

    return f"""# 📜 Constitution — {project_name}

> Source of Law cho dự án này. Mọi agent và workflow BẮT BUỘC tuân thủ.

## Core Principles
- **Spec trước Code**: WHAT trước, HOW sau.
- **No Hard-code**: URLs, Tokens, Keys phải dùng ENV vars.
- **Incremental**: Build incrementally, không bao giờ bắt đầu lại từ đầu.

## Tech Stack
{tech_stack_constitution}
{docker_section}
## Coding Standards
- TypeScript strict mode (nếu dùng TS).
- Functional programming style.
- Không `any` type, không placeholder code.
- File naming: kebab-case.

## Non-Negotiables
- Mọi destructive command (rm -rf, DROP TABLE, docker down -v) phải có user confirm.
- Backup database trước khi migration.
- Không import thư viện chưa được khai báo trong dependencies.
"""


# ============================================================================
# 3. PROJECT-SCOPED AGENTS.MD (auto-loaded by Antigravity)
# ============================================================================
def render_agents_md(project_name: str, needs_docker: bool, needs_seo: bool) -> str:
    docker_rules = ""
    if needs_docker:
        docker_rules = """- **Docker Protocol**: Chạy app trong container. Bind ports tới 127.0.0.1. Dùng multi-stage builds cho production.
"""

    seo_rules = ""
    if needs_seo:
        seo_rules = """- **SEO**: Tuân thủ checklist SEO trong `.agents/knowledge/seo_standards.md` nếu có.
"""

    return f"""# {project_name} — Agent Rules

## 1. Context Loading (BẮT BUỘC)
- Đọc `.agents/identity/master-identity.md` TRƯỚC KHI làm bất kỳ task nào.
- Đọc `.agents/memory/constitution.md` để biết luật dự án.
- KHÔNG suy diễn port, path, credentials từ memory hay dự án khác.

## 2. Project Rules
- Tuân thủ constitution.md — đây là "Source of Law".
{docker_rules}{seo_rules}- Mọi task ảnh hưởng > 3 files → phải tạo implementation_plan.md trước.
- KHÔNG chạy destructive commands mà không có user confirm.

## 3. Code Style
- Phản hồi developer bằng Tiếng Việt.
- PowerShell 5.1+, ngăn cách lệnh bằng dấu `;`.
- KHÔNG hard-code URLs, Tokens, Keys — dùng ENV vars (.env).

## 4. Workflow
- Sử dụng SDD flow: Specify → Plan → Tasks → Implement.
- Sau khi hoàn thành task, cập nhật trạng thái trong tasks.md.

## 5. Memorization Protocol (Quy tắc tự cập nhật)
Khi User yêu cầu "ghi nhớ", "cập nhật" quy tắc, tiêu chuẩn hoặc bản phân tích, BẮT BUỘC phân loại và lưu vào đúng vị trí:
- **Tiêu chuẩn Code / Tech Stack / Quy định nghiệp vụ**: Ghi vào `.agents/memory/constitution.md`.
- **Hành vi / Agent Rules đặc thù dự án**: Cập nhật thẳng vào `.agents/AGENTS.md`.
- **Bản phân tích dài hạn (SEO Plan, System Architecture, Spec)**: Tạo file markdown tại `.agents/specs/` (VD: `.agents/specs/seo-plan.md`).
- **Scripts / Tự động hóa**: Tạo Skill mới tại `.agents/skills/`.
TUYỆT ĐỐI KHÔNG lưu tài liệu, rule ra ngoài cấu trúc `.agents/`.
"""


# ============================================================================
# 4. CURSOR RULES (.cursor/rules/wb-agent.mdc)
# ============================================================================
def render_cursor_rules(project_name: str, needs_docker: bool) -> str:
    docker_note = "Docker-First: chạy app trong container." if needs_docker else ""
    return f"""---
description: wb-agent rules for {project_name}
globs: "**/*"
alwaysApply: true
---

# {project_name} — Cursor Rules

## Context
- Đọc `.agents/identity/master-identity.md` trước mọi task.
- Tuân thủ `.agents/memory/constitution.md`.
{f"- {docker_note}" if docker_note else ""}

## Code Style
- Tiếng Việt responses.
- No hard-coded URLs/Tokens/Keys.
- SDD flow: Specify → Plan → Tasks → Implement.
"""


# ============================================================================
# 5. CLAUDE.MD (root)
# ============================================================================
def render_claude_md(project_name: str, needs_docker: bool) -> str:
    docker_note = "\n- Docker-First: chạy app trong container. KHÔNG chạy node/python trên host." if needs_docker else ""
    return f"""# {project_name}

## Context
- Đọc `.agents/identity/master-identity.md` trước mọi task.
- Tuân thủ `.agents/memory/constitution.md`.

## Rules
- Phản hồi bằng Tiếng Việt.
- No hard-coded URLs, Tokens, Keys — dùng ENV vars.{docker_note}
- KHÔNG chạy destructive commands mà không có user confirm.
- SDD flow: Specify → Plan → Tasks → Implement.

## Project Structure
- `.agents/identity/master-identity.md` — Project config (Source of Truth)
- `.agents/memory/constitution.md` — Project Law
- `.agents/specs/` — Feature specifications
- `.agents/skills/` — Project-specific automation skills
"""
