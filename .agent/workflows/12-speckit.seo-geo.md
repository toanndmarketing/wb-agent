---
description: Technical SEO & GEO Audit & Optimization
---

# 🔍 SEO & GEO Audit

## Pre-conditions
- Trang public đã được triển khai (ví dụ: landing page, blog, product pages).
- `.agent/knowledge_base/seo_standards.md` tồn tại (khuyến nghị).

## Steps

1. **@speckit.seo-geo** — Tiến hành audit toàn diện qua 3 Phase:
   - **Phase 1: Content Audit**: Kiểm tra Heading structure, Readability, Multimodal (Alt text, video), Fact-density.
   - **Phase 2: Technical SEO Audit**: Check Title/Meta description, Canonical URLs, JSON-LD Schema (Structured data), Sitemap & Robots.txt, Core Web Vitals.
   - **Phase 3: GEO Audit (AI Search)**: Check file `llms.txt`, SSR/SSG, E-E-A-T signals, Direct Answer formatting (CẤM dùng Markdown Links trong các khối HTML protected như `.geo-direct-answer`).
2. Output: Báo cáo chi tiết tại `.agent/memory/seo-geo-report.md` (bao gồm Score 0-100, danh sách các lỗi 🔴 Critical, 🟡 Warning, 🟢 Info và giải pháp fix).
3. Nếu Score < 80 hoặc có lỗi 🔴 Critical → Fix các issues được phát hiện → Re-audit cho đến khi đạt yêu cầu.

## Success Criteria
- ✅ SEO-GEO Score ≥ 80
- ✅ 0 lỗi 🔴 Critical
- ✅ File `llms.txt` tồn tại ở root domain
- ✅ Báo cáo `seo-geo-report.md` được khởi tạo thành công
