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
- `/scan-static`: (Quét Tĩnh) Không cần build, chỉ đọc cấu trúc source code, kiểm tra lỗ hổng Hardcode Secrets, Component Reusability, Zod Validation, và Techstack Mismatch. Báo cáo ra `code-audit-report.md`.
- `/scan-dynamic`: (Quét Động) Khởi chạy quy trình QA Audit (Fast Scan + Deep Scan bằng Puppeteer). Chấm điểm SEO, Schema, Core Web Vitals. Báo cáo ra `qa-audit-report.md`.
- `/scan-hunter`: (Đội Đặc Nhiệm) Triệu hồi toàn bộ `hunter-team` chạy ngầm (Background). Quét rà soát Orphan Pages, Redirect Chains và Audit diện rộng trên hệ thống lớn. Lên Checklist cần sửa.

---

## 📥 Pre-flight (BẮT BUỘC ĐỌC TRƯỚC)
1. `.agent/identity/master-identity.md` → Base URL, framework, DB connection, cấu trúc Silo/Route.
2. `package.json` → Xác định dependencies có sẵn (puppeteer, axios, prisma…).
3. Config framework (`next.config.ts`, `astro.config.mjs`) → `trailingSlash`, `basePath`.

---

## 📋 Protocol

### Bước 1: URL Discovery & Cross-Check (Đối chiếu chéo)

Thu thập URL từ 2 nguồn độc lập và **BẮT BUỘC ĐỐI CHIẾU CHÉO** để bắt lỗi sitemap sai/thiếu:

| Nguồn | Cách lấy & Output |
|-------|---------|
| **Nguồn 1: Sitemap** | Fetch `{BASE_URL}/sitemap.xml` → parse `<loc>` → Output: `tmp/url-sitemap.txt` |
| **Nguồn 2: DB & Code** | Scan dynamic routes (`src/app/**/page.tsx`) + Query Database trực tiếp → Output: `tmp/url-db.txt` |

**Cross-Check Logic (Cực kỳ quan trọng):**
- URL có trong `url-db.txt` nhưng KHÔNG CÓ trong `url-sitemap.txt` → `[🔴 BUG SEO] Sitemap bị thiếu, Google không index được.`
- URL có trong `url-sitemap.txt` nhưng KHÔNG CÓ trong `url-db.txt` → `[🔴 BUG SEO] Sitemap chứa link rác/URL ảo (Ghost URL).`

→ Cuối cùng merge 2 tệp này lại thành tệp tổng `tmp/url-master.txt` để đưa vào Bước 2.

---

### Bước 2: Chiến Lược A — Quét Nhanh Toàn Bộ URL (Lightweight)

**Mục tiêu**: Phát hiện data gap, thiếu nội dung, link chết — không cần render JS.

Script `tmp/qa-fast-scan.js` dùng `fetch()` thuần (không Puppeteer), chạy song song 20 concurrent:

```javascript
// Với MỖI URL trong tmp/url-master.txt:
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

**Output**: `tmp/fast-scan-result.json` — toàn bộ URL + trạng thái từng check.

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

Script `tmp/qa-deep-audit.js` dùng Puppeteer với Stealth plugin:

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

  // Content Quality
  wordCount: document.body.innerText.replace(/\s+/g,' ').split(' ').length,
  hasFaqBlock: document.body.innerHTML.includes('FAQPage') ||
               !!document.querySelector('[data-faq], .faq-block'),
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
await page.screenshot({ path: `tmp/screenshots/${slug}.png`, fullPage: true })
```

**Phân loại từ Deep Audit:**

| Phát hiện | Severity |
|-----------|---------|
| JS Console Error | 🔴 BUG |
| `h1Count !== 1` | 🔴 SEO |
| `titleLength < 30` hoặc `> 60` | 🔴 SEO |
| `metaDescLength > 160` hoặc trống | 🟡 SEO |
| `hasBreadcrumbSchema === false` (trang con) | 🔴 SEO |
| `hasFaqBlock === false` (Silo Hub) | 🟡 MISSING |
| `hasDirectAnswer === false` | 🟡 MISSING |
| `lcpLazy === true` | 🔴 CWV |
| `h2InLink > 0` | 🔴 HTML SEMANTIC |
| `brokenImages > 0` | 🔴 UI |
| `crossSiloLinks === 0` (trang lá) | 🟡 LINK JUICE |
| Schema thiếu loại phù hợp | 🟡 SEO |

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
- Script chạy trong `tmp/` — không commit vào project.
- Deep Audit (Bước 3) tối đa **10 URL** — không crawl toàn bộ.
- Fast Scan (Bước 2) crawl ALL URL nhưng chỉ dùng `fetch()` thuần — nhanh, nhẹ.
- Phải đối chiếu chéo (Cross-check) Sitemap và Database để bắt lỗi Sitemap.
- Score < 80 hoặc có lỗi `🔴` → Đề xuất **KHÔNG DEPLOY**.
