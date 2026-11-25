---
name: dang-ky-bo-cong-thuong
description: Quy trình chuẩn mực Thông báo website TMĐT bán hàng với Bộ Công Thương (online.gov.vn) duyệt 1 phát ăn ngay. Rà soát 9 bẫy thực chiến, bảng Confirm thông tin chuẩn, tạo/sửa Footer & bộ 10 trang chính sách theo đúng ngành hàng, tự động xuất 7 file PDF đính kèm, soạn 7 đoạn text form và hướng dẫn thao tác thủ công trên online.gov.vn.
---

# 🏛️ Quy Trình Thông Báo Website TMĐT Bán Hàng Với Bộ Công Thương (1 Phát Ăn Ngay)

> **Nguyên tắc vàng:** Tuyệt đối **KHÔNG hardcode** nội dung mẫu của một ngành hàng/doanh nghiệp khác vào website đang triển khai. Mọi thông tin pháp lý, số tài khoản, địa chỉ, chính sách bảo hành/đổi trả phải được **Confirm chuẩn xác theo Giấy ĐKKD và ngành hàng thực tế** của website mục tiêu.

> **Cơ sở pháp lý:**
> - **Nghị định 52/2013/NĐ-CP** về thương mại điện tử.
> - **Nghị định 85/2021/NĐ-CP** sửa đổi, bổ sung một số điều của Nghị định 52.
> - **Nghị định 13/2023/NĐ-CP** về bảo vệ dữ liệu cá nhân.
> - **Thông tư 47/2014/TT-BCT** & **Thông tư 21/2018/TT-BCT** quy định về quản lý website TMĐT.

---

## 🎯 1. Phân Định Thủ Tục & Loại Hình Website

| Tiêu chí | Thông báo Website TMĐT bán hàng (SOP này) | Đăng ký Sàn giao dịch TMĐT |
| :--- | :--- | :--- |
| **Bản chất** | Website do thương nhân/tổ chức tự lập để bán hàng hóa, dịch vụ của **chính mình** | Cho phép **bên thứ ba (người bán khác)** mở gian hàng, đăng bán |
| **Tên gọi trên `online.gov.vn`** | *Nền tảng TMĐT kinh doanh trực tiếp có chức năng đặt hàng trực tuyến* | *Nền tảng cung cấp dịch vụ sàn giao dịch TMĐT* |
| **Huy hiệu được cấp** | **ĐÃ THÔNG BÁO BỘ CÔNG THƯƠNG** (Màu **Xanh dương**) | **ĐÃ ĐĂNG KÝ BỘ CÔNG THƯƠNG** (Màu **Đỏ**) |
| **Lệ phí nhà nước** | **0 VNĐ (Hoàn toàn miễn phí)** | **0 VNĐ (Nhưng hồ sơ phức tạp, cần Đề án)** |
| **Thời gian xét duyệt** | **3 – 7 ngày làm việc** | **15 – 30 ngày làm việc** |

---

## 🚨 2. "9 BẪY THỰC CHIẾN" Khiến Hồ Sơ Bị Trả Lại (Phải Kiểm Tra & Diệt Triệt Để)

Chuyên viên Cục TMĐT & KTS sẽ trực tiếp truy cập tên miền, đặt thử hàng test và soi từng trang chính sách đối chiếu với Giấy chứng nhận ĐKKD:

1. **Lệch ngành hàng trong nội dung chính sách:**
   - *Bẫy:* Copy code/seed mẫu từ dự án cũ (web bán ngành hàng A nhưng trang bảo hành/vận chuyển lại viết cho ngành hàng B).
   - *Xử lý:* Viết lại 100% nội dung chính sách theo đúng sản phẩm/dịch vụ thực tế của website.
2. **Cổng thanh toán trung gian trực tuyến (OnePay, VNPay, Bảo Kim, MoMo, ZaloPay...):**
   - *Bẫy:* Để nút thanh toán trực tuyến nhưng chưa có Hợp đồng kết nối chính thức hoặc đang dùng key Sandbox test $\rightarrow$ BCT sẽ test đơn hoặc yêu cầu nộp bản scan Hợp đồng thanh toán.
   - *Xử lý:* Nếu chưa có Hợp đồng nghiệm thu thật $\rightarrow$ **Tạm ẩn** các nút thanh toán trực tuyến trong 5–7 ngày chờ duyệt (chỉ để COD và Chuyển khoản ngân hàng). Duyệt xong có logo xanh thì bật lại.
