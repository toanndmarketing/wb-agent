# 🔍 SEO & GEO Standards

## 📋 Technical SEO Checklist (Bắt buộc)
- [ ] Mỗi page có `<title>` unique, độ dài ≤ 60 ký tự.
- [ ] **Keyword-First Title**: Từ khóa chính được đặt càng gần đầu tiêu đề càng tốt.
- [ ] **CTR Modifiers**: Sử dụng các từ bổ nghĩa tăng click-through-rate (như *tốt nhất, hướng dẫn, checklist, review, [năm hiện tại - ví dụ: 2026]*).
- [ ] Mỗi page có `<meta description>` lôi cuốn, độ dài ≤ 160 ký tự.
- [ ] Chỉ 1 `<h1>` duy nhất mỗi page, heading hierarchy chuẩn (H1 → H2 → H3, không nhảy cấp).
- [ ] Canonical URL cho mọi page để tránh duplicate content.
- [ ] `sitemap.xml` tự động generate và submit lên Google Search Console.
- [ ] `robots.txt` cấu hình đúng (cho phép các AI search crawlers).
- [ ] Image: có `alt` text mô tả chi tiết thực thể, sử dụng tên file ảnh chứa từ khóa chính (dạng `keyword.jpg`), lazy loading, format hiện đại WebP/AVIF.
- [ ] URL slug: lowercase, dấu gạch ngang, không dấu tiếng Việt, ngắn gọn chứa từ khóa chính.
- [ ] Mobile-first responsive design.
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1.

## ✍️ Helpful Content & SEO Copywriting (Backlinko Standard)
- [ ] **Lồng ghép trải nghiệm thực tế**: Bài viết có case study, trải nghiệm thực chứng thay vì lý thuyết suông.
- [ ] **Bypass AI Detectors**: Câu văn có nhịp điệu phong phú (burstiness), cấu trúc câu đa dạng, tránh dùng từ sáo rỗng thường thấy của AI.
- [ ] **Tone giọng E-E-A-T**: Thể hiện rõ chuyên môn của chuyên gia/tác giả (định nghĩa trong `master-identity.md`).
- [ ] **Keyword in first 100 words**: Từ khóa chính xuất hiện tối thiểu 1 lần trong 100-150 từ đầu tiên của trang.
- [ ] **APP Formula (Agree, Promise, Preview)**: Phần mở đầu bài viết tuân thủ cấu trúc APP: Đồng ý (Agree) -> Hứa hẹn (Promise) -> Xem trước (Preview).
- [ ] **Bucket Brigades**: Sử dụng các cụm từ chuyển tiếp (Ví dụ: *"Thực tế là...", "Nhưng đó chưa phải là tất cả...", "Bạn có muốn biết tại sao không?"...*) để tăng Dwell Time.
- [ ] **Above the Fold UX**: Tiêu đề và dòng chữ đầu tiên phải xuất hiện ngay lập tức ở màn hình đầu tiên khi tải trang, không bị banner/ảnh header lớn che khuất.
- [ ] **Độ sâu bài viết**: Độ dài từ 1000 - 3000 từ tùy từ khóa để bao quát chủ đề, giữ chân người dùng lâu nhất.

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` tại root domain để định hướng cho AI crawlers.
- [ ] Structured Data (JSON-LD) đầy đủ cho các trang công khai.
- [ ] **Direct Answer Box**: Có box tóm tắt nhanh (2-3 câu, ≤ 80 từ, bôi đậm thực thể chính) ở ngay đầu bài viết.
- [ ] **Semantic Chunking**: Chia nhỏ nội dung bằng H2/H3 có tính mô tả chi tiết, khớp với truy vấn đối thoại thực tế.
- [ ] **Lead with the Answer**: Đưa câu trả lời/kết luận ngay câu đầu tiên dưới H2/H3 trước khi phân tích chi tiết.
- [ ] **Quotable Statements & Statistics**: Sử dụng câu độc lập hoàn chỉnh, mang đầy đủ ngữ cảnh để LLM dễ trích xuất và trích dẫn trực tiếp. Lồng ghép số liệu thống kê hoặc quote từ chuyên gia (tăng 30-40% khả năng được AI Overviews trích dẫn).
- [ ] **Fact-Dense & So sánh**: Có bảng so sánh hoặc list số liệu cụ thể để AI dễ trích xuất dữ liệu dạng bảng.

## 🔗 Strict Internal Linking Rules
- [ ] **Tần suất**: Tối đa 1 link/destination trên toàn bộ bài viết.
- [ ] **Vị trí**: Chỉ chèn link ở từ khóa xuất hiện lần đầu tiên (First Occurrence Only).
- [ ] **Vùng loại trừ**: Không chèn link trong tiêu đề (H1, H2, H3), Frontmatter, Code blocks, Schema, Table code.
- [ ] **Mã nguồn an toàn**: Tuyệt đối không viết Markdown link `[text](url)` bên trong thẻ HTML thô, bắt buộc dùng `<a href="url">text</a>`.

## 🛠️ Google Search Console (GSC) & Indexability Troubleshooting
- [ ] **robots.txt Crawlability**: Đảm bảo robots.txt cho phép Googlebot và các AI bots crawl. `Crawl allowed` phải là "Yes".
- [ ] **noindex Gating**: Đảm bảo các trang quan trọng không chứa `<meta name="robots" content="noindex">` hoặc header `X-Robots-Tag: noindex`.
- [ ] **Canonical Alignment**: Khai báo thẻ `<link rel="canonical" href="...">` chính xác. Tránh trường hợp Google-selected canonical khác với User-declared canonical.
- [ ] **Robots.txt Availability**: Đảm bảo file `/robots.txt` luôn trả về HTTP 200/404 ổn định. Nếu robots.txt bị lỗi server (HTTP 5xx) hoặc không thể truy cập, Googlebot sẽ dừng crawl toàn bộ site.
- [ ] **DNS & SSL Health**: Tránh các lỗi DNS (unresponsive, private IP mapping) và đảm bảo chứng chỉ SSL hợp lệ. Googlebot sẽ không crawl trang HTTPS nếu chứng chỉ SSL không hợp lệ.
- [ ] **Server Connectivity & Response**: Server phải phản hồi nhanh (LCP < 2.5s), không bị ngắt kết nối giữa chừng (truncated response/headers) hoặc cấu hình nén dữ liệu (compression) lỗi.
- [ ] **Watch Page Video Indexing**: Nếu trang chứa video cần index, video đó phải nằm trên "Watch Page" (trang tập trung xem video, video chiếm vị trí nổi bật đầu trang HTML), có thẻ thumbnail và dữ liệu cấu trúc VideoObject chính xác.

## 📊 Schema.org (JSON-LD Templates)

### Article
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[Tiêu đề bài viết]",
  "image": "[URL hình ảnh đại diện]",
  "datePublished": "[Ngày đăng ISO]",
  "dateModified": "[Ngày cập nhật ISO]",
  "author": {
    "@type": "Person",
    "name": "[Tên chuyên gia/Tác giả]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Tên thương hiệu]"
  }
}
```

