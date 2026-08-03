# Báo cáo: Tối ưu hóa Kiến trúc SEO & Khắc phục Keyword Cannibalization cho TasteHi.com

## 1. Vấn đề phát hiện
Theo báo cáo phân tích dữ liệu Google Search Console trước đó trên TasteHi.com, hệ thống đang gặp hiện tượng **Keyword Cannibalization (ăn thịt từ khóa)** nghiêm trọng giữa các chi nhánh của cùng một Brand lớn (như Subway, Domino's Pizza, Starbucks, McDonald's...):
* **Sự trùng lặp tên thực thể (Entity Name):** Có nhiều trang chi nhánh con đều lưu trữ tên thực thể là tên Brand chung (ví dụ: `Subway` hoặc `Subway (shop for an in)`), dẫn đến thẻ `<title>` và heading `<h1>` trùng lặp trong mắt Google.
* **Sự bối rối của Google Bot:** Khi người dùng tìm kiếm từ khóa địa phương có chứa thương hiệu (ví dụ: `subway aina haina`), Google không thể xác định đâu là trang chính xác và liên tục hoán đổi thứ hạng giữa 9 trang Subway khác nhau.
* **Gãy liên kết Entity Schema:** Trong Next.js frontend, mặc dù component `<RestaurantSchema>` có code xử lý `brand` và `parentOrganization` (trỏ về trang Pillar Brand `/brands/[slug]/`), nhưng ở file route `RestaurantDetailPage (page.tsx)` lại quên truyền thuộc tính này, làm mất liên kết thực thể quan trọng của trang con về trang Pillar Brand cha.

---

## 2. Giải pháp kỹ thuật đã triển khai

### A. Tối ưu hóa dữ liệu (Database level)
Chúng tôi đã xây dựng và thực thi một script SQL tối ưu hóa nâng cao trực tiếp vào PostgreSQL database container (`alohaeats-postgres`):
* **Trích xuất tên đường tự động (Street Extraction):** Sử dụng Regular Expression để làm sạch địa chỉ, tự động tách số nhà ở đầu và các ký tự phòng/tầng ở cuối để lấy tên đường sạch nhất (ví dụ: `1020 Keolu Dr Suite C6a` -> `Keolu Dr`).
* **Chuẩn hóa tên chi nhánh độc bản:** Đổi tên toàn bộ **402 chi nhánh** thuộc **14 Brand lớn** sang định dạng:
  $$\text{Name} = \text{[Brand Name]} - \text{[City]} \ (\text{[Street Name]})$$
  *Ví dụ:*
  * `Subway (shop for an in)` -> `Subway - Honolulu (Hind Dr)`
  * `Domino's Pizza (4454 Nuhou street Unit 401 Ste 401)` -> `Domino's Pizza - Lihue (Nuhou street)`
  * `Zippy's - Honolulu (S King St)`
* **Đồng bộ Meta SEO:**
  * `metaTitle` cập nhật dạng: `Subway - Honolulu (Hind Dr) | Menu, Hours & Reviews - TasteHi`
  * `metaDescription` cập nhật dạng mô tả chi tiết local business chuẩn SEO chứa các từ khóa: *menu, prices, reviews, address map, phone, opening hours*.

### B. Khắc phục đứt gãy JSON-LD Schema (Next.js Level)
* **File chỉnh sửa:** `apps/public/app/(main)/restaurant/[slug]/page.tsx`
* **Nội dung sửa đổi:** Bổ sung trường `brand` lấy từ API vào object `restaurant` truyền cho component `<RestaurantSchema>`.
* **Kết quả:** Các trang chi tiết chi nhánh con hiện tại đã tự động render đầy đủ các thực thể Schema:
  * `@type: "Restaurant"`
  * `name: "[Brand] - [City] ([Street])"` (Ví dụ: `Subway - Ewa Beach (Fort Weaver Rd)`)
  * `brand`: `@type: "Brand"` trỏ trực tiếp về trang Pillar Brand `/brands/subway/`.
  * `parentOrganization`: `@type: "Organization"` trỏ trực tiếp về `/brands/subway/` củng cố liên kết Hub-and-Spoke.

---

## 3. Kết quả xác minh hệ thống
1. **Database:** Cập nhật thành công **402 records** trong bảng `Restaurant`. Dữ liệu mới đã hiển thị chuẩn xác ở cả tên, title và meta description.
2. **Next.js Dev Server:** Build/Compile thành công 100% không phát sinh bất kỳ lỗi cú pháp nào. Thay đổi được áp dụng tức thì qua cơ chế mount volume của Docker.

---

## 4. Các bước tiếp theo (Submit Google Search Console)
Để thúc đẩy Google Bot lập chỉ mục lại các thay đổi mới này một cách nhanh nhất, hãy cập nhật cấu hình file `.env` của `google-seo-tool` và chạy submit sitemap:

1. Mở file `d:\Project\google-seo-tool\.env` và cấu hình:
   ```env
   SITEMAP_URL=https://tastehi.com/sitemap.xml
   SITE_URL=sc-domain:tastehi.com
   ```
2. Chạy lệnh submit indexing các URL thay đổi:
   ```bash
   node index.js
   ```
