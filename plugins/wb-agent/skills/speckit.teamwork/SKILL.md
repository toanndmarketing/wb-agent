---
name: speckit.teamwork
description: Hệ thống Multi-Agent Routing — Tự động phân tích ngữ cảnh, chọn phương án tối ưu (Single Skill / Subagent / Team), đề xuất và chờ user xác nhận trước khi thực thi. Kèm blueprint chi tiết 4 đội chuyên biệt: HUNTER (SEO/QA), SPIDER (Crawler), BUILDER (Dev), DEPLOYER (DevOps).
---

# 🤖 SPECKIT.TEAMWORK — Multi-Agent Routing & Orchestration

## 🎯 Mission
Đảm bảo agent luôn **chọn đúng công cụ, đúng quy mô** cho từng yêu cầu — không over-engineer, không under-deliver — và **luôn xác nhận với user** trước khi triển khai tốn tài nguyên.

---

## 📋 QUY TRÌNH BẮT BUỘC — 4 Bước

### Bước 1: Phân Tích Ngữ Cảnh (Ngầm)

Agent tự hỏi:
| Tiêu chí | Câu hỏi |
|---|---|
| **Phạm vi** | 1 file / 1 module / toàn dự án? |
| **Độ phức tạp** | Giải quyết < 5 bước? Hay cần nhiều luồng? |
| **Rủi ro** | Deploy production / xóa data / thay đổi lớn? |
| **Song song** | Nhiều việc độc lập cần chạy cùng lúc không? |
| **Thời gian** | User cần ngay (< 1 phút) hay OK chờ vài phút? |

### Bước 2: Chọn Phương Án (Nhẹ nhất đủ dùng)

```
A) Trả lời thẳng    → câu hỏi lý thuyết, giải thích, so sánh
B) Dùng 1 Skill     → 1 lĩnh vực, < 5 bước, không cần parallel
C) 1 Subagent ngầm  → tác vụ dài, đơn luồng, cần chạy background
D) Spawn Team       → THỰC SỰ cần song song (>50% tiết kiệm thời gian)
```

> ⚠️ **Nguyên tắc tối giản:** Không dùng D nếu B hoặc C đã đủ.

### Bước 3: Trình Bày Đề Xuất

```
🎯 [Tóm tắt mục tiêu] | 📊 [Đơn giản/Trung bình/Phức tạp] | ⏱️ [X phút]
💡 Đề xuất: Phương án [X] — [Lý do 1 câu]
✋ Anh xác nhận không? (hoặc muốn cách khác?)
```

### Bước 4: Chờ Xác Nhận → Thực Thi
- `"ok"` / `"làm đi"` → Thực thi theo đề xuất
- `"dùng X thay"` → Chuyển phương án
- `"giải thích thêm"` → Phân tích chi tiết hơn

---

## ⚡ EXCEPTIONS — Tự Làm Ngay Không Cần Hỏi

Rủi ro thấp, quota thấp:
- Đọc file, giải thích code, tư vấn kiến trúc
- Tạo file mới trong `tmp/` hoặc `.agent/`
- Sửa typo / format nhỏ trong 1 file
- Lệnh read-only: `git log`, `docker ps`, `dir`
- Tạo artifact báo cáo / draft

---

## 🗺️ 4 ĐỘI CHUYÊN BIỆT

### 🔍 ĐỘI HUNTER — SEO & QA Audit
**Kích hoạt khi:** *"audit / check tổng thể / scan [dự án]"*

**3 Subagent song song:**
```
Sub-A1: SEO Analyst
  Skills: speckit.seo-geo, speckit.checklist
  Job: Audit Metadata → Schema → Silo → Internal Linking → GEO
  Output: seo_[YYYYMMDD].md

Sub-A2: Bug Hunter (Puppeteer)
  Skills: speckit.debug-crawler, speckit.qa-audit
  Job: Crawl 5-10 URL đại diện → JS Errors → Network 404 → Hydration
  + Scan nhanh ALL URLs (chỉ HTTP status)
  Output: bugs_[YYYYMMDD].md

Sub-A3: Content Auditor
  Skills: speckit.analyze
  Job: Sample data real vs mock → word count → duplicate pattern → alt text
  Output: content_[YYYYMMDD].md
```

