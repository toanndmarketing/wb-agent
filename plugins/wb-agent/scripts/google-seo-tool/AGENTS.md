# agent-seo-tool — Agent Instructions

Dự án: **agent-seo-tool** v2.0 — Automated SEO Analysis Suite (CLI Tool)

## 1. BẢN CHẤT DỰ ÁN
- CLI Tool chạy one-shot qua `node cli.js <command> [options]`.
- KHÔNG phải web app. Không có UI, server, port, database.
- Cross-project utility: được gọi từ project khác qua skill `seo-audit`.

## 2. ARCHITECTURE
- **Core** (`src/core/`): env, config, auth (Google JWT), crawler (axios+cheerio), reporter.
- **Modules** (`src/modules/`): 13 modules, mỗi module export `{ run(config) }`.
- **Pipeline** (`src/pipelines/full-audit.js`): Orchestrator chạy 6 safe modules.
- **Dependencies**: CHỈ 3 packages — `axios`, `cheerio`, `googleapis`.
- **CommonJS** (`require`), built-in `.env` loader.

## 3. CONFIG & AUTH
- Config chain: `CLI args → ENV vars (.env) → Default values (config.js)`.
- Auth: Google Service Account JWT (`service-account.json`).
- CẤM hard-code URLs, API keys, credentials.

## 4. NGÔN NGỮ & CODE
- Phản hồi developer bằng Tiếng Việt.
- PowerShell 5.1+, ngăn cách lệnh bằng `;` (KHÔNG dùng `&&`).
- Mỗi module PHẢI xuất `.md` + `.json` report có section `AGENT INSTRUCTIONS`.

## Build & Run
- Build: `docker compose build`
- Run module: `docker compose run --rm app node cli.js <command> --site <URL>`
- Run direct: `node cli.js <command> --site <URL>`
- Full audit: `node cli.js full-audit --site <URL> --output-dir <path>`