### Product
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Tên sản phẩm]",
  "image": "[URL ảnh sản phẩm]",
  "description": "[Mô tả ngắn]",
  "offers": {
    "@type": "Offer",
    "price": "[Giá tiền]",
    "priceCurrency": "VND",
    "availability": "https://schema.org/InStock"
  }
}
```

### FAQ
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Câu hỏi 1]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Câu trả lời 1]"
      }
    }
  ]
}
```

## 📖 Google Search Central Reference Library
Tài liệu tham khảo chính thống từ Google (đã được chắt lọc tối ưu token):
- [Google Search Essentials](file:///.agent/knowledge_base/google_search/search_essentials.md)
- [Cơ chế cào & Index của Google](file:///.agent/knowledge_base/google_search/crawling_indexing.md)
- [Quy chuẩn file robots.txt của Google](file:///.agent/knowledge_base/google_search/robots_txt.md)
- [Tối ưu hóa thẻ Canonical](file:///.agent/knowledge_base/google_search/canonicalization.md)
- [Quy chuẩn Sitemaps của Google](file:///.agent/knowledge_base/google_search/sitemaps.md)
- [Dữ liệu cấu trúc Schema của Google](file:///.agent/knowledge_base/google_search/structured_data.md)
- [Hệ thống nội dung hữu ích (Helpful Content)](file:///.agent/knowledge_base/google_search/helpful_content.md)
- [Tiêu chuẩn đánh giá EEAT chất lượng cao](file:///.agent/knowledge_base/google_search/eeat_guide.md)
- [Tối ưu hóa JavaScript Rendering SEO](file:///.agent/knowledge_base/google_search/javascript_seo.md)
- [Xử lý mã lỗi HTTP & Crawl Errors](file:///.agent/knowledge_base/google_search/http_status_codes.md)
