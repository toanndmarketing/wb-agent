import os
import re
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def crawl_google_search_docs(start_url="https://developers.google.com/search/docs/essentials", output_dir="tmp/google_search_docs"):
    """
    Quét toàn bộ sidebar menu của Google Search Central Docs và tải tất cả tài liệu về máy.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    os.makedirs(output_dir, exist_ok=True)
    print(f"🔍 Đang quét danh sách URL từ: {start_url}...")

    # 1. Tải trang chính để bóc tách Sidebar Navigation
    try:
        req = urllib.request.Request(start_url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"❌ Lỗi khi tải trang gốc {start_url}: {e}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    
    # Tim các liên kết thuộc phần /search/docs/
    doc_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/search/docs' in href:
            full_url = urllib.parse.urljoin(start_url, href).split('#')[0].split('?')[0]
            # Loại bỏ các link không phải bài viết
            if not full_url.endswith(('.png', '.jpg', '.pdf', '.svg')):
                doc_links.add(full_url)

    sorted_links = sorted(list(doc_links))
    print(f"🎯 Đã tìm thấy {len(sorted_links)} liên kết tài liệu unique trong Sidebar!")

    # 2. Tiến hành tải từng bài viết
    master_file = os.path.join(output_dir, "_master_all_docs.md")
    success_count = 0

    with open(master_file, "w", encoding="utf-8") as master_f:
        master_f.write(f"# GOOGLE SEARCH CENTRAL - TOÀN BỘ TÀI LIỆU CẢO ĐƯỢC\n\n")
        master_f.write(f"Nguồn gốc: {start_url}\nTổng số bài: {len(sorted_links)}\n\n" + "="*50 + "\n\n")

        for idx, url in enumerate(sorted_links, 1):
            print(f"[{idx}/{len(sorted_links)}] 📥 Đang tải: {url}")
            try:
                sub_req = urllib.request.Request(url, headers=headers)
                sub_html = urllib.request.urlopen(sub_req).read().decode('utf-8')
                sub_soup = BeautifulSoup(sub_html, 'html.parser')

                article = sub_soup.find('article') or sub_soup.find('main') or sub_soup.find(id='main-content')
                
                # Lấy tiêu đề bài viết
                h1 = sub_soup.find('h1')
                title = h1.get_text(strip=True) if h1 else url.split('/')[-1]

                if article:
                    for s in article.find_all(['script', 'style', 'nav', 'devsite-toc', 'devsite-content-footer', 'devsite-header']):
                        s.decompose()
                    text_content = article.get_text(separator='\n')
                    cleaned_text = re.sub(r'\n+', '\n', text_content).strip()
                else:
                    cleaned_text = "Không trích xuất được nội dung bài viết."

                # Tạo tên file đơn lẻ
                slug = url.replace('https://developers.google.com/search/docs/', '').strip('/').replace('/', '_')
                if not slug:
                    slug = "index"
                single_file = os.path.join(output_dir, f"{slug}.md")

                # Ghi file riêng lẻ
                with open(single_file, "w", encoding="utf-8") as f:
                    f.write(f"# {title}\nURL: {url}\n\n{cleaned_text}\n")

                # Ghi vào file tổng master
                master_f.write(f"## {title}\nURL: {url}\n\n{cleaned_text}\n\n" + "="*50 + "\n\n")

                success_count += 1
                time.sleep(0.2) # Nghỉ nhẹ chống rate limit

            except Exception as e:
                print(f"  ⚠️ Lỗi khi tải {url}: {e}")

    print(f"\n✅ ĐÃ HOÀN THÀNH! Đã tải thành công {success_count}/{len(sorted_links)} trang tài liệu.")
    print(f"📁 Thư mục lưu bài lẻ: {os.path.abspath(output_dir)}")
    print(f"📄 File tổng master: {os.path.abspath(master_file)}")

if __name__ == '__main__':
    crawl_google_search_docs()
