---
title: Robots.txt Specification (Quy chuẩn robots.txt)
source: https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=vi
last_updated: Wed, 15 Jul 2026 20:42:06 GMT
---

# 📖 Robots.txt Specification (Quy chuẩn robots.txt)

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

# Giới thiệu về tệp robots.txt
```html
noindex
```
Tệp robots.txt cho trình thu thập dữ liệu của công cụ tìm kiếm biết có thể truy cập vào những URL nào trên trang web của bạn. Tệp này chủ yếu dùng để ngăn trình thu thập dữ liệu gửi quá nhiều yêu cầu cho trang web; đây không phải là cơ chế để ẩn một trang web khỏi Google. Để ẩn một trang web khỏi Google, hãy chặn lập chỉ mục bằng hoặc bảo vệ trang đó bằng mật khẩu.Nếu sử dụng một Hệ thống quản lý nội dung (CMS), chẳng hạn như Wix hoặc Blogger, có thể bạn không cần (hoặc không thể) trực tiếp chỉnh sửa tệp robots.txt của mình. Thay vào đó, có thể CMS của bạn sử dụng trang cài đặt tìm kiếm hoặc một cơ chế khác để giúp công cụ tìm kiếm biết được có nên thu thập dữ liệu trên trang của bạn không.Nếu bạn muốn ẩn hoặc hiện một trong các trang của mình trên công cụ tìm kiếm, hãy tìm hướng dẫn về cách sửa đổi chế độ hiển thị của trang trong công cụ tìm kiếm trên CMS của bạn (ví dụ: tìm "wix ẩn trang khỏi công cụ tìm kiếm").
## Tệp robots.txt dùng để làm gì?Tệp robots.txt chủ yếu dùng để quản lý lưu lượng truy cập của trình thu thập dữ liệu vào trang web của bạn và thường dùng để ẩn tệp khỏi Google, tuỳ thuộc vào loại tệp:Ảnh hưởng của tệp robots.txt đến các loại tệp Trang web Đối với các trang web (HTML, PDF hoặc các định dạng khác không phải nội dung đa phương tiện mà Google đọc được), bạn có thể dùng một tệp robots.txt để quản lý lưu lượng thu thập dữ liệu nếu cho rằng máy chủ của bạn sẽ bị quá tải do số lượng yêu cầu của trình thu thập dữ liệu của Google. Bạn cũng có thể dùng tệp này để tránh thu thập dữ liệu các trang không quan trọng hoặc tương tự nhau trên trang web của mình.Cảnh báo: Đừng dùng tệp robots.txt như một phương tiện để ẩn các trang của bạn (kể cả các tệp PDF và các định dạng văn bản khác mà Google hỗ trợ) khỏi kết quả tìm kiếm trên Google.
```html
noindex
```
Nếu các trang khác trỏ đến trang của bạn kèm theo văn bản mô tả, Google vẫn có thể lập chỉ mục URL đó mà không cần truy cập trang. Nếu bạn muốn chặn trang của mình khỏi kết quả tìm kiếm, hãy dùng một phương thức khác, chẳng hạn như bảo vệ bằng mật khẩu hoặc .Nếu trang web của bạn bị chặn bằng tệp robots.txt thì URL của trang đó vẫn có thể xuất hiện trong kết quả tìm kiếm, nhưng kết quả tìm kiếm đó sẽ không có nội dung mô tả. Các tệp hình ảnh, tệp video, tệp PDF và các tệp không phải HTML khác được nhúng trên trang bị chặn cũng sẽ bị loại trừ khỏi quá trình thu thập dữ liệu, trừ phi các tệp đó được dẫn chiếu đến qua các trang khác được phép thu thập dữ liệu. Nếu bạn thấy kết quả tìm kiếm này cho trang của mình và muốn sửa, hãy xoá tệp robots.txt đang chặn trang. Nếu bạn muốn ẩn hoàn toàn trang khỏi Tìm kiếm, hãy sử dụng một phương thức khác.Tệp đa phương tiện Hãy dùng tệp robots.txt để quản lý lưu lượng thu thập dữ liệu, đồng thời để ngăn các tệp hình ảnh, video và âm thanh xuất hiện trong kết quả tìm kiếm trên Google. Tệp này sẽ không ngăn các trang hoặc người dùng khác liên kết đến tệp hình ảnh, video hay âm thanh của bạn.
- 
- 
## Tìm hiểu những hạn chế của tệp robots.txtĐọc thêm về cách ngăn hình ảnh xuất hiện trên Google. Đọc thêm về cách xóa hoặc hạn chế các tệp video của bạn xuất hiện trên Google. Tệp tài nguyên Bạn có thể dùng tệp robots.txt để chặn các tệp tài nguyên (chẳng hạn như hình ảnh, tập lệnh hoặc các tệp định kiểu không quan trọng) nếu bạn cho rằng lệnh chặn này sẽ không ảnh hưởng đáng kể đến những trang có thể tải mà không cần những tài nguyên này. Tuy nhiên, nếu trình thu thập dữ liệu của Google khó có thể hiểu được trang của bạn khi thiếu những tài nguyên này, thì bạn đừng chặn. Nếu không, Google sẽ không thể phân tích chính xác những trang cần đến những tài nguyên đó.Trước khi tạo hoặc chỉnh sửa tệp robots.txt, bạn nên biết những hạn chế của phương pháp chặn URL này. Tuỳ thuộc vào mục tiêu và tình huống của bạn, bạn nên cân nhắc cả những cơ chế khác để đảm bảo URL của bạn không tìm được trên web.
- 
- 
- 
```html
meta
```
```html
noindex
```
## Tạo hoặc cập nhật tệp robots.txtNếu bạn cho là mình cần một tệp robots.txt, hãy tìm hiểu cách tạo tệp robots.txt. Hoặc nếu đã có, hãy tìm hiểu cách cập nhật.
- 
- 
- 
