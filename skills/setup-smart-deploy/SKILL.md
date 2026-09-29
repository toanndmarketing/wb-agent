---
name: setup-smart-deploy
description: "Thiết lập quy trình Smart Deploy chuẩn (Shell + PS1 + Markdown Workflow) cho một dự án VPS mới."
---

# 🚀 Skill: Thiết lập Smart Deploy Workflow Chuẩn

**Khi nào sử dụng?** 
Mỗi khi setup môi trường deploy (triển khai VPS) cho một dự án mới, BẮT BUỘC Agent phải sử dụng Skill này để thiết lập 3 file nền tảng nhằm tự động hóa 100% vòng đời triển khai theo chuẩn Webest.

## 📋 Yêu cầu cấu trúc (Bắt buộc)
Agent phải tự tạo **3 file** sau vào thư mục gốc của dự án (`.agents/`):

### 1. File Bash chạy trên máy chủ VPS: `.agents/scripts/smart-deploy.sh`
- Dùng cho Docker Compose Project. Phải có: `git pull origin main`, `docker compose up -d --build`, `docker image prune -f`.

### 2. File PowerShell Trigger: `.agents/scripts/deploy-production.ps1`
- Dùng trên máy Local (Windows) của lập trình viên để bắn lệnh lên VPS.
- Phải khai báo biến `$serverIP` và lệnh `ssh -o StrictHostKeyChecking=no root@$serverIP "cd /var/www/ten-du-an && bash .agents/scripts/smart-deploy.sh"`

### 3. File Mô tả Workflow: `.agents/workflows/01-production-deploy.md`
- Phải giải thích cho Agent/User cách kích hoạt luồng: (1) Kiểm tra Git Status (2) Thực thi PS1 script (3) Kiểm tra URL Live trả về 200 OK.

> ⚠️ **Quy tắc Vàng (Golden Rule):** Không được tạo quy trình deploy thủ công bắt user phải SSH tay. Luôn luôn xây dựng Smart Deploy Pipeline 3 bước như trên để đảm bảo Agent tự kích hoạt được cho user qua file `deploy-production.ps1`.