3. **Số tài khoản ngân hàng cá nhân:**
   - *Bẫy:* Để STK cá nhân của giám đốc/nhân viên trên trang Chính sách thanh toán $\rightarrow$ BCT từ chối vì không khớp pháp nhân (hoặc bắt làm giấy ủy quyền nhận tiền).
   - *Xử lý:* Bắt buộc ghi Số tài khoản đứng tên **Công ty/Hộ kinh doanh** (trùng tên trên ĐKKD).
4. **Lệch địa chỉ giữa Footer và bản scan Giấy ĐKKD:**
   - *Bẫy:* Đổi địa chỉ theo địa giới hành chính mới hoặc viết tắt lệch với chữ in trên Giấy ĐKKD bản scan.
   - *Xử lý:* Khớp chính xác từng từ trên Giấy ĐKKD. Nếu có thay đổi địa giới hành chính, ghi rõ: `[Địa chỉ gốc ghi trên Giấy ĐKKD] (Nay là [Địa chỉ hành chính mới])`.
5. **Số Hotline hoặc Tổng đài ảo:**
   - *Bẫy:* Để số mẫu `1900 xxxx` hoặc số điện thoại chưa hoạt động.
   - *Xử lý:* Thay toàn bộ bằng số điện thoại thật có người trực.
6. **Thiếu cơ chế Đồng kiểm hàng hóa (Nghị định 85/2021/NĐ-CP):**
   - *Bẫy:* Trang vận chuyển chỉ ghi thời gian giao, không nêu quyền kiểm tra hàng.
   - *Xử lý:* Bắt buộc có điều khoản: Khách hàng được quyền **ĐỒNG KIỂM** (mở gói hàng kiểm tra ngoại quan, mẫu mã, số lượng) trước khi thanh toán, và quy định trách nhiệm bồi thường của đơn vị vận chuyển đối tác.
7. **Thiếu 7 điều khoản Bảo vệ dữ liệu cá nhân (Nghị định 13/2023/NĐ-CP & Điều 68-73 NĐ 52):**
   - *Bẫy:* Trang bảo mật sơ sài 1-2 đoạn chung chung.
   - *Xử lý:* Phải đủ 7 mục: Mục đích thu thập, Phạm vi sử dụng, Thời gian lưu trữ, Tổ chức/cá nhân được tiếp cận, Đơn vị thu thập & quản lý, Công cụ chỉnh sửa dữ liệu, Cơ chế tiếp nhận & giải quyết khiếu nại.
8. **Thiếu Checkbox chấp thuận điều khoản tại Giỏ hàng / Đặt hàng:**
   - *Bẫy:* Khách bấm đặt hàng không có bước xác nhận điều khoản giao dịch.
   - *Xử lý:* Thêm checkbox (hoặc thông báo xác nhận) bắt buộc trước nút Đặt hàng: *"Tôi đã đọc và đồng ý với Điều khoản giao dịch chung và Chính sách bảo mật của website"*.
9. **File PDF đính kèm bị thanh nổi (Floating Bar) đè chữ:**
   - *Bẫy:* Chụp PDF từ web nhưng thanh bottom-nav mobile hoặc nút Zalo/Hotline nổi lặp lại ở chân mỗi trang A4 đè lên nội dung.
   - *Xử lý:* Dùng script Playwright inject CSS `@media print` ẩn hoàn toàn các phần tử `fixed`/`sticky` trước khi xuất PDF.

---

## ✅ 3. Bảng Confirm Thông Tin Chuẩn Trước Khi Triển Khai (BẮT BUỘC HỎI KHÁCH)

Trước khi chỉnh sửa code hoặc tạo bộ file hồ sơ, Agent **BẮT BUỘC** yêu cầu User / Khách hàng cung cấp và xác nhận đầy đủ bảng thông tin sau:

