# 📜 Project Constitution

## 1. Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production. 
- **Local**: Dùng `docker-compose.yml` để dev. 
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening. 
- **Ports**: Tuân thủ dải **8900-8999**.

## 2. Security
- Production containers KHÔNG chạy quyền root.
- CẤM hard-code SSH/Tokens/Keys vào Dockerfile.
- Sử dụng Multi-stage builds để tối ưu size và bảo mật.

## 3. Environments
- Chỉ khởi tạo `local` và `production` mặc định. 
- `beta` hoặc `staging` chỉ tạo khi có yêu cầu cụ thể.
