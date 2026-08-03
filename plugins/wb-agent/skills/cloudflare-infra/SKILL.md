---
name: cloudflare-infra
description: Cloudflare & Network Infrastructure - Cấu hình Cloudflare CLI (wrangler/cloudflared), Tunnel, DNS, SSL, Page Rules, Workers, API Limit & Rate limiting.
role: Cloudflare & Edge Infrastructure Lead
---

## 🎯 Mission
Quản lý, tối ưu và bảo vệ hạ tầng Web trên Cloudflare (DNS, Tunnel, Workers, Edge Caching, Rate Limiting, SSL/TLS).

## 📋 Protocols & Commands

### 1. Cloudflare CLI & Tunnels (`cloudflared`)
- **Tự động Setup trên VPS**: 
  1. Tải & Cài đặt: `curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && dpkg -i cloudflared.deb`
  2. Lấy link Login: `cloudflared tunnel login` (Gửi link cho User bấm duyệt để sinh file `cert.pem`).
  3. Tạo Tunnel: `cloudflared tunnel create <tunnel-name>` (Lưu lại UUID sinh ra).
  4. Trỏ DNS (Ép ghi đè nếu đã tồn tại record A): `cloudflared tunnel route dns -f <tunnel-name> <domain>`
  5. Tạo Ingress Rules (file `~/.cloudflared/config.yml`): Trỏ domain về `http://127.0.0.1:<port>`.
  6. Cài chạy nền: `cloudflared service install; systemctl start cloudflared`.
- Kiểm tra status & kết nối tunnel: `cloudflared tunnel list`, `cloudflared tunnel info <tunnel-id>`.
- Quản lý file cấu hình `config.yml` cho Ingress Rules (routing traffic từ domain Cloudflare về local port/docker).
- Chạy service (Local): `cloudflared tunnel run <tunnel-name>`.

### 2. Workers & Page Rules (`wrangler`)
- Deploy & quản lý Workers/Pages: `npx wrangler dev`, `npx wrangler deploy`.
- Cấu hình SSL/TLS (Full / Strict Mode), diệt sạch lỗi Mixed Content (HTTP vs HTTPS).

### 3. Edge Caching & Rate Limiting
- Cấu hình Cache Rules/Page Rules để lưu cache static assets trên Edge Network.
- Bảo vệ origin server chống DDoS & Brute-force qua WAF & Rate Limiting.

### 4. SEO & GEO Bot Management (Auto-Routing)
Khi có yêu cầu publish SEO, cấu hình SEO hoặc "mở Cloudflare cho bot", LUÔN LUÔN dùng Cloudflare API để tự động cấu hình Bot Management mà không yêu cầu user phải thao tác thủ công trên Dashboard:
- **Tắt Bot Fight Mode & AI Protection (Hỗ trợ GEO)**: Các bot của Google/Bing và cả AI Crawler (Perplexity, ChatGPT) phải được cho phép truy cập để cào `llms.txt` và nội dung.
- **Thực thi bằng PowerShell**:
```powershell
$body = @{ fight_mode = $false; ai_bots_protection = "disabled" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/bot_management" -Method Put -Headers @{"X-Auth-Email"=$Email; "X-Auth-Key"=$ApiKey; "Content-Type"="application/json"} -Body $body
```
- **Cách truy xuất Credentials**: 
  - Ưu tiên đọc `$env:CLOUDFLARE_EMAIL` và `$env:CLOUDFLARE_API_KEY`.
  - Nếu rỗng trong process hiện tại, BẮT BUỘC phải đọc từ Windows Registry User Environment:
    `$Email = [Environment]::GetEnvironmentVariable('CLOUDFLARE_EMAIL', 'User')`
    `$ApiKey = [Environment]::GetEnvironmentVariable('CLOUDFLARE_API_KEY', 'User')`
  - CẤM báo thiếu Token hoặc bắt User nhập lại khi biến môi trường Global đã được cài đặt.

### 5. Tối Ưu Giới Hạn Cloudflare Pages (SSR Edge Caching & Protection)
Khi các dự án web (đặc biệt Astro/Next.js) deploy lên Cloudflare Pages sử dụng Server-Side Rendering (SSR), hệ thống dễ bị cạn "Worker Invocations Limit" (100k/ngày ở bản Free) do các request thực tế hoặc từ bot quét.
LUÔN LUÔN áp dụng 2 bước Global Rule sau để giải quyết dứt điểm:

**Bước 1. Tối ưu bằng Code (Middleware Caching)**
Gán `Cache-Control` header tại middleware của Framework web (Astro, Next.js) cho các trang HTML tĩnh (không cá nhân hóa, không API) để Cloudflare Edge tự động cache.
```typescript
// Astro Middleware Example (src/middleware.ts)
export const onRequest = defineMiddleware(async (context, next) => {
  const response = await next();
  const contentType = response.headers.get('content-type');
  
  // Cache HTML 24h tại Edge (s-maxage=86400). Bỏ qua các API route.
  if (contentType?.includes('text/html') && !context.url.pathname.startsWith('/api/')) {
    response.headers.set('Cache-Control', 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400');
  }
  return response;
});
```

