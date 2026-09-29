---
name: pseo-location-geo
description: >
  Blueprint Audit Kiến trúc Internal Linking & Onpage SEO cho ngách Location-Based pSEO.
  Tập trung 100% vào dòng chảy Link Juice (Home -> Pillar -> Silo -> Cluster Place) để chống Orphan Pages và tối ưu Onpage từng cấp.
---

# 🕸️ pSEO Location GEO — Link Juice & Hierarchy Blueprint

> **Mục tiêu**: Hướng dẫn Agent audit cấu trúc phân tầng, luân chuyển Link Juice (dòng chảy sức mạnh SEO) và thiết kế Onpage cho từng cấp độ của 1 dự án pSEO Location. Đảm bảo tuyệt đối **KHÔNG có Orphan Pages**.

---

## 1. 🏗️ HỆ THỐNG PHÂN TẦNG (THE HIERARCHY)

Mọi URL trong hệ thống phải nằm trong cây cấu trúc sau:

1. **L1 - HOME (Root)**: Điểm gom Link Juice lớn nhất.
2. **L2 - PILLAR (Vùng lớn / Global Hub)**: Ví dụ: Đảo (`/restaurants/oahu/`), Tỉnh/Thành phố lớn, hoặc Danh mục tổng (`/cuisines/seafood/`).
3. **L3 - SILO (Khu vực / Quận / Huyện)**: Ví dụ: Thành phố con (`/restaurants/oahu/honolulu/`).
4. **L4 - CLUSTER (Ngách cụ thể)**: Tổ hợp Location + Category/Feature. Ví dụ: (`/restaurants/oahu/honolulu/seafood/`).
5. **L5 - LEAF (Place / Detail)**: Trang chi tiết địa điểm (`/restaurant/dukes-waikiki/`).

---

## 2. 🌊 CHIẾN LƯỢC LUÂN CHUYỂN LINK JUICE (Tránh Orphan Pages)

> 🚨 **STRICT ARCHITECTURE CROSS-CHECK (BẮT BUỘC):** Khi Fix bug về Route, Links hoặc các Component điều hướng (SiblingLinks, CuisineLinks...), Agent **TUYỆT ĐỐI KHÔNG ĐƯỢC** fix bề mặt HTML/Syntax. Phải mở và đối chiếu chéo với bản vẽ SEO Matrix (`silo-seo-audit-matrix.md` hoặc `seo-audit.md`) để bảo toàn nguyên vẹn dòng chảy Link Juice. Nếu một trang Cấp 3 quên trỏ ngược lên Cấp 2, đó là Bug Kiến Trúc, phải fix logic Link Juice thay vì chỉ sửa UI.

Để không một địa điểm (Place) nào bị mồ côi (Orphan), Link Juice phải chảy theo 3 chiều:

### ⬇️ Dòng chảy từ trên xuống (Top-Down Flow)
- **Home → Pillars**: Trang chủ phải có Grid/List link tới 100% các Pillar L2 (Các khu vực chính).
- **Pillar → Silos**: Trang Pillar (Vùng lớn) NÊN hiển thị danh sách các Silos L3 (Các quận/huyện) có nhiều data nhất.
- **Silo → Clusters**: Trang Silo liệt kê các Category Clusters phổ biến nhất trong khu vực đó.
- **Cluster → Leaves**: Trang Cluster phân trang (Pagination) liệt kê các Places.

### ⬆️ Dòng chảy từ dưới lên (Bottom-Up Flow)
- **BREADCRUMBS (Bắt buộc 100%)**: Là vũ khí mạnh nhất để đẩy Link Juice ngược lên. Mọi trang Leaf phải có Breadcrumb trỏ ngược về Cluster -> Silo -> Pillar.
- **Tên Location là Anchor Text**: Trong UI của trang Leaf, khi nhắc đến thành phố, phải gắn link trỏ về trang Silo của thành phố đó.

### ↔️ Dòng chảy ngang (Horizontal / Contextual Flow)
- **Sibling Silo Links**: Ở cuối trang Silo A, gợi ý link sang Silo B, C (Cùng thuộc 1 Pillar). 
- **Nearby Places (Leaf to Leaf)**: Ở trang chi tiết địa điểm A, phải có widget "Nearby Places" (Địa điểm lân cận) để link sang địa điểm B, C.
- **Cross-Domain (Guide to Transactional)**: Bài viết Blog/Cẩm nang (Guide) BẮT BUỘC chèn In-text link trỏ về các Pillar/Silo hoặc Cluster.

> ⚠️ **Quy tắc Bảo toàn Link Juice (The 15-Link Rule)**: Các cụm Sibling Links hoặc Category Links ngang không được thả rông hiển thị hàng trăm links làm loãng Juice. **Bắt buộc hiển thị tối đa 15-20 links quan trọng nhất**, phần còn lại phải ẩn sau UI Accordion ("Show More / Xem thêm").

