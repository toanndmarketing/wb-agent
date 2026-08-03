---
name: speckit.devops
description: Quy trình & Chuẩn mực DevOps, Docker, Deploy DEV vs Production (Deploy Lần Đầu & Smart Deploy Update)
---

# 🚀 SPECKIT.DEVOPS — Quy Chuẩn Deploy DEV & Production

## 🎯 Mission
Chuẩn hóa 100% quy trình thiết lập, đóng gói Docker và triển khai hạ tầng từ môi trường **Development (DEV)** tới **Production (PROD)**. Đảm bảo tính bóc tách tuyệt đối, an toàn dữ liệu, chống xung đột port và không làm ảnh hưởng đến các dự án khác đang live trên cùng Server.

---

## 📂 PHẦN 1: QUY CHUẨN GIT REPOSITORY & COMMIT CONVENTION

### 1. Khởi tạo & Bảo mật Repository
- Cấu hình `.gitignore` chuẩn trước khi commit đầu tiên.
- 🚨 **CẤM COMMIT SECRETS**: Tuyệt đối không commit các file `.env`, API Keys, credentials, token lên Git. Nếu phát hiện rò rỉ, phải báo cáo lập tức.
- Phân nhánh cơ bản: Nhánh `main` (chỉ dành cho code đã pass QA và sẵn sàng lên Prod) và nhánh `dev` (dùng để code tính năng mới).

### 2. Định dạng Commit Message (Conventional Commits)
Bắt buộc tuân thủ tiền tố khi viết commit message để dễ tracking:
- `feat:`: Thêm tính năng mới.
- `fix:`: Sửa lỗi (bug).
- `chore:`: Cập nhật thư viện, build process, các việc không ảnh hưởng logic code.
- `seo:`: Cập nhật liên quan đến SEO (Schema, Title, Meta).
- `docs:`: Cập nhật tài liệu (`README.md`, specs).
- `refactor:`: Viết lại code nhưng không làm thay đổi tính năng hiện tại.

---

## 🛠️ PHẦN 2: QUY CHUẨN DEPLOY DEV (DEVELOPMENT)

### 1. Mục Tiêu Môi Trường DEV
- Linh hoạt, hỗ trợ Hot-Reload code tức thì.
- Cách ly môi trường chạy trên máy cá nhân (Local Machine).

### 2. Quản Lý Port & Quét Port Tự Động (Local)
- **CẤM HARD-CODE PORT**: Tất cả port host phải đọc qua file `.env` (Ví dụ: `PUBLIC_PORT=8920`).
- **Dải Port Quy Định**: Dùng trong khoảng `8900 - 8999`.
- **Cơ chế Quét Port Trống (Local)**:
  - Nếu Docker local **chưa chạy** (lần đầu): Tự động quét port trống qua PowerShell: `netstat -ano | findstr 89` -> Chọn port trống.
  - Nếu Docker local **đã chạy** (`docker compose ps` có container): **BỎ QUA** quét port, tiếp tục dùng port khai báo trong `.env`.

### 3. Cấu Trúc Docker Compose Local (`docker-compose.yml`)
- Read ports từ ENV: `"${PUBLIC_PORT:-8920}:3000"`.
- Bind Host cố định Localhost: `127.0.0.1:${PUBLIC_PORT:-8920}:3000` (tránh lộ port ra LAN).
- Mount Volumes trực tiếp cho Hot-reload (`./src:/app/src`).
- Named Volumes cho `node_modules` để tránh xung đột file system giữa Windows host và Linux container.

---

## 🚢 PHẦN 2: QUY CHUẨN DEPLOY PRODUCTION (PROD)

Deployment Production được bóc tách nghiêm ngặt thành **2 KỊCH BẢN ĐỘC LẬP**:

---

### 🟢 KỊCH BẢN A: DEPLOY PRODUCTION LẦN ĐẦU (FIRST-TIME DEPLOY)

Áp dụng khi đưa một website / dịch vụ hoàn toàn mới lên Server VPS.

#### Step 0: Xác Nhận IP VPS (Bắt Buộc)
- Agent **PHẢI** hỏi hoặc đối chiếu IP Server trước khi làm (Ví dụ: *"Dạ anh cho em xin địa chỉ IP VPS hoặc anh muốn dùng IP cũ 15.235.210.4 để em bắt đầu deploy ạ?"*).
- **CHỈ** thực hiện khi đã chắc chắn đúng IP.