| STT | Hạng mục cần Confirm | Chi tiết cần chốt | Mục đích sử dụng |
| :---: | :--- | :--- | :--- |
| **1** | **Giấy ĐKKD** | Bản scan màu (hoặc ảnh chụp rõ 4 góc) Giấy chứng nhận ĐKKD / Hộ kinh doanh mới nhất | Ghép 2 mặt thành 1 file PDF nộp `online.gov.vn` & đối chiếu từng chữ |
| **2** | **Thông tin Pháp nhân** | Tên doanh nghiệp/HKD, MST/Số GCN ĐKKD, Ngày cấp lần đầu + Ngày thay đổi gần nhất, Nơi cấp | Hiển thị ở Footer & điền form tài khoản BCT |
| **3** | **Địa chỉ trụ sở chính** | Địa chỉ **chính xác từng chữ trên Giấy ĐKKD** (kèm địa chỉ mới nếu có sáp nhập hành chính) | Khớp Footer, Trang liên hệ & Hồ sơ BCT |
| **4** | **Người đại diện pháp luật** | Họ tên, Chức vụ, Số CCCD, Ngày cấp, Nơi cấp | Hiển thị Footer & khai báo tài khoản `online.gov.vn` |
| **5** | **Liên hệ & Email BCT** | SĐT Hotline bán hàng/khiếu nại, Email hiển thị web, Email nhận thông báo từ `online.gov.vn` | Khai báo tài khoản, nhận mail kích hoạt & tra cứu |
| **6** | **Tài khoản Ngân hàng** | Số TK + Tên Ngân hàng + Chi nhánh (**Chủ TK bắt buộc là tên Công ty/HKD**) | Đưa vào trang Chính sách thanh toán & Text khai báo |
| **7** | **Cổng thanh toán Online** | Đã ký Hợp đồng chính thức với cổng thanh toán (OnePay/VNPay...) hay chưa? | Nếu chưa ký $\rightarrow$ Tạm ẩn khỏi giỏ hàng khi chờ duyệt |
| **8** | **Chính sách đặc thù ngành** | Thời hạn bảo hành, thời hạn đổi trả (7/15/30 ngày), phí ship & chính sách kiểm hàng | Viết chuẩn bộ 10 trang chính sách theo đúng ngành hàng |
| **9** | **Tên miền & Hosting** | Tên miền chính thức (`domain.com`), Chủ sở hữu tên miền, Tên nhà cung cấp Hosting/VPS | Điền phần *"Nếu nền tảng là Website"* trên `online.gov.vn` |

---

## 🛠️ 4. Quy Trình 4 Giai Đoạn Triển Khai

### 💻 Giai đoạn 1: Kiểm tra, Tạo mới / Sửa chuẩn Website
Đối chiếu mã nguồn website hiện tại với danh sách bắt buộc dưới đây (thiếu trang nào tạo mới trang đó, sai nội dung sửa đúng ngành hàng):

1. **Footer (Chân trang — Điều 29 NĐ 52):**
   - Hiển thị đầy đủ: Tên đơn vị, MST/Số ĐKKD, Ngày cấp, Nơi cấp, Người đại diện pháp luật, Địa chỉ trụ sở, SĐT, Email.
   - Đầy đủ cột liên kết trỏ tới tất cả các trang chính sách (không được ẩn link).
2. **Bộ Trang Chính sách & Điều khoản bắt buộc (đủ 10 mục nội dung):**
   - **Chính sách bảo mật:** Đủ 7 điều khoản theo Điều 68–73 NĐ 52 & NĐ 13/2023.
   - **Chính sách vận chuyển & Kiểm hàng:** Biểu phí, thời gian giao nhận, quyền **Đồng kiểm 100%**, phân định trách nhiệm logistics (NĐ 85/2021).
   - **Chính sách đổi trả & Hoàn tiền:** Điều kiện áp dụng, thời hạn đổi trả, thời gian & phương thức hoàn tiền.
   - **Chính sách bảo hành:** Thời hạn & quy trình bảo hành đúng theo mặt hàng đang bán.
   - **Chính sách thanh toán:** COD, Chuyển khoản (STK Công ty), Thanh toán thẻ/Trả góp (nếu có HĐ), Hóa đơn VAT.
   - **Điều khoản & Điều kiện giao dịch chung:** Phạm vi cung cấp, quy trình đặt hàng/giao kết hợp đồng, nghĩa vụ người bán & khách hàng, cơ chế giải quyết tranh chấp 4 bước.
   - **Trang Khiếu nại / Góp ý & Liên hệ:** Biểu mẫu trực tuyến + thông tin đường dây nóng tiếp nhận phản ánh.
   - **Hướng dẫn mua hàng / Quy định giá:** Minh bạch giá bằng VNĐ, thuế VAT và phí ship trước khi đặt hàng.
3. **Luồng Giỏ hàng / Đặt hàng:**
   - Có checkbox/xác nhận đồng ý Điều khoản giao dịch & Chính sách bảo mật trước khi hoàn tất đặt hàng.
   - Tạm ẩn các cổng thanh toán chưa có hợp đồng thật.
4. **Deploy lên Live Domain** trước khi nộp hồ sơ để chuyên viên BCT vào kiểm tra trực tiếp.

