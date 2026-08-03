---
name: speckit.teamwork
description: Hệ thống Multi-Agent Routing & Intent Recognition — Tự động nhận diện ý định ngôn ngữ tự nhiên, kích hoạt và đọc ngầm các Rule & Skill phù hợp (speckit.devops, studio-media, cloudflare-infra, speckit.seo-technical, v.v.), đề xuất và chờ user xác nhận trước khi thực thi.
---

# 🤖 SPECKIT.TEAMWORK — Natural Language Intent Recognition & Routing

## 🎯 Mission
Đảm bảo agent **luôn tự động nhận diện ý định từ câu chat của User**, lập tức gọi và tuân thủ đúng Rule/Skill tương ứng mà **không cần chờ User phải nhắc tên file hay gõ slash command**.

---

## ⚡ 3 QUICK COMMANDS — Lệnh Tắt Cho 3 Case Thường Dùng

Agent **BẮT BUỘC** tự động kích hoạt kịch bản tương ứng khi User gõ:

| Command | Mô tả | Skill Chain Kích Hoạt |
|---|---|---|
| **`/new-site`** | Khởi tạo dự án pSEO mới từ đầu | `speckit.specify` → `speckit.seo-content` → `speckit.plan` → `speckit.implement` + `seo-preflight-card` → `speckit.qa-audit` |
| **`/add-module`** | Thêm module/trang mới vào dự án sẵn có | `speckit.implement` + `seo-preflight-card` (Pre-code A1-A3 → Post-code B1-B19) |
| **`/audit-seo`** | Audit SEO + UI/UX (3 cấp: static → dynamic → hunter) | `speckit.qa-audit` + `seo-preflight-card` (Section C Scoring) |

### `/new-site` — Khởi Tạo Dự Án Mới
- **Cú pháp**: `/new-site [Mô tả dự án]. Tech: [stack]. Keywords: [nguồn dữ liệu]`
- **Ví dụ**: `/new-site Dự án pSEO dịch vụ sửa điện nước TP.HCM. Tech: Next.js + PostgreSQL. Keywords: file CSV Ahrefs đính kèm`
- **Luồng**: Full SDD 5 bước. Agent DỪNG 2 trạm chờ anh duyệt (sau Spec + sau QA).

### `/add-module` — Thêm Module / Trang Mới
- **Cú pháp**: `/add-module [Tên module]. Keyword: "[keyword]". Silo: [route cha]`
- **Ví dụ**: `/add-module Trang chi tiết Blog. Keyword: "hướng dẫn sửa ống nước". Silo: /blog/`
- **Luồng**: Agent đọc `seo-preflight-card` → check Anti-Cannibalization (A2) → code → tự kiểm 19 mục.

### `/audit-seo` — Audit SEO + UI/UX (Linh hoạt 3 cấp)
- **Cú pháp**: `/audit-seo [URL hoặc tên dự án] [--level 1|2|3] [--batch]`
- **Ví dụ**:
  - `/audit-seo http://localhost:8920` → Mặc định cấp 2 (dynamic)
  - `/audit-seo https://example.com --level 3` → Full hunter scan
  - `/audit-seo --batch` → Quét tất cả dự án trong workspace
- **3 cấp độ**:
  - `--level 1` (static): Quét source code, không build. Check hardcode, thiếu alt, `href="#"`, `<a>` bọc div.
  - `--level 2` (dynamic): Build + Puppeteer test. DOM check, Console errors, CWV, Schema, navigation.
  - `--level 3` (hunter): Full audit + Lighthouse + Sitemap cross-check + Orphan pages + Cannibalization.
- **`--batch` mode**: Quét đồng loạt nhiều dự án. Agent tự scan thư mục workspace, phát hiện các project có `package.json` / `next.config.ts` / `astro.config.mjs`, build lần lượt, audit từng site và xuất **1 báo cáo tổng hợp `batch-audit-summary.md`**.

---

## 🧠 BẢNG NHẬN DIỆN Ý ĐỊNH NGÔN NGỮ TỰ NHIÊN (AUTO-TRIGGER INTENT MATRIX)

Khi User gõ câu lệnh bằng văn bản tự nhiên (không dùng Quick Commands), Agent **BẮT BUỘC phải tự động đối chiếu từ khóa để KÍCH HOẠT VÀ ĐỌC NGẦM các Skill & Rule tương ứng**:

