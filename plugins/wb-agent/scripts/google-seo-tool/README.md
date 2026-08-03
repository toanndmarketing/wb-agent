# Google SEO Tool API Integration

Bộ công cụ tự động hóa SEO, sử dụng Google APIs (Indexing API & Search Console API) để tối ưu index URL và phân tích dữ liệu Search Console.

---

## 🛠️ Yêu cầu hệ thống

- **Docker** và **Docker Compose** (Môi trường runtime chính thức, không chạy trực tiếp trên host).
- File thông tin xác thực Google Cloud:
  - `service-account.json`: Service Account key file.
  - `oauth-credentials.json` (nếu dùng tool tự động phân quyền owner): OAuth 2.0 Credentials file.

---

## ⚙️ Cấu hình biến môi trường

Sao chép file `.env.example` thành `.env` và cập nhật các cấu hình:

```bash
cp .env.example .env
```

Cấu hình trong `.env`:
- `SITEMAP_URL`: URL Sitemap dùng để quét và submit Indexing API.
- `SITE_URL`: URL Property Search Console cần phân tích.
- `DAYS`: Khoảng thời gian lấy dữ liệu phân tích (mặc định 30 ngày).
- `ROW_LIMIT`: Giới hạn số hàng dữ liệu truy xuất (mặc định 5000).

---

## 🐳 Hướng dẫn vận hành với Docker

Tất cả các script của dự án bắt buộc phải được chạy thông qua Docker để đảm bảo tính cô lập và bảo mật.

### 1. Build Docker Image

```powershell
docker compose build
```

### 2. Tự động thêm Service Account làm Owner trên Search Console

Script này yêu cầu OAuth2 xác thực tài khoản Google có quyền quản trị Search Console của bạn để tự động phân quyền Owner cho Service Account email:

```powershell
# Chạy với chế độ tương tác (-it) để nhập mã xác thực từ trình duyệt
docker compose run --rm app node auto-add-owner.js
```

### 3. Submit URL từ Sitemap lên Google Indexing API

Quét Sitemap được cấu hình ở `SITEMAP_URL`, so sánh với lịch sử submit local, và tự động gửi yêu cầu Index các URL mới/cập nhật:

```powershell
docker compose run --rm app node index.js
```

Lịch sử submit sẽ được lưu dưới dạng file `history-<domain>.json` tại thư mục root dự án.

### 4. Phân tích hiệu suất từ khóa & trang đích Google Search Console

Quét hiệu suất của property cấu hình ở `SITE_URL` và tự động phân tích:
- **Striking Distance Keywords**: Từ khóa tiềm năng đang xếp hạng trang 2 (rank 8-20).
- **CTR Optimization**: Các trang đứng top đầu (rank 1-5) nhưng có tỷ lệ CTR thấp (< 3%).
- **Keyword Cannibalization**: Hiện tượng ăn thịt từ khóa giữa các trang đích.

```powershell
docker compose run --rm app node gsc-analyzer.js
```

Bạn cũng có thể truyền tham số ghi đè trực tiếp thông qua CLI:
```powershell
docker compose run --rm app node gsc-analyzer.js --site https://yourdomain.com/ --days 30 --limit 5000
```

Báo cáo chi tiết dạng Markdown và JSON sẽ được xuất bản trong thư mục `./reports/`.
