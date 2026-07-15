#!/usr/bin/env python3
"""
SeoLearner - Tự động tải, chắt lọc và lưu trữ tài liệu Google Search Central.
Chuyển đổi sang Markdown súc tích để tiết kiệm token tối đa cho AI Agent.
Sử dụng hoàn toàn Python Standard Library (urllib, html.parser, re).
"""

import os
import re
import urllib.request
from html.parser import HTMLParser

# Danh sách tài liệu Google Search Central cốt lõi cần cào (phiên bản tiếng Việt)
GOOGLE_SEO_DOCS = {
    "search_essentials": {
        "url": "https://developers.google.com/search/docs/essentials?hl=vi",
        "title": "Google Search Essentials (Nguyên tắc cốt lõi)"
    },
    "crawling_indexing": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=vi",
        "title": "Google Crawlers & Indexing Overview (Cơ chế cào & index)"
    },
    "robots_txt": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=vi",
        "title": "Robots.txt Specification (Quy chuẩn robots.txt)"
    },
    "canonicalization": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=vi",
        "title": "Consolidate Duplicate URLs (Tối ưu hóa Canonical)"
    },
    "sitemaps": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=vi",
        "title": "Sitemaps Overview (Quy chuẩn Sitemap)"
    },
    "structured_data": {
        "url": "https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=vi",
        "title": "Intro to Structured Data (Dữ liệu cấu trúc Schema)"
    },
    "helpful_content": {
        "url": "https://developers.google.com/search/docs/appearance/helpful-content-system?hl=vi",
        "title": "Google Helpful Content System (Hệ thống nội dung hữu ích)"
    },
    "eeat_guide": {
        "url": "https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=vi",
        "title": "Google E-E-A-T Quality Guidelines (Tiêu chuẩn EEAT)"
    },
    "javascript_seo": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=vi",
        "title": "JavaScript SEO Basics (Tối ưu hóa JS Rendering)"
    },
    "http_status_codes": {
        "url": "https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=vi",
        "title": "HTTP Status Codes & Crawl Errors (Xử lý mã trạng thái & lỗi kết nối)"
    }
}


class DevsiteHtmlParser(HTMLParser):
    """
    Parser thông minh để trích xuất nội dung từ thẻ có class devsite-article-body.
    Chuyển đổi trực tiếp sang Markdown súc tích (chắt lọc tri thức tinh khiết).
    """
    def __init__(self):
        super().__init__()
        self.in_article_body = False
        self.div_depth = 0
        self.article_div_depth = -1
        self.markdown = []
        
        # Tags tracking
        self.current_tag = None
        self.in_code_block = False
        self.code_block_content = []
        self.list_level = 0
        self.list_type = [] # 'ul' or 'ol'
        
        # Buffer text
        self.text_buffer = ""

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        # Theo dõi chiều sâu div để định vị chính xác devsite-article-body
        if tag == "div":
            self.div_depth += 1
            if "class" in attrs_dict and "devsite-article-body" in attrs_dict["class"]:
                self.in_article_body = True
                self.article_div_depth = self.div_depth

        if not self.in_article_body:
            return

        # Bắt đầu code block
        if tag in ("pre", "code"):
            # Nếu thẻ pre có class devsite-code hoặc code block
            if tag == "pre" or (tag == "code" and not self.in_code_block):
                self.in_code_block = True
                self.code_block_content = []

        # Danh sách
        elif tag == "ul":
            self.list_level += 1
            self.list_type.append("ul")
        elif tag == "ol":
            self.list_level += 1
            self.list_type.append("ol")
        elif tag == "li":
            indent = "  " * (self.list_level - 1)
            bullet = "-" if (not self.list_type or self.list_type[-1] == "ul") else "1."
            self.markdown.append(f"\n{indent}{bullet} ")

        # Tiêu đề
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            self.markdown.append(f"\n\n{'#' * level} ")

    def handle_endtag(self, tag):
        if tag == "div":
            if self.in_article_body and self.div_depth == self.article_div_depth:
                self.in_article_body = False
                self.article_div_depth = -1
            self.div_depth -= 1

        if not self.in_article_body:
            return

        if tag == "pre" or (tag == "code" and self.in_code_block):
            if self.in_code_block:
                self.in_code_block = False
                code_text = "".join(self.code_block_content).strip()
                # Xác định ngôn ngữ code block nếu có
                lang = "json" if "{" in code_text and "}" in code_text else "html"
                self.markdown.append(f"\n```{lang}\n{code_text}\n```\n")

        elif tag in ("ul", "ol"):
            if self.list_level > 0:
                self.list_level -= 1
                self.list_type.pop()
        
        elif tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6"):
            if self.text_buffer.strip():
                clean_text = re.sub(r'\s+', ' ', self.text_buffer).strip()
                # Tinh lọc nội dung: Bỏ các câu chuyển hướng/quảng cáo của Google
                if not any(x in clean_text.lower() for x in ["chuyển đến nội dung", "tìm hiểu thêm", "tài liệu tham khảo", "phản hồi"]):
                    self.markdown.append(clean_text)
                self.text_buffer = ""

    def handle_data(self, data):
        if not self.in_article_body:
            return

        if self.in_code_block:
            self.code_block_content.append(data)
        else:
            if self.current_tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self.markdown.append(data.strip())
            elif self.current_tag == "li":
                self.markdown.append(data.strip())
            else:
                self.text_buffer += data


