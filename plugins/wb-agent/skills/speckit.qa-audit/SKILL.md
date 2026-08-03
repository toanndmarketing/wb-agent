---
name: speckit.qa-audit
description: Quy trình kiểm thử và đánh giá tổng thể website (Pre-publish QA Audit Workflow)
---

## 🎯 Mission
Kiểm tra toàn diện mọi URL thực tế của project theo **2 chiến lược song song**:
- **Chiến lược A — Quét Nhanh Toàn Bộ**: Chạy qua 100% URL để phát hiện thiếu data, 404, thin content.
- **Chiến lược B — Scan Sâu 5-10 URL Đại Diện**: Puppeteer kiểm tra cấu trúc SEO, UI/UX, Schema, Console errors.

## 🪄 CUSTOM SLASH COMMANDS (TRIGGER ALIAS)
Agent **BẮT BUỘC** tự động kích hoạt các kịch bản tương ứng nếu User bắt đầu câu chat bằng các lệnh sau:

### `/audit-seo` — Lệnh Chính (Primary Command)
- **Cú pháp**: `/audit-seo [URL hoặc tên dự án] [--level 1|2|3] [--batch]`
- **Mặc định**: Không có `--level` → tự động chạy cấp 2 (dynamic).
- `--level 1` = `/scan-static` | `--level 2` = `/scan-dynamic` | `--level 3` = `/scan-hunter`
- `--batch`: Quét đồng loạt nhiều dự án. Agent tự scan thư mục workspace, phát hiện các project (dựa trên `package.json` / `next.config.ts` / `astro.config.mjs`), build lần lượt, audit từng site và xuất **1 báo cáo tổng hợp `batch-audit-summary.md`**.

### Lệnh tắt (Alias — tương thích ngược):
- `/scan-static`: (Cấp 1 — Quét Tĩnh) Không cần build, chỉ đọc source code. Check: Hardcode Secrets, `<a>` thiếu `title`, `href="#"`, `<a>` bọc `<div>`, thiếu `alt`, thiếu Schema, thiếu canonical, ảnh PNG/JPG chưa convert WebP. Output: `code-audit-report.md`.
- `/scan-dynamic`: (Cấp 2 — Quét Động) Build + Puppeteer test. DOM check: H1, headings, canonical, Schema JSON-LD, Console errors. UI check: GEO box, FAQ accordion, image alt/dimensions, navigation priority, live search. CWV check: LCP lazy, CLS dimensions, INP handlers. Output: `qa-audit-report.md` + screenshots.
- `/scan-hunter`: (Cấp 3 — Đội Đặc Nhiệm) Full audit: Lighthouse CLI, Sitemap cross-check DB, Orphan Pages, Redirect Chains, Keyword Cannibalization (so sánh Meta Title toàn site). Output: `qa-audit-report.md` + `fix-checklist.md`.

---

## 📥 Pre-flight (BẮT BUỘC ĐỌC TRƯỚC)
1. **🚨 MANDATORY: Deep Context Scan**: Rà soát triệt để các file Báo cáo Audit cũ (`seo_*.md`, `qa-audit-report.md`), workflow files (`12-seo-geo.md`), và `master-identity.md`. CẤM đọc lướt rồi tự suy diễn.
2. **Anti-Surface Fix**: Khi phát hiện lỗi QA/Audit, BẮT BUỘC đối chiếu với Kiến trúc Quy chuẩn của dự án (ví dụ Sitemap Index vs Single Sitemap). CẤM đưa ra giải pháp sửa nông/bề nổi.
3. `.agent/identity/master-identity.md` → Base URL, framework, DB connection, cấu trúc Silo/Route.
4. `package.json` → Xác định dependencies có sẵn (puppeteer, axios, prisma…).
5. Config framework (`next.config.ts`, `astro.config.mjs`) → `trailingSlash`, `basePath`.

---

## 📋 Protocol

### Bước 1: URL Discovery & Cross-Check (Đối chiếu chéo)

Thu thập URL từ 2 nguồn độc lập và **BẮT BUỘC ĐỐI CHIẾU CHÉO** để bắt lỗi sitemap sai/thiếu:

| Nguồn | Cách lấy & Output |
|-------|---------|
| **Nguồn 1: Sitemap** | Fetch `{BASE_URL}/sitemap.xml` → parse `<loc>` → Output: `C:\Users\Opengate\.gemini\tmp\url-sitemap.txt` |
| **Nguồn 2: DB & Code** | Scan dynamic routes (`src/app/**/page.tsx`) + Query Database trực tiếp → Output: `C:\Users\Opengate\.gemini\tmp\url-db.txt` |

**Cross-Check Logic (Cực kỳ quan trọng):**
- URL có trong `url-db.txt` nhưng KHÔNG CÓ trong `url-sitemap.txt` → `[🔴 BUG SEO] Sitemap bị thiếu, Google không index được.`
- URL có trong `url-sitemap.txt` nhưng KHÔNG CÓ trong `url-db.txt` → `[🔴 BUG SEO] Sitemap chứa link rác/URL ảo (Ghost URL).`

