<RULE[user_global]>
# ⚓ GLOBAL RULE: Anchor Tag & SEO Standards

**Trạng thái**: BẮT BUỘC (Non-Negotiable) áp dụng cho TOÀN BỘ các dự án web (Astro, Next.js, React, HTML tĩnh...).

Khi code hoặc chỉnh sửa bất kỳ UI Component nào có chứa liên kết (thẻ `<a>`), Agent TUYỆT ĐỐI tuân thủ các quy tắc sau, bất kể prompt của User có nhắc đến từ khóa SEO hay không:

## 1. 7 Quy Tắc Thép Cho Thẻ `<a>`
1. **Title bắt buộc**: TẤT CẢ thẻ `<a>` (internal, external, nav) phải có `title="..."` giải thích rõ đích đến.
2. **CẤM bọc block-level**: KHÔNG dùng `<a>` bọc `<div>`, `<section>`, `<article>`, `<p>`, `<ul>`, `<nav>`, `<header>`, `<footer>` (như các khối Card lớn). Thay vào đó, bọc `<a>` ở text bên trong, và dùng CSS `::before`/`::after` với `position: absolute` để phủ clickable area ra toàn khối.
3. **CẤM ký tự trang trí trong anchor text**: KHÔNG chèn `→`, `>>`, `&rarr;`, `&raquo;`, hoặc icon trực tiếp vào nội dung text của `<a>` (làm nhiễu keyword). Mọi ký tự trang trí phải bọc trong `<span aria-hidden="true">` hoặc xử lý bằng CSS `::after`.
4. **Href hợp lệ**: CẤM dùng `href="#"`, `href=""`, `href="javascript:void(0)"`. Nếu là một action không chuyển trang, bắt buộc dùng `<button>` thay thế.
5. **External links**: Bất kỳ link nào trỏ ra ngoài (`http://`, `https://`) ĐỀU PHẢI có `rel="noopener noreferrer"` và `target="_blank"`.
6. **CẤM anchor text rỗng**: Thẻ `<a>` bắt buộc phải có visible text. Tránh việc link chỉ có khoảng trắng.
7. **Image-only link phải có alt**: Nếu thẻ `<a>` chỉ chứa duy nhất `<img>` hoặc `<svg>`, thẻ ảnh đó BẮT BUỘC phải có thuộc tính `alt="..."` mô tả chi tiết.

## 2. Quy Trình Kiểm Duyệt Bắt Buộc (SEO Auditor Gate)
Ngay sau khi sinh code có thẻ `<a>` mới hoặc sửa đổi UI Component chứa link:
- **BẮT BUỘC** phải tự động chạy lệnh kiểm duyệt bằng Node.js script: `node C:\Users\Opengate\.gemini\config\scripts\anchor-seo-auditor.cjs` từ thư mục gốc của dự án đang làm việc.
- Nếu linter báo lỗi đỏ 🔴, Agent phải tự động sửa code, sau đó chạy lại lệnh trên cho đến khi hiển thị màn hình xanh `✅ Tuyệt vời...` rồi mới được thông báo hoàn thành task cho User.
</RULE[user_global]>
