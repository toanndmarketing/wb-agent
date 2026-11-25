#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động chụp giao diện website và xuất trọn bộ 7 file PDF tài liệu đính kèm
chuẩn quy định Thông báo Website TMĐT Bán hàng của Bộ Công Thương (online.gov.vn).

Yêu cầu thư viện:
  pip install playwright pypdf
  playwright install chromium
"""

import os
import sys
import argparse
import subprocess
from urllib.parse import urljoin
from pypdf import PdfWriter

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ LỖI: Chưa cài đặt thư viện playwright. Hãy chạy: pip install playwright && playwright install chromium")
    sys.exit(1)

CSS_PRINT_CLEANUP = """
@media print {
    /* Ẩn các thanh menu cố định, nút gọi nổi, chat Zalo, bottom navigation trên mobile */
    header.sticky, 
    nav.sticky,
    .fixed,
    .sticky,
    [class*="floating"],
    [class*="float"],
    [class*="quick-contact"],
    [class*="zalo"],
    [class*="hotline-btn"],
    [class*="bottom-nav"],
    [class*="mobile-nav"],
    [class*="mobile-menu"],
    [class*="back-to-top"],
    button[aria-label*="chat"],
    button[aria-label*="zalo"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Đảm bảo trang hiển thị chữ rõ nét, nền sáng */
    body {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* Ngắt trang tự nhiên */
    h1, h2, h3 {
        page-break-after: avoid;
    }
    table, figure, img {
        page-break-inside: avoid;
    }
}
"""

def print_page_to_pdf(page, url, output_pdf_path):
    print(f"  🌐 Đang tải trang: {url}")
    try:
        response = page.goto(url, wait_until="networkidle", timeout=30000)
        if response and response.status >= 400:
            print(f"  ⚠️ Cảnh báo: Trang trả về mã lỗi HTTP {response.status}: {url}")
    except Exception as e:
        print(f"  ⚠️ Không thể tải {url}: {e}")
        # Thử lại với domcontentloaded
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception:
            return False

    # Inject CSS ẩn floating bar & bottom bar
    page.add_style_tag(content=CSS_PRINT_CLEANUP)
    
    # Cuộn trang để kích hoạt lazy loading hình ảnh
    page.evaluate("""async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 300;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;
                if(totalHeight >= scrollHeight || totalHeight > 10000){
                    clearInterval(timer);
                    window.scrollTo(0, 0);
                    resolve();
                }
            }, 50);
        });
    }""")
    page.wait_for_timeout(1000)

    # Xuất PDF khổ A4, có header & footer chuẩn
    page.emulate_media(media="print")
    page.pdf(
        path=output_pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"},
        display_header_footer=True,
        header_template='<div style="font-size: 8px; color: #888888; width: 100%; text-align: right; padding-right: 12mm;"><span class="title"></span></div>',
        footer_template='<div style="font-size: 8px; color: #888888; width: 100%; display: flex; justify-content: space-between; padding: 0 12mm;"><span>Bộ hồ sơ Thông báo Website TMĐT - online.gov.vn</span><span>Trang <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>'
    )
    return True

def merge_pdfs(input_pdf_list, output_pdf_path):
    writer = PdfWriter()
    added_any = False
    for pdf_path in input_pdf_list:
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            writer.append(pdf_path)
            added_any = True
    if added_any:
        with open(output_pdf_path, "wb") as f_out:
            writer.write(f_out)
        return True
    return False

def generate_bct_files(base_url, brand_slug, out_dir, logo_path=None):
    os.makedirs(out_dir, exist_ok=True)
    temp_dir = os.path.join(out_dir, "_temp_pdf")
    os.makedirs(temp_dir, exist_ok=True)

    base_url = base_url.rstrip("/")

    # Danh mục 7 file chuẩn kèm danh sách đường dẫn cần gộp
    file_definitions = [
        {
            "id": 1,
            "filename": f"1_Chinh_sach_bao_mat_{brand_slug}.pdf",
            "title": "Chính sách bảo mật",
            "urls": [f"{base_url}/chinh-sach-bao-mat"]
        },
        {
            "id": 2,
            "filename": f"2_Phuong_thuc_tiep_nhan_va_giai_quyet_khieu_nai_{brand_slug}.pdf",
            "title": "Phương thức tiếp nhận & giải quyết khiếu nại",
            "urls": [f"{base_url}/gop-y", f"{base_url}/dieu-khoan-su-dung"]
        },
        {
            "id": 3,
            "filename": f"3_Chinh_sach_gia_{brand_slug}.pdf",
            "title": "Chính sách giá",
            "urls": [f"{base_url}/dieu-khoan-su-dung", f"{base_url}/huong-dan-mua-hang"]
        },
        {
            "id": 4,
            "filename": f"4_Chinh_sach_ve_thanh_toan_{brand_slug}.pdf",
            "title": "Chính sách về thanh toán",
            "urls": [f"{base_url}/chinh-sach-thanh-toan"]
        },
        {
            "id": 5,
            "filename": f"5_Dieu_kien_cung_cap_hang_hoa_dich_vu_{brand_slug}.pdf",
            "title": "Điều kiện cung cấp hàng hóa/dịch vụ",
            "urls": [f"{base_url}/dieu-khoan-su-dung"]
        },
        {
            "id": 6,
            "filename": f"6_Chinh_sach_giao_hang_doi_tra_hoan_tien_{brand_slug}.pdf",
            "title": "Chính sách giao hàng, đổi trả & hoàn tiền",
            "urls": [
                f"{base_url}/chinh-sach-van-chuyen",
                f"{base_url}/chinh-sach-doi-tra",
                f"{base_url}/chinh-sach-bao-hanh"
            ]
        },
        {
            "id": 7,
            "filename": f"7_Hinh_thuc_ho_tro_truc_tuyen_{brand_slug}.pdf",
            "title": "Hình thức hỗ trợ trực tuyến",
            "urls": [f"{base_url}/lien-he", f"{base_url}/gop-y"]
        }
    ]

    print("🚀 BẮT ĐẦU XUẤT TRỌN BỘ 7 TÀI LIỆU PDF ĐĂNG KÝ BỘ CÔNG THƯƠNG...")
    print(f"👉 Website đích: {base_url}")
    print(f"📂 Thư mục xuất: {out_dir}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BCT-Exporter/1.0"
        )
        page = context.new_page()

        for item in file_definitions:
            file_num = item["id"]
            final_name = item["filename"]
            final_path = os.path.join(out_dir, final_name)
            sub_urls = item["urls"]

            print(f"📄 [{file_num}/7] Đang xử lý: {item['title']} -> {final_name}")

            temp_pdfs = []
            for idx, u in enumerate(sub_urls):
                tmp_pdf = os.path.join(temp_dir, f"file_{file_num}_part_{idx}.pdf")
                ok = print_page_to_pdf(page, u, tmp_pdf)
                if ok:
                    temp_pdfs.append(tmp_pdf)

            if len(temp_pdfs) == 1:
                # 1 trang duy nhất, đổi tên hoặc copy sang file chính
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.replace(temp_pdfs[0], final_path)
            elif len(temp_pdfs) > 1:
                # Gộp nhiều trang
                merge_pdfs(temp_pdfs, final_path)
                for t in temp_pdfs:
                    if os.path.exists(t):
                        os.remove(t)

            if os.path.exists(final_path):
                size_kb = os.path.getsize(final_path) // 1024
                print(f"  ✅ Đã xuất: {final_name} ({size_kb} KB)\n")
            else:
                print(f"  ❌ LỖI: Không xuất được file {final_name}\n")

        browser.close()

    # Dọn dẹp thư mục tạm
    try:
        os.rmdir(temp_dir)
    except Exception:
        pass

    # Xử lý Logo nếu được chỉ định
    if logo_path and os.path.exists(logo_path):
        target_logo = os.path.join(out_dir, f"0_Logo_{brand_slug}.png")
        import shutil
        shutil.copy2(logo_path, target_logo)
        print(f"🖼️ Đã sao chép logo: {target_logo}")

    print("🎉 HOÀN TẤT 100%! Toàn bộ 7 file PDF đã sẵn sàng nộp lên online.gov.vn.")

    # Mở thư mục Windows File Explorer tự động
    if sys.platform == "win32":
        try:
            os.startfile(out_dir)
        except Exception:
            subprocess.run(["explorer.exe", out_dir])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xuất bộ 7 file PDF tài liệu đính kèm Bộ Công Thương")
    parser.add_argument("--url", required=True, help="URL trang chủ website (ví dụ: https://mkpc.vn)")
    parser.add_argument("--brand", default="web", help="Slug thương hiệu (ví dụ: mkpc)")
    parser.add_argument("--out", default="./docs/bct-files", help="Thư mục lưu file PDF xuất ra")
    parser.add_argument("--logo", default=None, help="Đường dẫn file ảnh logo (nếu có)")
    args = parser.parse_args()

    generate_bct_files(args.url, args.brand, args.out, args.logo)