→ Cuối cùng merge 2 tệp này lại thành tệp tổng `C:\Users\Opengate\.gemini\tmp\url-master.txt` để đưa vào Bước 2.

---

### Bước 2: Chiến Lược A — Quét Nhanh Toàn Bộ URL (Lightweight)

**Mục tiêu**: Phát hiện data gap, thiếu nội dung, link chết — không cần render JS.

Script `C:\Users\Opengate\.gemini\tmp\qa-fast-scan.js` dùng `fetch()` thuần (không Puppeteer), chạy song song 20 concurrent:

```javascript
// Với MỖI URL trong C:\Users\Opengate\.gemini\tmp\url-master.txt:
const res = await fetch(url)
const html = await res.text()

const checks = {
  status: res.status,                              // 404/500 → 🔴 BUG
  hasContent: html.length > 500,                   // Page rỗng → 🔴 BUG
  titleMissing: !/<title>[^<]{10,}<\/title>/.test(html), // Thiếu title → 🔴 SEO
  h1Missing: !/<h1[\s>]/.test(html),              // Thiếu H1 → 🔴 SEO
  wordCount: html.replace(/<[^>]+>/g, ' ')
                 .replace(/\s+/g, ' ').split(' ').length, // < 300 → 🔴 THIN
  hasMockData: /Khu phố 1|Tổ dân phố 1|lorem ipsum|placeholder/i.test(html), // → 🔴 BUG
  schemaPresent: html.includes('application/ld+json'), // Thiếu → 🟡 SEO
}
```

**Ngưỡng phân loại:**
- `status >= 400` → `🔴 BROKEN`
- `wordCount < 300` → `🔴 THIN CONTENT`
- `wordCount < 600` → `🟡 THIN CONTENT WARNING`
- `hasMockData === true` → `🔴 MOCK DATA LEAK`
- `titleMissing || h1Missing` → `🔴 SEO CRITICAL`
- `schemaPresent === false` → `🟡 SEO`

**Output**: `C:\Users\Opengate\.gemini\tmp\fast-scan-result.json` — toàn bộ URL + trạng thái từng check.

---

### Bước 3: Chiến Lược B — Scan Sâu 5-10 URL Đại Diện (Deep Audit)

**Cách chọn 5-10 URL đại diện:**
```
1 URL Trang chủ (/)
1 URL mỗi Silo Hub (/lich-cat-dien, /phat-nguoi, …)
1 URL Province đại diện mỗi Silo
1 URL Ward/District (trang lá - leaf node)
1 URL Blog/Article (nếu có)
```
→ Tổng: 7-10 URL, cover đủ mọi loại template.

Script `C:\Users\Opengate\.gemini\tmp\qa-deep-audit.js` dùng Puppeteer với Stealth plugin:

```javascript
// Với MỖI URL đại diện → crawl đầy đủ:

page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()) })
page.on('pageerror', err => criticals.push(err.message))

const deep = await page.evaluate(() => ({
  // SEO Structure
  title: document.title,
  titleLength: document.title.length,
  h1Count: document.querySelectorAll('h1').length,
  h1Text: document.querySelector('h1')?.innerText?.trim(),
  metaDesc: document.querySelector('meta[name="description"]')?.content,
  metaDescLength: document.querySelector('meta[name="description"]')?.content?.length,
  canonical: document.querySelector('link[rel="canonical"]')?.href,

  // Content Quality & UI Section Depth
  wordCount: document.body.innerText.replace(/\s+/g,' ').split(' ').length,
  homepageSectionCount: document.querySelectorAll('main > section, main > div > section, section').length,
  hasFaqBlock: document.body.innerHTML.includes('FAQPage') ||
               !!document.querySelector('[data-faq], .faq-block'),
  hasVisualFaqAccordion: !!document.querySelector('[data-faq-accordion], details, .faq-accordion, .accordion-item'),
  hasDirectAnswer: !!document.querySelector('.geo-direct-answer, [class*="direct-answer"]'),

  // Schema & Technical
  schemas: [...document.querySelectorAll('script[type="application/ld+json"]')]
             .map(s => JSON.parse(s.innerText)['@type']),
  hasBreadcrumbSchema: document.body.innerHTML.includes('BreadcrumbList'),

  // UI/UX Issues
  h2InLink: document.querySelectorAll('a h2, a h3').length,     // Heading lồng trong Link
  lcpLazy: [...document.querySelectorAll('img')]
             .filter(img => img.getBoundingClientRect().top < 500)
             .some(img => img.loading === 'lazy'),              // LCP image lazy → 🔴 CWV
  brokenImages: [...document.querySelectorAll('img')]
                  .filter(img => !img.naturalWidth).length,
  crossSiloLinks: document.querySelectorAll('[data-cross-silo], .cross-silo-links').length,
}))

// Screenshot để review trực quan
await page.screenshot({ path: `C:\Users\Opengate\.gemini\tmp\screenshots/${slug}.png`, fullPage: true })
```