| Từ khóa / Ý định của User | Skill & Rule Tự Động Kích Hoạt | Quy Trình Bắt Buộc Agent Phải Tuân Thủ |
|---|---|---|
| *"tạo logo"*, *"thiết kế logo"*, *"làm favicon"* | [studio-media](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/studio-media/SKILL.md) | Bắt buộc sinh **3 BẢN CONCEPT LOGO KHÁC NHAU** (Modern Tech, Dynamic Energy, Monogram) theo chuẩn tỷ lệ ngang 3:1, SVG Vector, Màu Thủy-Mộc để User chọn 1 bản ưng ý nhất. |
| *"deploy dev"*, *"chạy local"*, *"up docker local"* | [speckit.devops (DEV)](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.devops/SKILL.md) | Hot-reload code, dùng `.env`, bind 127.0.0.1, quét port 8900-8999 local. |
| *"deploy prod"*, *"deploy vps"*, *"đưa lên server"*, *"deploy lần đầu"* | [speckit.devops (PROD-A)](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.devops/SKILL.md) + [first_time_deployment_rule.md](file:///C:/Users/Opengate/.gemini/config/rules/first_time_deployment_rule.md) | PROD Lần Đầu: Hỏi IP VPS, quét port collision `ss -tulpn`, Nginx Proxy, Cloudflare API, Certbot SSL. |
| *"deploy update"*, *"cập nhật code lên vps"*, *"push bản mới lên server"* | [speckit.devops (PROD-B)](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.devops/SKILL.md) + [deployer-team.md](file:///C:/Users/Opengate/.gemini/config/subagents/deployer-team.md) | Smart Deploy: Project isolation `cd /home/[domain]`, Smart Rebuild (`--no-deps`), Zero Downtime, flush cache an toàn. |
| *"cấu hình cloudflare"*, *"trỏ domain"*, *"bật ssl"*, *"bật đám mây cam"* | [cloudflare-infra](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/cloudflare-infra/SKILL.md) + [cloudflare_automation_rule.md](file:///C:/Users/Opengate/.gemini/config/rules/cloudflare_automation_rule.md) | Cloudflare 100%: Tự lấy API Key từ Windows Env, trỏ A Record, áp Security Rules tự động. |
| *"audit"*, *"check seo"*, *"scan tổng thể site"*, *"soi lỗi web"* | [speckit.qa-audit](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.qa-audit/SKILL.md) + [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md) | HUNTER Team: Scan SEO, Schema, Link rác, CWV, UI/UX & lập báo cáo audit. |
| *"cào data"*, *"crawl"*, *"scrape site"* | [speckit.debug-crawler](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.debug-crawler/SKILL.md) | SPIDER Team: Stealth Puppeteer, chống bot, retry batching. |
| *"lập cấu trúc dự án"*, *"lập kế hoạch pillar silo"*, *"cấu trúc pillar silo"*, *"phân tích keyword seo"*, *"route url seo"* | [speckit.seo-content](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.seo-content/SKILL.md) + [speckit.nextjs-pseo](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.nextjs-pseo/SKILL.md) | Bắt buộc thiết kế **Cấu trúc Pillar-Silo Public Frontend chuẩn Technical SEO 5 cấp** trước khi code. |
| *"thêm tính năng X"*, *"viết code module Y"*, *"fix bug Z"* | [speckit.specify](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.specify/SKILL.md) + [speckit.implement](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.implement/SKILL.md) | BUILDER Team: Đánh giá SDD 3 bước (Spec -> Code -> Test Loop). |
| *"học cái này đi"*, *"lưu rule này lại"*, *"nhớ nhé"* | [ai_self_learning_directive.md](file:///C:/Users/Opengate/.gemini/config/rules/ai_self_learning_directive.md) | Tự phân tích bối cảnh, trích xuất bài học và ghi file memory local (`.agent/`) hoặc global (`.gemini/config/rules/`). |

---

## 📋 QUY TRÌNH BẮT BUỘC — 4 Bước

### Bước 1: Phân Tích Ngữ Cảnh (Ngầm)
Agent tự động nhận diện từ khóa theo ma trận Intent phía trên.

### Bước 2: Chọn Phương Án (Nhẹ nhất đủ dùng)
```
A) Trả lời thẳng    → câu hỏi lý thuyết, giải thích, so sánh
B) Dùng 1 Skill     → 1 lĩnh vực, < 5 bước, không cần parallel
C) 1 Subagent ngầm  → tác vụ dài, đơn luồng, cần chạy background
D) Spawn Team       → THỰC SỰ cần song song (>50% tiết kiệm thời gian)
```

### Bước 3: Trình Bày Đề Xuất
```
🎯 [Tóm tắt mục tiêu] | 📊 [Đơn giản/Trung bình/Phức tạp] | ⏱️ [Ước tính thời gian]
💡 Đề xuất: Phương án [X] — [Lý do 1 câu]
✋ Anh xác nhận không? (hoặc muốn cách khác?)
```

### Bước 4: Chờ Xác Nhận → Thực Thi

---

## 🏗️ QUY CHUẨN TEAMWORK SDD (PROJECT LIFECYCLE WORKFLOW)

Quy trình chuẩn khi khởi tạo hoặc phát triển một tính năng/dự án mới để đảm bảo tính chặt chẽ, tối ưu token (Quota-driven), và an toàn (Anti-Surface Fix).

### Bước 0: Phân loại Yêu cầu & Khoanh vùng Tech Stack (Routing)
- **Hành động:** Tự động phân tích yêu cầu để định tuyến.
  - **Stack 1 (Astro + Cloudflare Pages + D1):** Ưu tiên Text, Blog, pSEO.
  - **Stack 2 (Next.js + PostgreSQL + VPS Cloud):** Ưu tiên Web App logic phức tạp.
  - **Luật Chống Đoán Mò:** Nếu yêu cầu Tech Stack lạ (PHP, Django...), Agent **dừng lại ngay** và hỏi trắc nghiệm (A/B) để User quyết định.

### Bước 1: Lập Đặc tả & Kiến trúc (BA/Spec & SEO Architecture)
- **Hành động:** Phân tích, chốt Tech Stack, vẽ Blueprint kiến trúc, luồng data. Ghi vào `.agents/specs/spec.md`.
- **Quy chuẩn Lập Kế hoạch Pillar-Silo (Bắt buộc cho Public Frontend pSEO):**
  Khi dự án khởi tạo có Public Frontend / pSEO, BẮT BUỘC phải lập kế hoạch cấu trúc 5 Cấp độ chuẩn Technical SEO trước khi viết code:
  1. **Cấp 1 — Entity Classification & Taxonomy:** Phân loại sản phẩm/dịch vụ/entity theo Tier ưu tiên (Tier 1 Core/National, Tier 2-6 Regional/State/Sub-category).
  2. **Cấp 2 — Keyword Research & Intent Mapping:** Phân tích 4 nhóm intent (*Commercial, Informational, Tutorial/Guides, Long-tail*) kèm Volume ước tính và target URL tương ứng.
  3. **Cấp 3 — Cấu trúc Cây Pillar - Silo - Cluster & Mapping Route URL Next.js:**
     - *Pillar Hub (`/category/`)*: Hub tổng quan thương mại, prose ~1500+ từ.
     - *Silo Pages (`/category/sub-item/`)*: Trang ngách chuyên sâu + Interactive Live Tester/Widget, ~1200+ từ.
     - *Cluster Pages (`/category/sub-item/feature/`)*: Trang hướng dẫn/dữ liệu chi tiết.
     - Route tree linh hoạt bám sát Next.js App Router.
  4. **Cấp 4 — Technical SEO Onpage & Schema JSON-LD Checklist:**
     - Single `<h1>` per page, Heading hierarchy H1->H2->H3.
     - Canonical Tag absolute (`trailingSlash: true`).
     - Multi-layer Schema JSON-LD (`Organization`, `WebSite`, `Article`/`Product`/`SoftwareApplication`/`LocalBusiness`, `FAQPage`, `BreadcrumbList`).
     - Internal linking 3 chiều Pillar <-> Silo <-> Cluster qua Component `<RelatedLinks>`.
  5. **Cấp 5 — Chiến lược Hybrid Content & Định danh Con số Phong Thủy Bát Tự:**
     - **Hybrid Content Model**: Kết hợp văn bản tĩnh SSR Prose Indexable cô đọng (cho Google Crawlers & AI Search) với các khối tương tác động Client Interactive Widgets/Tools (cho trải nghiệm người dùng).
     - **Quy tắc Con số Phong Thủy Bát Tự (Universal Feng Shui Numeric Rule)**: Mọi con số hiển thị công khai trên website (gói dịch vụ, số giá, hotline, số đếm thống kê, số lượng items, badges, số đại diện...) BẮT BUỘC tuân thủ Bát Tự Phong Thủy — ưu tiên chọn các số may mắn Phát (8), Trường Thịnh (9), Lộc (6), tránh tuyệt đối các số xui như Tử (4).
- **Trạm kiểm dịch 1:** Dừng lại hỏi: "Bản Spec & Cấu trúc Pillar-Silo này chuẩn ý anh chưa?". Chỉ đi tiếp khi User chốt "OK".

### Bước 2: Bóc tách Task & Lên Plan (Planner)
- **Hành động:** Bóc tách Checklist lưu vào `.agents/specs/tasks.md`. Áp dụng **Quota-Driven Routing** (Pro cho logic khó, Flash/Flash Lite cho UI/Content).

### Bước 3: Đội hình Thực thi Code theo Module (Builder / Coder)
- **Hành động:** Coder/Builder xây dựng từng Module/Page theo `tasks.md`.
- **🛡️ CONTRACT BẮT BUỘC KHI CODE TỪNG PAGE — SEO Preflight Card:**
  Khi code hoàn tất bất kỳ trang nào (Home, Pillar, Silo, Cluster), Coder BẮT BUỘC đọc và đối chiếu đủ **19 Hạng Mục Kiểm Tra** trong [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md) (Single Source of Truth). Bao gồm: URL/Canonical, Content Structure, Schema, Internal Links, CWV Performance, Image Pipeline, Logo/Favicon, Navigation Priority, Live Search, SSR/Font.
- **Trạm kiểm dịch 2 (Anti-Hallucination):** Gặp lỗi rẽ nhánh phức tạp hoặc đụng quota -> **Dừng lại, sinh báo cáo lỗi (`debug-report.md`)**. Không tự ý bịa code.

### Bước 4: Kiểm thử & Audit Chuẩn Trang (QA Tester / Hunter)
- **Hành động:** QA Tester kiểm thử chi tiết **TỪNG PAGE 1 (Page-by-Page Audit)** dựa ĐÚNG THEO 10 Case Kiểm Thử Nối Tiếp ở Bước 3.
- **Phương pháp QA:**
  - Fast Scan (100% URLs): Phát hiện 404, Thin content (< 300 từ), Thiếu Title/H1, Leaked Mock Data.
  - Deep Audit (URL Đại diện từng loại Page): Puppeteer kiểm tra Console Error, Headings, GEO Box, Schema JSON-LD, LCP Lazy images, Visual Accordion.
- **Tiêu chí duyệt:** Score ≥ 80/100 VÀ KHÔNG CÓ LỖI 🔴 CRITICAL -> Mới được phép cho Deploy. Nếu vi phạm 🔴 -> Block Deploy ngay lập tức và xuất `qa-audit-report.md`.

---

## 🗺️ 4 ĐỘI CHUYÊN BIỆT & QUY TRÌNH DEPLOY

### 🚢 ĐỘI DEPLOYER — DevOps & Infrastructure
**Tuân thủ 100% quy chuẩn quy định tại [speckit.devops](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/speckit.devops/SKILL.md):**

#### 1. DEPLOY DEV (Development - Máy cá nhân)
- Hot-reload code, dùng `docker-compose.yml`.
- Tự động quét port trống local (dải 8900-8999).
- Bind Localhost `127.0.0.1:${PUBLIC_PORT:-8920}:3000`.

#### 2. DEPLOY PRODUCTION (Server VPS) — BẮT BUỘC BÓC TÁCH 2 KỊCH BẢN:
- **Kịch Bản 1: Deploy Production Lần Đầu**: Xác nhận IP VPS -> Quét Port Collision (`ss -tulpn`) -> Build `docker-compose.prod.yml` -> Nginx Proxy (`nginx -t`) -> Cloudflare API & Certbot SSL.
- **Kịch Bản 2: Deploy Update Thường Xuyên (Smart Deploy)**: Project Isolation (`cd /home/[domain]`) -> Smart Differential Rebuild (`--no-deps`) -> Zero Downtime & Memory check (`free -m`) -> Safe Cache flush.

---

## 💰 MODEL ALLOCATION

| Loại tác vụ | Model |
|---|---|
| Phân tích / Spec / Kiến trúc | Pro |
| Code / Script / DevOps | flash |
| Crawl / Monitor / Read-only | flash-lite |
