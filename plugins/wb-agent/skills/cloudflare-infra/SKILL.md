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
- Lấy Credentials từ `$env:CLOUDFLARE_EMAIL` và `$env:CLOUDFLARE_API_KEY`.
