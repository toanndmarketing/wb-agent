---
name: speckit.devops
description: DevOps automation: Docker, CI/CD, deploy scripts, server config
---

## 🎯 Mission
Thiết lập và quản lý hệ thống Docker chuẩn hóa, bảo mật cho dự án.
Port PHẢI luôn cấu hình qua ENV vars — KHÔNG BAO GIỜ hard-code.

## 📥 Input
- `.agent/memory/constitution.md` (port range, security rules)
- Existing `Dockerfile`, `docker-compose.yml` (nếu có)
- `.env.example`

## 📋 Protocol

### 1. Port Allocation (ENV-first) ⭐

**LUÔN cấu hình port qua ENV:**
- `.env` file (local) hoặc server ENV (production)
- `docker-compose.yml` đọc: `"${PUBLIC_PORT:-8920}:3000"`
- KHÔNG hard-code port number trong bất kỳ file nào

**Quy tắc quét port theo môi trường:**

| Môi trường | Docker đã chạy? | Hành động |
|---|---|---|
| **Local** | ❌ Chưa (lần đầu) | Quét `netstat -ano \| findstr 89` → chọn 3 ports trống liên tiếp |
| **Local** | ✅ Đã chạy | **BỎ QUA** quét — dùng ports hiện tại từ `.env` / docker |
| **Staging/Beta/Prod** | Bất kỳ | **LUÔN** quét lần đầu để cấu hình → ghi vào `.env` |

**Check Docker đã chạy (Local):**
```bash
docker compose ps --format json 2>$null
# Có containers → SKIP port scan
# Trống/error → RUN port scan
```

- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`

### 2. Local Docker (`docker-compose.yml`):
- Ports đọc từ ENV: `"${PUBLIC_PORT:-8920}:3000"`
- Volume mounts cho hot-reload code
- Named volumes cho `node_modules` (tránh host-container lock)
- Health checks cho mỗi service

### 3. Production Docker (`docker-compose.prod.yml`):
- Multi-stage builds (builder → runner)
- `USER node` hoặc `USER appuser` (KHÔNG chạy root)
- Loại bỏ devDependencies trong image final
- Alpine/Slim base images
- Ports đọc từ ENV (KHÔNG hard-code)

### 4. Security & Production Robustness Checklist:
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- Không hard-code secrets trong Dockerfile
- Chỉ EXPOSE ports cần thiết
- **Mạng Container (DNS/EAI_AGAIN)**: Sử dụng explicit `networks` (ví dụ: `internal` và `external`) để tránh lỗi phân giải DNS khi container gọi API lẫn nhau.
- **Volume Permissions**: Cẩn trọng khi set cứng `user: 999:999` (như Postgres) với host bind-mounts. Nếu gặp lỗi `Operation not permitted`, cân nhắc gỡ bỏ để fallback về user mặc định của image, hoặc set quyền chuẩn trên host.
- **Package Managers**: Nếu dùng pnpm qua Corepack trong Docker bị lỗi quyền, cân nhắc fallback về `npm` cho môi trường build an toàn hơn hoặc set quyền root cho build phase.
- **Alpine Healthcheck (LỖI IPv6)**: Các image dựa trên Alpine (như `node:20-alpine`) KHÔNG có sẵn `curl` và có lỗi resolve `localhost` ra IPv6. BẮT BUỘC dùng `wget -qO- http://127.0.0.1:<port>` thay cho `localhost` và `curl` trong lệnh healthcheck.
- **Port Collision (Xung đột Port trên Server)**: CẤM hard-code Host Port trong `docker-compose.prod.yml` (vd: `127.0.0.1:9011:3000`). BẮT BUỘC sử dụng biến môi trường (vd: `127.0.0.1:${PUBLIC_PORT:-9051}:3000`) để dễ dàng đổi port khi deploy chung nhiều web trên 1 VPS.

### 5. Deployment Strategies (BẮT BUỘC TÁCH BẠCH)
Luôn bóc tách quy trình deploy thành 2 kịch bản (2 script riêng):
1. **Initial Deploy (`deploy-initial.sh`)**: Dùng cho lần đầu (hoặc sau khi clean data). 
   - Sử dụng `--no-deps` khi `docker compose run` (đặc biệt khi chạy Next.js SSG build) để ngăn Docker tự động kích hoạt container liên quan quá sớm, tránh race-conditions làm treo tiến trình.
   - Luôn khởi động và chờ Database (`docker compose up -d db`) -> Wait 10s -> Build App.
2. **Update Deploy (`deploy-update.sh`)**: Dùng khi chỉ cập nhật code/tính năng thường xuyên.
   - Pull code nhanh, chỉ rebuild những image bị đổi, và `up -d` nhẹ nhàng để giảm downtime.
3. **Next.js SSG ở quy mô lớn**: Nếu dự án có hàng chục nghìn trang tĩnh (ví dụ: tra cứu địa lý), build time rất lâu (5-10 phút). Tiến trình deploy phải đảm bảo KHÔNG làm ngắt kết nối SSH hoặc timeout.

### 6. Documentation:
- Cập nhật `.agent/knowledge_base/infrastructure.md` với kết quả
- Cập nhật `.env.example` với tất cả port vars

## 📤 Output
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.dockerignore`
- Config: `.env` (ports), `.env.example` (documented)
- Doc: `.agent/knowledge_base/infrastructure.md` (updated)

## 🚫 Guard Rails
- KHÔNG dùng port ngoài dải 8900-8999.
- KHÔNG hard-code port number — LUÔN dùng ENV vars.
- KHÔNG chạy `docker compose down -v` trên production.
- KHÔNG hard-code credentials vào Dockerfile.
- KHÔNG quét port khi Docker local đã chạy (có containers).