---

### 📦 Giai đoạn 2: Tự động Xuất Bộ 8 File Đính Kèm & Soạn Text Khai Báo

#### 1. Chuẩn bị file cấu hình đường dẫn (nếu slug của web khác mặc định)
Tạo file JSON (ví dụ `tmp/bct_routes.json`) map 7 mục với slug thực tế trên website:
```json
{
  "1_privacy": ["/chinh-sach-bao-mat"],
  "2_complaint": ["/gop-y", "/dieu-khoan-su-dung"],
  "3_pricing": ["/dieu-khoan-su-dung", "/huong-dan-mua-hang"],
  "4_payment": ["/chinh-sach-thanh-toan"],
  "5_terms": ["/dieu-khoan-su-dung"],
  "6_delivery_return": ["/chinh-sach-van-chuyen", "/chinh-sach-doi-tra", "/chinh-sach-bao-hanh"],
  "7_support": ["/lien-he", "/gop-y"]
}
```

#### 2. Chạy Script xuất 7 file PDF + 1 Logo:
```powershell
python "C:\Users\Opengate\.gemini\config\plugins\wb-agent\skills\dang-ky-bo-cong-thuong\scripts\export_bct_files.py" `
  --url "https://domain.com" `
  --brand "brand-slug" `
  --out "./docs/bct-files" `
  --logo "./path/to/logo.png" `
  --routes-json "./tmp/bct_routes.json"
```
Script tự động chụp giao diện desktop sắc nét, ẩn toàn bộ floating bar, gộp các trang liên quan thành 7 file PDF đánh số từ `1_` đến `7_` và tự động mở thư mục chứa file.

#### 3. Soạn sẵn 7 đoạn Text khai báo cho khách/người nộp:
Đọc file mẫu tại:
`C:\Users\Opengate\.gemini\config\plugins\wb-agent\skills\dang-ky-bo-cong-thuong\templates\bct_form_texts.md`
Thay thế toàn bộ biến `{...}` bằng thông tin đã Confirm ở Bước 3 và xuất ra cho người dùng copy-paste từng ô.

---

### 🖥️ Giai đoạn 3: Hướng Dẫn Thao Tác Thủ Công Chi Tiết Trên Cổng `online.gov.vn`

Hướng dẫn người thực hiện đăng nhập và điền đầy đủ từng hạng mục trên cổng Bộ Công Thương:

1. **Bước 1 — Đăng nhập / Đăng ký tài khoản Chủ quản:**
   - Truy cập `https://online.gov.vn` (hoặc đăng nhập qua SSO Cổng dịch vụ công Bộ Công Thương `dichvucong.moit.gov.vn` / VNeID định danh tổ chức).
   - Chọn đúng loại hình chủ thể: **DOANH NGHIỆP** (Cty TNHH/Cổ phần) hoặc **HỘ KINH DOANH / CÁ NHÂN**.
   - Nếu báo tài khoản đã tồn tại nhưng quên mật khẩu $\rightarrow$ kiểm tra lại email cũ đã từng dùng đăng ký MST này hoặc dùng chức năng khôi phục qua SSO Dịch vụ công.

2. **Bước 2 — Hoàn thiện Hồ sơ Chủ quản Nền tảng:**
   - Điền Tên tổ chức/chủ quản, MST/Số GCN ĐKKD, Địa chỉ trụ sở (khớp 100% ĐKKD).
   - Điền thông tin Người đại diện pháp luật (Họ tên, Chức vụ, CCCD, Ngày cấp, Nơi cấp).
   - Điền Email tiếp nhận thông tin & SĐT liên hệ.
   - Mục **File ảnh đăng ký doanh nghiệp (ĐKKD)**: Upload file PDF đã ghép rõ nét 2 mặt Giấy ĐKKD.

