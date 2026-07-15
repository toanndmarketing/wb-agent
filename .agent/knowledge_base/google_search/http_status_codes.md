---
title: HTTP Status Codes & Crawl Errors (Xử lý mã trạng thái & lỗi kết nối)
source: https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=vi
last_updated: Wed, 15 Jul 2026 20:42:11 GMT
---

# 📖 HTTP Status Codes & Crawl Errors (Xử lý mã trạng thái & lỗi kết nối)

> [!NOTE]
> Tài liệu chắt lọc tinh khiết từ tài liệu chính thống của Google Search Central. 
> Phục vụ làm kim chỉ nam tối ưu SEO & lập chỉ mục cho AI Agent.

# Ảnh hưởng của mã trạng thái HTTP đối với trình thu thập thông tin của Google
```html
418 (I'm a teapot)
```
Trang này mô tả các ảnh hưởng của mã trạng thái HTTP đối với khả năng thu thập thông tin của Google đối với nội dung trên web của bạn. Chúng tôi sẽ đề cập đến 20 mã trạng thái phổ biến nhất mà Google gặp trên môi trường web. Các mã trạng thái ít gặp hơn, chẳng hạn như , sẽ không được đề cập.
## Mã trạng thái HTTPChúng tôi không hỗ trợ tính năng thử nghiệm của các giao thức được hỗ trợ (HTTP và FTP), trừ khi có quy định khác.
```html
4xx—5xx
```
```html
3xx
```
```html
2xx
```
```html
2xx (success)
```
Đối với Google Tìm kiếm, mã trạng thái HTTP không đảm bảo hoạt động lập chỉ mục sẽ diễn ra. Bảng sau đây trình bày những mã trạng thái HTTP mà Google hay bắt gặp nhất và cách Google xử lý từng mã trạng thái đó.
### 
```html
2xx (success)
```
Mã trạng thái HTTP
```html
soft 404
```
```html
200 (success)
```
```html
201 (created)
```
```html
202 (accepted)
```
```html
204 (no content)
```
Google không nhận được nội dung nào nên không thể xử lý.
### 
```html
3xx (redirection)
```
Theo mặc định, trình thu thập thông tin của Google sẽ đi theo tối đa 10 bước chuyển hướng. Tuy nhiên, trình thu thập thông tin của một số sản phẩm cụ thể có thể có các giới hạn riêng. Ví dụ: Googlebot thường đi theo 10 bước chuyển hướng khi thu thập thông tin cho nội dung chung trên web, nhưng Công cụ kiểm tra của Google thì không đi theo các bước chuyển hướng.
```html
3xx
```
```html
301 (moved permanently)
```
Google sẽ đi theo lệnh chuyển hướng và các hệ thống của Google sẽ xem lệnh chuyển hướng này là một tín hiệu mạnh cho thấy trang đích của lệnh chuyển hướng nên được xử lý.
```html
302 (found)
```
```html
303 (see other)
```
```html
304 (not modified)
```
```html
307 (temporary redirect)
```
```html
302
```
```html
308 (moved permanently)
```
```html
301
```
### 
```html
4xx (client errors)
```
Tương đương với . Tương đương với . Tuy Google Tìm kiếm xử lý những mã trạng thái này như nhau, nhưng hãy lưu ý rằng ý nghĩa của những mã này vẫn khác nhau. Hãy dùng mã trạng thái thích hợp đối với lệnh chuyển hướng để giúp ích cho các ứng dụng khác (ví dụ: máy đọc sách, các công cụ tìm kiếm khác).
```html
4xx
```
```html
4xx
```
```html
4xx
```
```html
4xx
```
Google không sử dụng nội dung từ những URL trả về mã trạng thái . Nếu trước đây một URL từng được sử dụng nhưng hiện đang trả về mã trạng thái , thì các hệ thống của Google sẽ ngừng sử dụng URL đó theo thời gian. Trong trường hợp Google Tìm kiếm, Google không lập chỉ mục những URL trả về mã trạng thái , đồng thời những URL đã được lập chỉ mục và trả về mã trạng thái sẽ bị xoá khỏi chỉ mục.
```html
4xx
```
```html
400 (bad request)
```
```html
429
```
```html
4xx
```
```html
404
```
```html
401
```
```html
403
```
```html
429
```
```html
4xx
```
```html
401 (unauthorized)
```
```html
403 (forbidden)
```
```html
404 (not found)
```
```html
410 (gone)
```
```html
411 (length required)
```
```html
429 (too many requests)
```
```html
429
```
### 
```html
5xx (server errors)
```
```html
5xx
```
```html
429
```
Các lỗi máy chủ và sẽ thông báo để trình thu thập thông tin của Google tạm thời giảm tốc độ thu thập thông tin. Đối với Google Tìm kiếm, những URL đã lập chỉ mục sẽ vẫn còn trong chỉ mục, nhưng cuối cùng sẽ bị xoá.
```html
5xx
```
```html
5xx
```
```html
2xx
```
```html
500 (internal server error)
```
```html
502 (bad gateway)
```
```html
503 (service unavailable)
```