#### Step 1: Kiểm Tra & Gán Port Trống Trên VPS (Port Collision Safety)
- SSH vào Server, chạy lệnh quét port đang lắng nghe trên VPS:
  `ss -tulpn | grep :[PORT]` hoặc `netstat -tulpn | grep :[PORT]`
- Chọn port trống chưa bị chiếm bởi bất kỳ website/docker container nào trên VPS.
- Lưu port này vào file `.env` trên VPS.

#### Step 2: Đóng Gói Docker Production (`docker-compose.prod.yml`)
- Dùng Multi-stage Dockerfile (builder -> runner).
- Không chứa `devDependencies` trong final image.
- Chạy bằng Non-root User (`USER node` hoặc `USER appuser`).
- **Container Networking**: Bind `127.0.0.1:${PUBLIC_PORT}:3000` để đảm bảo an toàn tuyệt đối, chỉ Nginx trên VPS mới route tới được.

#### Step 3: Cấu Hình Nginx Reverse Proxy Tự Động 100%
- Agent tự động viết file cấu hình Nginx trên VPS: `/etc/nginx/sites-available/[domain].conf`.
- Proxy pass về port nội bộ: `proxy_pass http://127.0.0.1:[PUBLIC_PORT];`.
- Tạo Symlink: `ln -s /etc/nginx/sites-available/[domain].conf /etc/nginx/sites-enabled/`.
- **CẤM KỊ**: Bắt buộc chạy `nginx -t` kiểm tra cú pháp trước. Chỉ reload `systemctl reload nginx` khi `nginx -t` báo `successful`. KHÔNG BAO GIỜ làm sập các domain khác đang live trên VPS.

#### Step 4: Tự Động Hóa Cloudflare API & SSL Certbot 100%
- Lấy Credentials Cloudflare từ Env Var Windows (`CLOUDFLARE_EMAIL`, `CLOUDFLARE_API_KEY`).
- Gọi Cloudflare API: Trỏ DNS (Record A) về IP VPS, bật Proxied Orange Cloud (`proxied: true`).
- Áp dụng Global Security Rules (Tắt Bot Fight Mode gây block API, Bật Browser Integrity Check).
- Chạy Certbot cấp SSL tự động trên VPS:
  `certbot --nginx -d [domain] -d www.[domain] --non-interactive --agree-tos -m toannd.marketing@gmail.com`
- Verify HTTPS hoạt động chuẩn (tránh lỗi 520 / 522).

#### Step 5: Post-Deploy — Google Search Console & Analytics
- Chủ động nhắc/yêu cầu thực hiện Verify Google Search Console (qua DNS TXT record).
- Báo cáo và Submit Sitemap.xml ngay lập tức.
- Kiểm tra Manual Actions & Security Issues trong GSC nếu domain là mua lại (Expired Domain).
- Hướng dẫn hoặc chèn script Google Analytics / GA4 / Plausible vào thẻ `<head>`.

---

### 🔵 KỊCH BẢN B: DEPLOY UPDATE THƯỜNG XUYÊN (REGULAR SMART DEPLOY)

Áp dụng khi nâng cấp tính năng, fix bug hoặc cập nhật nội dung cho dự án đang chạy live.

#### 1. Backup & Rollback Protocol (Bắt Buộc Trước Khi Update)
- Trước khi kéo code mới về, phải backup DB hoặc lưu snapshot trạng thái hiện hành nếu có thay đổi DB schema.
- Giữ lại ít nhất 3 bản image Docker hoặc source code backup gần nhất.
- Luôn chuẩn bị sẵn phương án Rollback nhanh (chạy lại container từ image tag phiên bản trước) nếu deploy mới gặp lỗi nghiêm trọng (500 Error, dập web).

#### 2. Cách Ly Dự Án (Project Isolation)
- **Đúng thư mục**: Bắt buộc `cd /home/[domain]` hoặc đường dẫn dự án trên VPS.
- **Tuyệt đối không xâm phạm**: Chỉ thao tác đúng container của dự án đó.
- **CẤM KỊ**:
  - ❌ **CẤM** `docker system prune` hay `docker compose down -v` trên Production.
  - ❌ **CẤM** `FLUSHALL` toàn bộ Redis Server nếu Redis dùng chung cho nhiều web (chỉ flush namespace/key của dự án).

