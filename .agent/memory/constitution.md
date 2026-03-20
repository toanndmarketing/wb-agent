# 📜 Project Constitution

## §0 WB-Agent Protocol (MANDATORY)
- **BẮT BUỘC**: Mọi hoạt động phát triển (Code), kiểm thử (Test), và triển khai (Deploy Production) PHẢI sử dụng `wb-agent`.
- **Pipeline**: Tuân thủ nghiêm ngặt quy trình: Specify → Plan → Tasks → Implement.
- **Tools**: Chỉ sử dụng các workflows trong `.agent/workflows` để thực hiện task.

## §1 Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production. KHÔNG chạy `npm`/`node`/`python` trực tiếp trên host.
- **Local**: Dùng `docker-compose.yml` để dev.
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening.
- **Ports**: Chỉ dùng dải **8900-8999**.
  - Public FE: `N` | Admin FE: `N+1` | Backend API: `N+2`
- **Lệnh PowerShell**: Dùng PowerShell 5.1+, ngăn cách lệnh bằng `;` (KHÔNG dùng `&&`).

## §2 Security & Production Safety
- **CẤM**: `docker compose down -v` trên Production.
- **CẤM**: Deploy thủ công (phải dùng workflows `/deploy-production` hoặc `/deploy-staging`).
- **Xác nhận**: Yêu cầu xác nhận trước khi Deep Clean, Deploy Prod, hoặc Delete Data.
- **Runtime**: Production containers KHÔNG chạy quyền root.

## §3 Code Standards & ENV
- **CẤM hard-code**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive vars**: PHẢI dùng ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical vars: `throw new Error()` nếu thiếu.
  - Optional vars: `console.error()` nếu thiếu.
- **Documentation**: Phải có `.env.example` đầy đủ.

## §4 Workflow & Scripting
- **Tự động hóa**: Tạo script khi gặp lỗi hoặc task lặp lại.
- **Git**: Lưu script vào `.agent/scripts`, commit vào hệ thống version control.
- **Update**: Cập nhật workflow tương ứng sau khi tạo script mới.
