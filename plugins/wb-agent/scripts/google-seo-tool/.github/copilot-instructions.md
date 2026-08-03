# Copilot Instructions — agent-seo-tool v2.0

Dự án: **agent-seo-tool** — Automated SEO Analysis Suite (CLI Tool)

## 1. BẢN CHẤT DỰ ÁN
- CLI Tool chạy one-shot: `node cli.js <command> [options]`.
- KHÔNG phải web app. Không có UI, server, port, database.
- Cross-project utility: gọi từ project khác qua skill `seo-audit`.
- Tuân thủ `.agent/memory/constitution.md`.

## 2. ARCHITECTURE & DEPS
- Core (`src/core/`): env, config, auth, crawler, reporter.
- Modules (`src/modules/`): 13 modules, export `{ run(config) }`.
- CHỈ 3 packages: `axios`, `cheerio`, `googleapis`. CommonJS (`require`).
- Config chain: CLI args → ENV vars → Defaults.

## 3. NGÔN NGỮ & CODE
- Phản hồi developer bằng Tiếng Việt.
- 15-Minute Rule: Mỗi task atomic, ≤ 15 phút, ≤ 3 files.
- PowerShell 5.1+, ngăn cách lệnh bằng `;`.
- CẤM hard-code URLs, API keys, credentials.
- Report PHẢI có `## 🤖 AGENT INSTRUCTIONS` (P0/P1/P2).

## 4. SAFETY
- 🟢 Safe: full-audit, audit, decay, top-pages, geo, sitemap, internal, rank-compare*
- 🟠 Manual: outbound, mentions, broken-links, content-gap
- 🔴 Destructive: index (writes to Google)

## References
- Constitution: `.agent/memory/constitution.md`
- Infrastructure: `.agent/knowledge_base/infrastructure.md`
- Workflows: `.agent/workflows/`
- Skills: `.agent/skills/`