**Bước 2. Triển khai API Security Protection (Chặn Bot rác)**
Thay vì người dùng lên Dashboard cấu hình tay, hãy tự động gọi PowerShell/Bash để bật WAF cản bot (nhưng vẫn tuân thủ Rule 4 - không chặn SEO Crawler).
Lệnh PowerShell Auto-Setup:
```powershell
$ZoneId = "YOUR_ZONE_ID"
$headers = @{"X-Auth-Email"=$env:CLOUDFLARE_EMAIL; "X-Auth-Key"=$env:CLOUDFLARE_API_KEY; "Content-Type"="application/json"}
# 1. Tắt Bot Fight Mode, tắt AI Bot protection (Để Googlebot, Bing, AI Crawler được index)
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/bot_management" -Method Put -Headers $headers -Body '{"fight_mode":false,"ai_bots_protection":"disabled"}'
# 2. Bật Browser Integrity Check (Chặn các Script Bot cào data dỏm)
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/browser_check" -Method Patch -Headers $headers -Body '{"value":"on"}'
# 3. Đưa Security Level về Medium (Chặn các IP Threat Score xấu > 14)
Invoke-RestMethod -Uri "https://api.cloudflare.com/client/v4/zones/$ZoneId/settings/security_level" -Method Patch -Headers $headers -Body '{"value":"medium"}'
```
Quy tắc: Với mọi dự án Cloudflare Pages có kết nối SSR/D1, đây là chuẩn BẮT BUỘC phải thực hiện.

### 6. Tự động Add Domain & R2 CNAME (Workflow)
Khi cần add domain mới vào Cloudflare và cấu hình nhanh R2 CNAME, SEO & Security Rules (như đã định nghĩa ở phần 4 và 5), hãy sử dụng script cf-add-domain-r2.ps1 đã được tạo sẵn.

**Cách chạy:**
```powershell
# Đọc account mặc định từ file config (tự động load, không cần nhập tay)
$cfDefaults = Get-Content "$env:USERPROFILE\.gemini\config\credentials\cloudflare_defaults.json" | ConvertFrom-Json

& "$env:USERPROFILE\.gemini\config\plugins\wb-agent\scripts\cf-add-domain-r2.ps1" `
  -Domain "{domain}" `
  -AccountId $cfDefaults.account_id `
  -R2Endpoint "{r2_endpoint}"
```
> 📌 Credentials mặc định đọc tự động từ `cloudflare_defaults.json` — xem hướng dẫn setup tại mục **Setup Mặc Định** bên dưới.
Script này sẽ tự động:
1. Thêm Zone mới vào Cloudflare (gói Free).
2. Lấy NameServers yêu cầu trỏ và Zone ID.
3. Tạo CNAME cdn trỏ về R2Endpoint (Bật Proxied).
4. Cấu hình bảo mật & SEO: Tắt Bot Fight Mode, tắt AI Bot protection, Bật Browser Integrity Check, Set Security Level về Medium.

Yêu cầu: Môi trường PowerShell phải có sẵn biến $env:CLOUDFLARE_EMAIL và $env:CLOUDFLARE_API_KEY (Global API Key).

**⚙️ SETUP MẶC ĐỊNH — Cloudflare Default Account:**

Để agent tự động dùng đúng account mà không cần nhập tay, tạo file `%USERPROFILE%\.gemini\config\credentials\cloudflare_defaults.json`:
```json
{
  "account_id": "<your_cloudflare_account_id>",
  "account_name": "<your_account_name>",
  "email": "<your_cloudflare_email>"
}
```
Agent BẮT BUỘC đọc file này làm **default account** cho mọi thao tác Zone Create, Workers, R2.

**🚨 LƯU Ý quan trọng khi 1 email có nhiều Account ID:**
- BẮT BUỘC chỉ định `account_id` trong file config để tránh lấy nhầm account.
- TUYỆT ĐỐI KHÔNG hardcode lấy account đầu tiên (`result[0].id`) từ API `/client/v4/accounts` — có thể lấy nhầm account khác gây lỗi `403 Forbidden`.
- Nếu cần override cho dự án cụ thể: ghi `cloudflare_account_id` vào `master-identity.md` của dự án đó.

### 7. Quy Tắc Tối Ưu Quota Cloudflare Free Tier (Pages & D1)
Khi quản lý các dự án sử dụng Cloudflare Pages (gói Free) kết hợp D1 Database, BẮT BUỘC tuân thủ các mốc giới hạn sau:
- **Tối ưu Lượt Build (Max 500 builds/tháng):** 
  - KHÔNG tự động deploy sau mỗi lần sửa 1 file nhỏ. Phải **Gom (Batch)** nhiều thay đổi code/UI lại và CHỈ deploy 1 lần khi kết thúc tác vụ lớn.
  - Nếu tác vụ chỉ thao tác dữ liệu (Database D1) hoặc cập nhật bài Content, **TUYỆT ĐỐI KHÔNG RUN DEPLOY**, chỉ cần gọi lệnh Clear Cache (Purge Everything) là đủ.
- **Tối ưu Ghi/Đọc Database D1:** 
  - Limit Write: 100.000 rows/ngày. Khi crawl/insert data số lượng lớn, bắt buộc dùng cú pháp `INSERT ... VALUES (...), (...)` (Batch Insert).
  - Limit Read: 5 triệu rows/ngày.
- **Tối ưu File Assets:** Tối đa 20.000 files/deploy, mỗi file không quá 25MB.
- **Tối ưu Cache Purge:** Chỉ clear cache 1 lần cuối cùng sau khi hoàn tất batch upload dữ liệu vào D1, hoặc sau khi lệnh deploy đã chạy xong 100%. Không gọi Purge liên tục để chống spam API.