#### 3. Phân Loại Build Thông Minh (Smart Differential Rebuild)
Agent check Git diff trước khi kích hoạt build:
- **Level 1 (Core Changes)**: Thay đổi `docker-compose.prod.yml`, `Dockerfile`, `package.json`, DB schema -> **Full Build**:
  `docker compose -f docker-compose.prod.yml up -d --build`
- **Level 2 (Service Changes)**: Thay đổi chỉ trong 1 service (vd: `apps/public` hoặc `apps/api`) -> **Targeted Build**:
  `docker compose build [service] && docker compose up -d --no-deps [service]`
  *(Sử dụng `--no-deps` để không restart các container khác, đảm bảo Zero Downtime)*.
- **Level 3 (No Code Changes)**: Bỏ qua build.

#### 4. Kiểm Tra Tài Nguyên VPS (Resource & Memory Safety)
- Trước khi build ứng dụng nặng (Next.js SSG), chạy `free -m` và `df -h`.
- Nếu RAM khả dụng < 500MB, chủ động cảnh báo hoặc xử lý build nhẹ nhàng để tránh kích hoạt Linux OOM Killer làm đai VPS.

---

## 🚫 CHỐT CHẶN BẮT BUỘC (GUARD RAILS)
1. **Xác nhận User (Y/N)**: Mọi thao tác deploy Production BẮT BUỘC phải trình bày phương án ngắn gọn và chờ User xác nhận "OK/Làm đi" mới được thực thi.
2. **Không làm nửa vời**: Agent phải hoàn thành trọn vẹn 100% từ A-Z, không bắt User phải gõ lệnh hay vào dashboard thao tác bằng tay.
3. **Verify sau Deploy**: Sau khi deploy xong, bắt buộc chạy kiểm tra HTTP 200, SSL valid, và API response để đảm bảo trang live mượt mà.
4. **Bắt Buộc Chuẩn Hóa Document (`deploy-production.md`)**: TẤT CẢ các dự án bắt buộc phải khởi tạo và duy trì file `.agents/workflows/deploy-production.md`. Tài liệu này phải định nghĩa rõ:
   - Các kịch bản Deploy Code lên VPS (Kèm tên script thực thi tự động, vd: `deploy-vps.ps1`).
   - Các kịch bản Deploy / Đồng Bộ Database (Từ Local -> Prod hoặc Prod -> Local) bằng script an toàn (vd: `deploy-db-vps.ps1`), để Agent hoặc User đời sau nắm rõ luồng chạy và IP/Credentials liên quan mà không phải tự đoán.

---

## 💾 PHẦN 3: QUY CHUẨN DATABASE MIGRATION & PROTECTION (CHỐNG MẤT DỮ LIỆU)

### 1. Hành Vi Nghiêm Cấm (The "NEVER" List)
- ❌ **Cấm Sửa Bằng Tay (No Manual GUI Edits):** Không dùng GUI mở Production DB sửa trực tiếp.
- ❌ **Cấm Đẩy Dump Local Lên Prod (No Local-to-Prod Dump Overwrite):** Kéo DB từ Prod -> Sửa Local -> Push đè lên Server là HÀNH VI BỊ NGHIÊM CẤM tuyệt đối vì gây mất User/Order.
- ❌ **Cấm Sync 2 Chiều:** Data chỉ chảy 1 chiều từ **Prod -> Local/Staging**.

### 2. Luồng Update DB Tự Động (Infrastructure as Code)
Khi cần cập nhật Master Data (Categories, Tags) hoặc đổi Schema:
1. **Sync Data:** Kéo bản sao Production về Local qua file SQL Dump để làm môi trường test thật nhất.
2. **Viết Script:** Mọi thay đổi dữ liệu phải được code bằng file script (VD: `scripts/update-categories.ts` qua Prisma/TypeORM) hoặc Migration Scripts.
3. **Dry-Run:** Chạy thử và Verify (Walkthrough) script trên Local.
4. **Execute on Prod:** Chạy lệnh Backup DB Prod nóng trước. Sau đó đưa script lên Server và thực thi trực tiếp bằng lệnh (VD: `npx tsx scripts/update-categories.ts`). Server sẽ cập nhật DB an toàn trong 1s mà không làm gián đoạn User.