3. **Bước 3 — Khai báo Nền tảng Trực tuyến (Thông báo Website TMĐT):**
   - Chọn menu **Nền tảng trực tuyến** $\rightarrow$ **Thêm mới hồ sơ thông báo** $\rightarrow$ Chọn loại hình: **`Nền tảng TMĐT kinh doanh trực tiếp có chức năng đặt hàng trực tuyến`**.
   - **Phần Thông tin chung website:**
     + `* Ngôn ngữ`: Chọn **`Tiếng Việt`**
     + `* Địa chỉ website`: Nhập tên miền gốc (ví dụ `domain.com`, **không** điền `https://` và dấu `/` ở cuối)
     + `* Chủ sở hữu tên miền`: Nhập đúng Tên công ty / Cá nhân đứng tên tên miền
     + `* Đơn vị cung cấp hosting`: Chọn/gõ tên đơn vị cung cấp VPS/Hosting (ví dụ: *Viettel IDC*, *VNPT*, *FPT*, *Mắt Bão*, *P.A Việt Nam*, *AWS*, *Cloudflare*...)
     + `* Logo website`: Bấm nút Upload $\rightarrow$ Chọn file `0_Logo_<brand>.png`
   - **Phần `Các thông tin bắt buộc khác cho nền tảng` (7 ô Text + 7 nút Upload PDF):**
     + Dán lần lượt 7 đoạn text đã soạn vào đúng 7 ô:
       1. *Chính sách bảo mật `(*)`* $\rightarrow$ Upload `1_Chinh_sach_bao_mat_<brand>.pdf`
       2. *Phương thức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại `(*)`* $\rightarrow$ Upload `2_Phuong_thuc_tiep_nhan_va_giai_quyet_khieu_nai_<brand>.pdf`
       3. *Chính sách giá `(*)`* $\rightarrow$ Upload `3_Chinh_sach_gia_<brand>.pdf`
       4. *Chính sách về thanh toán `(*)`* $\rightarrow$ Upload `4_Chinh_sach_ve_thanh_toan_<brand>.pdf`
       5. *Các điều kiện hoặc hạn chế trong việc cung cấp hàng hóa hoặc dịch vụ `(*)`* $\rightarrow$ Upload `5_Dieu_kien_cung_cap_hang_hoa_dich_vu_<brand>.pdf`
       6. *Chính sách giao hàng, đổi trả và hoàn tiền `(*)`* $\rightarrow$ Upload `6_Chinh_sach_giao_hang_doi_tra_hoan_tien_<brand>.pdf`
       7. *Hình thức hỗ trợ trực tuyến* $\rightarrow$ Upload `7_Hinh_thuc_ho_tro_truc_tuyen_<brand>.pdf`
     + Ô cuối *Cam kết theo đúng quy định tại Nghị định*: Giữ nguyên nội dung mặc định của hệ thống.

4. **Bước 4 — Gửi duyệt & Theo dõi:**
   - Kiểm tra lại toàn bộ thông tin $\rightarrow$ Bấm nút **`Lưu & Gửi duyệt`**.
   - Nếu xuất hiện thông báo nhắc cập nhật thông tin thay đổi trong 20 ngày làm việc (từ SSO) đối với hồ sơ mới $\rightarrow$ bỏ qua, chỉ cần xác nhận trạng thái hồ sơ là **`Chờ duyệt`**.
   - Sau 3–7 ngày làm việc, check email hoặc đăng nhập lại `online.gov.vn`. Nếu bị yêu cầu bổ sung, sửa đúng điểm chuyên viên ghi chú rồi bấm gửi lại; nếu trạng thái chuyển sang **`Đã xác nhận`** $\rightarrow$ sang Giai đoạn 4.

---

### 🎖️ Giai đoạn 4: Hậu Kiểm & Gắn Huy Hiệu BCT Khi Được Duyệt

Khi trạng thái hồ sơ trên `online.gov.vn` là **"Đã xác nhận"**:

1. **Lấy liên kết tra cứu công khai:**
   - Đường dẫn định danh: `https://online.gov.vn/nen-tang/<UUID-HO-SO>`
   - Lưu file ảnh logo xanh **"ĐÃ THÔNG BÁO BỘ CÔNG THƯƠNG"** vào thư mục `public/` của website.
2. **Gắn Huy hiệu vào Footer Website:**
   ```html
   <a href="https://online.gov.vn/nen-tang/<UUID-HO-SO>" target="_blank" rel="noopener noreferrer" title="Đã xác nhận với Bộ Công Thương">
     <img src="/path/to/logo-da-thong-bao-bo-cong-thuong.png" alt="Đã thông báo Bộ Công Thương" width="150" height="56" loading="lazy" />
   </a>
   ```
3. **Bổ sung Schema `Organization` (`sameAs`):**
   - Thêm `"https://online.gov.vn/nen-tang/<UUID-HO-SO>"` vào mảng `sameAs` của JSON-LD để tăng độ uy tín Entity E-E-A-T với Google.
4. **Deploy lại Production & Kiểm tra live** (click vào logo phải mở đúng trang xác nhận của Bộ Công Thương).
5. **Bật lại cổng thanh toán online** (nếu trước đó tạm ẩn để chờ duyệt).