**Main Agent tổng hợp:** `audit_full_[YYYYMMDD].md` + Priority Action List
**Lưu tại:** `D:\Project\[du-an]\.agent\reports\`
**Thời gian mục tiêu:** < 5 phút

---

### 🕷️ ĐỘI SPIDER — Data Pipeline & Crawler
**Kích hoạt khi:** *"crawl / cào data / scrape [target]"*

**Pipeline 3 tầng:**
```
Sub-C1: Stealth Crawler (gemini-2.5-flash-lite)
  Skills: speckit.debug-crawler
  Config: Puppeteer Stealth, concurrency=3, delay 1.5-3s, retry=3
  Anti-bot: Rotate UA, fake fingerprint
  Output: raw/batch_[N].json

Sub-C2: Data Processor (gemini-2.5-flash)
  Job: Clean → Validate → Deduplicate → Chuẩn hóa Unicode
  Output: processed/data_[YYYYMMDD].json + error_log.md

Sub-C3: Monitor (gemini-2.5-flash-lite)
  Job: Track block rate, speed, ETA
  Alert: Block > 30% → giảm concurrency | Block > 50% → DỪNG, báo ngay
```

---

### ⚙️ ĐỘI BUILDER — Feature Development
**Kích hoạt khi:** *"thêm tính năng / build / fix bug phức tạp"*

**Pipeline SDD 3 Phase:**
```
Phase 1 (Song song):
  Sub-B1: Spec Writer (Pro) — speckit.specify → spec.md → CHỜ DUYỆT
  Sub-B2: Codebase Researcher (flash) — speckit.analyze → research_notes.md

Phase 2 (Sau duyệt):
  Sub-B3: Implementer (flash) — speckit.implement → code theo tasks.md
  Sub-B4: Tester (flash) — speckit.tester → test → feedback → B3 fix
  [B3 và B4 trao đổi tự động, loop đến khi PASS]

Phase 3:
  Main Agent tổng hợp → walkthrough.md → báo user
```

**Framework configs:** Next.js (`npm run build`), WordPress (`php -l`), Node.js (`node --check`)

---

### 🚢 ĐỘI DEPLOYER — DevOps & Infrastructure
**Kích hoạt khi:** *"deploy / setup docker / config cloudflare"*

**⚠️ Production = BẮT BUỘC xác nhận explicit trước**

```
Sub-D1: Docker Specialist — pc-sysadmin
  Build → Up → Health check → Log check → Port check

Sub-D2: Cloudflare Configurer — cloudflare-infra
  Cache purge → DNS verify → Tunnel health → SSL check

Sub-D3: Post-Deploy Verifier — speckit.qa-audit (quick mode)
  Homepage 200 + < 3s → No JS Error → SSL valid → API OK
  Nếu lỗi: Alert ngay + đề xuất rollback
```

**Safety Rules tuyệt đối:**
- KHÔNG `docker system prune` khi chưa hỏi
- KHÔNG xóa DB volume khi chưa backup
- Production: bắt buộc anh reply `"ok deploy production"`

---

## 💰 MODEL ALLOCATION

| Loại tác vụ | Model |
|---|---|
| Phân tích / Spec / Kiến trúc | Pro |
| Code / Script / DevOps | flash |
| Crawl / Monitor / Read-only | flash-lite |

---

## 🔗 Blueprint Files (Chi Tiết)

- [hunter-team.md](file:///C:/Users/Opengate/.gemini/config/subagents/hunter-team.md)
- [spider-team.md](file:///C:/Users/Opengate/.gemini/config/subagents/spider-team.md)
- [builder-team.md](file:///C:/Users/Opengate/.gemini/config/subagents/builder-team.md)
- [deployer-team.md](file:///C:/Users/Opengate/.gemini/config/subagents/deployer-team.md)
- [Global Rule (auto-load)](file:///C:/Users/Opengate/.gemini/config/rules/multi_agent_routing_rule.md)
