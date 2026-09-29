---
name: fco-squad-builder
description: Tự động cào dữ liệu Fifaaddict, phân tích và tối ưu hóa xây dựng đội hình chuẩn meta FC Online / FIFA Online 4 (Trần lương 305 FP, ưu tiên 2 chân 5-5, giảm lương cánh/GK).
---

# ⚽ FC Online Squad Builder & Fifaaddict Integration Skill

Skill chuyên biệt hỗ trợ kết nối, cào bóc tách dữ liệu cầu thủ từ **FIFAaddict** (`vn.fifaaddict.com`) và vận hành thuật toán giải bài toán tối ưu hóa đội hình 11 vị trí cho bất kỳ CLB nào (Team Color) trong game **FC Online (FIFA Online 4)**.

---

## 1. Thông Số Meta FC Online Cốt Lõi

- **Trần Lương (Fair Play - FP):** Hiện tại là **`305 FP`** (cập nhật mới nhất từ bản nâng cấp FCO Squadmaker).
- **Quy tắc Vàng về Chân Thuận (Two-Footed Meta):**
  - Các vị trí tấn công và kiến tạo then chốt (`ST`, `CF`, `LW`, `RW`, `CAM`, `LAM`, `RAM`) bắt buộc ưu tiên cầu thủ có **hai chân 5-5** để đảm bảo khả năng dứt điểm hai chân như một, không bị phụ thuộc góc sút (Z+D, D cận chân).
- **Chiến Thuật Giảm Lương (Salary Savers / Salary Allocation):**
  - Không dàn đều lương cho 11 vị trí.
  - Hậu vệ cánh (`LB`, `RB`) và Thủ môn (`GK`) ưu tiên các phương án lương thấp (khoảng `7 - 18 FP`) nhưng có thể hình/chỉ số ẩn tốt (GK quốc dân như Courtois, Mendy, Pope...).
  - Dồn toàn bộ phần lương dôi dư cho trục dọc sống còn: `ST`, `CAM`, cặp `CDM`, và cặp `CB`.

---

## 2. Cấu Trúc Nguồn Dữ Liệu & Endpoint

- **Database tra cứu trực tiếp:**
  ```http
  GET https://vn.fifaaddict.com/fo4db?team={club_slug}&pos={position}
  ```
  - `club_slug`: `chelsea`, `real-madrid`, `manchester-united`, `fc-barcelona`, `bayern-munchen`, `arsenal`, `liverpool`, `milan`, `juventus`...
  - `pos`: `st`, `cf`, `lw`, `rw`, `cam`, `cm`, `cdm`, `lb`, `rb`, `cb`, `gk`.
  - Dữ liệu trả về dạng bảng HTML (`<table><tbody><tr>...</tr></tbody></table>`), chứa đầy đủ: Vị trí (`pos_rec`), Tên cầu thủ, Mùa thẻ (`badgedss`), Lương (`td.fp`), Chỉ số OVR (`td.ovr`), Thể lực (`td.stamina`), Chân thuận (`5 5`, `4 5`...).

---

## 3. Kiến Trúc Bộ Tooling (.agent/scripts/)

Tất cả mã nguồn điều khiển phải nằm tại thư mục `.agent/scripts/` của dự án:

1. **`crawler.py`**:
   - Gửi HTTP request giả lập browser bóc tách danh sách cầu thủ theo vị trí của CLB.
   - Cơ chế Cache JSON cục bộ lưu tại `.agent/cache/{club_slug}.json` để tránh spam mạng và tra cứu tức thì 0ms.
2. **`optimizer.py`**:
   - Hỗ trợ các sơ đồ phổ biến: `4-2-1-3`, `4-2-3-1`, `4-2-2-2`, `4-1-2-3`.
   - Thuật toán **Beam Search kết hợp Lookahead Salary Pruning**:
     - Đảm bảo mỗi danh thủ chỉ ra sân đúng 1 mùa thẻ.
     - Khống chế Tổng Lương $\le 305$ FP.
     - Tối đa hóa tổng điểm hiệu quả: $OVR + Bonus_{5-5}$.
3. **`main.py`**:
   - Giao diện CLI điều khiển.
   - Render bảng đội hình trực tiếp trên terminal và xuất báo cáo Markdown sang `.agent/squads/`.

---

## 4. Hướng Dẫn Vận Hành Thực Chiến

Chạy lệnh terminal từ thư mục gốc của dự án:

```powershell
# Chạy tương tác hỏi đáp:
python .agent/scripts/main.py

# Hoặc truyền tham số trực tiếp cho CLB và sơ đồ mong muốn:
python .agent/scripts/main.py --club chelsea --formation 4-2-1-3 --salary 305
python .agent/scripts/main.py --club real-madrid --formation 4-2-3-1 --salary 305
python .agent/scripts/main.py --club mu --formation 4-2-2-2 --salary 305
python .agent/scripts/main.py --club arsenal --formation 4-1-2-3 --salary 305

# Bắt buộc cào mới (bỏ qua cache):
python .agent/scripts/main.py --club chelsea --refresh
```
