---
title: Google Crawlers & Indexing Overview (Cơ chế cào & index)
source: https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=vi
last_updated: Wed, 15 Jul 2026 20:42:05 GMT
---

# 📖 Google Crawlers & Indexing Overview (Cơ chế cào & index)

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

# Tổng quan về trình thu thập thông tin và trình tìm nạp của Google (tác nhân người dùng)Google sử dụng trình thu thập thông tin và trình tìm nạp để thực hiện hành động cho các sản phẩm của Google, theo cách tự động hoặc kích hoạt theo yêu cầu của người dùng. Trình thu thập thông tin (đôi khi còn gọi là "robot" hoặc "spider") là thuật ngữ chung để chỉ mọi chương trình có chức năng tự động phát hiện và quét các trang web. Trình tìm nạp đóng vai trò như một chương trình giống như wget, thường thay mặt người dùng thực hiện một yêu cầu. Ứng dụng khách của Google được chia thành ba loại:
```html
AdsBot
```
```html
*
```
## Thuộc tính kỹ thuật của các trình thu thập thông tin và trình tìm nạp của GoogleBạn đang tìm thông tin cập nhật mới nhất cho trang này? Hãy xem thông tin cập nhật về tài liệu của chúng tôi. Các trình thu thập thông tin chung Các trình thu thập thông tin chung dùng cho các sản phẩm của Google (chẳng hạn như Googlebot). Các trình thu thập thông tin này luôn tuân thủ các quy tắc trong tệp robots.txt đối với hoạt động thu thập thông tin tự động. Trình thu thập thông tin theo trường hợp đặc biệt Trình thu thập thông tin theo trường hợp đặc biệt tương tự như trình thu thập thông tin chung, tuy nhiên sẽ được một số sản phẩm cụ thể sử dụng trong trường hợp có thoả thuận về quá trình thu thập thông tin giữa trang web được thu thập dữ tin và sản phẩm của Google. Ví dụ: bỏ qua tác nhân người dùng chung trong tệp robots.txt () khi có sự cho phép của nhà xuất bản quảng cáo. Trình tìm nạp do người dùng kích hoạt Trình tìm nạp do người dùng kích hoạt là một trong số các công cụ và chức năng sản phẩm mà người dùng cuối kích hoạt hoạt động tìm nạp. Ví dụ: Google Site Verifier thực hiện hành động theo yêu cầu của người dùng.Chúng tôi đã thiết kế để có thể cho phép hàng nghìn máy chạy các trình thu thập thông tin và trình tìm nạp của Google cùng lúc nhằm cải thiện hiệu suất và quy mô tương ứng với sự phát triển của môi trường web. Để tối ưu hoá mức sử dụng băng thông, các ứng dụng khách này được phân phối trên nhiều trung tâm dữ liệu trên toàn thế giới để được ở gần những trang web mà chúng có thể truy cập. Do đó, nhật ký của bạn có thể cho thấy các lượt truy cập từ một vài địa chỉ IP. Google chủ yếu truy cập từ các địa chỉ IP ở Hoa Kỳ. Trong trường hợp phát hiện thấy một trang web chặn yêu cầu từ Hoa Kỳ, có thể Google sẽ cố gắng thu thập thông tin qua địa chỉ IP ở các quốc gia khác.
### Các giao thức truyền dữ liệu được hỗ trợ
```html
421
```
Cơ sở hạ tầng của trình thu thập thông tin của Google cũng hỗ trợ hoạt động thu thập thông tin thông qua FTP (được định nghĩa trong RFC959 và các nội dung cập nhật của tài liệu này) và FTPS (được định nghĩa trong RFC4217 và các nội dung cập nhật của tài liệu này). Tuy nhiên, hoạt động thu thập thông tin thông qua các giao thức này rất hiếm khi xảy ra.
### Các định dạng mã hoá nội dung được hỗ trợ
```html
Accept-Encoding
```
```html
Accept-Encoding: gzip, deflate, br
```
Trình thu thập thông tin và trình tìm nạp của Google hỗ trợ các phương thức mã hoá (nén) nội dung sau: gzip, deflate và Brotli (br). Các phương thức mã hoá nội dung mà từng tác nhân người dùng của Google hỗ trợ sẽ được giới thiệu trong tiêu đề của từng yêu cầu mà chúng thực hiện. Ví dụ: .
### Giới hạn kích thước tệpTheo mặc định, các trình thu thập thông tin và trình tìm nạp của Google chỉ thu thập thông tin 15 MB đầu tiên của một tệp, đồng thời mọi nội dung vượt quá giới hạn này sẽ bị bỏ qua. Tuy nhiên, các dự án riêng lẻ có thể thiết lập những giới hạn khác nhau đối với trình thu thập thông tin và trình tìm nạp, cũng như đối với các loại tệp khác nhau. Ví dụ: một trình thu thập thông tin của Google như Googlebot có thể đặt giới hạn kích thước nhỏ hơn (ví dụ: 2 MB) hoặc chỉ định giới hạn kích thước tệp lớn hơn cho tệp PDF so với tệp HTML.
### Tốc độ thu thập dữ liệu và mức tải của máy chủ lưu trữ
### Hoạt động lưu vào bộ nhớ cache HTTP
```html
ETag
```
```html
If-None-Match
```
```html
Last-Modified
```
```html
If-Modified-Since
```
```html
Etag
```
```html
Last-Modified
```
```html
ETag
```
```html
Last-Modified
```
```html
ETag
```
```html
ETag
```
```html
Last-Modified
```
```html
ETag
```
Các lệnh khác để lưu vào bộ nhớ cache HTTP không được hỗ trợ.
```html
Googlebot
```
```html
Storebot-Google
```
Các trình thu thập thông tin và trình tìm nạp riêng lẻ của Google có thể sử dụng hoặc không sử dụng tính năng lưu vào bộ nhớ cache, tuỳ thuộc vào nhu cầu của sản phẩm mà các trình thu thập và trình tìm nạp này liên kết. Ví dụ: hỗ trợ lưu vào bộ nhớ cache khi thu thập lại dữ liệu trên các URL cho Google Tìm kiếm và chỉ hỗ trợ lưu vào bộ nhớ cache trong một số điều kiện nhất định.Để triển khai tính năng lưu vào bộ nhớ cache HTTP cho trang web, hãy liên hệ với nhà cung cấp dịch vụ lưu trữ hoặc hệ thống quản lý nội dung.
#### 
```html
ETag
```
```html
If-None-Match
```
và
```html
ETag
```
```html
If-None-Match
```
```html
ETag
```
```html
If-None-Match
```
#### Last-Modified và If-Modified-Since
```html
Last-Modified
```
```html
If-Modified-Since
```
Cơ sở hạ tầng thu thập thông tin của Google hỗ trợ và được định nghĩa trong Tiêu chuẩn lưu vào bộ nhớ cache HTTP với các lưu ý sau:
- Ngày trong tiêu đề
```html
Last-Modified
```
- Mặc dù không bắt buộc, nhưng bạn cũng nên cân nhắc việc thiết lập
```html
max-age
```
```html
Cache-Control
```
```html
max-age
```
```html
Cache-Control: max-age=94043
```
```html
Last-Modified
```
```html
If-Modified-Since
```
## Xác minh trình thu thập thông tin và trình tìm nạp của GoogleCác trình thu thập thông tin của Google tự xác định mình theo 3 cách:
1. Tiêu đề yêu cầu HTTP
```html
user-agent
```
1. Địa chỉ IP nguồn của yêu cầu.
1. Tên máy chủ DNS ngược của IP nguồn.. Tìm hiểu cách sử dụng những thông tin này để xác minh trình thu thập thông tin và trình tìm nạp của Google.