def distill_content(markdown_text):
    """
    Tinh lọc sâu tài liệu Markdown để giảm dung lượng token xuống tối thiểu:
    - Loại bỏ các đoạn văn giải thích lý thuyết dông dài.
    - Giữ lại các H2/H3, list points (Checklist), mã cấu hình (code) và Alert Boxes.
    """
    lines = markdown_text.split("\n")
    distilled = []
    
    in_code_block = False
    keep_paragraph = False
    
    for line in lines:
        stripped = line.strip()
        
        # Luôn giữ lại code blocks (Schema, sitemap, robots.txt configs)
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            distilled.append(line)
            continue
        
        if in_code_block:
            distilled.append(line)
            continue

        # Giữ lại các Headings để giữ cấu trúc bài viết
        if stripped.startswith("#"):
            distilled.append(line)
            keep_paragraph = True # Đoạn văn ngay sau heading thường chứa kết luận quan trọng
            continue

        # Giữ lại các dòng Checklist / Bullet points / Code inline
        if stripped.startswith("-") or stripped.startswith("*") or re.match(r'^\d+\.', stripped):
            distilled.append(line)
            continue

        # Giữ lại các dòng quan trọng có từ khóa: "Bắt buộc", "Lưu ý", "Cảnh báo", "Không được", "Nên", "Phải"
        if any(keyword in stripped.lower() for keyword in ["bắt buộc", "lưu ý", "cảnh báo", "không được", "nên", "phải", "tránh"]):
            distilled.append(line)
            continue

        # Giữ lại đoạn văn đầu tiên sau Heading (Lead with the Answer), bỏ qua các đoạn văn bổ trợ phía sau
        if keep_paragraph and stripped:
            distilled.append(line)
            keep_paragraph = False

    return "\n".join(distilled)


def learn_google_seo(target_dir):
    """Tải và chắt lọc tài liệu SEO chính chủ từ Google."""
    knowledge_dir = os.path.join(target_dir, ".agent", "knowledge_base", "google_search")
    os.makedirs(knowledge_dir, exist_ok=True)

    print("\n🚀 Bắt đầu quá trình nạp tri thức Google Search Central...")
    print(f"📂 Thư mục lưu trữ: {knowledge_dir}\n")

    for key, doc in GOOGLE_SEO_DOCS.items():
        print(f"📥 Đang tải: {doc['title']}...")
        try:
            req = urllib.request.Request(
                doc["url"],
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                html_content = response.read().decode('utf-8')

            # Parse HTML
            parser = DevsiteHtmlParser()
            parser.feed(html_content)
            
            raw_markdown = "".join(parser.markdown)
            
            # Tinh lọc sâu để tiết kiệm token
            distilled_markdown = distill_content(raw_markdown)
            
            # Thêm header thông tin nguồn
            final_content = f"""---
title: {doc['title']}
source: {doc['url']}
last_updated: {response.info().get('Date', 'N/A')}
---

# 📖 {doc['title']}

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

{distilled_markdown}
"""
            
            file_path = os.path.join(knowledge_dir, f"{key}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)
                
            print(f"  ✅ Đã lưu và chắt lọc thành công: {key}.md ({len(final_content.split())} words)")
            
        except Exception as e:
            print(f"  ❌ Lỗi khi xử lý {key}: {e}")

    # Cập nhật file liên kết tri thức chính
    _update_seo_standards_link(target_dir)


def _update_seo_standards_link(target_dir):
    """Tự động liên kết các tài liệu Google Search mới cào vào file seo_standards.md."""
    seo_standards_path = os.path.join(target_dir, ".agent", "knowledge_base", "seo_standards.md")
    if not os.path.exists(seo_standards_path):
        return

    print("\n🔗 Đang liên kết tài liệu Google Search vào SEO Standards...")
    
    with open(seo_standards_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Thêm phần tham chiếu tài liệu Google Search Central
    reference_section = """
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
"""

    # Thay thế hoặc nối thêm phần tham chiếu
    if "## 📖 Google Search Central Reference Library" in content:
        content = re.sub(
            r"## 📖 Google Search Central Reference Library.*?(?=\n##|$)",
            reference_section.strip(),
            content,
            flags=re.DOTALL
        )
    else:
        content = content.strip() + "\n\n" + reference_section.strip() + "\n"

    with open(seo_standards_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✅ Đã cập nhật xong liên kết thư viện vào seo_standards.md!")


if __name__ == "__main__":
    # Test chạy trực tiếp
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    learn_google_seo(target)
