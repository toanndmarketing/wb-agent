---
name: pseo-mass-deployment
description: Framework sinh nội dung hàng loạt (Programmatic SEO) an toàn, chống hallucination bằng JSON Context và chiến thuật ép Index.
triggers:
  - "pseo"
  - "programmatic seo"
  - "mass deployment"
  - "sinh bài hàng loạt"
  - "data driven"
od:
  mode: workflow
  craft:
    requires: []
  design_system:
    requires: false
---

# 🚀 pSEO Mass Deployment Protocol

Skill này hướng dẫn Agent quy trình chuẩn mực để triển khai các chiến dịch pSEO (sinh hàng nghìn URLs) mà không vi phạm chính sách Spam của Google.

## Workflow Thực Thi

1. **Thiết kế Cấu trúc Dữ liệu (Data-Driven Prompting)**
   - Khảo sát Database hiện có. Trích xuất các dữ kiện thật (Facts) dưới dạng JSON.
   - CẤM gọi AI sinh bài nếu chỉ có mỗi "Title". BẮT BUỘC thiết kế Prompt dạng: `[System Role] + [Instruction] + [JSON Context Data]`. AI chỉ đóng vai trò "văn vẻ hóa" dữ kiện thực tế và không được bịa đặt thêm (Hallucination).

2. **Định hình Cấu trúc SEO (Indexing Strategy)**
   - Chọn đúng loại Schema thay vì rập khuôn (ví dụ: dùng `Dataset`, `Trip`, `LocalBusiness`, `FAQPage`, `Product` thay vì `Article`/`BlogPosting`). Google ưu tiên directory-type content hơn so với thin blog.
   - Thiết kế các trang Hub (Danh mục) chứa Interlinking chặt chẽ (Hub & Spoke).

3. **Cấu hình Bot Crawling (Link Juice)**
   - KHÔNG lạm dụng Google Indexing API. Thiết lập Breadcrumbs, Related Posts và Menu Hub tốt để Google Bot luân chuyển tự nhiên (Organic Indexing).
   - Nếu phải dùng sitemap.xml: Chia nhỏ (Silo Sitemap) tối đa 500 URLs/file. Áp dụng chiến thuật Drip-feed (submit rải rác từng ngày). CẤM submit toàn bộ cho domain mới. Các UI Component không được tĩnh mà phải phụ thuộc Context Render.
   - BẮT BUỘC phải inject thẻ `<lastmod>` để báo hiệu Google ưu tiên Crawl.

4. **Tích hợp Automation Pipeline**
   - Đảm bảo script tự động có truyền thêm Random Variables (như `Tone_Variation` hoặc `Story_Hook`) để bài viết không bị dập khuôn bố cục.
   - Khi gọi API Local LLM (VD: Ollama), hãy chạy Background Script có giới hạn Timeout an toàn, tránh block luồng chính (Main Thread) của IDE.
