---
name: dinh-huong-hoc-sinh-no-hour
description: "Đánh giá điểm mạnh/yếu, năng khiếu, khí chất và định hướng giáo dục học sinh khi KHÔNG CÓ GIỜ SINH dựa trên Bát Tự Tam Trụ (Năm-Tháng-Ngày theo Tiết Khí Dương Lịch) kết hợp Thần Số Học Pythagoras. Hỗ trợ phân tích học sinh đơn lẻ hoặc toàn bộ danh sách lớp, xuất bảng ma trận, phân bổ 6 ban cán sự lớp, xuất PDF/Word/Markdown không header/footer."
---

# Định Hướng Học Sinh Không Có Giờ Sinh (Bát Tự Tam Trụ & Thần Số Học)

## 1. Mục Tiêu & Phạm Vi Ứng Dụng
Skill này chuyên dùng cho môi trường giáo dục, phụ huynh và thầy cô khi chỉ có **Họ tên, Giới tính, Ngày/tháng/năm sinh Dương lịch** (không có Giờ sinh).

Phương pháp tích hợp 2 lớp lý thuyết:
1. **Bát Tự Tam Trụ (Tử Bình Dương Lịch):**
   - Trụ Năm: Gốc gác, nền tảng gia đình (ngắt tại Tiết Lập Xuân ~04/02).
   - Trụ Tháng (Nguyệt Lệnh): Mùa sinh theo 12 Tiết Khí, quyết định khí chất và cấu trúc học thuật.
   - Trụ Ngày (Nhật Chủ): Bản thể chân thực của bé (10 Thiên Can: Giáp, Ất, Bính, Đinh, Mậu, Kỷ, Canh, Tân, Nhâm, Quý).
2. **Thần Số Học Pythagoras:**
   - Số Chủ Đạo (Life Path 1–9, Master 11, 22, 33): Phong cách tư duy, điểm mạnh/yếu bẩm sinh, cách tiếp cận bài học.
   - 6 Nhóm Khí Chất & Năng Khiếu trọng tâm.

---

## 2. Cách Sử Dụng Script

### A. Xem 1 học sinh đơn lẻ
```powershell
python D:\Tuvi\.agents\skills\dinh-huong-hoc-sinh-no-hour\scripts\evaluate_students_no_hour.py --name "Phạm Khánh An" --dob "17/04/2019" --gender "Nữ"
```

### B. Quét theo danh sách file JSON
```powershell
python D:\Tuvi\.agents\skills\dinh-huong-hoc-sinh-no-hour\scripts\evaluate_students_no_hour.py --input danh_sach_lop.json --output ket_qua_lop.json
```

---

## 3. Cấu Trúc Báo Cáo Chuẩn

Khi xuất kết quả cho người dùng hoặc phụ huynh, bản báo cáo gồm:
1. **Header cá nhân:** Họ tên, Ngày sinh (DL/ÂL), Giới tính.
2. **Bát Tự Tam Trụ:** Trụ Năm | Trụ Tháng | Trụ Ngày | Nhật Chủ (Ngũ Hành).
3. **Thần Số Học:** Số Chủ Đạo & Nhóm Khí Chất.
4. **Điểm mạnh bẩm sinh:** Năng khiếu, tư duy vượt trội.
5. **Điểm yếu / Điểm cần lưu ý:** Những góc khuất tâm lý cần uốn nắn nhẹ nhàng.
6. **Năng khiếu & Định hướng:** Môn học thế mạnh, phong trào, cờ vua, nghệ thuật, STEM.
7. **Gợi ý phân công vai trò trong lớp:** 6 nhóm ban cán sự lớp.

---

## 4. Bảng Phân Bổ 6 Ban Cán Sự Lớp Học

| Nhóm Cán Sự | Đặc Điểm Bát Tự & Số CĐ | Vai Trò Lớp Học |
|---|---|---|
| **👑 Ban Chỉ Huy** | Số 1, 8, Dương Kim/Dương Mộc (Giáp, Canh) | Lớp trưởng, Lớp phó Kỷ luật, Sao đỏ, Tổ trưởng |
| **🔍 Ban Học Tập & Logic** | Số 7, Master 11, Thủy/Hỏa sâu (Đinh, Quý, Nhâm) | Trưởng ban học tập, Cờ vua, Toán logic, STEM |
| **🎨 Ban Văn Thể Mỹ & MC** | Số 3, 5, Master 33, Bính Hỏa/Canh Kim | Quản ca, MC dẫn chương trình, Văn nghệ, Hoạt náo |
| **❤️ Ban Đời Sống & Nề Nếp** | Số 6, Kỷ Thổ/Tân Kim/Giáp Mộc | Thủ quỹ, Nề nếp Vở sạch chữ đẹp, Chăm sóc lớp |
| **📐 Ban Kỷ Luật & Thư Viện** | Số 4, Kỷ Thổ/Canh Kim | Giữ trật tự tự quản, Quản lý tủ sách, Kiểm tra bài |
| **⚡ Ban Trải Nghiệm Ngoại Khóa** | Số 5, Tân Kim/Nhâm Thủy | Phụ trách dã ngoại, Vận động ngoài trời, Kỹ năng sống |
