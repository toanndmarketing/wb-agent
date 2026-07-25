# ⚡ WB-Agent v2.0 — Thin Agent CLI

> **Python CLI tool** tạo cấu trúc `.agents/` tối giản cho mọi dự án, **kế thừa Global Rules** và **smart-detect project type**.

## 🎯 Triết lý v2.0: "Thin Agent"

| | v1.x (cũ) | v2.0 (mới) |
|---|---|---|
| **Output** | 60+ files (27 skills, 29 workflows, 7 templates) | **6 files** |
| **Code** | ~4,300 dòng Python | **~1,200 dòng** |
| **Skills** | Nhúng vào từng project | **Global Plugin** (cài 1 lần, dùng mọi nơi) |
| **IDE Rules** | 8 IDE | **3 IDE** (Antigravity, Cursor, Claude Code) |
| **Project Type** | Hỏi thủ công | **Smart-detect** từ codebase |

### Nguyên tắc
1. **Kế thừa Global**: Skills & Rules chung sống ở `~/.gemini/config/`, không copy vào từng project.
2. **Chỉ giữ Context**: `.agents/` chỉ chứa thông tin **riêng biệt** của project (port, tech stack, credentials).
3. **Smart-detect**: Tự quét codebase → xác định project type → chỉ hỏi khi không chắc chắn.

---

## 📋 Requirements

- Python 3.9+ (Windows, Linux, macOS)
- Không cần thư viện ngoài (Pure Python stdlib)

---

## 📦 Cài đặt

```bash
# Cách 1: pip install từ GitHub (Khuyến nghị)
pip install git+https://github.com/toanndmarketing/wb-agent.git

# Cách 2: pipx (isolated)
pipx install git+https://github.com/toanndmarketing/wb-agent.git

# Cách 3: Development mode
git clone https://github.com/toanndmarketing/wb-agent.git
cd wb-agent && pip install -e .

# Kiểm tra
wb-agent version
# → wb-agent v2.0.0
```

---

## 🚀 Cách sử dụng

```bash
# Smart-detect: quét codebase → tự chọn project type
wb-agent init

# Chỉ định project type
wb-agent init --type fullstack

# Init tại thư mục cụ thể
wb-agent init --target /path/to/project --name "My Project"

# Ghi đè không hỏi
wb-agent init --force

# Validate cấu trúc .agents/
wb-agent validate

# Xem version
wb-agent version
```

### Loại dự án có sẵn

| Type | Mô tả | SEO | Docker |
|------|--------|-----|--------|
| `web_public` | Blog, E-commerce, Landing Page | ✅ | ✅ |
| `web_saas` | Dashboard, Admin, API Service | ❌ | ✅ |
| `fullstack` | Frontend + Backend API | ✅ | ✅ |
| `wordpress` | WordPress Theme/Plugin | ✅ | ❌ |
| `mobile_app` | iOS/Android | ❌ | ❌ |
| `script` | Python/Bash/JS scripts | ❌ | ❌ |

---

## 📂 Output: Cấu trúc `.agents/` được tạo

```
.agents/
├── AGENTS.md                  ← Auto-loaded bởi Antigravity (Project Rules)
├── identity/
│   └── master-identity.md     ← Source of truth (port, tech, credentials)
├── memory/
│   └── constitution.md        ← Project Law (principles, standards)
├── specs/                     ← Thư mục cho spec.md, plan.md, tasks.md
├── skills/                    ← Thư mục cho project-specific skills
└── project.json               ← Metadata

+ .cursor/rules/wb-agent.mdc   ← Cursor rules
+ CLAUDE.md                    ← Claude Code rules
```

**Tổng: 6 files + 2 IDE rules = 8 files** (so với 60+ files ở v1.x)

---

## 🤖 Smart-Detect Logic

Khi chạy `wb-agent init` mà **không** chỉ định `--type`, tool tự quét:

| Detect | Project Type |
|--------|-------------|
| `wp-content/`, `functions.php` | `wordpress` |
| Next.js + Prisma + Docker | `fullstack` |
| Next.js + pages (no API) | `web_public` |
| NestJS / Express / FastAPI / Django | `web_saas` |
| Python (no web framework) | `script` |
| Không detect được | **Hỏi user** |

---

## 🏗️ Architecture

```
wb-agent/
├── pyproject.toml           # Package config (v2.0.0)
├── README.md
├── wb_agent/
│   ├── __init__.py          # Version
│   ├── __main__.py          # python -m wb_agent
│   ├── cli.py               # Entry point (init, validate, version)
│   ├── registry.py          # Project types + auto-detect logic
│   ├── templates.py         # 5 render functions (identity, constitution, rules)
│   ├── scanner.py           # Codebase scanner (package.json, Docker, Prisma...)
│   └── validators.py        # Validate .agents/ structure
```

---

## 📄 License

MIT