---

## 3. 🧩 ONPAGE COMPONENT CHECKLIST (THEO TỪNG CẤP)

Khi Audit codebase, hãy check xem mỗi cấp (Level) có render đúng các component Onpage bắt buộc sau không:

### Cấp độ: Pillar / Silo / Cluster (Các trang Danh sách)
- [ ] **Breadcrumbs**: (Top) Điều hướng ngược.
- [ ] **GeoDirectAnswer (Featured Snippet Block)**: Đoạn văn bản ngay H1 tóm tắt câu trả lời trực tiếp cho AI Search (Có nhúng tên 2-3 Entity nổi bật nhất trong khu vực).
- [ ] **H2/H3 Contextual Headings**: Không dùng H2 chung chung như "Danh sách". Phải dùng "Top-Rated [Category] in [Location]".
- [ ] **Item Card (ListItem)**: Phải chứa link (a href) trỏ thẳng về trang Leaf (Detail).
- [ ] **Horizontal Sibling Links Widget**: Đặt ở cuối trang, điều hướng ngang sang các Silo/Cluster lân cận.
- [ ] **Schema.org**: Render `ItemList` chứa các item bên trong.

### Cấp độ: Leaf / Place (Trang Chi tiết)
- [ ] **Breadcrumbs**: (Top) Rất quan trọng, bắt buộc trỏ ngược về Cluster/Silo.
- [ ] **Structured Address**: In đậm/hiển thị rõ Địa chỉ, Thành phố, Zipcode (Local SEO signals).
- [ ] **Location Anchor trong UI Card**: Toàn bộ UI Card (VD: RestaurantCard) khi hiển thị tên Khu vực/Thành phố bên trong Card bắt buộc phải là `<Link>` trỏ về Hub Silo (chuẩn TasteHi).
- [ ] **Nearby Widget**: Block "Khám phá địa điểm lân cận" (Link sang các Leaf khác).
- [ ] **Related Cluster & Global Silo Widget**: Block "Các danh mục phổ biến tại [Location]". Bắt buộc phải chèn 1 Link "Global Silo" (VD: "All Restaurants in Wynwood") đẩy ngược Juice về Level 2 (chuẩn TasteHi).
- [ ] **Quy tắc Fallback Anchor Text**: Khi viết logic tự động rút gọn Category (VD: Xóa chữ "Restaurant" để UI gọn hơn), nếu kết quả chuỗi bị rỗng (Blank), phải fallback về tên gốc để tránh lỗi SEO rỗng Anchor Text (VD: chỉ hiện "in Wynwood").
- [ ] **Schema.org**: Render `LocalBusiness` hoặc `Restaurant`. `aggregateRating` BẮT BUỘC tính từ 1st-party comments.
- [ ] **Title/Meta**: Công thức `{Name} - {Street Address}, {City}`.

---

## 4. 📋 LỆNH AUDIT DÀNH CHO AGENT (Codebase Check)

Khi bắt đầu Audit dự án, Agent phải rà soát mã nguồn qua các bước sau:

1. **Check Mồ Côi (Orphan Check)**: 
   - Trace luồng Data Fetching của trang Leaf. Kiểm tra xem trang Danh sách (Cluster/Silo) có component phân trang (Pagination) hay Load More không. Nếu không có phân trang mà data > 100, các item cũ sẽ bị Orphan.
2. **Check Breadcrumb**: 
   - `grep_search` component `Breadcrumbs`. Đảm bảo nó được gắn trên Layout gốc hoặc tất cả Page templates.
3. **Check rò rỉ Link Juice (Juice Leak)**:
   - Tìm các component "Liên kết liên quan" (Related links, Sibling links). Kiểm tra logic code xem có dùng `.slice(0, 15)` hay logic giới hạn hiển thị ban đầu không. Nếu render > 100 links trực tiếp vào DOM (không qua tab/accordion), báo lỗi "Link Juice Dilution".
4. **Check Schema Listing**:
   - Mở component sinh schema trang Listing, kiểm tra xem vòng lặp `itemListElement` có match với danh sách render trên giao diện không.
5. **Check Cross-Linking**:
   - Đọc source code trang Blog/Guide. Xem có module "Related Locations / Featured Places" tự động sinh link về trang Transactional (Pillar/Silo) không.

> **Output mong đợi sau Audit**: Đánh giá chi tiết dòng chảy Link Juice (Thủng ở đâu, nghẽn ở đâu, trang detail có nguy cơ mồ côi không) + Báo cáo thiếu hụt Onpage Component theo từng Level.