**Phân loại từ Deep Audit — Đối chiếu 1:1 với [seo-preflight-card](file:///C:/Users/Opengate/.gemini/config/plugins/wb-agent/skills/seo-preflight-card/SKILL.md) (Single Source of Truth cho tất cả SEO Criteria):**

| Case Protocol | Phát hiện | Severity |
|---------------|-----------|---------|
| **Case 1** | URL thiếu Trailing Slash / Redirect 308 | 🔴 SEO |
| **Case 2** | `titleLength < 30` hoặc `> 60` / `metaDescLength > 160` hoặc trống | 🔴 SEO |
| **Case 3** | `h1Count !== 1` (Thiếu H1 hoặc thừa H1) / `h2InLink > 0` (Thẻ `<a>` bọc khối H2/H3) | 🔴 SEO / SEMANTIC |
| **Case 4** | `hasDirectAnswer === false` (Thiếu GEO Direct Answer Hero Box hợp nhất) | 🔴 GEO / AI OVERVIEWS |
| **Case 5** | Canonical relative / Meta Robots `noindex` ở public page | 🔴 SEO |
| **Case 6** | `hasBreadcrumbSchema === false` (trang con) / Schema thiếu loại phù hợp | 🔴 SEO |
| **Case 7** | `crossSiloLinks === 0` (Thiếu internal links 3 chiều Pillar<->Silo<->Cluster) | 🟡 LINK JUICE |
| **Case 8** | `hasFaqSchema === true && hasVisualFaqAccordion === false` (Có Schema nhưng thiếu UI Accordion) | 🔴 FAQ VISUAL MISSING |
| **Case 9** | Page rỗng/lỗi data nhưng trả về HTTP 200 thay vì `notFound()` (Soft 404) | 🔴 SOFT 404 |
| **Case 10** | `brokenImages > 0` / Thiếu dynamic Alt text / Background màu Kim-Hỏa sai Phong Thủy | 🔴 UI / ALT TEXT |
| **Chung** | JS Console Error | 🔴 BUG |
| **Trang chủ** | `homepageSectionCount < 6` (Trang chủ < 6 Section) | 🔴 HOMEPAGE THIN CONTENT (-15đ, Block Deploy) |

---

## 📤 Output — `.agent/specs/qa-audit-report.md`

```markdown
# QA Audit Report — [Project] — [Date]

## 📊 Tổng Quan
| Metric | Số lượng |
|--------|---------|
| Tổng URL quét (Fast Scan) | X |
| Lỗi Sitemap (Thiếu/Thừa) | X |
| 404 Broken | X |
| Thin Content (< 300 từ) | X |
| Mock Data Leak | X |
| Deep Audit (URL đại diện) | 8 |

## Score: XX/100 | Verdict: ✅ PASS / ❌ BLOCK DEPLOY

---
## 🔴 Critical (Fast Scan — Tất cả URL)
### Sitemap Discrepancies (Lệch Sitemap vs DB)
| URL | Lỗi |
### Broken 404/500
| URL | Status |
### Thin Content / Mock Data
| URL | Vấn đề |

---
## 🔴🟡 Deep Structural Issues (5-10 URL Đại Diện)
| URL | Issue | Fix gợi ý |

---
## 🛠 Action Items + Code Snippet Fix
1. Fix logic sinh sitemap: `code snippet`
2. Fix BreadcrumbList JSON-LD: `code snippet`

---
## 📝 Living Documentation Check
- [ ] So khớp logic code thực tế với `spec.md`. Có sự sai lệch (Drift) nào không?
- [ ] BẮT BUỘC yêu cầu Agent Dev cập nhật ngược (Reverse Update) `spec.md` nếu phát hiện sai lệch trước khi duyệt Release.
```

**Scoring:**
- `🔴` Critical: -10 điểm/lỗi (tối đa -50)
- `🟡` Warning: -3 điểm/lỗi
- Score ≥ 80 → ✅ PASS | Score < 80 → ❌ BLOCK DEPLOY

---

## 🚫 Guard Rails
- Script chạy trong `C:\Users\Opengate\.gemini\tmp\` — không commit vào project.
- Deep Audit (Bước 3) tối đa **10 URL** — không crawl toàn bộ.
- Fast Scan (Bước 2) crawl ALL URL nhưng chỉ dùng `fetch()` thuần — nhanh, nhẹ.
- Phải đối chiếu chéo (Cross-check) Sitemap và Database để bắt lỗi Sitemap.
- Score < 80 hoặc có lỗi `🔴` → Đề xuất **KHÔNG DEPLOY**.
